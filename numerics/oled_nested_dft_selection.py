"""Nested DFT method-and-calibration selection on the 14 published OLED emitters.

Source: Genin et al., arXiv:2512.13657v2, SI.1-2 and SI.1-3.
This is a small retrospective cohort analysis, not prospective validation.
"""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np

from oled_calibration_sensitivity import DFT, MAIN, REPORTED_DFT_MAE


def predict(x, y, train, test, calibration):
    if calibration == "raw":
        return x[test]
    if calibration == "offset":
        return x[test] + np.mean(y[train] - x[train])
    if calibration == "affine":
        matrix = np.column_stack((x[train], np.ones(len(train))))
        slope, intercept = np.linalg.lstsq(matrix, y[train], rcond=None)[0]
        return slope * x[test] + intercept
    raise ValueError(calibration)


def choose_method(x_by_method, y, training):
    # Every inner validation target lies inside the outer training set.
    scores = []
    for method, x in x_by_method.items():
        for calibration in ("raw", "offset", "affine"):
            errors = []
            for held_out in training:
                inner_train = training[training != held_out]
                estimate = predict(x, y, inner_train, held_out, calibration)
                errors.append(abs(float(estimate) - y[held_out]))
            scores.append((float(np.mean(errors)), method, calibration))
    return min(scores)


def evaluate(x_by_method, y, folds):
    output = np.empty(len(y))
    choices = []
    for test in folds:
        train = np.setdiff1d(np.arange(len(y)), test)
        score, method, calibration = choose_method(x_by_method, y, train)
        output[test] = predict(x_by_method[method], y, train, test, calibration)
        choices.append({
            "held_out": [int(i + 1) for i in test],
            "selected_method": method,
            "selected_calibration": calibration,
            "inner_mae_ev": score,
            "outer_mae_ev": float(np.mean(np.abs(output[test] - y[test]))),
        })
    return {
        "mae_ev": float(np.mean(np.abs(output - y))),
        "predictions_ev": [float(value) for value in output],
        "choices": choices,
        "choice_counts": dict(sorted(Counter(
            f"{item['selected_method']}:{item['selected_calibration']}"
            for item in choices
        ).items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with MAIN.open(newline="", encoding="utf-8") as handle:
        main_rows = list(csv.DictReader(handle))
    with DFT.open(newline="", encoding="utf-8") as handle:
        dft_rows = list(csv.DictReader(handle))
    if [row["material"] for row in main_rows] != [row["material"] for row in dft_rows]:
        raise ValueError("Molecular rows do not match")
    y = np.array([float(row["experiment"]) for row in main_rows])
    x_by_method = {
        method: np.array([float(row[method]) for row in dft_rows])
        for method in REPORTED_DFT_MAE
    }
    loo = evaluate(x_by_method, y, [np.array([i]) for i in range(len(y))])
    family = evaluate(x_by_method, y, [np.arange(7), np.arange(7, 14)])
    result = {
        "source": "https://arxiv.org/html/2512.13657",
        "source_tables": ["SI.1-2", "SI.1-3"],
        "candidates": "six published DFT methods × raw, offset, affine calibration",
        "selection": "For each outer fold, select minimum inner leave-one-out MAE using only outer-training targets; refit selected calibration on all outer-training molecules.",
        "nested_leave_one_molecule_out": loo,
        "nested_leave_one_metal_family_out": family,
        "raw_iqcc_pt_mae_ev_from_rounded_table": float(
            np.mean(np.abs(
                np.array([float(row["iqcc_pt"]) for row in main_rows]) - y
            ))
        ),
        "limitations": [
            "The 18 candidate pipelines and this analysis were designed after seeing the publication; nested selection prevents per-fold target leakage but cannot undo study-level model choice.",
            "Fourteen related molecules give imprecise generalization estimates; the two-family holdout has only two outer folds.",
            "Differences in geometry and computational cost between methods are not controlled.",
            "A prospective test set and same-instance quantum costs remain unavailable."
        ],
    }
    content = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
