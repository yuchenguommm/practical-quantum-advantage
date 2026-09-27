"""Same-instance audit of the public nine-option BMW/BCG illustrative ILP.

The quantum oracle is compiled from arithmetic on the input coefficients, not
from a precomputed list of winning assignments. The success probability is
the exact ideal Grover formula; no 45-qubit statevector or hardware run is
claimed. Run with --compile to obtain gate counts using Qiskit Terra 0.23.3.
"""
import argparse
import hashlib
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINNED_UPSTREAM_COMMIT = "8456eaddb0033fa703c169c19ff264b51ccd0711"


def portable_sha256(path):
    """Hash the repository's LF-form input, independent of checkout line endings."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def evaluate(weights, assignment):
    return sum(w * bit for w, bit in zip(weights, assignment))


def exact_audit(data, threshold):
    weights = data["objective"]
    capacity = data["constraints_rhs"][0]
    feasible = []
    for bits in itertools.product((0, 1), repeat=len(weights)):
        if sum(bits) <= capacity:
            feasible.append((evaluate(weights, bits), bits))
    best = max(feasible)
    winners = [bits for score, bits in feasible if score >= threshold]
    sorted_ids = sorted(range(len(weights)), key=lambda i: weights[i], reverse=True)
    direct = tuple(int(i in sorted_ids[:capacity]) for i in range(len(weights)))
    assert evaluate(weights, direct) == best[0]
    n = 1 << len(weights)
    m = len(winners)
    theta = math.asin(math.sqrt(m / n))
    iterations = max(0, round(math.pi / (4 * theta) - 0.5))
    result = {
        "input_sha256": portable_sha256(HERE / "instance.json"),
        "variables": len(weights), "capacity": capacity, "threshold": threshold,
        "all_assignments": n, "feasible_assignments": len(feasible),
        "optimum": best[0], "optimal_bits": list(direct),
        "winning_assignments": m, "ideal_grover_iterations": iterations,
        "ideal_grover_success_probability": math.sin((2 * iterations + 1) * theta) ** 2,
        "uniform_one_draw_success_probability": m / n,
        "classical_sort_certificate": sorted_ids[:capacity],
    }
    return result


def arithmetic_phase_oracle(weights, threshold, capacity):
    """45-qubit clean phase oracle for score>=threshold AND count<=capacity."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import WeightedAdder, IntegerComparator

    assert len(weights) == 9 and capacity == 5
    score_add = WeightedAdder(9, weights)
    count_add = WeightedAdder(9, [1] * 9)
    score_cmp = IntegerComparator(score_add.num_sum_qubits, threshold, geq=True)
    count_cmp = IntegerComparator(count_add.num_sum_qubits, capacity + 1, geq=False)
    assert (score_add.num_qubits, count_add.num_qubits) == (33, 17)
    assert (score_cmp.num_qubits, count_cmp.num_qubits) == (24, 8)
    q = QuantumCircuit(45, name="pricing_oracle")
    score_add_q = list(range(33))
    score_cmp_q = list(range(9, 21)) + [33] + list(range(34, 45))
    count_add_q = list(range(17))
    count_cmp_q = list(range(9, 13)) + [17] + list(range(18, 21))
    q.append(score_add, score_add_q)
    q.append(score_cmp, score_cmp_q)
    q.append(score_add.inverse(), score_add_q)
    q.append(count_add, count_add_q)
    q.append(count_cmp, count_cmp_q)
    q.cz(33, 17)
    q.append(count_cmp.inverse(), count_cmp_q)
    q.append(count_add.inverse(), count_add_q)
    q.append(score_add, score_add_q)
    q.append(score_cmp.inverse(), score_cmp_q)
    q.append(score_add.inverse(), score_add_q)
    return q


def compile_circuits(weights, threshold, capacity, iterations):
    from qiskit import QuantumCircuit, transpile

    oracle = arithmetic_phase_oracle(weights, threshold, capacity)
    grover = QuantumCircuit(45)
    grover.h(list(range(9)))
    for _ in range(iterations):
        grover.compose(oracle, inplace=True)
        # H^n X^n MCZ X^n H^n is the usual diffusion reflection,
        # up to a global phase, on the nine decision bits.
        grover.h(list(range(9)))
        grover.x(list(range(9)))
        grover.h(8)
        grover.mcx(list(range(8)), 8)
        grover.h(8)
        grover.x(list(range(9)))
        grover.h(list(range(9)))

    def describe(q):
        compiled = transpile(q, basis_gates=["u1", "u2", "u3", "cx"],
                             optimization_level=0)
        counts = {str(k): int(v) for k, v in compiled.count_ops().items()}
        return {"logical_qubits": q.num_qubits, "depth": compiled.depth(),
                "gate_counts": counts}

    return {"qiskit_terra_version": __import__("qiskit").__version__,
            "basis": ["u1", "u2", "u3", "cx"],
            "one_oracle": describe(oracle),
            "full_ideal_grover_circuit": describe(grover),
            "note": "Unoptimized generic decomposition; these are neither fault-tolerant T counts nor physical runtimes."}


def check_oracle(weights, threshold, capacity):
    """Interference checks on one winning and one losing input pair."""
    from qiskit import QuantumCircuit, transpile
    from qiskit.providers.aer import AerSimulator

    oracle = arithmetic_phase_oracle(weights, threshold, capacity)
    simulator = AerSimulator(method="matrix_product_state")
    checks = {}
    for label, fixed_ones, probe, expected in (
        ("winner_vs_neighbor", [1, 2, 7, 8], 5, "1"),
        ("exact_threshold", [1, 2, 4, 5], 7, "1"),
        ("over_capacity", [1, 2, 5, 7, 8], 0, "1"),
        ("two_losers", [], 5, "0"),
    ):
        qc = QuantumCircuit(45, 1)
        for i in fixed_ones:
            qc.x(i)
        qc.h(probe)
        qc.compose(oracle, inplace=True)
        qc.h(probe)
        qc.measure(probe, 0)
        counts = simulator.run(transpile(qc, simulator), shots=32).result().get_counts()
        if counts != {expected: 32}:
            raise AssertionError((label, counts))
        checks[label] = counts
    return checks


def audit_upstream_encoding(data, upstream):
    import numpy as np

    upstream = upstream.resolve()
    source = upstream / "pipelines/data/milp_formulation.json"
    commit = subprocess.check_output(
        ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    if commit != PINNED_UPSTREAM_COMMIT:
        raise ValueError(f"Expected pinned upstream commit {PINNED_UPSTREAM_COMMIT}, got {commit}")
    dirty = subprocess.check_output(
        ["git", "-C", str(upstream), "status", "--porcelain", "--untracked-files=no"],
        text=True).strip()
    if dirty:
        raise ValueError("Upstream tracked files differ from the pinned commit")
    source_bytes = subprocess.check_output(
        ["git", "-C", str(upstream), "show", "HEAD:pipelines/data/milp_formulation.json"])
    source_data = json.loads(source_bytes)
    if json.loads(source.read_text(encoding="utf-8")) != source_data:
        raise ValueError("Upstream working-tree input differs from the pinned Git blob")
    if any(source_data[k] != data[k] for k in ("objective", "constraints", "constraints_rhs")):
        raise ValueError("Public ILP differs from the pinned local copy")
    sys.path.insert(0, str(upstream))
    from pipelines.generate_B import generate_B_matrix_and_rhs

    c = np.asarray(data["objective"])
    shifted = c - c.min() + 1
    beta = int(np.abs(shifted).sum() / 2)
    B, v, ell, distance, maxsat, _ = generate_B_matrix_and_rhs(
        np.asarray(data["constraints"]), np.asarray(data["constraints_rhs"]),
        shifted, beta=beta)
    return {"upstream_commit": commit, "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "binary_matrix_rows": int(B.shape[0]), "binary_matrix_columns": int(B.shape[1]),
            "nonzero_entries": int(B.sum()), "rhs_ones": int(v.sum()),
            "reported_generator_row_min_weight": int(distance), "ell": ell,
            "beta_in_shifted_objective": beta,
            "objective_threshold_in_shifted_units": beta + 1,
            "gadget_max_satisfied": int(maxsat)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=1500)
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--check-circuit", action="store_true")
    ap.add_argument("--upstream", type=Path, help="Pinned clone of BCG-X-Official/dqi")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = json.loads((HERE / "instance.json").read_text(encoding="utf-8"))
    result = exact_audit(data, args.threshold)
    if args.compile:
        result["compiled_circuits"] = compile_circuits(
            data["objective"], args.threshold, data["constraints_rhs"][0],
            result["ideal_grover_iterations"])
    if args.check_circuit:
        result["circuit_interference_checks"] = check_oracle(
            data["objective"], args.threshold, data["constraints_rhs"][0])
    if args.upstream:
        result["upstream_dqi_encoding"] = audit_upstream_encoding(data, args.upstream)
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
