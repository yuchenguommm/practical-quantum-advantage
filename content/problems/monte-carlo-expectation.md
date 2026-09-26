---
type: problem
id: monte-carlo-expectation
title: Monte Carlo expectation values and sampling
title_zh: 蒙特卡洛期望值与采样
summary: In the sampling-oracle model, classical bounded-variance mean estimation needs order 1/ε² samples while a coherent quantum sampler and its inverse permit near-1/ε queries. This is a proved query separation, not an end-to-end advantage for an explicit application. A compiled autocallable pricing route is separately assessed as uneconomic under its one-second comparator.
summary_zh: 在只提供抽样接口的模型中，有界方差均值估计的经典查询次数按 1/ε² 增长；若能相干实现采样电路及其逆电路，量子查询次数接近 1/ε。这是严格的查询复杂度差距，尚未证明具体应用的端到端优势。已编译的自赎回产品定价方案在其一秒对照假设下另行评为不经济。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: lower-bound, note: "Ω(1/ε²) classical samples for a black-box bounded Bernoulli mean at constant success; this does not lower-bound known-structure algorithms, quasi-Monte Carlo, variance reduction or parallel wall time"}
  quantum_easiness: {level: conditional, note: "Montanaro gives near-O(σ/ε) calls when the randomized subroutine and its inverse have efficient coherent circuits; full oracle and error-correction cost are not bounded by query count"}
  willingness_to_pay: {level: second-hand, note: "Goldman Sachs co-authored the pricing estimates; a one-second classical comparator is assumed, while a desk-defined purchase threshold is not documented"}
resources: {logical_qubits: "8,000 in one derivative-pricing benchmark; 4,700 in later QSP study", gates: "autocallable T-depth 5.4e7 (2021) or 4.5e7 (later QSP, different error settings)", note: "at an assumed one-second runtime, the respective T-layer rates are 54 and 45 MHz; 2021 text also says 10 MHz, contrary to its table"}
related:
  applications: [derivative-pricing, weather-forecasting, turbulence-cfd]
  problems: [combinatorial-optimization, pde-solving, sorting-fft-storage]
  methods: [grover-amplitude-estimation, qram]
  questions: [autocallable-same-instance-cost-crossover]
references:
  - {arxiv: "1504.06987", title: "Quantum speedup of Monte Carlo methods", authors: "A. Montanaro", year: 2015, note: "Proc. R. Soc. A 471, 20150301; near-quadratic speedup for bounded-variance expectations and partition functions"}
  - {arxiv: "2011.04149", title: "Focus beyond quadratic speedups for error-corrected quantum advantage", authors: "R. Babbush, J. R. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven", year: 2021, note: "PRX Quantum 2, 010103; break-even iteration counts and runtimes"}
  - {arxiv: "2012.03819", title: "A Threshold for Quantum Advantage in Derivative Pricing", authors: "S. Chakrabarti, R. Krishnakumar, G. Mazzola, N. Stamatopoulos, S. Woerner, W. J. Zeng", year: 2021, note: "Quantum 5, 463"}
  - {arxiv: "2307.14310", title: "Derivative Pricing using Quantum Signal Processing", authors: "N. Stamatopoulos, W. J. Zeng", year: 2024, note: "Quantum 8, 1322; 4.7k logical qubits, 2.4e9 total T gates, 4.5e7 T-depth"}
  - {arxiv: "2203.12497", title: "Quantum-enhanced Markov chain Monte Carlo", authors: "D. Layden, G. Mazzola, R. V. Mishmash, M. Motta, P. Wocjan, S. Sheldon", year: 2023, note: "Nature 619, 282; empirical polynomial gain in mixing on small spin glasses"}
  - {arxiv: "2403.03087", title: "Bounding speedup of quantum-enhanced Markov chain Monte Carlo", authors: "A. Orfi, D. Sels", year: 2024, note: "Phys. Rev. A 110, 052414; Markov-gap upper bound, no worst-case speedup for any unital proposal"}
  - {arxiv: "2510.19928", title: "Mind the gaps: The fraught road to quantum advantage", authors: "J. Eisert, J. Preskill", year: 2025, note: "assessment of the time horizon for quadratic speedups"}
---

## Best classical

Plain Monte Carlo reaches additive error ε in O(σ²/ε²) samples at constant success, and independent samples parallelise across cores and GPUs. In the **sampling-only black-box model**, this ε exponent is optimal: distinguishing two Bernoulli means separated by order ε needs Ω(1/ε²) independent outcomes [1, Introduction]. This is a lower bound on sample queries, not on wall time or on classical computation when the distribution has a usable formula. Quasi-Monte Carlo, control variates, importance sampling and multilevel methods can substantially improve the concrete task after using its structure. For Boltzmann sampling, parallel tempering, cluster updates and tensor-network samplers are relevant alternatives; that sampling task has a different input and output from estimating a mean.

## Best quantum

Montanaro's algorithm estimates the expected output of a bounded-variance subroutine to error ε using roughly σ/ε calls, up to logarithmic factors [1]. Its oracle model assumes a coherent implementation of the subroutine **and its inverse**. If the subroutine is a classical stochastic path generator, its randomness, model and payoff must be compiled into a reversible circuit; that construction has a cost not captured by query count. The calls are sequential in amplitude estimation. In the black-box model the query gap is proved; it does not certify a speedup for a named payoff, distribution or material property.

The break-even arithmetic of Babbush and colleagues [2] uses a distance-30 surface code with 1 μs cycles, yielding about 170 μs per logical Toffoli in their model. Their *illustrative quantum primitive* contains 100 Toffolis, so one quantum step takes 17 ms; they assign its classical counterpart 33 ns. With those assumptions a quadratic speedup crosses one classical core after 5.2×10⁵ quantum steps and 2.4 hours. A separately compiled simulated-annealing example needs 6.3×10⁷ steps and 320 days. Their Table 1 gives 100 days and 880 years respectively when the classical speedup factor is 10³. These are scenario calculations, not universal lower bounds for expectation estimation. More parallel classical capacity worsens this comparison, while faster quantum gates or a cheaper oracle can improve it.

For a basket autocallable, Chakrabarti and colleagues estimate 8,000 logical qubits and T-depth 54 million at a target error of 2×10⁻³ [3]. Dividing that depth by their assumed one-second runtime gives 54 MHz, although the same paper's discussion states 10 MHz. The later QSP calculation [4] gives 4,700 logical qubits, T-depth 45 million and T-count 2.4 billion for an autocallable with a different error specification. At a one-second comparator its required T-layer rate is 45 MHz. Neither paper supplies a bank's written procurement target or a measured best-classical runtime for exactly the compiled payoff at identical accuracy. Other finance or reliability tasks need their own oracle and baseline rather than inheriting these numbers.

For sampling rather than expectation, Layden et al.'s quantum-enhanced MCMC uses a quantum device to propose moves and reports an empirical polynomial gain in mixing on small spin-glass instances [5]. Orfi and Sels give an upper bound on the Markov gap for any unital quantum proposal and show there is no speedup over classical sampling on a worst-case unstructured problem [6]. Quantum walks give at most a quadratic gain in spectral gap (Szegedy). There is no provable super-quadratic quantum speedup for sampling from a classical distribution.

## Verdict

Surviving as a **foundational computational task**: the sampling-only query lower bound and quantum near-quadratic query improvement are rigorous [1]. The proved gap requires coherent access to the sampler and its inverse and says nothing by itself about physical runtime or known-structure classical algorithms. The [autocallable application](../applications/derivative-pricing.html) remains `uneconomic` under its published one-second comparator and current circuit constructions [3, 4]. A concrete application would need a fully specified instance, an efficiently reversible oracle, a measured classical bottleneck after variance reduction and parallelism, and an output whose accuracy has an explicit use.
