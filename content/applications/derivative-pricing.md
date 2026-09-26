---
type: application
id: derivative-pricing
title: Derivative pricing by quantum amplitude estimation
title_zh: 衍生品定价（量子振幅估计）
summary: Amplitude estimation gives a quadratic query improvement for Monte Carlo pricing, but two Goldman Sachs/IBM-backed circuit studies still require thousands of logical qubits and tens of millions of sequential T layers for benchmark autocallables. The one-second classical comparator is an assumption in those papers, not a published buyer acceptance threshold. The 2021 paper's quoted 10 MHz rate is inconsistent with its own 54-million-layer table under a one-second target; the later QSP study gives 45 million layers and 45 MHz for a different error budget.
summary_zh: 振幅估计使蒙特卡洛定价的查询次数获得二次改善，但高盛与 IBM 参与的两项电路研究对自赎回产品仍需数千逻辑比特和数千万层串行 T 门。两篇文章使用的经典一秒对照是研究假设，并非已公布的买方验收指标。2021 年论文表格的 5,400 万层若需一秒，应对应约 5,400 万层每秒，与正文所写 1,000 万不符；后续 QSP 研究在另一误差设定下给出 4,500 万层及 4,500 万层每秒。
status: seed
last_verified: 2026-09-26
verdict: uneconomic
dimensions:
  classical_hardness: {level: empirical, note: "path-dependent Monte Carlo work is substantial but parallel; the cited one-second classical comparator is an assumption, without a matched published runtime-and-error benchmark for the exact quantum contract"}
  quantum_easiness: {level: proven, note: "amplitude estimation gives 1/ε given a payoff oracle; the oracle (path generation plus payoff arithmetic) is the whole cost"}
  willingness_to_pay: {level: first-hand, note: "Goldman Sachs researchers co-authored the benchmark studies, documenting direct industry interest. Their one-second comparator is a modelling assumption, not a desk-defined acceptance, throughput or procurement threshold."}
resources: {logical_qubits: "8,000 in the 2021 autocallable estimate; 4,700 in a later QSP estimate with different error settings", gates: "2021 autocallable: 5.4e7 T-depth; later QSP: 4.5e7 T-depth and 2.4e9 T-count", note: "at an assumed one-second comparator these depths require about 54 MHz and 45 MHz respectively; the 2021 text separately quotes 10 MHz, inconsistent with its table"}
related:
  problems: [monte-carlo-expectation, pde-solving]
  methods: [grover-amplitude-estimation]
  questions: [autocallable-same-instance-cost-crossover, first-hand-payment-evidence]
references:
  - {arxiv: "2012.03819", title: "A Threshold for Quantum Advantage in Derivative Pricing", authors: "S. Chakrabarti, R. Krishnakumar, G. Mazzola, N. Stamatopoulos, S. Woerner, W. J. Zeng (Goldman Sachs, IBM)", year: 2021, note: "Table 1: autocallable at error 2e-3, 8k logical qubits, T-depth 54 million; text assumes ~1 s"}
  - {arxiv: "2307.14310", title: "Derivative Pricing using Quantum Signal Processing", authors: "N. Stamatopoulos, W. J. Zeng", year: 2024, note: "QSP autocallable at error 1e-3: 4.7k logical qubits, T-depth 45 million, T-count 2.4e9"}
  - {arxiv: "1905.02666", title: "Option Pricing using Quantum Computers", authors: "N. Stamatopoulos, D. J. Egger, Y. Sun, C. Zoufal, R. Iten, N. Shen, S. Woerner", year: 2020, note: "Quantum 4, 291; the amplitude-estimation pricing construction"}
  - {arxiv: "1504.06987", title: "Quantum speedup of Monte Carlo methods", authors: "A. Montanaro", year: 2015, note: "Proc. R. Soc. A 471, 20150301; the general near-quadratic bound"}
  - {arxiv: "2011.04149", title: "Focus beyond quadratic speedups for error-corrected quantum advantage", authors: "R. Babbush, J. R. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven", year: 2021, note: "PRX Quantum 2, 010103; logical Toffoli ~170 μs at code distance ~30"}
---

## Who needs it

Investment banks and market makers price path-dependent contracts such as autocallables and target accrual redemption forwards (TARFs). Goldman Sachs researchers co-authored the two estimates [1, 2], establishing direct industry interest. Neither paper reports a particular desk's acceptance tolerance, price for compute or procurement decision.

## Bottleneck

The price is an expectation of a payoff over simulated paths of the underlying. Plain classical Monte Carlo reaches standard error ε with O(1/ε²) paths, given finite variance, and the path evaluations parallelise. The 2021 paper says some autocallables take five to ten seconds with at least 40,000 paths in a classical implementation [1, Appendix A.4]; its one-second crossover target is a further assumption. Its three-asset resource row does not supply a complete numerical basket contract: the individual volatilities and correlations, dated strikes and payments, barrier and put parameters are not fixed together [1, Sections 4.2.3, 5.1]. The appendix's numerical payoff example is single-asset and three-date. The [input audit](../questions/autocallable-same-instance-cost-crossover.html) details the missing fields. Classical variance reduction, quasi-Monte Carlo and PDE solvers for suitable low-dimensional contracts must be checked for the same payoff, model and error.

## Computational problems

- [Monte Carlo expectation](../problems/monte-carlo-expectation.html): the core task, quantum amplitude estimation giving O(1/ε) [4].
- [PDE solving](../problems/pde-solving.html): the alternative for low-dimensional contracts, where quantum methods offer at most polynomial gains.

## Best quantum

Stamatopoulos and colleagues described the path-loading, payoff and amplitude-estimation construction [3]. The 2021 resource study [1, Table 1] gives a basket autocallable with three underlyings, 20 time steps and target error 2×10⁻³: 8,000 logical qubits, T-count 1.2×10¹⁰ and T-depth 5.4×10⁷. Its TARF row is a separate instance: 11,500 qubits and T-depth 8.2×10⁷. The authors posit about one second as a useful autocallable runtime and write that this requires a 10 MHz T-gate rate [1, Discussion]. Direct division of the reported autocallable depth by one second instead gives **54 MHz**. We retain both statements as an unresolved inconsistency in that paper, and use the table value when comparing a serial depth to a specified runtime.

The later QSP paper [2] studies an autocallable with three underlyings and 20 steps, but its target amplitude error is 10⁻³ at 68% confidence rather than the 2021 table's 2×10⁻³ target. It estimates 4,700 logical qubits, total T-depth 4.5×10⁷ and T-count 2.4×10⁹. With the assumed one-second classical comparator, this is 45 MHz. The paper's approximately 16-fold T-count and fourfold qubit improvements compare its QSP *oracle* with a specific arithmetic oracle in its own Table 1; they are not the percentage reduction from the 2021 end-to-end estimate at equal error. These are resource estimates for benchmark contracts, not observed quantum runtimes.

## Why it does not pay

Babbush and colleagues modelled a distance-30 surface code with a 1 μs cycle and estimated about 170 μs per *logical Toffoli* under stated factory and routing assumptions [5]. A Toffoli rate in that model cannot be directly equated to the T-layer rate required by [1, 2]; a common hardware architecture, distillation layout and schedule are needed. Nonetheless, 45–54 million serial T layers in a one-second budget are a demanding target. Parallel factories can trade additional qubits for throughput, while amplitude estimation retains a sequential sequence of oracle calls. A full cost comparison must also use the best measured classical runtime for the same contract and tolerance.

Credit risk, VaR and CVA also involve expectation estimation, but their oracle, model, accuracy target and classical baseline differ. The autocallable numbers cannot be transferred to them without a separate benchmark.

## Verdict

Uneconomic under the published one-second comparator and present resource constructions. The quadratic query gain is proven for the [underlying computational task](../problems/monte-carlo-expectation.html), whose broader verdict remains `surviving`; no buyer-defined tolerance or price is published, and the exact classical baseline for the compiled contracts is missing. The paper-internal 10-versus-54-MHz inconsistency prevents a precise single threshold. A verdict change needs a public contract and model, equal total pricing error, measured best-classical runtime and cost, a compiled quantum circuit for the same task, and an architecture-level schedule showing lower total cost or latency. The [same-instance benchmark question](../questions/autocallable-same-instance-cost-crossover.html) lists the needed inputs.
