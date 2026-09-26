---
type: method
id: dmft-impurity-solver
title: Quantum impurity solver inside dynamical mean-field theory (DMFT)
title_zh: 动力学平均场（DMFT）中的量子杂质求解器
summary: "DMFT places a quantum impurity solver inside a classical self-consistency loop. Some hypothetical discretised d- and f-shell models occupy 50–100 system qubits, but no named application has both a converged bath and a same-observable classical-versus-quantum cost curve. The original roughly 100-logical-qubit proposal targets zero temperature, whereas the cited CT-HYB/Inchworm sign-problem benchmark measures a finite-temperature imaginary-time Green's function."
summary_zh: "DMFT 将杂质求解器放在经典自洽循环中。一些假设的 d、f 壳离散模型需要 50 到 100 个系统比特，但尚无具体应用同时给出收敛的浴和同一物理量下的经典与量子成本曲线。最初的约百逻辑比特方案针对零温；所引 CT-HYB/Inchworm 符号问题基准则计算有限温虚时格林函数。"
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: empirical, note: "CT-HYB sign problems occur for some multi-orbital models, but the cited cathode application was solved with classical CT-QMC; no matched application-level failure curve is supplied"}
  quantum_easiness: {level: conditional, note: "the original algorithm assumes impurity ground-state preparation and a discretised bath; finite-temperature response needs a different state preparation and cost analysis. No compiled cost exists for the named application instances"}
  willingness_to_pay: {level: second-hand, note: "inherits the spectroscopy users of the linear-response problem; rare-earth magnet and actinide groups run DMFT but have not stated targets; industry mostly avoids DMFT"}
resources: {logical_qubits: "50–100 system qubits in illustrative bath discretisations; additional ancillas and fault tolerance not counted", gates: "unknown for a named material at matched temperature and error", note: "five d orbitals with 4–8 bath orbitals per spin orbital give 50–90 system qubits by arithmetic; bath convergence, thermal state preparation and the full self-consistency loop remain unmeasured"}
related:
  problems: [linear-response-spectral-functions, quench-dynamics, ground-state-energy]
  methods: [embedding-divide-and-conquer, phase-estimation]
  applications: [rare-earth-permanent-magnets, battery-cathode-spectroscopy, nuclear-fuel-actinide-spectra]
  questions: [dmft-impurity-cost-vs-ctqmc-sign-problem, embedding-fragment-size-vs-correlation-length]
references:
  - {arxiv: "1510.03859", title: "Hybrid quantum-classical approach to correlated materials", authors: "B. Bauer, D. Wecker, A. J. Millis, M. B. Hastings, M. Troyer", year: 2016, note: "Phys. Rev. X 6, 031045"}
  - {arxiv: "2404.09527", title: "Dynamical Mean Field Theory for Real Materials on a Quantum Computer", authors: "J. Selisko, M. Amsler, C. Wever, Y. Kawashima, G. Samsonidze, et al., I. Tavernelli, T. Eckl", year: 2024, note: "Ca2CuO2Cl2 on IBM hardware, 14 qubits"}
  - {arxiv: "2605.22920", title: "Estimating Green's functions with a robust quantum Arnoldi method", authors: "J. S. Nelson, A. D. Baczewski", year: 2026}
  - {arxiv: "2207.06135", title: "Learning Feynman Diagrams with Tensor Trains", authors: "Y. Núñez Fernández, M. Jeannin, P. T. Dumitrescu, T. Kloss, J. Kaye, O. Parcollet, X. Waintal", year: 2022, note: "tensor cross interpolation, sign-problem-free"}
  - {arxiv: "2603.15741", title: "Neural-network quantum embedding solvers for correlated materials", authors: "A. Valenti, I. Park, A. Georges, A. J. Millis, O. Parcollet", year: 2026}
  - {arxiv: "2206.15093", title: "Ce and Dy substitutions in Nd$_{2}$Fe$_{14}$B: site-specific magnetic anisotropy from first-principles", authors: "J. Boust et al.", year: 2022, note: "Direct Ce-substituted alloy calculation; mixed-valent Ce approximated while Nd 4f uses Hubbard-I"}
  - {arxiv: "1907.08570", title: "A Multiorbital Quantum Impurity Solver for General Interactions and Hybridizations", authors: "E. Eidelstein, E. Gull, G. Cohen", year: 2019, note: "classical Inchworm handles low-temperature examples where CT-HYB fails"}
  - {arxiv: "2601.04832", title: "Affordable Five-Orbital Dynamical Mean-Field Theory for Layered Iridates and Rhodates", authors: "L. Gaspard, C. Martins", year: 2026, note: "hybrid versus full five-orbital DMFT on two oxides"}
  - {arxiv: "1504.07979", title: "Electronic structure and core-level spectra of light actinide dioxides in the dynamical mean-field theory", authors: "J. Kolorenč, A. B. Shick, A. I. Lichtenstein", year: 2015, note: "UO2/NpO2/PuO2 solved with classical finite-bath Lanczos; 14 impurity and 14 bath spin orbitals"}
  - {arxiv: "1609.00735", title: "Complexity of quantum impurity problems", authors: "S. Bravyi, D. Gosset", year: 2017, note: "Theorem 1: classical ground-energy algorithm for a quadratic bath plus interactions on m impurity Majorana modes; does not bound finite-temperature Green's-function cost"}
---

## How it works

DMFT replaces the lattice self-energy by a local one, obtained from an Anderson impurity model whose bath is fixed self-consistently from the lattice Green's function. The loop is: guess the hybridisation, solve the impurity for its Green's function, extract the self-energy, recompute the lattice Green's function, update the hybridisation, repeat. The impurity solve is a potential classical bottleneck; the surrounding loop uses classical linear algebra. Its difficulty depends on the impurity, temperature and requested accuracy. The roughly one-hundred-logical-qubit proposal of Bauer and colleagues prepared an impurity **ground state** and measured **zero-temperature real-time** Green's functions after discretising the bath [1]. Its own example projected roughly 10⁸ measurements of roughly 10⁸ gates each; these are historical generic-gate estimates, not compiled T counts for a named material. Selisko and colleagues closed a small loop for Ca₂CuO₂Cl₂ on 14 noisy physical qubits [2]. A more recent Arnoldi method discusses thermal Green's functions through a thermofield-double construction, but its numerical cost study used zero-temperature single-impurity Anderson models with at most five bath sites and supplied the ground state by exact diagonalisation [3].

## Preconditions

1. The embedding must be adequate. DMFT is exact only in infinite coordination; the quantum solver removes solver error, not the errors from the choice of U, double counting or the single-site approximation, which are typically larger.
2. The bath discretisation must fit the register and converge the requested observable. The small bath counts used in the examples are assumptions, not a uniform convergence guarantee. Real-frequency resolution may require larger baths; the required count must be measured for each model.
3. Match temperature and response definition. The classical Inchworm benchmark [7] computes a finite-temperature *imaginary-time* Green's function. To compare costs, the quantum workflow must return that same function at the same β and error, including thermal-state preparation, or both workflows must be re-benchmarked on the same zero-temperature observable.
4. The impurity state must be preparable at the required temperature and accuracy; for f shells with strong multiplet structure this is not automatic.
5. The target regime must be one where the best classical solvers actually fail at the requested accuracy. Multi-orbital spin–orbit models, dynamical f-shell treatments and low-temperature clusters are candidates. The cited cathode example was solved with CT-QMC. The Ce-substituted magnet calculation [6] approximated the mixed-valent Ce contribution while fitting magnetic measurements; that approximation is a research gap, not evidence that CT-QMC failed on this alloy.

## Known limits

- **Quantum cost remains instance-specific.** The 2016 zero-temperature proposal gave an illustrative ~10¹⁶ total generic gates across many independent shots [1]. Later methods can change this cost, but no T-gate number here is calibrated for a named impurity, temperature, target error, bath discretisation and complete DMFT loop.

- **Classical alternatives.** A finite-temperature two-orbital Kanamori impurity with a continuous Bethe bath had a CT-HYB cost extrapolated to roughly 3 × 10⁹ core-hours at βt = 64, yet classical Inchworm produced its imaginary-time Green's function in roughly 1.5 × 10³ core-hours [7]. The large CT-HYB figure is an extrapolation, and Inchworm still scales exponentially in impurity-orbital count. For Ba₂IrO₄ and Ba₂RhO₄, full five-orbital DMFT completed classically, while hybrid DMFT gave 43.8-fold and 41.2-fold total-time gains with reported low-energy agreement [8]. For UO₂, NpO₂ and PuO₂, a 14-orbital 5f impurity plus 14 bath orbitals was solved with classical finite-bath Lanczos; the calculation also reproduced 4f-core XPS features [9]. CT-HYB difficulty on a different model cannot be transferred to these applications.

- **Public benchmark quality.** The pinned Sr₂RuO₄ CT-HYB archive provides a material-derived six-mode impurity input and one completed classical run. Our [archive audit and finite-bath fit](../questions/dmft-impurity-cost-vs-ctqmc-sign-problem.html) find a nearly diagonal bath, no recorded average sign, a tenfold mismatch between the archived and current script's cycle settings, and four diagonal `G(τ)` values above the normalized fermionic bound. Two bath levels per spin per orbital fit its archived hybridisation to below `10⁻³` maximum held-out `Δ(τ)` error using 18 system modes. A further consistency check finds up-to-`0.0454` differences between symmetry-equivalent spin outputs in the first 80 Matsubara frequencies; the stored `G(iω)` agrees with a transform of the same noisy `G(τ)` and does not independently validate it. These are one-run diagnostics, not error bars. The archive is useful for constructing a same-input test; its interacting output needs independent checking before a quantum-versus-classical accuracy comparison.

- **A rigorous classical boundary for ground energy.** For a finite impurity model with `n` fermion modes, a quadratic bath and interactions confined to `m` Majorana modes, Theorem 1 of [10] gives a classical additive-error `γ` ground-energy algorithm with runtime `O(n³) exp[O(m log³(m/γ))]`. At fixed impurity size and fixed absolute error, this is polynomial in the number of bath modes. Its dependence on impurity size and precision can still be prohibitive in practice. The theorem concerns ground energy and a low-energy state; it does **not** provide a comparable bound for the finite-temperature imaginary-time Green's functions in [7], real-frequency resolution, or a full DMFT loop. Thus bath-register growth alone does not certify exponential quantum advantage for the *ground-energy* subtask.

## Verdict

Surviving. DMFT offers a useful way to isolate a quantum subproblem, and a small hardware demonstration shows a self-consistency loop can close [2]. The cited cathode impurity was solved classically; the strongest cited sign-problem instance was also solved by a different classical algorithm [7]. A credible crossover needs the same hybridisation function, temperature, Green's function, error tolerance and bath convergence for optimized classical and quantum workflows, including the full loop cost. No practical advantage follows from a system-register count alone.
