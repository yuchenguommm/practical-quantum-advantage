"""Run pinned dqi-mcmc single-coordinate Gibbs on the low-rate OPI instances.

Install the upstream package separately; it is not a site dependency. This
wrapper pins ell=floor(n/2), recreates and hashes the same allowed sets, and
counts p candidate scores per Gibbs update. It is not a reproduction of the
paper's block-size-three, high-rate experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import time
from importlib.metadata import version
from pathlib import Path

os.environ.setdefault("DQI_MCMC_NUM_PROCESSES", "1")
os.environ.setdefault("NUMBA_NUM_THREADS", "1")

import numpy as np
from dqi_mcmc.api.maxlinsat.block_gibbs_sampler import BlockGibbsSampler
from dqi_mcmc.api.maxlinsat.max_opi_problem import MaxOPIProblem

from opi_low_rate_probe import instance_mask
from opi_low_rate_verify import score_horner


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON from opi_low_rate_probe.py")
    parser.add_argument("--primes", type=int, nargs="+", help="subset of primes; default all")
    parser.add_argument("--instances", type=int, default=20, help="RHS indices below this bound")
    parser.add_argument("--budget", type=int, default=100000, help="max scored candidates per instance")
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.budget < max(args.primes or [1]):
        parser.error("budget must exceed every chosen prime")
    source = json.loads(args.input.read_text(encoding="utf-8"))
    rows = [row for row in source["rows"] if (not args.primes or row["p"] in args.primes)
            and row["rhs_index"] < args.instances]
    if not rows:
        parser.error("no matching instances")
    output = []
    for row in rows:
        p, n, m, r = (row[key] for key in ("p", "n", "m", "r"))
        mask = instance_mask(p, r, row["rhs_index"], source["parameters"]["seed"])
        if hashlib.sha256(mask.tobytes()).hexdigest() != row["allowed_mask_sha256"]:
            raise ValueError("allowed-set hash mismatch")
        v = np.array([np.flatnonzero(mask[i]) for i in range(m)], dtype=np.int64)
        ell = n // 2
        problem = MaxOPIProblem(p=p, v=v, num_variables=n, ell=ell, use_cache=False)
        if not math.isclose(problem.n_predicted(), row["dqi_expected_fraction"], abs_tol=1e-12):
            raise ValueError("formula target mismatch")
        lookup_sha256 = hashlib.sha256(
            np.asarray(problem.lookup_log_polynomial_squared, dtype=np.float64).tobytes()
        ).hexdigest()
        run_seed = args.seed * 1000003 + p * 1009 + row["rhs_index"] + 3
        rng = np.random.default_rng(run_seed)
        x0 = rng.integers(0, p, size=n, dtype=np.int64)
        target = row["integer_target"]
        start = time.perf_counter()
        initial_score = int(problem.n_satisfied(x0))
        if initial_score >= target:
            best_x = x0
            best_score = initial_score
            steps = 0
            first_hit = 1
        else:
            max_steps = (args.budget - 1) // p
            sampler = BlockGibbsSampler(problem)
            samples, values = sampler.sample_with_values(
                max_steps, x_0=x0, block_size=1, block_strategy="permutation",
                rng=rng, stop_above=target - 1,
            )
            scores = ((values[:, 1].astype(np.int64) + m) // 2)
            idx = int(np.argmax(scores))
            best_score = int(scores[idx])
            best_x = samples[idx]
            steps = len(samples)
            first_hit = 1 + p * steps if best_score >= target else None
        elapsed = time.perf_counter() - start
        if score_horner(best_x.tolist(), mask, p) != best_score:
            raise AssertionError("independent witness evaluation failed")
        result = {
            "p": p, "rhs_index": row["rhs_index"], "n": n,
            "output_qubits": row["output_qubits"], "ell": ell,
            "target": target, "allowed_mask_sha256": row["allowed_mask_sha256"],
            "lookup_sha256": lookup_sha256, "initial_score": initial_score,
            "best": best_score, "best_coefficients": best_x.tolist(),
            "gibbs_updates": steps, "scored_candidates": 1 + p * steps,
            "first_hit_evaluations": first_hit, "seconds": elapsed,
        }
        output.append(result)
        print(f"p={p} rhs={row['rhs_index']} best={best_score}/{m} "
              f"target={target}/{m} scores={result['scored_candidates']} hit={first_hit}", flush=True)
    document = {
        "upstream": "matanninio/dqi-mcmc@4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b",
        "upstream_version": version("dqi-mcmc"),
        "environment": {"python": platform.python_version(), "numpy": np.__version__},
        "algorithm": "one chain, block size 1, random start, permutation sweep, ell=n//2",
        "candidate_budget": args.budget, "rows": output,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
