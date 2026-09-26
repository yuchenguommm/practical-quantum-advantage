# Reproducing the DMFT bath-input check

## Sr2RuO4 public CT-HYB archive audit

`sr2ruo4_archive_audit.py` downloads the pinned public 8 MB `TRIQS/benchmarks/Sr2RuO4/results/cthyb.h5` and verifies its SHA-256, then reads the HDF5 metadata, input `Delta_tau`, and output `G_tau`. It compares the archived run's embedded script with the current script at the same commit. Requires NumPy and h5py:

```sh
python numerics/sr2ruo4_archive_audit.py --output numerics/results/sr2ruo4_cthyb_archive_audit.json
```

The archive reports ten million Monte Carlo cycles, 280 MPI processes and 2536 seconds. The current repository script specifies one million cycles; the embedded original script agrees with the archive. The particular non-SOC bath has negligible off-diagonal hybridisation, and the archive contains four isolated diagonal `G(tau)` entries exceeding magnitude one. The script records the worst coordinates. It does not determine the average sign or repair the Green's-function output. A new solver comparison should first reproduce a physically consistent curve with error bars; no quantum or finite-bath result is produced here.

`sr2ruo4_green_consistency.py` tests whether the archive's saved `G(iw)` is numerically consistent with its `G_tau`, and compares output channels whose input bath and local Hamiltonian are symmetry-equivalent. It also reports the sensitivity of the first 80 frequencies to **diagnostically interpolating** only the four diagonal `|G_tau|>1` samples:

```sh
python numerics/sr2ruo4_green_consistency.py --output numerics/results/sr2ruo4_green_consistency.json
```

The raw Fourier transform and archived `G(iw)` agree within about `1e-5`, so these files do not provide two independent classical answers. Output up/down differences reach `0.0454` despite identical bath inputs; orbital-1/2 differences reach `0.0362`. Interpolation shifts some frequencies by up to `0.00677`, but it is **not** a statistical correction. The single archive has no repeated-run uncertainty estimate. Do not use these descriptive discrepancies as formal error bars or infer their precise cause.

`sr2ruo4_finite_bath_fit.py` fits the **same archive's noninteracting hybridisation input**, using a nonnegative-weight sum of negative-energy bath poles. It needs NumPy, SciPy and h5py. The script verifies the archive and pinned Wannier file by SHA-256, fits 352 selected imaginary-time points and checks 9649 held-out points. It independently reconstructs the Matsubara hybridisation from the archived `G0_iw`, onsite Wannier matrix and `mu=5.3938` in the pinned model:

```sh
python numerics/sr2ruo4_finite_bath_fit.py --output numerics/results/sr2ruo4_finite_bath_fit.json
```

The JSON supplies bath energies and couplings for one to five bath levels per spin per orbital, along with held-out `Delta(tau)` and first-80-frequency `Delta(iw)` errors. It uses 6 impurity spin orbitals and 6n bath spin orbitals for n levels per spin and orbital. At n=2 the 18-mode input fit is below `1e-4` maximum held-out imaginary-time error. This is a finite-bath **input** approximation, not an interacting Green's-function result; the published `G_tau` anomaly and its uncertainty must be resolved before an accuracy or runtime crossover can be assessed.

## OLED calibration sensitivity

`oled_genin2026_dft_si1.csv` transcribes the six DFT columns of Supplementary Table SI.1-3 in [arXiv:2512.13657v2](https://arxiv.org/html/2512.13657). `oled_genin2026_si1.csv` contains the measured and other calculated gaps from SI.1-2. The script checks that each transcribed DFT column reproduces the published Table 2 MAE within rounding, then fits either a mean offset or a two-parameter affine map inside each leave-one-molecule-out fold. It also tests transfer between the seven Ir and seven Pt molecules. With NumPy installed, run:

```sh
python numerics/oled_calibration_sensitivity.py --output numerics/results/oled_genin2026_calibration_sensitivity.json
```

The output includes all ten methods and both calibration rules. The six DFT methods were inspected as a group, so selecting the smallest cross-validated error after the fact is optimistic. These 14 related molecules are not an independent prospective test, and no method runtime is measured here. This sensitivity check is a classical comparator for the OLED application, not a quantum algorithm result.

`oled_nested_dft_selection.py` adds a nested classical method-selection check. For each outer held-out molecule, its inner folds compare the six DFT methods with raw, offset and affine predictions using only the other 13 molecules. A second outer test holds out all Ir and then all Pt compounds, selecting on just the seven training molecules each time. It writes every selected pipeline and prediction:

```sh
python numerics/oled_nested_dft_selection.py --output numerics/results/oled_genin2026_nested_dft_selection.json
```

This prevents each outer test target from influencing its own fitted offset, slope or method choice. The candidate set and analysis were still devised after inspecting the publication; the two metal-family folds are especially noisy. Do not interpret the resulting MAEs as prospective screening guarantees or compare their wall times with iQCC.

## DMFT bath-input check

The scripts `dmft_semicircle_bath.py` and `dmft_semicircle_bath_fit.py` examine the *input bath* of the two-orbital Kanamori model in [Eidelstein, Gull and Cohen, arXiv:1907.08570](https://arxiv.org/abs/1907.08570), Eqs. 5 and the continuous-band paragraph following it. The parameters are `t=1`, `D=2`, `r=1`. The model has four interacting spin orbitals; at `r=1`, its orbital hybridisation matrix has rank one for each spin.

The first script uses the fixed Gauss-Chebyshev rule for the semicircular spectral density. It is a useful check of the analytic transform, **not** an optimized fit. The second fits symmetric pairs of finite-bath poles with positive normalized weights to the first 80 fermionic Matsubara values. It then checks the imaginary-time bath kernel at 81 points against 2048-node quadrature; 4096-node quadrature checks the numerical reference. The fitted kernel is the noninteracting hybridisation `Delta`. It is **not** the interacting impurity Green's function `G`, a DMFT result or a quantum-algorithm benchmark.

The fixed quadrature script uses the Python standard library. For the fit, install NumPy and SciPy, then run from the repository root:

```sh
python numerics/dmft_semicircle_bath.py --output numerics/results/dmft_semicircle_bath.json
python numerics/dmft_semicircle_bath_fit.py --beta 64 --output numerics/results/dmft_semicircle_bath_fit_beta64.json
```

The other published JSON files use `--beta 16`, `32`, `128` and `256`. The optimization stops at the first tested even number of bath nodes with maximum Matsubara error below `1e-3`, or at ten nodes. Results are achieved errors for this local optimizer, not global optima or lower bounds on the number of bath sites. A quantum comparison still needs convergence of `G` at the same temperature and output error, plus state preparation and full workflow costs.

With matplotlib installed, `python numerics/plot_dmft_bath_fit.py` regenerates the [figure](figs/dmft_bath_input_fit.png). The shaded 50–100-qubit region is a register-size reference, not a crossover claim.

## Discrete-bath interacting Green's-function check

`dmft_discrete_kanamori_ed.py` independently reconstructs the paper's two-orbital **discrete** example: two bath energies `±2.3t` per impurity spin-orbital, `r=0.5`, `U=2t`, `J=0.2t`, hence 12 fermionic modes under the stated bath construction. The script diagonalises all fixed-`N_up`, fixed-`N_down` blocks and evaluates `G_00(τ)` from the finite-temperature Lehmann sum. Its built-in noninteracting check compares against an independently diagonalised one-body Hamiltonian; the maximum difference is around `2.5e-14`. It also checks `G(0+) + G(β-) = -1`.

The printed local Hamiltonian in Eq. 5 contains no explicit impurity one-body energy and no explicit pair-hopping operator, though the prose mentions pair hopping. To make this ambiguity visible, the script computes the printed quartic expression both alone and with an **illustrative** pair-hopping term of strength `J`. Run two impurity-level assumptions:

```sh
python numerics/dmft_discrete_kanamori_ed.py --impurity-level 0 --output numerics/results/dmft_discrete_kanamori_ed_printed_level0.json
python numerics/dmft_discrete_kanamori_ed.py --impurity-level -1 --output numerics/results/dmft_discrete_kanamori_ed_level_minus1.json
```

NumPy is required. `dmft_digitize_fig2.py` downloads the public arXiv v2 source and reads the dashed ED path endpoints from the original vector figure using requests and PyMuPDF. The extracted numbers are **approximate figure readouts**, not raw author data. With matplotlib, `plot_dmft_discrete_ed.py` regenerates the [comparison figure](figs/dmft_discrete_ed_audit.png). A level of `−1` gives a much closer match to the published endpoints, but it is an inference. Other undocumented conventions may contribute. The code therefore makes no claim to have reproduced the authors' exact input Hamiltonian.

The JSON also records the low-energy gap. In the level-`−1` variant without the illustrative pair-hopping addition, a doublet lies only `0.0254t` above the ground doublet. Its relative Boltzmann weight at `βt=64` is about `0.20`; a zero-temperature calculation should not be compared directly with the paper's finite-temperature result.

## Continuous-bath interacting Green's-function check

The ED script also accepts the **fitted semicircular bath**. This remains finite-temperature ED of a small discretised Hamiltonian. The option does not simulate a quantum computer. For example, from the repository root:

```sh
python numerics/dmft_discrete_kanamori_ed.py --semicircle-fit numerics/results/dmft_semicircle_bath_fit_beta16.json --bath-nodes-per-spin 4 --beta 16 --impurity-level -1 --output numerics/results/dmft_semicircle_interacting_ed_beta16_n4_levelminus1.json
python numerics/dmft_digitize_fig2.py --output numerics/results/dmft_kanamori_fig2_digitized.json
python numerics/dmft_compare_inchworm.py --output numerics/results/dmft_semicircle_interacting_comparison.json
```

The other committed ED outputs use `(βt, bath nodes/spin) = (16,2), (32,4), (64,4)`. The digitizer reads the green continuous-bath Inchworm curves from the same vector Fig. 2 source as the dashed discrete ED curves. It can also use `--figure path/to/kanamori_gf.pdf` if the original arXiv v2 figure is cached locally. The code reports five plotted coordinates and the curve's line half-width, about `0.026` in Green's-function units. This is a limit of reading a published plot, not a confidence interval. The source paper does not document the `-1` impurity level for this panel; it was inferred from the separate discrete-bath example. The four-level finite bath at `βt=64` has Matsubara input error `0.084`, so agreement at five plot coordinates is **not** a bath-size convergence test. Reproducing the authors' raw curve and exact Hamiltonian convention remains open.
