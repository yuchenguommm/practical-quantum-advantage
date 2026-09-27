---
type: problem
id: pde-solving
title: Solving partial differential equations
title_zh: 偏微分方程求解
summary: The computational task behind weather, CFD, electromagnetics and other engineering applications. The strongest classical and quantum comparisons depend on the equation, input and requested output. A heat-in-a-region task permits at most a quadratic quantum gain in the studied setting, while a compiled radar instance is far beyond practical resources. Selected fluid observables remain under investigation; no general PDE verdict follows from the individual examples.
summary_zh: 天气、流体、电磁等工程应用背后的计算问题。经典与量子方法的比较取决于方程、输入和所需输出。已有热方程区域热量任务至多给出二次加速，编译过的雷达实例则远超实用资源。部分流体观测量仍在研究中，个别实例的结论不能推广到所有偏微分方程。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: unknown, note: "well-conditioned linear discretisations often have strong multigrid, Krylov or transform baselines; hardness and the relevant baseline depend on equation, dimension, geometry, accuracy and output; no classical hardness result is established here for the broad PDE category"}
  quantum_easiness: {level: conditional, note: "linear PDEs: QLSA or Hamiltonian simulation given efficient operator access, state preparation and restricted output; nonlinear Carleman algorithms require convergence conditions; the Lewis bound addresses normalised-state output for specified chaotic systems"}
  willingness_to_pay: {level: second-hand, note: "engineering demand is attached to application outputs and tolerances, not generic PDE solves; the derived applications (RCS, CFD, weather) are catalogued separately and lack a documented buyer threshold for a quantum solver"}
resources: {gates: "depth ~1e29 for the compiled 2D RCS instance (N=3.3e8)", note: "Scherer et al. 2017; Jennings et al. give model-dependent gate estimates for selected fluid observables, not a matched industrial benchmark"}
related:
  applications: [weather-forecasting, turbulence-cfd, radar-cross-section, derivative-pricing]
  problems: [sparse-linear-systems, monte-carlo-expectation]
  methods: [hhl-qsvt]
references:
  - {arxiv: "2307.09593", title: "Limitations for Quantum Algorithms to Solve Turbulent and Chaotic Systems", authors: "D. Lewis, S. Eidenbenz, B. Nadiga, Y. Subaşı", year: 2024, note: "Quantum 8, 1509"}
  - {arxiv: "2505.10445", title: "On the quantum computational complexity of classical linear dynamics with geometrically local interactions: Dequantization and universality", authors: "K. Sakamoto, K. Fujii", year: 2026, note: "Quantum 10, 2182"}
  - {arxiv: "2004.06516", title: "Quantum vs. classical algorithms for solving the heat equation", authors: "N. Linden, A. Montanaro, C. Shao", year: 2022, note: "Commun. Math. Phys. 395, 601; ten algorithms compared"}
  - {arxiv: "1512.05903", title: "Quantum algorithms and the finite element method", authors: "A. Montanaro, S. Pallister", year: 2016, note: "Phys. Rev. A 93, 032324"}
  - {arxiv: "1010.2745", title: "High-order quantum algorithm for solving linear differential equations", authors: "D. W. Berry", year: 2014, note: "J. Phys. A 47, 105301; the linear-ODE-to-linear-system route"}
  - {arxiv: "2011.03185", title: "Efficient quantum algorithm for dissipative nonlinear differential equations", authors: "J.-P. Liu, H. Ø. Kolden, H. K. Krovi, N. F. Loureiro, K. Trivisa, A. M. Childs", year: 2021, note: "PNAS 118, e2026805118; Carleman linearisation"}
  - {arxiv: "1505.06552", title: "Concrete resource analysis of the quantum linear system algorithm used to compute the electromagnetic scattering cross section of a 2D target", authors: "A. Scherer et al.", year: 2017, note: "Quantum Inf. Process. 16, 60"}
  - {arxiv: "2512.03758", title: "An end-to-end quantum algorithm for nonlinear fluid dynamics with bounded quantum advantage", authors: "D. Jennings, K. Korzekwa, M. Lostaglio, R. Ashworth, E. Marsili, S. Rolston", year: 2025}
  - {arxiv: "2607.12688", title: "Quantum PDE Solvers in Practice: Application-Driven Benchmarking of the Heat Equation", authors: "M. ElKarargy, A. Rahwan, A. Elsayed, F. Hatem", year: 2026}
  - {arxiv: "2011.04149", title: "Focus beyond quadratic speedups for error-corrected quantum advantage", authors: "R. Babbush, J. R. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven", year: 2021, note: "PRX Quantum 2, 010103"}
---

## Best classical

Finite-difference, finite-element and spectral discretisations feed multigrid, Krylov, transform and problem-specific solvers. For some well-conditioned linear discretisations, these give strong classical baselines; their costs depend on the equation, mesh, condition number, time horizon, accuracy and output. There is no single classical complexity for “PDE solving.” Sakamoto and Fujii establish quantum-complexity results for exponentially long geometrically local **linear** dynamics [2]. That result does not supply a hard industrial instance at a specified tolerance.

## Best quantum

Three routes illustrate how strongly the result depends on the PDE and requested output.

Linear PDEs via linear systems. Discretise, then apply a quantum linear-system solver (Berry's construction for linear ODEs [5], the finite-element analysis of Montanaro and Pallister [4]). The conditions are those of [sparse linear systems](sparse-linear-systems.html): efficient source-state preparation and operator access, controlled conditioning, and a restricted output. Under their assumptions Montanaro and Pallister find a polynomial speedup whose degree grows with spatial dimension, and give evidence against a super-polynomial gain at fixed dimension for smooth solutions [4]. For the heat equation, Linden, Montanaro and Shao compare ten algorithms for **heat in a specified region**. In their setting, the best quantum route in d ≥ 2 is at most quadratically faster, while the linear-system route never beats the best classical algorithm [3]. A compiled 2D radar cross-section instance has circuit depth of order 1e29 with oracles included [7]. A separate 2026 study compares eleven **quantum** heat-equation kernels on grids of 16–128 points and highlights reconstruction and readout costs; it does not establish a classical-versus-quantum runtime crossover [9].

Linear dynamics via Hamiltonian simulation. Some wave-type equations admit an evolution formulation with a compact receiver output. Sakamoto and Fujii dequantize short-time (polynomial-time) geometrically local classical linear dynamics in their model, excluding an exponential gain **there** [2]. An acoustic or seismic receiver calculation still needs an instance-specific comparison that counts construction of the medium model and readout.

Nonlinear PDEs via Carleman linearisation. Liu et al. embed a dissipative nonlinear ODE into a larger linear one, with convergence requiring weak nonlinearity relative to dissipation [6]. Lewis et al. tighten those bounds and derive an exponential-in-time limitation for algorithms outputting an approximate normalised solution state for specified chaotic dynamics in natural coordinates [1]. This constrains that state-output formulation; it does not prove an impossibility result for every coarse observable or nonlinear PDE task. Jennings et al. analyse selected turbulence observables under their own lattice-Boltzmann and resolution assumptions [8].

## What survives

Narrow tasks with efficiently prepared inputs and a scalar output remain candidates. One class is a well-conditioned linear boundary-value problem at stated accuracy [4]; another is a selected observable from a nonlinear fluid model [8]. Jennings et al. find that a modest gain may survive for some observables and tolerances under their lattice-Boltzmann assumptions [8]. This is a model-dependent estimate, not a demonstrated industrial crossover. Babbush et al. show why quadratic speedups are difficult to monetize on their early surface-code assumptions, while quartic speedups fare better [10]. That economic estimate is not a lower bound on PDE algorithms.

## Verdict

Surviving as a broad computational problem, without a demonstrated practical quantum advantage. Specific routes fare poorly: the compiled radar instance is uneconomic [7], and the heat-in-a-region comparison permits at most a quadratic gain in its studied setting [3]. State-output bounds for specified chaotic systems and dequantization of short-time local linear dynamics constrain other formulations [1, 2]. The lattice-Boltzmann analysis leaves selected fluid observables open under stated assumptions [8]. To support a stronger positive verdict, fix one application-relevant equation, input, observable and error target, then compare complete quantum and best classical costs on that same instance. The existing negative results do not justify assigning one negative verdict to every PDE application.
