---
type: question
id: dmft-impurity-cost-vs-ctqmc-sign-problem
title: Which DMFT impurity defeats the best classical solver, and can a quantum solver help?
title_zh: 哪个 DMFT 杂质超出最强经典求解器的能力，量子求解器能否帮助？
summary: "Sign-problem papers supply concrete CT-HYB bottlenecks and classical responses: Inchworm solves a low-temperature model whose CT-HYB cost was extrapolated to 3 billion core-hours, while hybrid DMFT runs roughly 40 times faster than full five-orbital DMFT on two real oxides. A quantum advantage needs the strongest classical baseline on the same impurity and observable."
summary_zh: 符号问题论文给出了 CT-HYB 的具体瓶颈，也给出了经典替代方案：Inchworm 求解了一个 CT-HYB 外推需要约 30 亿核小时的低温模型；混合 DMFT 在两种真实氧化物上比完整五轨道 DMFT 快约 40 倍。量子优势必须在同一杂质和输出量上与最强经典方法比较。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Publish a named impurity Hamiltonian or hybridisation function, inverse temperature, Green's-function definition and error tolerance tied to an application. Compare optimised CT-HYB, Inchworm, hybrid DMFT where valid, tensor-train, MPS and neural-network solvers on that same observable. For a quantum algorithm either prepare the corresponding thermal state and compute the same finite-temperature imaginary-time response, or benchmark both sides at zero temperature. Include bath-discretisation error, state preparation, ancillas, repetitions, and full DMFT-loop cost. A small CT-HYB average sign by itself does not settle the question."
  difficulty: phd
  resolved: false
related:
  applications: [rare-earth-permanent-magnets, battery-cathode-spectroscopy, nuclear-fuel-actinide-spectra]
  problems: [linear-response-spectral-functions]
  methods: [dmft-impurity-solver, phase-estimation]
references:
  - {arxiv: "1510.03859", title: "Hybrid quantum-classical approach to correlated materials", authors: "B. Bauer, D. Wecker, A. J. Millis, M. B. Hastings, M. Troyer", year: 2016, note: "PRX 6, 031045 (2016); the 'about a hundred logical qubits' proposal"}
  - {arxiv: "2605.22920", title: "Estimating Green's functions with a robust quantum Arnoldi method", authors: "J. S. Nelson, A. D. Baczewski", year: 2026}
  - {arxiv: "2603.15741", title: "Neural-Network Quantum Embedding Solvers for Correlated Materials", authors: "A. Valenti, J. Park, A. Georges, A. J. Millis, O. Parcollet", year: 2026}
  - {arxiv: "2207.06135", title: "Learning Feynman Diagrams with Tensor Trains", authors: "Y. Núñez Fernández et al.", year: 2022, note: "PRX 12, 041018 (2022); tensor cross interpolation for diagrammatic sums"}
  - {arxiv: "2206.15093", title: "Ce and Dy substitutions in Nd$_{2}$Fe$_{14}$B: site-specific magnetic anisotropy from first-principles", authors: "J. Boust et al.", year: 2022, note: "Direct alloy study; mixed-valent Ce modelled approximately"}
  - {arxiv: "2510.02875", title: "Redox Chemistry of LiCoO$_2$, LiNiO$_2$, and LiNi$_{1/3}$Mn$_{1/3}$Co$_{1/3}$O$_2$ Cathodes: Deduced via XPS, DFT+DMFT, and Charge Transfer Multiplet Simulations", authors: "Y. Xie, F. Mellin, W. Jaegermann, S. Hofmann, F. M. F. de Groot, H. Zhang", year: 2025}
  - {arxiv: "2404.09527", title: "Dynamical Mean Field Theory for Real Materials on a Quantum Computer", authors: "J. Selisko, M. Amsler, C. Wrigley et al.", year: 2024, note: "Ca2CuO2Cl2 on 14 IBM qubits"}
  - {arxiv: "1907.08570", title: "A Multiorbital Quantum Impurity Solver for General Interactions and Hybridizations", authors: "E. Eidelstein, E. Gull, G. Cohen", year: 2019, note: "Figs. 1-3; Inchworm versus CT-HYB on matched models"}
  - {arxiv: "2601.04832", title: "Affordable Five-Orbital Dynamical Mean-Field Theory for Layered Iridates and Rhodates", authors: "L. Gaspard, C. Martins", year: 2026, note: "Table 4; full DMFT and hybrid DMFT on two real materials"}
  - {arxiv: "1907.11298", title: "Alleviating the Sign Problem in Quantum Monte Carlo Simulations of Spin-Orbit-Coupled Multi-Orbital Hubbard Models", authors: "A. J. Kim, P. Werner, R. Valentí", year: 2020, note: "basis optimisation changes the measured CT-HYB sign"}
  - {arxiv: "1504.07979", title: "Electronic structure and core-level spectra of light actinide dioxides in the dynamical mean-field theory", authors: "J. Kolorenč, A. B. Shick, A. I. Lichtenstein", year: 2015, note: "classically solved UO2/NpO2/PuO2 benchmark; valence and 4f-core XPS"}
  - {url: "https://github.com/TRIQS/benchmarks/tree/e51cbe48ac0e7106c5b9e0b1b80e17af58e4548f/Sr2RuO4", title: "TRIQS impurity-solver benchmark: Sr2RuO4", authors: "TRIQS benchmark contributors", note: "Pinned public model.py, Wannier hopping file and CT-HYB HDF5 output; a material-derived solver test, not an industrial quantum-advantage result"}
  - {arxiv: "1609.00735", title: "Complexity of quantum impurity problems", authors: "S. Bravyi, D. Gosset", year: 2017, note: "Theorem 1 bounds classical ground-energy cost for a fixed interacting impurity and quadratic bath; it does not cover the thermal Green's-function benchmark"}
---

## Why it matters

DMFT has material users. A direct Ce-substituted Nd₂Fe₁₄B study used Hubbard-I for localised Nd 4f states and approximated mixed-valent Ce through LSDA and an experimentally informed sublattice model [5]. The need for a more dynamical Ce treatment is a research question; the paper did not show that CT-QMC fails for its alloy. A cathode spectroscopy study combined DFT+DMFT with a separate charge-transfer multiplet calculation [6]. **That cathode study solved its DMFT impurity with classical CT-QMC**, then used Quanty for the core-level XPS. A discretised impurity with five d orbitals and four bath orbitals per spin orbital would have 50 system qubits; eight bath orbitals would give 90. These counts do not establish bath convergence or quantum advantage for the cited materials.

Hard impurity regimes exist, but difficulty depends on the Hamiltonian, basis, temperature and observable. Off-diagonal hybridisation and spin–orbit coupling can worsen CT-HYB's sign; [8–10] show why one solver's failure does not determine the classical frontier. There is also an output mismatch in the commonly quoted comparison: Inchworm [8] computes a **finite-temperature imaginary-time** Green's function, whereas the original hundred-logical-qubit quantum proposal [1] treats a **zero-temperature ground-state** response. The Arnoldi algorithm [2] describes a thermal extension, but its numerical resource study uses zero-temperature small impurity models with an exact input ground state. No matched quantum cost curve exists for the finite-temperature Kanamori example or a named industrial impurity.

## What is known

| Instance and observable | Measured or reported classical result | Limit of the evidence |
|---|---|---|
| Two-orbital Kanamori impurity with continuous Bethe bath; imaginary-time Green's function at βt = 64 [8] | CT-HYB cost of comparable quality extrapolated to ~3 × 10⁹ core-hours; classical Inchworm ran for ~1.5 × 10³ core-hours and gave controlled results | The huge CT-HYB cost is an extrapolation; this is a model impurity, not an industrial material or a quantum benchmark |
| Ba₂IrO₄ five-orbital DMFT [9] | Full classical DMFT converged with CT-QMC average sign 0.37; hybrid DMFT obtained sign 0.53 and a 43.8-fold total-time speedup | Hybrid DMFT treats part of the orbital manifold at mean-field level; the result concerns an oxide research problem |
| Ba₂RhO₄ five-orbital DMFT [9] | Full-DMFT sign 0.58; hybrid-DMFT sign 0.60 and 41.2-fold total-time speedup | Neither method establishes an industrial buyer or a quantum crossover |
| UO₂, NpO₂ and PuO₂ valence and 4f-core XPS [11] | LDA+DMFT with classical Lanczos on 14 impurity plus 14 bath spin orbitals reproduced the reported spectra | This is a finite-bath success case; M-edge XAS is a different observable, and a harder fuel instance is not identified |
| Sr₂RuO₄ impurity-solver benchmark [12] | Public three-orbital model code, Wannier hopping file and CT-HYB HDF5 output for a material-derived hybridisation | Six impurity spin orbitals; no quantum bath fit, bath-size convergence, measured quantum cost or industrial target |

The first row is unusually clear evidence that **one classical algorithm** has a bottleneck, followed by evidence that another classical algorithm overcame it for the same Green's function. Inchworm avoids this example's exponential temperature scaling but still has exponential dependence on the number of interacting orbitals [8]. In the oxide examples, the full five-orbital calculation itself completed, and the cheaper approximation reproduced the reported low-energy self-energies within Monte Carlo noise [9]. The classical frontier also includes basis optimisation for CT-HYB [10], tensor-train diagram summation [4] and neural-network embedding solvers [3]. These methods must be considered before calling a sign-problem instance classically intractable.

### A reproducible model to start from

The continuous-bath Kanamori case in [8, Eqs. 5 and the paragraph below it, Figs. 2–3] is more specific than a generic “DMFT sign problem.” It defines two *spinful* interacting orbitals (four impurity spin orbitals). In units where `t=1`, the reported parameters are `U=2`, `J=0.2`, off-diagonal hybridisation ratio `r=1`, and a semicircular bath with half-bandwidth `D=2`. The measured quantity is the diagonal, same-spin imaginary-time Green's function `G(iσ,iσ; τ)`, with the low-temperature endpoint at `β=64`. The paper specifies its analytic bath function and describes 80 imaginary-time intervals, maximum Inchworm diagram order 8 and five independent runs for its error bars [8]. Its prose says the local Hamiltonian includes spin exchange and pair hopping, while printed Eq. 5 displays an exchange-like term without an explicit pair-transfer operator. This ambiguity does not affect the bath-only fit below, but an interacting-Green's-function replication should publish the exact local Hamiltonian it uses.

| Reproducibility item | Current evidence and next action |
|---|---|
| Classical reference | The published Inchworm result used about 1,500 core-hours. The comparable CT-HYB cost of about 3 billion core-hours is an **extrapolation**, not a completed run. Reproduce the Green's-function error at fixed cost before fitting any new scaling curve [8]. |
| Quantum input | The classical bath is continuous. A finite quantum register needs a discrete fit to that same hybridisation function; publish bath energies, couplings and convergence of `G(τ)` as the number of bath orbitals grows. Four impurity spin orbitals alone do not make this a 50–100-qubit instance. |
| Quantum output | Match `β=64`, the imaginary-time grid and the diagonal Green's function, with a stated absolute error. Include thermal-state preparation, repetitions and bath-fit error. The existing zero-temperature quantum proposals do not provide this comparison [1, 2]. |
| Application link | This is a generic Bethe-bath model. To support a magnet, cathode or fuel claim, repeat the comparison for a material-derived hybridisation function and show that the improved solver changes a decision-relevant prediction. |

The analytic model is a useful algorithm benchmark. It is not yet evidence for a practical quantum advantage: the best reported classical solver solved it, and no matched finite-temperature quantum cost has been published [8].

**Finite-bath input check.** For the continuous semicircular case at `r=1`, each spin's two-by-two orbital hybridisation matrix has rank one. A symmetric positive-weight discretisation with `N` bath energy levels per spin therefore uses `4 + 2N` system qubits. We fitted the first 80 fermionic Matsubara values of the analytic hybridisation with paired poles and independently checked the imaginary-time bath kernel on 81 points against high-order quadrature. These are **our calculations of the bath input**, not results reported by [8]. Only `βt=64` is the paper's low-temperature endpoint; the other temperatures below are an exploratory input-fit sweep. The [script and JSON outputs](https://github.com/yuchenguommm/practical-quantum-advantage/tree/main/numerics) make the fit reproducible.

| Inverse temperature `βt` | First tested fit below `10⁻³` maximum Matsubara input error | System qubits | Achieved maximum Matsubara error | Achieved maximum imaginary-time bath error |
|---|---:|---:|---:|---:|
| 16 | 6 bath levels per spin | 16 | `3.85 × 10⁻⁵` | `1.64 × 10⁻⁵` |
| 32 | 6 | 16 | `9.08 × 10⁻⁴` | `1.76 × 10⁻⁴` |
| 64 | 8 | 20 | `3.22 × 10⁻⁴` | `3.02 × 10⁻⁵` |
| 128 | 10 | 24 | `1.42 × 10⁻⁴` | `7.73 × 10⁻⁶` |
| 256 | 10 | 24 | `8.13 × 10⁻⁴` | `4.65 × 10⁻⁵` |

The node counts are the first **tested even-node fits** reaching the chosen input threshold, not proven minima. An unfitted eight-node Gauss-Chebyshev discretisation has a much larger maximum Matsubara error (`0.783` at `βt=64`), so the fitting rule matters. Neither input check bounds the error of the **interacting** Green's function, proves bath convergence inside a DMFT loop, nor estimates quantum runtime. It does show that this particular two-orbital model can be represented accurately at the *bath-input level* well below 50–100 system qubits; increasing its bath to fill a larger register is not itself an advantage argument.

![Finite-bath input errors for the semicircular DMFT benchmark. This figure does not show interacting Green's-function or quantum runtime errors.](../figs/dmft_bath_input_fit.png)

**Interacting Green's-function check on the continuous bath.** We also evaluated the *interacting* thermal `G_00(tau)` for four fitted finite baths. These calculations use the quartic terms in printed Eq. 5 and an impurity one-body level of `-1t`. That level was inferred from the paper's **different discrete-bath** panel; it is not an input parameter documented for the continuous-bath panel. The reference below is read at five points from the green Inchworm curves in the paper's original vector Fig. 2 [8]. The curves are drawn with a line half-width of about `0.026` in `G` units, so differences below that scale cannot be resolved from the published plot. This graphical width is not an uncertainty estimate for the authors' computation.

| Inverse temperature `βt` | Bath levels per spin | System modes | Maximum bath-input error on first 80 Matsubara points | Mean / largest absolute difference at five plotted `G(tau)` points |
|---|---:|---:|---:|---:|
| 16 | 2 | 8 | `0.240` | `0.0077 / 0.0132` |
| 16 | 4 | 12 | `0.00552` | `0.0069 / 0.0105` |
| 32 | 4 | 12 | `0.0251` | `0.0031 / 0.0074` |
| 64 | 4 | 12 | `0.0842` | `0.0074 / 0.0093` |

The small plot differences are useful for checking the implementation, but **they do not establish interacting-bath convergence**. At `βt=64`, this four-level bath misses the stated `1e-3` *input* threshold by two orders of magnitude. The five plotted values also cannot resolve the difference between the two- and four-level `βt=16` results. Adding an illustrative pair-hopping term changes the sampled finite-bath `G` by as much as `0.022` at `βt=16` and `0.042` at `βt=64`; the missing Hamiltonian convention matters at the same scale as the graphical comparison. The [source-figure readout, ED outputs and comparison script](https://github.com/yuchenguommm/practical-quantum-advantage/tree/main/numerics) provide every plotted coordinate, bath coupling and calculated `G` value. A higher-resolution classical reference with explicit local parameters is needed before fitting a meaningful bath-size scaling curve. No quantum cost is inferred here.

**Interacting Green's-function cross-check on the paper's discrete bath.** Figure 2 of [8] also shows ED curves for a *different*, discrete bath with levels `±2.3t` and orbital-mixing ratio `r=0.5`. This is a 12-spin-orbital model under the printed two-levels-per-spin-orbital construction. We independently diagonalised its particle-number blocks and computed the finite-temperature Lehmann Green's function. The implementation reproduces its noninteracting one-particle limit to `2.5 × 10⁻¹⁴` and satisfies the fermionic endpoint sum rule. We read the published ED curve endpoints from the vector figure, so the values in the first column below are **approximate plot readouts**, not the authors' underlying data.

| `βt` | Published Fig. 2 `G(β)` [8] | Reconstruction with printed Eq. 5 and impurity level 0 | Same reconstruction with impurity level `−1` |
|---|---:|---:|---:|
| 8 | `−0.306` | `−0.148` | `−0.304` |
| 16 | `−0.305` | `−0.111` | `−0.298` |
| 32 | `−0.312` | `−0.104` | `−0.300` |
| 64 | `−0.322` | `−0.104` | `−0.305` |

Across those endpoints, the mean absolute discrepancy falls from about `0.195` to `0.010` after the illustrative level shift. Adding a pair-hopping term of strength `J` to the printed Hamiltonian changes our sampled `G(τ)` by at most about `0.0013`, so that term alone does not explain the larger mismatch. **The level shift is an inference from the plotted data, not a documented paper parameter.** Bath normalization or another omitted convention may also matter. The [ED code, numerical outputs and vector-figure readout](https://github.com/yuchenguommm/practical-quantum-advantage/tree/main/numerics) permit independent checking; this comparison does not establish which Hamiltonian the authors ran and does not yet test convergence of the continuous-bath interacting Green's function.

For the inferred level-`−1` version *without* added pair hopping, our ED has a twofold ground manifold and a gap of `0.0254t` to the next doublet. At `βt=64`, its Boltzmann factor relative to the ground manifold is about `0.20`. A ground-state-only Green's function therefore cannot simply stand in for this finite-temperature benchmark. This gap belongs to our reconstructed discrete model, not a reported measurement in [8].

![Independent discrete-bath ED curves at two assumed impurity levels, compared with approximate endpoints read from the paper's Fig. 2.](../figs/dmft_discrete_ed_audit.png)

For a **material-derived input**, the pinned TRIQS Sr₂RuO₄ benchmark [12] is a stronger reproducibility starting point than a generic material name. Its `model.py` sets `β=25`, `U=2.3`, `J=0.4` and three correlated orbitals with two spins; it builds the matrix hybridisation from the supplied Wannier hopping file. Its published `cthyb.h5` contains Matsubara and imaginary-time Green's functions, the supplied bath data and solver settings. This archive provides a concrete classical input path, but its output needs the audit below before use as a reference curve. It does **not** itself give a converged finite quantum bath, a full self-consistent DMFT loop for a target application, or evidence that CT-HYB is prohibitively expensive. A separate `Sr2RuO4_SOC` folder defines a spin-orbit-coupled model but does not contain a results archive at the pinned revision [12]. Keep these two folders and their outputs distinct.

**Pinned archive audit.** We inspected the public `cthyb.h5` file at commit `e51cbe4` (SHA-256 `2fe7dbc3…f443d`). The [audit script and complete numerical result](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/sr2ruo4_archive_audit.py) are reproducible without TRIQS:

| Archived item | Measured value | Interpretation |
|---|---:|---|
| Inverse temperature and local modes | `β=25`; six impurity spin orbitals | Material-derived, finite-temperature three-orbital input |
| CT-HYB run record | `10,000,000` cycles; `2536.1 s`; `280` MPI processes | One completed classical run; no cost–error curve or full DMFT loop |
| Current repository script | `1,000,000` cycles | Differs from both archive metadata and its embedded original script, which say ten million |
| Largest off-diagonal bath element, relative to largest diagonal element | `7.0 × 10⁻¹³` | This particular non-SOC hybridisation is numerically diagonal; it does not test an off-diagonal-hybridisation sign bottleneck |
| Archived diagonal `G(τ)` entries with `|G|>1` | Four points across both spins; largest `−2.8904` for down-spin orbital 1 (zero-based index) at `τ=24.0975` | Isolated values violate the bound for a normalized canonical-fermion Green's function; inspect the estimator or serialization before using the full curve as ground truth |

The archive does not record an average sign. A numerically diagonal bath does not by itself prove a good Monte Carlo sign for a Kanamori interaction, but neither this input nor its runtime documents a severe sign problem. The anomalous `G(τ)` points are in the archived output itself; we did not infer their cause. A same-instance bath fit should use the pinned `Δ(τ)` input, then seek a cleaned or independently replicated `G(τ)` with uncertainty bars. The archived run is a useful baseline to audit, not yet a certified accuracy target for a quantum solver.

**Finite bath on the same archived input.** We fitted nonnegative-weight discrete bath poles to the archived diagonal `Δ(τ)` for the two distinct orbital curves. The two spins have identical bath inputs, and orbitals 1 and 2 differ by less than `4 × 10⁻¹⁰` in the archive. Fitting used 352 selected imaginary-time points; the other 9649 points were held out. We also reconstructed `Δ(iω)` independently from the archived `G₀(iω)`, the pinned Wannier onsite matrix and the model's chemical potential. The first 80 Matsubara values agree with the numerical Fourier transform of archived `Δ(τ)` within `6.82 × 10⁻⁶` maximum absolute difference. The [fit script, bath energies, couplings and all errors](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/sr2ruo4_finite_bath_fit.py) are public.

| Bath levels per spin per correlated orbital | System fermion modes, including six impurity modes | Worst maximum held-out `Δ(τ)` error across orbitals | Worst maximum `Δ(iω)` error on first 80 frequencies versus archived `G₀` |
|---:|---:|---:|---:|
| 1 | 12 | `2.64 × 10⁻³` | `5.12 × 10⁻⁴` |
| 2 | 18 | `7.50 × 10⁻⁵` | `7.31 × 10⁻⁶` |
| 3 | 24 | `7.50 × 10⁻⁵` | `3.51 × 10⁻⁶` |

The two-level row is the first **tested** fit below `10⁻³` maximum held-out imaginary-time input error, within this restricted negative-energy, positive-weight bath ansatz. It is not a proof of the minimum bath size. The archived `Δ(τ)` itself has small positive endpoint ringing of `7.63 × 10⁻⁵`, which a positive-weight bath cannot reproduce and which explains the held-out error plateau. Under a direct fermion-to-qubit encoding, 18 system modes would use 18 system qubits before ancillary and fault-tolerance overhead. This material-derived input is therefore smaller than the illustrative 50–100-qubit register often cited for DMFT. Bath-input agreement alone does **not** bound the interacting `G(τ)` error, prepare the thermal state, or show a quantum speedup. The archived interacting curve still needs an independent quality check before fitting a solver cost–accuracy crossover.

There is also a complexity limit on a tempting shortcut: for an impurity with a fixed number of interacting modes and an arbitrary number of noninteracting bath modes, a classical algorithm approximates the **ground energy** in polynomial time in bath size at fixed additive precision [13, Theorem 1]. Its bound can have enormous constants and says nothing directly about the finite-temperature Green's function used above. Increasing only the bath register therefore cannot, by itself, establish a Shor-like exponential separation for the ground-energy task; the response calculation needs its own evidence.

- Hardware demonstrations are at 2-site and 14-qubit scale [7]; they show the loop closes, not that it wins.
- The cathode example [6] already has a successful classical CT-QMC calculation. Its core-hole physics is handled in a distinct multiplet step, so a quantum solver for the first-stage impurity cannot claim the full XPS computation as its benchmark.
- Embedding error (U, double counting, single-site approximation) is usually larger than solver error; the quantum computer removes only the latter. This bounds the value of a perfect solver from above.

## What would settle it

See the front matter. One practical entry point is to reproduce the public Sr₂RuO₄ CT-HYB archive [12], fit finite baths to its published hybridisation and report Green's-function error versus bath orbitals. Separately, reproduce the continuous-bath Inchworm result [8] and the full versus hybrid-DMFT results [9]; they are **different instances**. Test CT-HYB with an optimised basis [10], tensor-train and MPS alternatives, recording errors as well as the average sign. A quantum comparison must match temperature and output definition before comparing cost. For the finite-temperature Inchworm instance, thermal-state preparation is part of the quantum task; a zero-temperature spectral calculation alone cannot beat its classical result.

## Who could take it

A DMFT group with CT-HYB (TRIQS or w2dynamics) and an interest in quantum solvers, or a quantum-algorithms group willing to run the classical benchmarks honestly. The result sets the verdict of `dmft-impurity-solver` and of the three application pages that depend on it.
