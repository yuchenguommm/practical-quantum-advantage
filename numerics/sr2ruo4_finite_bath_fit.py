"""Positive-weight finite-bath input fit for the pinned Sr2RuO4 archive.

Fits the archived Delta(tau), not its interacting Green's function. Requires
NumPy, SciPy and h5py. The current model has a numerically diagonal,
spin-independent hybridisation; we fit its two distinct orbital curves.
"""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import h5py
import numpy as np
from scipy.optimize import least_squares

from sr2ruo4_archive_audit import EXPECTED_SHA256, BASE, download

WANNIER_SHA256 = "f60b863bcd9c40d042e15cdfa942444dbf0ba2f656aec2bbd44ed52bb4942562"


def onsite_matrix(path):
    matrix = np.zeros((3, 3), dtype=complex)
    found = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if len(fields) != 7:
            continue
        try:
            rx, ry, rz, i, j = map(int, fields[:5])
            real, imag = map(float, fields[5:])
        except ValueError:
            continue
        if (rx, ry, rz) == (0, 0, 0) and 1 <= i <= 3 and 1 <= j <= 3:
            if (i, j) in found:
                raise ValueError("duplicate onsite Wannier entry")
            found.add((i, j))
            matrix[i - 1, j - 1] = real + 1j * imag
    if len(found) != 9 or np.max(np.abs(matrix - matrix.conj().T)) > 1e-8:
        raise ValueError("incomplete or non-Hermitian onsite Wannier matrix")
    return matrix


def kernel(x, energies, amplitudes):
    return np.exp(-x[:, None] * energies[None, :]) @ amplitudes


def fit_curve(x, target, train, n_poles):
    x_train = x[train]
    y_train = target[train]
    best = None
    for scale in (1.0, 2.0, 4.0):
        start_e = np.geomspace(0.5, 8.0 * scale, n_poles)
        start_w = np.full(n_poles, max(target[0], 0.01) / n_poles)
        result = least_squares(
            lambda p: kernel(x_train, p[:n_poles], p[n_poles:]) - y_train,
            np.r_[start_e, start_w],
            bounds=(np.r_[np.full(n_poles, 1e-5), np.zeros(n_poles)],
                    np.r_[np.full(n_poles, 150.0), np.full(n_poles, 2.0)]),
            max_nfev=1000,
            ftol=1e-11,
            xtol=1e-11,
            gtol=1e-11,
        )
        if best is None or np.linalg.norm(result.fun) < np.linalg.norm(best.fun):
            best = result
    energies = best.x[:n_poles]
    amplitudes = best.x[n_poles:]
    # For a negative bath energy -E, Delta(beta-x) =
    # -V^2 exp(-E*x)/(1+exp(-beta*E)).
    return energies, amplitudes, best.success


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--wannier", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-levels", type=int, default=5)
    args = parser.parse_args()

    archive = args.archive or Path(tempfile.gettempdir()) / "pqa_sr2ruo4_cthyb.h5"
    if not archive.exists():
        download(f"{BASE}/results/cthyb.h5", archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("archive SHA256 differs from audited source")
    wannier = args.wannier or Path(tempfile.gettempdir()) / "pqa_sr2ruo4_w2w_hr.dat"
    if not wannier.exists():
        download(f"{BASE}/w2w_hr.dat", wannier)
    wannier_digest = hashlib.sha256(wannier.read_bytes()).hexdigest()
    if wannier_digest != WANNIER_SHA256:
        raise ValueError("Wannier SHA256 differs from audited source")
    h0 = onsite_matrix(wannier)
    with h5py.File(archive, "r") as source:
        beta = float(source["Solver_Info/constr_params/beta"][()])
        delta_pair = source["Solver_Info/solver/Delta_tau/up/data"][:]
        delta_down = source["Solver_Info/solver/Delta_tau/dn/data"][:]
        if np.max(np.abs(delta_pair - delta_down)) > 1e-10:
            raise ValueError("spin blocks differ; current spin-independent fit is invalid")
        delta = delta_pair[..., 0] + 1j * delta_pair[..., 1]
        off_diagonal = max(
            np.max(np.abs(delta[:, i, j]))
            for i in range(3) for j in range(3) if i != j
        )
        if off_diagonal > 1e-8:
            raise ValueError("bath matrix is not approximately diagonal")
        orbital_difference = float(np.max(np.abs(delta[:, 1, 1] - delta[:, 2, 2])))
        if orbital_difference > 1e-7:
            raise ValueError("orbital 1 and 2 are not equivalent")
        g0_pair = source["Solver_Info/solver/G0_iw/up/data"][:]
        g0 = g0_pair[..., 0] + 1j * g0_pair[..., 1]
        if len(g0) < 160 or len(g0) % 2:
            raise ValueError("unexpected Matsubara mesh in G0 archive")
        g0_positive = g0[len(g0) // 2:len(g0) // 2 + 80]

    x = np.linspace(0, beta, len(delta))
    # x = beta - tau: reverse the archived order. Dense near the rapid
    # endpoint decay, with independent withheld grid points for validation.
    train = np.unique(np.rint(np.r_[
        np.linspace(0, 300, 151),
        np.linspace(301, len(x) - 1, 201),
    ]).astype(int))
    held_out = np.setdiff1d(np.arange(len(x)), train)
    tau = np.linspace(0, beta, len(delta))
    omega = (2 * np.arange(80) + 1) * np.pi / beta
    phase = np.exp(1j * omega[:, None] * tau[None, :])
    mu = 5.3938  # Pinned Sr2RuO4/model.py
    direct_matsubara = (
        1j * omega[:, None, None] * np.eye(3)[None, :, :]
        + mu * np.eye(3)[None, :, :]
        - h0[None, :, :]
        - np.linalg.inv(g0_positive)
    )
    archived_matsubara = {
        orbital: np.trapz(phase * delta[None, :, orbital, orbital], tau, axis=1)
        for orbital in (0, 1)
    }
    source_consistency = max(
        float(np.max(np.abs(
            archived_matsubara[orbital]
            - direct_matsubara[:, orbital, orbital]
        ))) for orbital in (0, 1)
    )
    if source_consistency > 1e-4:
        raise ValueError("archive Delta(tau) and G0-derived Delta(iw) disagree")
    rows = []
    for n in range(1, args.max_levels + 1):
        by_orbital = []
        for orbital in (0, 1):
            target = -delta[::-1, orbital, orbital].real
            energies, amplitudes, success = fit_curve(x, target, train, n)
            estimate = kernel(x, energies, amplitudes)
            error = np.abs(estimate - target)
            weights = amplitudes * (1 + np.exp(-beta * energies))
            fitted_matsubara = np.sum(
                weights[None, :] / (1j * omega[:, None] + energies[None, :]),
                axis=1,
            )
            freq_error = np.abs(fitted_matsubara - archived_matsubara[orbital])
            direct_freq_error = np.abs(
                fitted_matsubara - direct_matsubara[:, orbital, orbital]
            )
            order = np.argsort(energies)
            energies = energies[order]
            amplitudes = amplitudes[order]
            by_orbital.append({
                "orbital_zero_based": orbital,
                "bath_energies": [float(-e) for e in energies],
                "couplings": [
                    float(np.sqrt(w * (1 + np.exp(-beta * e))))
                    for e, w in zip(energies, amplitudes)
                ],
                "max_abs_error_all_tau": float(np.max(error)),
                "max_abs_error_held_out_tau": float(np.max(error[held_out])),
                "rms_error_held_out_tau": float(np.sqrt(np.mean(error[held_out] ** 2))),
                "max_abs_error_first_80_matsubara_from_archived_tau": float(np.max(freq_error)),
                "lowest_matsubara_abs_error_from_archived_tau": float(freq_error[0]),
                "max_abs_error_first_80_matsubara_from_g0": float(np.max(direct_freq_error)),
                "fit_success": bool(success),
            })
        rows.append({
            "bath_levels_per_spin_per_orbital": n,
            "system_fermion_modes": 6 + 6 * n,
            "worst_max_abs_error_held_out_tau": max(
                item["max_abs_error_held_out_tau"] for item in by_orbital
            ),
            "orbitals": by_orbital,
        })
    result = {
        "source": f"{BASE}/results/cthyb.h5",
        "sha256": digest,
        "wannier_sha256": wannier_digest,
        "beta": beta,
        "target": "archived up-spin diagonal Delta(tau), orbital 0 and degenerate orbitals 1/2",
        "fit": "positive-weight negative-energy bath poles, nonlinear least squares on selected imaginary-time points",
        "training_points": len(train),
        "held_out_points": len(held_out),
        "orbital_1_2_max_difference": orbital_difference,
        "max_delta_tau_fourier_vs_g0_first_80": source_consistency,
        "max_positive_diagonal_delta_tau": max(
            float(np.max(delta[:, orbital, orbital].real))
            for orbital in (0, 1)
        ),
        "limitations": [
            "The archive Delta(tau) has small positive ringing near tau=0; positive-weight finite baths cannot reproduce that exactly.",
            "This is a held-out input-kernel fit, not interacting-G convergence or a quantum computation.",
            "The 80 Matsubara values derived from archived G0 and pinned Wannier onsite terms independently cross-check the Delta(tau) fit. The separate numerical Fourier transform of Delta(tau) has endpoint ringing and integration error.",
            "The selected multi-start optimizer does not certify minimal bath size.",
            "Any scalar bath fit must still be checked against Matsubara Delta, the interacting Green's function, and the full DMFT loop.",
        ],
        "rows": rows,
    }
    content = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
