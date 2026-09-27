"""Independent standard-library check of the public ILP and exact case numbers.

This does not import run.py or validate the DQI encoder or compiled circuits.
By default it downloads the file at the pinned upstream commit.
"""

import argparse
import hashlib
import json
import math
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMMIT = "8456eaddb0033fa703c169c19ff264b51ccd0711"
SOURCE_URL = ("https://raw.githubusercontent.com/BCG-X-Official/dqi/" + COMMIT
              + "/pipelines/data/milp_formulation.json")


def require_equal(name, actual, expected):
    if actual != expected:
        raise ValueError(f"{name}: obtained {actual!r}, recorded {expected!r}")


def verify(download=True):
    local_bytes = (HERE / "instance.json").read_bytes()
    instance = json.loads(local_bytes)
    recorded = json.loads((HERE / "result.json").read_text(encoding="utf-8"))
    canonical_local_hash = hashlib.sha256(local_bytes.replace(b"\r\n", b"\n")).hexdigest()
    require_equal("local input SHA-256", canonical_local_hash, recorded["input_sha256"])
    require_equal("upstream commit", recorded["upstream_dqi_encoding"]["upstream_commit"], COMMIT)

    source_hash = None
    if download:
        with urllib.request.urlopen(SOURCE_URL, timeout=15) as response:
            upstream_bytes = response.read()
        source_hash = hashlib.sha256(upstream_bytes).hexdigest()
        require_equal("pinned source SHA-256", source_hash,
                      recorded["upstream_dqi_encoding"]["source_sha256"])
        upstream = json.loads(upstream_bytes)
        for key in ("objective", "constraints", "constraints_rhs"):
            require_equal("upstream " + key, instance[key], upstream[key])

    weights = instance["objective"]
    capacity = instance["constraints_rhs"][0]
    threshold = recorded["threshold"]
    require_equal("one-cardinality constraint", instance["constraints"], [[1] * len(weights)])
    feasible = 0
    winners = 0
    optimum = -1
    for mask in range(1 << len(weights)):
        bits = [(mask >> i) & 1 for i in range(len(weights))]
        if sum(bits) > capacity:
            continue
        feasible += 1
        score = sum(w * bit for w, bit in zip(weights, bits))
        optimum = max(optimum, score)
        winners += score >= threshold

    top = sorted(range(len(weights)), key=lambda i: weights[i], reverse=True)[:capacity]
    if sum(weights[i] for i in top) != optimum:
        raise ValueError("sorting certificate does not reach the enumerated optimum")
    bits = [int(i in top) for i in range(len(weights))]
    require_equal("variables", len(weights), recorded["variables"])
    require_equal("capacity", capacity, recorded["capacity"])
    require_equal("assignments", 1 << len(weights), recorded["all_assignments"])
    require_equal("feasible assignments", feasible, recorded["feasible_assignments"])
    require_equal("qualifying assignments", winners, recorded["winning_assignments"])
    require_equal("optimum", optimum, recorded["optimum"])
    require_equal("optimal bits", bits, recorded["optimal_bits"])
    require_equal("sorting certificate", top, recorded["classical_sort_certificate"])

    theta = math.asin(math.sqrt(winners / (1 << len(weights))))
    rounds = recorded["ideal_grover_iterations"]
    require_equal("ideal Grover iterations", rounds,
                  max(0, round(math.pi / (4 * theta) - 0.5)))
    ideal_success = math.sin((2 * rounds + 1) * theta) ** 2
    if not math.isclose(ideal_success, recorded["ideal_grover_success_probability"], abs_tol=1e-12):
        raise ValueError("ideal Grover formula differs from recorded value")
    if not math.isclose(winners / (1 << len(weights)),
                        recorded["uniform_one_draw_success_probability"], abs_tol=1e-12):
        raise ValueError("uniform success probability differs from recorded value")

    return {
        "source_url": SOURCE_URL,
        "source_sha256": source_hash,
        "input_sha256_lf": canonical_local_hash,
        "feasible_assignments": feasible,
        "qualifying_assignments": winners,
        "optimum": optimum,
        "sorting_certificate": top,
        "ideal_grover_success_probability_formula": ideal_success,
        "scope": "Pinned input, exact enumeration, sorting certificate and ideal formula only",
        "not_checked": ["DQI encoding", "oracle circuit", "compiled gate counts", "hardware performance"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Skip the upstream source check")
    parser.add_argument("--output", type=Path, help="Write a machine-readable verification receipt")
    args = parser.parse_args()
    if args.offline and args.output:
        parser.error("a saved receipt requires checking the pinned upstream source")
    receipt = verify(download=not args.offline)
    output = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output)
