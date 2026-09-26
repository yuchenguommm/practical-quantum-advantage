"""Check every published low-rate OPI witness by modular Horner evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from opi_low_rate_probe import instance_mask, smallest_primitive_root


def score_horner(coefficients: list[int], mask, p: int) -> int:
    gamma = smallest_primitive_root(p)
    point = 1
    hits = 0
    for i in range(p - 1):
        value = 0
        for coefficient in reversed(coefficients):
            value = (value * point + coefficient) % p
        hits += bool(mask[i, value])
        point = point * gamma % p
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("--gibbs", type=Path, help="optional result from opi_low_rate_block_gibbs.py")
    args = parser.parse_args()
    data = json.loads(args.result.read_text(encoding="utf-8"))
    rows = data["rows"]
    if len({(row["p"], row["rhs_index"]) for row in rows}) != len(rows):
        raise AssertionError("duplicate instance")
    seed = data["parameters"]["seed"]
    budget = data["parameters"]["budget"]
    for row in rows:
        p, n, m, r = (row[key] for key in ("p", "n", "m", "r"))
        assert m == p - 1 and r == p // 2 and n == round(m / 10)
        assert row["output_qubits"] == n * math.ceil(math.log2(p))
        mask = instance_mask(p, r, row["rhs_index"], seed)
        assert hashlib.sha256(mask.tobytes()).hexdigest() == row["allowed_mask_sha256"]
        for name in ("random", "prange_coordinate"):
            result = row[name]
            x = result["best_coefficients"]
            assert len(x) == n and all(isinstance(c, int) and 0 <= c < p for c in x)
            assert score_horner(x, mask, p) == result["best"]
            hit = result["first_hit_evaluations"]
            assert (hit is not None) == (result["best"] >= row["integer_target"])
            assert 0 < result["evaluations"] <= budget
            if hit is not None:
                assert 0 < hit <= result["evaluations"]
    print(f"verified {len(rows)} instances and {2 * len(rows)} best-polynomial witnesses")
    if args.gibbs:
        gibbs = json.loads(args.gibbs.read_text(encoding="utf-8"))
        by_id = {(row["p"], row["rhs_index"]): row for row in rows}
        assert len(gibbs["rows"]) == len(by_id)
        assert len({(row["p"], row["rhs_index"]) for row in gibbs["rows"]}) == len(by_id)
        for result in gibbs["rows"]:
            key = (result["p"], result["rhs_index"])
            reference = by_id[key]
            p = result["p"]
            assert result["target"] == reference["integer_target"]
            assert result["ell"] == reference["n"] // 2
            assert result["output_qubits"] == reference["output_qubits"]
            assert result["allowed_mask_sha256"] == reference["allowed_mask_sha256"]
            assert result["scored_candidates"] == 1 + p * result["gibbs_updates"]
            assert result["scored_candidates"] <= gibbs["candidate_budget"]
            assert (result["first_hit_evaluations"] is not None) == (
                result["best"] >= reference["integer_target"]
            )
            mask = instance_mask(p, reference["r"], result["rhs_index"], seed)
            assert score_horner(result["best_coefficients"], mask, p) == result["best"]
        print(f"verified {len(gibbs['rows'])} Gibbs witnesses against the same instances")


if __name__ == "__main__":
    main()
