---
type: application
id: turbulence-cfd
title: Turbulent flow simulation (CFD)
title_zh: 湍流模拟（计算流体力学）
summary: Engineering CFD needs fields or specified observables at useful accuracy. A published Airbus-coauthored quantum lattice-Boltzmann analysis treats drag readout, but its numerical convergence tests use periodic flows without an obstacle and do not validate drag on a common industrial instance. Its favourable drag scaling survives in only one tested low-order 2D regime under the paper's numerical condition-number estimates.
summary_zh: 工程流体计算需要在有用精度下给出流场或指定观测量。Airbus 参与的量子格子玻尔兹曼研究分析了阻力读出，但数值收敛测试采用无障碍物的周期流，没有在同一工程实例上验证阻力误差。按论文数值估计的条件数标度，阻力计算只有一个低阶二维设定仍有较优渐近标度。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: empirical, note: "direct numerical simulation at Kolmogorov resolution scales as a power of Re and is out of reach at engineering Re; industry uses RANS/LES models instead, which are cheap and calibrated"}
  quantum_easiness: {level: unknown, note: "Lewis et al. bound normalised-state output for specified chaotic dynamics; Jennings et al. give a drag readout construction, but test Carleman convergence only on periodic flows without walls; no matched-observable error and cost curve exists for a named geometry"}
  willingness_to_pay: {level: first-hand, note: "Airbus Operations Ltd coauthored the 2026 PRX Quantum study, establishing direct industrial research interest; the paper does not state a buyer acceptance tolerance, latency or willingness to pay for a quantum drag solver"}
resources: {note: "Zhuang et al. claim 8.71e6 physical qubits and 42.6 days for a 2^80-grid Navier–Stokes instance at 5e-4 error rate; not independently checked, and its output model must be reconciled with the Lewis bound"}
related:
  problems: [pde-solving, sparse-linear-systems, monte-carlo-expectation]
  methods: [hhl-qsvt]
  applications: [weather-forecasting]
  questions: [cfd-drag-same-instance-crossover]
references:
  - {arxiv: "2307.09593", title: "Limitations for Quantum Algorithms to Solve Turbulent and Chaotic Systems", authors: "D. Lewis, S. Eidenbenz, B. Nadiga, Y. Subaşı", year: 2024, note: "Quantum 8, 1509; exp(Ω(T)) lower bound and tightened Carleman bounds"}
  - {arxiv: "2512.03758", doi: "10.1103/xysy-q3fp", title: "An end-to-end quantum algorithm for nonlinear fluid dynamics with bounded quantum advantage", authors: "D. Jennings, K. Korzekwa, M. Lostaglio, R. Ashworth, E. Marsili, S. Rolston", year: 2026, note: "PRX Quantum 7, 033060; published title omits initial 'An'; lattice-Boltzmann route and drag extraction"}
  - {arxiv: "2011.03185", title: "Efficient quantum algorithm for dissipative nonlinear differential equations", authors: "J.-P. Liu, H. Ø. Kolden, H. K. Krovi, N. F. Loureiro, K. Trivisa, A. M. Childs", year: 2021, note: "PNAS 118, e2026805118; Carleman linearisation, requires weak nonlinearity"}
  - {arxiv: "2509.08807", title: "A Pathway to Practical Quantum Advantage in Solving Navier-Stokes Equations", authors: "X.-N. Zhuang, Z.-Y. Chen, M.-Y. Tan, J. Zhang, C.-C. Ye, et al.", year: 2025, note: "claims 2^80 grid with 8.71 million physical qubits in 42.6 days; unverified"}
  - {arxiv: "2511.18802", title: "Toward end-to-end quantum simulation of rapidly distorted turbulence", authors: "Z. Meng, L. Chen, J.-P. Liu, G. He", year: 2025, note: "linear rapid-distortion turbulence via LCHS with statistics as output"}
  - {arxiv: "2505.10445", title: "On the quantum computational complexity of classical linear dynamics with geometrically local interactions: Dequantization and universality", authors: "K. Sakamoto, K. Fujii", year: 2026, note: "Quantum 10, 2182; applies to the linearised routes"}
  - {arxiv: "2011.04149", title: "Focus beyond quadratic speedups for error-corrected quantum advantage", authors: "R. Babbush, J. R. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven", year: 2021, note: "PRX Quantum 2, 010103"}
---

## Who needs it

Aircraft and turbine makers (drag, lift, stall margins), automotive (aerodynamics, cabin acoustics), energy (combustion, wind-farm wakes), process industries (mixing). CFD is among the largest consumers of engineering HPC time. What a designer buys is a resolved flow field or a derived quantity (drag coefficient, heat-transfer rate, pressure spectrum) at the operating Reynolds number.

## Bottleneck

Direct numerical simulation must resolve the Kolmogorov scale, so the grid grows as a power of the Reynolds number (Re^{9/4} in three dimensions under the standard Kolmogorov estimate, which Jennings et al. adopt as their resolution assumption [2]), and engineering Reynolds numbers are far beyond what DNS reaches. Industry therefore runs modelled equations (RANS, LES) whose fidelity is limited by the turbulence model, not by compute. The unmet demand is DNS-grade fidelity at engineering Re.

## Computational problems

- [PDE solving](../problems/pde-solving.html): nonlinear, chaotic, in 3D.
- [Sparse linear systems](../problems/sparse-linear-systems.html): the linearised solves inside every time step and inside Carleman-type embeddings.
- [Monte Carlo expectation](../problems/monte-carlo-expectation.html): statistics over realisations when the engineering task asks for them; drag is a separate scalar observable.

## Why the field is out of reach

For systems satisfying its positive-Lyapunov and growth assumptions, Lewis et al. prove an exponential-in-time lower bound on producing an approximate normalised solution state in natural coordinates [1]. This constrains algorithms with that output contract, including proposed linearisations when their assumptions apply. It does not cover every coarse CFD observable or every encoding. The paper also tightens worst-case bounds for the Carleman algorithm of Liu et al. [3], whose convergence requires a weakly nonlinear regime. Independently, distributing an N-value flow field requires Ω(N) output values; that output cost alone does not exclude a polynomial speedup over a more expensive classical computation.

## What survives: statistics

Lewis's bound constrains state output, leaving coarse observables as a separate task. Jennings et al. construct and cost an incompressible lattice-Boltzmann route with a boundary-drag readout [2]. Under their resolution and observable assumptions, the scaling improvement is bounded by O(Re^{3D/8}). In their two-dimensional numerical condition-number fits, drag readout removes the favourable exponent for every tested truncation order except NC=1, where the remaining factor is Re^{0.287} [2, Sec. VIII]. Their Carleman-error tests use periodic boundaries and no solid obstacle, so they do not establish drag accuracy on a cylinder. If NC=1 proves accurate enough, a classical solver for the same linearised approximation must join the baseline; the paper's asymptotic classical comparison counts updates of the full LBE [2, Sec. VIII]. The paper reports no public research data or software [2, Data Availability]. Babbush et al. estimate that small polynomial speedups are difficult to turn into runtime wins on early surface-code machines under their gate-speed assumptions [7].

Two other routes are on record. Meng et al. simulate rapidly distorted turbulence, a linear model, by linear combination of Hamiltonians with statistics as output [5]; being linear and local it is subject to the Sakamoto–Fujii dequantization at short times [6]. Zhuang et al. claim an end-to-end exponential speedup with 8.71 million physical qubits and 42.6 days for a 2^80-grid Navier–Stokes instance [4]; this has not been independently checked, and any such claim has to state what is output and how the Lewis bound is avoided.

## Verdict

Surviving as an application category, with no demonstrated quantum advantage. The cited state-output bound and the cost of reading a full field weaken proposals to deliver direct numerical simulation at engineering Reynolds number. The Airbus-coauthored work establishes industrial research interest, while its drag formula and its numerical error tests still need to meet on one geometry [2]. A [same-instance cylinder benchmark](../questions/cfd-drag-same-instance-crossover.html) specifies the next check. A buyer-defined accuracy and latency threshold is still missing.
