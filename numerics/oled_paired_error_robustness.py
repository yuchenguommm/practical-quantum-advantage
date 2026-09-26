"""Paired-error sensitivity for the public 14-emitter OLED gap table.

The comparison is between two classical calculations on the same measured
emitters. The stratified bootstrap describes finite-cohort sensitivity; it is
not a prospective prediction interval or a quantum-computing benchmark.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "results" / "oled_genin2026_si1.csv"
DESTINATION = ROOT / "results" / "oled_paired_error_robustness.json"
SEED = 20260927
REPLICATES = 20000


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    location = fraction * (len(ordered) - 1)
    lower = int(location)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (location - lower) * (ordered[upper] - ordered[lower])


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if [row["material"] for row in rows] != [f"Q{i}" for i in range(1, 15)]:
        raise ValueError("unexpected molecule order")
    molecules = []
    for index, row in enumerate(rows):
        target = float(row["experiment"])
        td_error = abs(float(row["td_b3lyp"]) - target)
        iqcc_error = abs(float(row["iqcc_pt"]) - target)
        molecules.append({
            "molecule": row["material"], "family": "Ir" if index < 7 else "Pt",
            "td_b3lyp_abs_error_ev": td_error,
            "iqcc_pt_abs_error_ev": iqcc_error,
            "td_minus_iqcc_abs_error_ev": td_error - iqcc_error,
        })
    td = [row["td_b3lyp_abs_error_ev"] for row in molecules]
    iqcc = [row["iqcc_pt_abs_error_ev"] for row in molecules]
    paired = [row["td_minus_iqcc_abs_error_ev"] for row in molecules]
    if not (abs(mean(td) - 0.1209) < 0.001 and abs(mean(iqcc) - 0.0501) < 0.001):
        raise AssertionError("transcription does not match published Table 2 within rounding")
    rng = random.Random(SEED)
    boot = []
    for _ in range(REPLICATES):
        sampled = [paired[rng.randrange(0, 7)] for _ in range(7)]
        sampled += [paired[rng.randrange(7, 14)] for _ in range(7)]
        boot.append(mean(sampled))
    loo = [mean(paired[:i] + paired[i + 1:]) for i in range(14)]
    result = {
        "source": "Genin et al., arXiv:2512.13657v2, Supplementary Table SI.1-2",
        "units": "eV", "bootstrap_seed": SEED,
        "bootstrap_replicates": REPLICATES,
        "bootstrap_design": "Resample 7 Ir and 7 Pt molecule pairs with replacement within their own family; keep the published predictions fixed.",
        "td_b3lyp_mae_from_rounded_table": mean(td),
        "iqcc_pt_mae_from_rounded_table": mean(iqcc),
        "mean_paired_absolute_error_improvement_ev": mean(paired),
        "iqcc_pt_lower_error_count": sum(delta > 0 for delta in paired),
        "td_b3lyp_lower_error_count": sum(delta < 0 for delta in paired),
        "ties": sum(delta == 0 for delta in paired),
        "by_family": {
            family: {
                "td_b3lyp_mae_ev": mean(td[lo:hi]),
                "iqcc_pt_mae_ev": mean(iqcc[lo:hi]),
                "paired_improvement_ev": mean(paired[lo:hi]),
                "iqcc_pt_lower_error_count": sum(delta > 0 for delta in paired[lo:hi]),
            }
            for family, lo, hi in (("Ir", 0, 7), ("Pt", 7, 14))
        },
        "leave_one_molecule_out_improvement_range_ev": [min(loo), max(loo)],
        "stratified_bootstrap_percentile_interval_95_ev": [
            percentile(boot, 0.025), percentile(boot, 0.975)
        ],
        "per_molecule": molecules,
        "limitations": [
            "The 14 emitters are a selected, related cohort, not a random sample of future commercial molecules.",
            "The bootstrap holds both method predictions fixed and does not include geometry, model-selection or experimental systematic uncertainty.",
            "iQCC+PT was run on classical processors, so this is a comparison of two classical workflows, not quantum advantage.",
            "The source table rounds gaps to 0.001 eV; the paper reports 0.0501 eV from unrounded values.",
        ],
    }
    DESTINATION.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("paired improvement", result["mean_paired_absolute_error_improvement_ev"])
    print("stratified bootstrap", result["stratified_bootstrap_percentile_interval_95_ev"])
    print("leave-one-out", result["leave_one_molecule_out_improvement_range_ev"])


if __name__ == "__main__":
    main()
