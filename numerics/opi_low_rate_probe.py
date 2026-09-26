"""Seeded classical OPI probe near coefficient-to-field ratio 0.1.

This tests explicit random instances at the original DQI comparison's rate.
Methods are random polynomial search and Prange initialization followed by
single-coordinate ascent with restarts. Neither is a quantum runtime benchmark.
Requires NumPy; use --instances/--budget to control the experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import time
from pathlib import Path

import numpy as np


def smallest_primitive_root(p: int) -> int:
    factors = [q for q in range(2, p) if (p - 1) % q == 0 and all(q % d for d in range(2, math.isqrt(q) + 1))]
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in factors))


def vandermonde(p: int, n: int) -> np.ndarray:
    gamma = smallest_primitive_root(p)
    points = np.array([pow(gamma, i, p) for i in range(p - 1)], dtype=np.int64)
    return np.array([[pow(int(a), j, p) for j in range(n)] for a in points], dtype=np.int64)


def interpolate_modp(a: np.ndarray, b: np.ndarray, p: int) -> np.ndarray:
    """Solve a square full-rank Vandermonde subsystem over F_p."""
    n = len(b)
    aug = np.column_stack((a, b)).astype(np.int64) % p
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row, col] % p)
        aug[[col, pivot]] = aug[[pivot, col]]
        aug[col] = aug[col] * pow(int(aug[col, col]), -1, p) % p
        for row in range(n):
            if row != col:
                aug[row] = (aug[row] - aug[row, col] * aug[col]) % p
    return aug[:, n]


def instance_mask(p: int, r: int, index: int, seed: int) -> np.ndarray:
    """Match the upstream generator's stream for a selected RHS index."""
    rng = np.random.default_rng(seed)
    mask = np.zeros((p - 1, p), dtype=bool)
    for k in range((index + 1) * (p - 1)):
        values = rng.choice(p, size=r, replace=False)
        if k >= index * (p - 1):
            mask[k % (p - 1), values] = True
    return mask


def score_batch(x: np.ndarray, a: np.ndarray, mask: np.ndarray, p: int) -> np.ndarray:
    y = (a @ x.T) % p
    return mask[np.arange(len(a))[:, None], y].sum(axis=0)


def prange_seed(a: np.ndarray, mask: np.ndarray, p: int, rng: np.random.Generator) -> np.ndarray:
    n = a.shape[1]
    selected = rng.choice(len(a), size=n, replace=False)
    values = np.array([rng.choice(np.flatnonzero(mask[i])) for i in selected], dtype=np.int64)
    x = interpolate_modp(a[selected], values, p)
    if not np.all(mask[selected, (a[selected] @ x) % p]):
        raise AssertionError("interpolated polynomial misses its selected constraints")
    return x


def random_search(a: np.ndarray, mask: np.ndarray, p: int, target: int, budget: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    best = -1
    best_x = None
    first_hit = None
    first_hit_position = None
    t0 = time.perf_counter()
    for offset in range(0, budget, 512):
        count = min(512, budget - offset)
        xs = rng.integers(0, p, size=(count, a.shape[1]), dtype=np.int64)
        scores = score_batch(xs, a, mask, p)
        idx_best = int(np.argmax(scores))
        if int(scores[idx_best]) > best:
            best = int(scores[idx_best])
            best_x = xs[idx_best].tolist()
        if first_hit is None and np.any(scores >= target):
            idx_hit = int(np.flatnonzero(scores >= target)[0])
            first_hit_position = offset + idx_hit + 1
            # The whole vectorized batch was evaluated before this check.
            first_hit = offset + count
            break
    return {"best": best, "first_hit_evaluations": first_hit, "evaluations": first_hit or budget,
            "first_hit_position": first_hit_position, "best_coefficients": best_x,
            "seconds": time.perf_counter() - t0}


def coordinate_search(a: np.ndarray, mask: np.ndarray, p: int, target: int, budget: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    m, n = a.shape
    symbols = np.arange(p, dtype=np.int64)
    best = -1
    best_x = None
    evaluations = 0
    restarts = 0
    first_hit = None
    t0 = time.perf_counter()
    while evaluations + p <= budget and first_hit is None:
        x = prange_seed(a, mask, p, rng)
        restarts += 1
        y = (a @ x) % p
        score = int(mask[np.arange(m), y].sum())
        evaluations += 1
        if score > best:
            best = score
            best_x = x.tolist()
        if score >= target:
            first_hit = evaluations
            break
        while evaluations + p <= budget and first_hit is None:
            improved = False
            for j in rng.permutation(n):
                if evaluations + p > budget:
                    break
                base = (y - x[j] * a[:, j]) % p
                trial = (base[:, None] + a[:, j, None] * symbols[None, :]) % p
                scores = mask[np.arange(m)[:, None], trial].sum(axis=0)
                evaluations += p
                new_score = int(scores.max())
                if new_score > score:
                    choices = np.flatnonzero(scores == new_score)
                    x[j] = int(rng.choice(choices))
                    y = trial[:, x[j]]
                    score = new_score
                    improved = True
                    if score > best:
                        best = score
                        best_x = x.tolist()
                if score >= target:
                    first_hit = evaluations
                    break
            if not improved:
                break
    return {"best": best, "first_hit_evaluations": first_hit, "evaluations": evaluations,
            "best_coefficients": best_x, "restarts": restarts, "seconds": time.perf_counter() - t0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=int, nargs="+", default=[31, 43, 61, 89, 127])
    parser.add_argument("--instances", type=int, default=10)
    parser.add_argument("--budget", type=int, default=20000, help="max scored polynomial candidates per method and instance")
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.instances < 1 or args.budget < max(args.primes):
        parser.error("need at least one instance and budget >= largest prime")
    rows = []
    for p in args.primes:
        if p < 11 or any(p % d == 0 for d in range(2, math.isqrt(p) + 1)):
            parser.error(f"expected an odd prime >= 11, got {p}")
        m = p - 1
        n = max(1, round(m / 10))
        r = p // 2
        ell = n // 2
        if ell == 0:
            parser.error("need at least two coefficients")
        fraction = (math.sqrt(ell / m * (1 - r / p)) + math.sqrt(r / p * (1 - ell / m))) ** 2
        target = math.ceil(fraction * m)
        a = vandermonde(p, n)
        for i in range(args.instances):
            mask = instance_mask(p, r, i, args.seed)
            mask_sha256 = hashlib.sha256(mask.tobytes()).hexdigest()
            run_seed = args.seed * 1000003 + p * 1009 + i
            random_result = random_search(a, mask, p, target, args.budget, run_seed)
            coord_result = coordinate_search(a, mask, p, target, args.budget, run_seed + 1)
            for result in (random_result, coord_result):
                witness = np.array(result["best_coefficients"], dtype=np.int64)
                verified = int(score_batch(witness[None, :], a, mask, p)[0])
                if verified != result["best"]:
                    raise AssertionError("stored witness score failed independent recomputation")
            row = {"p": p, "rhs_index": i, "n": n, "m": m, "r": r, "ell": ell,
                   "allowed_mask_sha256": mask_sha256,
                   "output_qubits": n * math.ceil(math.log2(p)),
                   "dqi_expected_fraction": fraction, "integer_target": target,
                   "random": random_result, "prange_coordinate": coord_result}
            rows.append(row)
            print(f"p={p} rhs={i} q={row['output_qubits']} target={target}/{m} "
                  f"random={random_result['first_hit_evaluations']} "
                  f"coord={coord_result['first_hit_evaluations']}", flush=True)
    result = {"description": "seeded low-rate OPI classical search probe",
              "environment": {"python": platform.python_version(), "numpy": np.__version__},
              "parameters": vars(args) | {"output": None},
              "rows": rows}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
