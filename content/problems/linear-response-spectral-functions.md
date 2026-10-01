---
type: problem
id: linear-response-spectral-functions
title: Linear response and spectral functions (Green's functions, XAS, ARPES, INS)
title_zh: 线性响应与谱函数（格林函数、XAS、ARPES、INS）
summary: Spectra help interpret correlated materials, but an application-level quantum advantage requires a named impurity, output and measured classical bottleneck. A cited cathode XPS study used classical CT-QMC for the DMFT step and a separate multiplet code for the core-level spectrum. A 50–100-system-qubit count does not establish cost, and zero-temperature quantum response cannot be directly compared with finite-temperature classical Green's functions.
summary_zh: 谱学有助于解读关联材料，但量子优势需要具体杂质、输出量和可测量的经典瓶颈。所引正极 XPS 研究用经典 CT-QMC 完成 DMFT 步骤，再以独立的多重态程序计算核能级谱。50 到 100 个系统比特的计数不能确定成本；零温量子响应也不能直接与有限温经典格林函数比较。
status: seed
last_verified: 2026-10-01
verdict: surviving
dimensions:
  classical_hardness: {level: empirical, note: "CT-HYB has a sign problem on some multi-orbital models, but the cited cathode impurity was solved classically; a matched hard application instance has not been supplied"}
  quantum_easiness: {level: conditional, note: "zero-temperature response algorithms assume a prepared impurity ground state; finite-temperature response also needs thermal-state preparation and a matched observable. Bath discretisation and full-loop cost remain unmeasured for the named applications"}
  willingness_to_pay: {level: second-hand, note: "spectroscopy users (cathode XAS/XPS, rare-earth magnets, actinide fuels) exist and DMFT is changing interpretations, but no company has written an accuracy target and industry mostly uses DFT+U or multiplet fits"}
resources: {logical_qubits: "50–100 system qubits in illustrative impurity-plus-bath mappings", gates: "unknown for a named material and matched observable", note: "bath convergence, thermal or ground-state preparation, ancillas, response accuracy and the complete DMFT loop must be included"}
related:
  applications: [battery-cathode-spectroscopy, rare-earth-permanent-magnets, nuclear-fuel-actinide-spectra]
  problems: [quench-dynamics, ground-state-energy, excited-states]
  methods: [dmft-impurity-solver, embedding-divide-and-conquer, phase-estimation]
  questions: [dmft-impurity-cost-vs-ctqmc-sign-problem]
references:
  - {arxiv: "1510.03859", title: "Hybrid quantum-classical approach to correlated materials", authors: "B. Bauer, D. Wecker, A. J. Millis, M. B. Hastings, M. Troyer", year: 2016, note: "Phys. Rev. X 6, 031045; proposes the ~100 logical qubit impurity solver"}
  - {arxiv: "2510.02875", title: "Redox chemistry of LiCoO2, LiNiO2, and LiNi1/3Mn1/3Co1/3O2 cathodes: deduced via XPS, DFT+DMFT, and charge transfer multiplet simulations", authors: "Y. Xie, et al., F. M. F. de Groot, H. Zhang", year: 2025}
  - {arxiv: "2206.15093", title: "Ce and Dy substitutions in Nd$_{2}$Fe$_{14}$B: site-specific magnetic anisotropy from first-principles", authors: "J. Boust et al.", year: 2022, note: "Direct magnet alloy study: Nd 4f in Hubbard-I, mixed-valent Ce approximated"}
  - {arxiv: "2008.13295", title: "Fast inversion, preconditioned quantum linear system solvers, and fast evaluation of matrix functions", authors: "Y. Tong, D. An, N. Wiebe, L. Lin", year: 2020, note: "QSVT route to Green's functions"}
  - {arxiv: "2605.22920", title: "Estimating Green's functions with a robust quantum Arnoldi method", authors: "J. S. Nelson, A. D. Baczewski", year: 2026}
  - {arxiv: "2603.15741", title: "Neural-network quantum embedding solvers for correlated materials", authors: "A. Valenti, I. Park, A. Georges, A. J. Millis, O. Parcollet", year: 2026}
  - {arxiv: "2207.06135", title: "Learning Feynman Diagrams with Tensor Trains", authors: "Y. Núñez Fernández, M. Jeannin, P. T. Dumitrescu, T. Kloss, J. Kaye, O. Parcollet, X. Waintal", year: 2022, note: "tensor cross interpolation; sign-problem-free diagrammatic summation"}
  - {arxiv: "1504.07979", title: "Electronic structure and core-level spectra of light actinide dioxides in the dynamical mean-field theory", authors: "J. Kolorenč, A. B. Shick, A. I. Lichtenstein", year: 2015, note: "finite-bath exact diagonalisation of UO2/NpO2/PuO2, including XPS"}
  - {arxiv: "1908.03759", title: "Hardware-efficient quantum algorithm for the simulation of open-system dynamics and thermalisation", authors: "H.-Y. Su, Y. Li", year: 2019, note: "compresses a model environment by matching selected reservoir correlation functions; no general small-bath guarantee"}
---

## Best classical

The observables include single-particle and core-level spectra, magnetic response and optical conductivity. Different experiments require different models. In the cited cathode study, DFT+DMFT provided transition-metal configuration probabilities through a classical CT-QMC solver; Quanty then used those probabilities in a separate charge-transfer multiplet model to calculate XPS [2]. The study found that delithiation does not follow a rigid-band picture. It did not report CT-QMC failure or a quantum computation of the core-hole response. For UO₂, NpO₂ and PuO₂, a separate LDA+DMFT study used classical finite-bath Lanczos to reproduce valence and 4f-core XPS features [8]. Its impurity had 14 f and 14 bath spin orbitals. This is a benchmark of classical success on named actinide oxides, not a measured quantum opportunity.

The bottleneck inside some DMFT calculations is the impurity solver. Continuous-time hybridisation-expansion QMC (CT-HYB) can suffer a severe sign problem with off-diagonal hybridisation, spin–orbit coupling and low temperature; severity depends on the model and basis. Candidate hard regimes include multi-orbital d and f shells and low-temperature clusters. The direct Ce-substituted magnet study [3] treated localised Nd 4f states in the Hubbard-I limit and approximated mixed-valent Ce without a dynamical Ce impurity solve. It does not measure a CT-HYB failure on that alloy. Classical alternatives include tensor-train diagram summation [7] and neural-network embedding solvers [6]; their performance must be checked on the same hybridisation function and observable before declaring any industrial instance classically hard.

## Best quantum

Bauer, Wecker, Millis, Hastings and Troyer proposed in 2016 that the impurity problem be handed to a quantum computer of "about one hundred logical qubits", with the lattice self-consistency kept classical [1]. Their algorithm prepares a **zero-temperature ground state** and measures real-time response. Qubit arithmetic is simple: (orbitals × 2 spins) × (1 + bath sites per spin-orbital). A 5-orbital d shell with 4 bath sites per spin-orbital is 50 system qubits, with 8 it is 90; a 7-orbital f shell with 3–6 bath sites is 56–98. These are mapping examples, excluding ancillas, and do not establish bath convergence for a named material.

The Green's function can be approached through time evolution and interferometric measurements [1], or Krylov and Arnoldi constructions [5]. These methods differ in their input state and output. The Arnoldi paper describes a thermofield-double route to thermal Green's functions, but its reported numerical resource study used a zero-temperature single-impurity Anderson model with at most five bath sites and a ground state obtained by classical exact diagonalisation [5]. No result cited here compiles an end-to-end quantum cost for the finite-temperature, multi-orbital impurity used in the strong classical sign-problem benchmark. A comparison requires the same temperature, hybridisation, Green's-function definition and error tolerance on both sides.

Equilibrium linear response can often be expressed through correlation or Green's functions of a prepared equilibrium state. A pump-driven excited state or another nonequilibrium process needs a different initial-state and response specification; one equilibrium spectrum does not determine its full dynamics. Coupling to an environment adds a further modelling choice. A bath can sometimes be represented by a compact set of modes, ancillas or effective open-system evolution: Su and Li construct one such compression by matching reservoir correlation functions at a chosen expansion order [9]. That result does not guarantee a small register for a named material, long memory time or high-order response. The qubit budget must include the selected bath representation and the error in the target observable.

## What survives

Three possible settings are cathode XPS interpretation [2], rare-earth magnet electronic structure [3] and actinide spectra. The first cited cathode calculation succeeded with classical CT-QMC, so it is evidence of relevance, not of a hard impurity instance. The connection from any improved impurity spectrum to a purchase or changed material decision remains undocumented here. Embedding choices such as U and double counting also contribute uncertainty that a more accurate impurity solver alone cannot remove.

## Verdict

Surviving as a computational problem. Some discretised impurity models fit a 50–100-qubit system register, and some classical solvers have a sign problem. The current applications do not yet identify an instance with both a measured best-classical failure and a documented decision benefit. A matched impurity benchmark with converged bath, identical temperature and output, and full workflow cost would decide whether this candidate progresses.
