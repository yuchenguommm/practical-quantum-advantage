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


if __name__ == "__main__":
    main()
