"""Audit archived OPI block-Gibbs search trajectories from dqi-mcmc.

Input is the public IBM-author repository pinned in opi_mcmc_archive_audit.md.
Only the Python standard library is needed. This reanalyses existing trajectories;
it does not rerun the sampler or benchmark a quantum circuit.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import median


def log_linear_fit(xs: list[int], ys: list[int]) -> dict[str, float]:
    """Fit log(y) = intercept + slope*x and report exp(slope)."""
    if len(xs) != len(ys) or len(xs) < 3 or any(y <= 0 for y in ys):
        raise ValueError("need at least three positive, paired observations")
    lx = [float(x) for x in xs]
    ly = [math.log(y) for y in ys]
    xbar = sum(lx) / len(lx)
    ybar = sum(ly) / len(ly)
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(lx, ly)) / sum(
        (x - xbar) ** 2 for x in lx
    )
    intercept = ybar - slope * xbar
    residual = sum((y - intercept - slope * x) ** 2 for x, y in zip(lx, ly))
    total = sum((y - ybar) ** 2 for y in ly)
    return {"base_per_output_qubit": math.exp(slope), "log_r2": 1 - residual / total}


def audit_file(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        records = [json.loads(line) for line in handle if line.strip()]
    meta, *rows = records
    if meta.get("type") != "metadata" or len(rows) != 100:
        raise ValueError(f"unexpected metadata or instance count: {path}")
    p, n, m = (meta[key] for key in ("p", "num_variables", "num_constraints"))
    if m != p - 1 or n != p // 2 or meta.get("num_bit_flips") != 3:
        raise ValueError(f"unexpected benchmark parameters: {path}")
    threshold = math.floor(meta["predicted_fraction"] * m)
    if meta["predN"] != threshold:
        raise ValueError(f"threshold mismatch: {path}")
    ids = [row["rhs_idx"] for row in rows]
    if sorted(ids) != list(range(100)):
        raise ValueError(f"missing or repeated RHS index: {path}")
    times = []
    later_improvement_count = 0
    for row in rows:
        crossing = next(
            (step for step, score, *_ in row["trajectory"] if score > threshold), None
        )
        if not row.get("surpassed_predN") or crossing is None:
            raise ValueError(f"censored trajectory; handle separately: {path} RHS {row['rhs_idx']}")
        # tau_k records the last improvement in some archived rows, not the
        # first crossing of the target. Take first crossing from the trajectory.
        if row["resume_state"]["tau_k"] != row["trajectory"][-1][0]:
            raise ValueError(f"last-improvement/resume mismatch: {path} RHS {row['rhs_idx']}")
        later_improvement_count += crossing != row["resume_state"]["tau_k"]
        times.append(crossing)
    return {
        "p": p,
        "n_coefficients": n,
        "m_constraints": m,
        "output_qubits": n * math.ceil(math.log2(p)),
        "rate_n_over_m": n / m,
        "predicted_fraction": meta["predicted_fraction"],
        "integer_success_rule": f"score > {threshold}",
        "instances": len(times),
        "successful": len(times),
        "resume_tau_is_later_improvement": later_improvement_count,
        "min_steps": min(times),
        "median_steps": median(times),
        "max_steps": max(times),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="root of pinned dqi-mcmc checkout")
    parser.add_argument("--output", type=Path, help="write deterministic JSON summary")
    args = parser.parse_args()
    base = args.source / "paper-data" / "opi" / "base_sample"
    files = list(base.glob("gibbs3_p*_no_warmup.jsonl"))
    if not files:
        parser.error(f"no archived OPI trajectories at {base}")
    rows = sorted((audit_file(path) for path in files), key=lambda row: row["p"])
    all_fit = log_linear_fit(
        [row["output_qubits"] for row in rows], [row["max_steps"] for row in rows]
    )
    loo = [
        log_linear_fit(
            [r["output_qubits"] for j, r in enumerate(rows) if i != j],
            [r["max_steps"] for j, r in enumerate(rows) if i != j],
        )["base_per_output_qubit"]
        for i in range(len(rows))
    ]
    result = {
        "source": "matanninio/dqi-mcmc, paper-data/opi/base_sample",
        "metric": "maximum across 100 RHS instances of first Gibbs step exceeding the archived integer DQI target",
        "rows": rows,
        "fit_all": all_fit,
        "leave_one_size_out_base_range": [min(loo), max(loo)],
        "limitations": [
            "Archived p=53 trajectories cited as the largest size in the paper are absent from this checkout.",
            "The p/2 coefficient regime differs from the n/p~0.1 example with 0.7179 vs 0.55 satisfaction.",
            "Output-qubit equivalents exclude ancillas and input-oracle circuitry.",
            "The fit is descriptive for these ten sizes, not an asymptotic lower bound or hardware crossover.",
        ],
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
