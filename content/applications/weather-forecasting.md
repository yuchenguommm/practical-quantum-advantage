---
type: application
id: weather-forecasting
title: Numerical weather forecasting
title_zh: 数值天气预报
summary: Operational numerical weather prediction ingests classical observations, evolves a nonlinear atmosphere model and delivers a large forecast field. These requirements undermine proposed exponential speedups from state-output PDE solvers, but existing bounds do not rule out every quantum subroutine or a polynomial advantage on a narrower forecast product. No matched operational benchmark is documented here.
summary_zh: 业务化数值天气预报需要读入经典观测、演化非线性大气模型并交付大范围预报场。这些要求削弱了输出量子态的偏微分方程算法所声称的指数加速，但现有下界没有排除所有量子子程序，也没有排除某些较窄预报产品上的多项式优势。这里尚无同任务的业务基准比较。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: none, note: "operational forecasts already run on schedule on conventional supercomputers; the cost is scale, not an obstruction, and data-driven models have lowered it further"}
  quantum_easiness: {level: unknown, note: "Lewis et al. bound algorithms that output a normalised solution state for specified chaotic systems; Sakamoto–Fujii dequantize short-time local linear dynamics. Classical observation loading and full-field extraction add costs, but these results do not exclude every forecast observable or subroutine."}
  willingness_to_pay: {level: second-hand, note: "Weather services have operational requirements; the cited quantum-weather assessment does not state a service's acceptance or procurement target for a quantum solver."}
resources: {note: "no end-to-end resource estimate exists for an operational forecast; the obstruction is at the level of lower bounds, not gate counts"}
related:
  problems: [pde-solving, sparse-linear-systems, monte-carlo-expectation, sorting-fft-storage]
  methods: [hhl-qsvt, qram]
  applications: [turbulence-cfd]
references:
  - {arxiv: "2210.17460", title: "Quantum Computers for Weather and Climate Prediction: The Good, the Bad and the Noisy", authors: "F. Tennie, T. Palmer", year: 2022, note: "assessment from the weather-modelling side; names big-data input as the central obstacle"}
  - {arxiv: "2307.09593", title: "Limitations for Quantum Algorithms to Solve Turbulent and Chaotic Systems", authors: "D. Lewis, S. Eidenbenz, B. Nadiga, Y. Subaşı", year: 2024, note: "Quantum 8, 1509; exp(Ω(T)) for systems with a positive Lyapunov exponent"}
  - {arxiv: "2505.10445", title: "On the quantum computational complexity of classical linear dynamics with geometrically local interactions: Dequantization and universality", authors: "K. Sakamoto, K. Fujii", year: 2026, note: "Quantum 10, 2182; short-time geometrically local linear dynamics dequantized"}
  - {doi: "10.1038/nphys3272", title: "Read the fine print", authors: "S. Aaronson", year: 2015, note: "Nature Physics 11, 291; the input/output conditions on quantum linear-algebra speedups"}
  - {arxiv: "2011.04149", title: "Focus beyond quadratic speedups for error-corrected quantum advantage", authors: "R. Babbush, J. R. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven", year: 2021, note: "PRX Quantum 2, 010103; why the remaining polynomial speedups do not pay"}
---

## Who needs it

National and regional meteorological services produce forecasts used by insurers, energy companies, airlines and agriculture. A useful quantum contribution would have to improve forecast skill, resolution or delivery time within an operational workflow. The cited assessment by Tennie and Palmer discusses possibilities and the difficulty of handling large data sets [1]; it does not supply a service-defined acceptance target for a quantum algorithm.

## Bottleneck

An operational forecast combines observations with a previous model state, integrates a nonlinear atmosphere model and distributes fields and derived products. Each stage has a different input and output contract. Higher resolution and larger ensembles have value, but a quantum speedup for one mathematical kernel does not establish a faster end-to-end forecast. Tennie and Palmer identify the large classical data input as a major obstacle [1].

## Computational problems

- [PDE solving](../problems/pde-solving.html): the integration step. The catalogue assesses linear-system solvers, local linear dynamics and Carleman linearisation there; conclusions remain specific to each model and output.
- [Sparse linear systems](../problems/sparse-linear-systems.html): the implicit solves and the variational data-assimilation step.
- [Monte Carlo expectation](../problems/monte-carlo-expectation.html): ensemble statistics.
- [Sorting, FFT and storage](../problems/sorting-fft-storage.html): spectral transforms compute on forecast data; the observation database adds storage and data-movement costs.

## What current bounds actually constrain

Input. If an algorithm must read N independently supplied observations, acquiring them takes Ω(N) classical-data accesses. A formula-defined or already structured source has a different cost model. QRAM-based analyses must account for building and maintaining the memory; the input bound alone does not forbid an advantage in later processing [4].

Dynamics. For specified chaotic systems in natural coordinates, Lewis et al. prove an exponential-in-time lower bound on quantum algorithms that output a state approximating the normalised solution vector, assuming positive Lyapunov exponents and sub-exponentially growing solutions [2]. The output model and assumptions matter: this theorem does not by itself rule out a small set of forecast statistics, shorter horizons or other tasks. Sakamoto and Fujii dequantize short-time geometrically local **linear** dynamics in their model [3]; the nonlinear forecast workflow needs separate analysis.

Output. Delivering an N-component field requires Ω(N) output values, which removes a polylog(N) **end-to-end** runtime claim based solely on a state-preparation subroutine [4]. It does not eliminate every possible polynomial gain over a classical workflow that costs much more than N, and some downstream products request selected statistics rather than the whole field.

For an early error-corrected machine, Babbush et al.'s assumed gate speeds and surface-code overhead make quadratic advantages difficult to turn into a runtime win; quartic gains look more favourable in their examples [5]. This is an economic estimate under hardware and oracle assumptions, not a general lower bound for weather prediction. A useful forecast comparison must also include current numerical and data-driven classical methods at matched skill, resolution and latency.

## Verdict

Surviving as a broad application category, with **no supported operational quantum advantage** in the cited work. The strongest exclusions apply to particular state-output and short-time local-linear formulations. A full forecast also has substantial classical input and output costs. To move this entry toward promising, define a service-relevant product and tolerance, show the best classical cost at that tolerance, and give a quantum algorithm with complete data movement, repetitions and error-correction costs. Until such a matched benchmark exists, neither a general no-go theorem nor a practical speedup follows from the available papers.
