"""Audit the pinned TRIQS Sr2RuO4 CT-HYB archive and its current source script.

Requires h5py and NumPy. Downloads the public 8 MB archive unless --archive is
given. This inspects metadata and bath input; it does not solve the impurity.
"""

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path
from urllib.request import urlopen

import h5py
import numpy as np


COMMIT = "e51cbe48ac0e7106c5b9e0b1b80e17af58e4548f"
BASE = f"https://raw.githubusercontent.com/TRIQS/benchmarks/{COMMIT}/Sr2RuO4"
EXPECTED_SHA256 = "2fe7dbc3bb1d58f6816b61e6dd182196c34354eac5bda04cdfd117952e7f443d"


def download(url, path):
    with urlopen(url, timeout=45) as response, path.open("wb") as target:
        for chunk in iter(lambda: response.read(1 << 20), b""):
            target.write(chunk)


def cycles_in_script(source):
    matches = re.findall(r"['\"]n_cycles['\"]\s*:\s*(\d+)", source)
    if len(matches) != 1:
        raise ValueError(f"expected one n_cycles setting, found {len(matches)}")
    return int(matches[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="already downloaded cthyb.h5")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    archive = args.archive or Path(tempfile.gettempdir()) / "pqa_sr2ruo4_cthyb.h5"
    if not archive.exists():
        download(f"{BASE}/results/cthyb.h5", archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("archive SHA256 differs from the audited pinned copy")

    # Sr2RuO4/scripts/cthyb is a text pointer to ../../common/cthyb.
    with urlopen(f"https://raw.githubusercontent.com/TRIQS/benchmarks/{COMMIT}/common/cthyb", timeout=45) as response:
        current_script = response.read().decode("utf-8")
    with h5py.File(archive, "r") as source:
        info = source["Solver_Info"]
        embedded_script = info["script"][()].decode("utf-8")
        delta_pair = info["solver/Delta_tau/up/data"][:]
        delta = delta_pair[..., 0] + 1j * delta_pair[..., 1]
        diagonal = max(np.max(np.abs(delta[:, i, i])) for i in range(3))
        off_diagonal = max(
            np.max(np.abs(delta[:, i, j]))
            for i in range(3) for j in range(3) if i != j
        )
        g_tau_checks = {}
        for spin in ("up", "dn"):
            g_pair = source[f"G_tau/{spin}/data"][:]
            g = g_pair[..., 0] + 1j * g_pair[..., 1]
            diagonal_g = np.stack([g[:, i, i] for i in range(3)], axis=1)
            worst = np.unravel_index(np.argmax(np.abs(diagonal_g)), diagonal_g.shape)
            g_tau_checks[spin] = {
                "diagonal_points_abs_gt_1": int(np.count_nonzero(np.abs(diagonal_g) > 1)),
                "max_abs_diagonal": float(np.abs(diagonal_g[worst])),
                "worst_orbital_zero_based": int(worst[1]),
                "worst_tau": float(worst[0] * info["constr_params/beta"][()] / (len(g) - 1)),
                "worst_value_real": float(diagonal_g[worst].real),
            }
        result = {
            "source_archive": f"{BASE}/results/cthyb.h5",
            "source_current_script": f"https://raw.githubusercontent.com/TRIQS/benchmarks/{COMMIT}/common/cthyb",
            "sha256": digest,
            "beta": float(info["constr_params/beta"][()]),
            "impurity_spin_orbitals": 6,
            "archive_n_cycles": int(info["solve_params/n_cycles"][()]),
            "embedded_script_n_cycles": cycles_in_script(embedded_script),
            "repository_script_n_cycles": cycles_in_script(current_script),
            "archive_num_threads_label": int(info["num_threads"][()]),
            "num_threads_interpretation": "The script assigns mpi.size to this field, so the value counts MPI processes; it is not a hardware-thread count.",
            "archive_wall_seconds": float(info["run_time"][()]),
            "delta_tau_shape": list(delta_pair.shape),
            "g_tau_shape": list(source["G_tau/up/data"].shape),
            "max_abs_delta_tau_diagonal": float(diagonal),
            "max_abs_delta_tau_off_diagonal": float(off_diagonal),
            "off_diagonal_to_diagonal_ratio": float(off_diagonal / diagonal),
            "g_tau_diagonal_bound_check": g_tau_checks,
            "average_sign_recorded": False,
            "limitations": [
                "The near-diagonal bath is specific to this archived non-SOC input; it does not determine the Monte Carlo average sign.",
                "Some archived diagonal G(tau) values exceed magnitude one, the bound for a normalized canonical fermionic Green's function; the archive's estimator or serialization must be checked before treating it as a benchmark reference.",
                "The recorded wall time and MPI count are one run, not a cost-versus-error curve.",
                "The archive stores a Green's function but no independent quantum calculation or finite-bath convergence series.",
                "The current repository script uses a different n_cycles value from the archived run."
            ],
        }
    content = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
