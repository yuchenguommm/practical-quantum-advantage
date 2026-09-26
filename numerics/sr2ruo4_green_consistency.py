"""Internal consistency and isolated-spike sensitivity of Sr2RuO4 CT-HYB output.

Uses the pinned HDF5 archive. No replacement values are presented as a new
classical reference; interpolation is only a sensitivity test.
"""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import h5py
import numpy as np

from sr2ruo4_archive_audit import BASE, EXPECTED_SHA256, download


def complex_array(pair):
    return pair[..., 0] + 1j * pair[..., 1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    archive = args.archive or Path(tempfile.gettempdir()) / "pqa_sr2ruo4_cthyb.h5"
    if not archive.exists():
        download(f"{BASE}/results/cthyb.h5", archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("archive differs from pinned source")

    rows = []
    with h5py.File(archive, "r") as source:
        beta = float(source["Solver_Info/constr_params/beta"][()])
        delta_up = source["Solver_Info/solver/Delta_tau/up/data"][:]
        delta_dn = source["Solver_Info/solver/Delta_tau/dn/data"][:]
        bath_spin_difference = float(np.max(np.abs(delta_up - delta_dn)))
        bath_orbital_difference = float(np.max(np.abs(
            delta_up[:, 1, 1] - delta_up[:, 2, 2]
        )))
        if bath_spin_difference > 1e-10 or bath_orbital_difference > 1e-8:
            raise ValueError("expected spin and orbital bath symmetries absent")
        output_g = {}
        for spin in ("up", "dn"):
            g_tau = complex_array(source[f"G_tau/{spin}/data"][:])
            g_iw = complex_array(source[f"G/{spin}/data"][:])
            output_g[spin] = g_iw
            if len(g_iw) != 500 or len(g_tau) != 10001:
                raise ValueError("unexpected archive mesh size")
            n_freq = 80
            omega = (2 * np.arange(n_freq) + 1) * np.pi / beta
            tau = np.linspace(0, beta, len(g_tau))
            phase = np.exp(1j * omega[:, None] * tau[None, :])
            for orbital in range(3):
                raw = g_tau[:, orbital, orbital]
                archived_frequency = g_iw[250:250 + n_freq, orbital, orbital]
                transformed = np.trapz(phase * raw[None, :], tau, axis=1)
                spikes = np.flatnonzero(np.abs(raw) > 1)
                corrected = raw.copy()
                spike_details = []
                for index in spikes:
                    if index == 0 or index == len(raw) - 1:
                        raise ValueError("endpoint outlier cannot be interpolated")
                    neighbor_mean = (raw[index - 1] + raw[index + 1]) / 2
                    spike_details.append({
                        "tau_index": int(index),
                        "tau": float(tau[index]),
                        "archived_real": float(raw[index].real),
                        "neighbor_mean_real": float(neighbor_mean.real),
                    })
                    corrected[index] = neighbor_mean
                corrected_frequency = np.trapz(
                    phase * corrected[None, :], tau, axis=1
                )
                change = np.abs(corrected_frequency - transformed)
                rows.append({
                    "spin": spin,
                    "orbital_zero_based": orbital,
                    "endpoint_sum_real": float((raw[0] + raw[-1]).real),
                    "endpoint_sum_imag": float((raw[0] + raw[-1]).imag),
                    "max_abs_archived_g_tau": float(np.max(np.abs(raw))),
                    "spikes_abs_gt_1": spike_details,
                    "max_abs_raw_tau_fourier_vs_archived_g_iw_first_80": float(
                        np.max(np.abs(transformed - archived_frequency))
                    ),
                    "max_abs_frequency_shift_after_interpolating_spikes_first_80": float(
                        np.max(change)
                    ),
                    "lowest_frequency_shift_after_interpolating_spikes": float(
                        change[0]
                    ),
                    "lowest_abs_archived_g_iw": float(abs(archived_frequency[0])),
                    "max_abs_corrected_tau_fourier_vs_archived_g_iw_first_80": float(
                        np.max(np.abs(corrected_frequency - archived_frequency))
                    ),
                })
    up = output_g["up"][250:330]
    dn = output_g["dn"][250:330]
    spin_differences = [np.abs(up[:, i, i] - dn[:, i, i]) for i in range(3)]
    orbital_differences = {
        spin: np.abs(output_g[spin][250:330, 1, 1] - output_g[spin][250:330, 2, 2])
        for spin in ("up", "dn")
    }
    result = {
        "source": f"{BASE}/results/cthyb.h5",
        "sha256": digest,
        "beta": beta,
        "input_bath_max_up_down_difference": bath_spin_difference,
        "input_bath_max_orbital_1_2_difference": bath_orbital_difference,
        "output_symmetry_checks_first_80_matsubara": {
            "up_down_max_abs_difference_by_orbital": [
                float(np.max(value)) for value in spin_differences
            ],
            "max_up_down_abs_difference": float(max(
                np.max(value) for value in spin_differences
            )),
            "at_least_one_raw_spin_channel_abs_error_lower_bound": float(
                max(np.max(value) for value in spin_differences) / 2
            ),
            "up_down_lowest_frequency_abs_difference_by_orbital": [
                float(value[0]) for value in spin_differences
            ],
            "orbital_1_2_max_abs_difference_by_spin": {
                spin: float(np.max(value))
                for spin, value in orbital_differences.items()
            },
            "orbital_1_2_lowest_frequency_abs_difference_by_spin": {
                spin: float(value[0])
                for spin, value in orbital_differences.items()
            },
        },
        "method": "Trapezoidal Fourier transform of archived G_tau at 80 positive fermionic Matsubara frequencies; compare with archived G; replace only diagonal samples with |G_tau|>1 by neighbor mean as a sensitivity test.",
        "limitations": [
            "The stored G(iw) may have been calculated from the same G(tau); agreement is internal consistency, not independent validation.",
            "The spin bound follows from |G_up-G_dn| <= |G_up-G_exact|+|G_dn-G_exact| for a spin-symmetric model. It applies to at least one unsymmetrized archived channel at one frequency, not a symmetrized estimator or a rerun; it is not a statistical confidence interval.",
            "Interpolation is diagnostic only and does not recover an unbiased CT-HYB estimator or uncertainty bars.",
            "A canonical diagonal fermionic G(tau) should have magnitude at most one; this test does not diagnose the cause of the outliers.",
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
