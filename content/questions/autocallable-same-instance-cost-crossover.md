---
type: question
id: autocallable-same-instance-cost-crossover
title: Can amplitude estimation price the same autocallable faster at equal error?
title_zh: 同一自赎回产品在相同误差下，振幅估计能否更快定价？
summary: Published quantum circuits give concrete resource estimates for a three-underlying, 20-step autocallable, but the two studies use different error targets and do not publish a measured best-classical runtime on the identical contract. The 2021 paper's 54-million T-depth and one-second assumption imply 54 MHz, conflicting with its prose figure of 10 MHz. A public same-instance, same-error cost curve would resolve the decision.
summary_zh: 已发表的量子电路对三种标的、20 个时间步的自赎回产品给出具体资源估算，但两项研究采用不同误差目标，也未公开完全相同产品的最强经典实测时间。2021 年论文的 5,400 万层 T 门和一秒假设意味着每秒 5,400 万层，与正文的 1,000 万不符。公开同实例、同误差的成本曲线才能判断交叉点。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Publish a machine-readable three-asset contract and model: initial prices, full volatility vector and correlation matrix, risk-free rate, 20 monitoring times, five call dates, call strikes and payments, knock-in barrier, put strike and notional, discounting convention and payoff code. State a common total price-error/confidence target. Measure wall time and monetary cost for optimized CPU/GPU Monte Carlo with variance reduction and relevant quasi-Monte Carlo alternatives. Compile both the 2021 re-parameterization and later QSP quantum pipelines for that identical payoff and error, reporting T-depth, T-count, logical qubits, distillation throughput, latency and total quantum cost. Resolve the 2021 paper's 10-versus-54-MHz discrepancy, then vary the classical time target and ask a desk for its actual acceptance requirement."
  difficulty: phd
  resolved: false
related:
  applications: [derivative-pricing]
  problems: [monte-carlo-expectation]
  methods: [grover-amplitude-estimation]
  questions: [first-hand-payment-evidence]
references:
  - {arxiv: "2012.03819", title: "A Threshold for Quantum Advantage in Derivative Pricing", authors: "S. Chakrabarti, R. Krishnakumar, G. Mazzola, N. Stamatopoulos, S. Woerner, W. J. Zeng", year: 2021, note: "Table 1: 8k qubits, 5.4e7 T-depth at error 2e-3; Discussion: one second and 10 MHz"}
  - {arxiv: "2307.14310", title: "Derivative Pricing using Quantum Signal Processing", authors: "N. Stamatopoulos, W. J. Zeng", year: 2024, note: "QSP: 4.7k qubits, 4.5e7 T-depth at amplitude error 1e-3, confidence 68%"}
  - {arxiv: "2011.04149", title: "Focus beyond quadratic speedups for error-corrected quantum advantage", authors: "R. Babbush, J. R. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven", year: 2021, note: "illustrative logical-Toffoli latency, not a compiled T-layer clock for the pricing circuits"}
---

## Why it matters

The application has a clear computational target: an expected discounted payoff for a path-dependent contract. Amplitude estimation can reduce the number of coherent oracle queries relative to independent Monte Carlo samples. Whether that saves a trading desk time or money depends on the cost of constructing the path distribution and payoff, the required accuracy, and the desk's existing classical infrastructure. The existing Goldman Sachs and IBM co-authored studies establish industry interest; they do not document a purchase threshold [1, 2].

## What is known

| Study | Contract and error | Quantum estimate | Missing comparison |
|---|---|---|---|
| Re-parameterization [1, Table 1] | Basket autocallable, 3 assets, 20 steps, target error 2×10⁻³ | 8,000 logical qubits; T-depth 5.4×10⁷; T-count 1.2×10¹⁰ | Measured best-classical runtime for that precise payoff and error |
| QSP payoff [2] | Autocallable, 3 assets, 20 steps, amplitude error 10⁻³ at 68% confidence | 4,700 logical qubits; T-depth 4.5×10⁷; T-count 2.4×10⁹ | Equal-error end-to-end comparison with [1] and classical code |

The first paper says some autocallables take five to ten seconds with at least 40,000 classical paths, then uses a **one-second target** in its quantum discussion [1, Appendix A.4 and Discussion]. It does not give the full measured classical cost–error curve for its compiled contract. Its T-depth divided by one second is 54 MHz; the discussion separately states 10 MHz. This is a source inconsistency, not a measured hardware speed. The QSP paper's 45 MHz follows from its own 45-million-layer depth and the same assumed one-second comparator [2].

### Contract availability audit

The 2021 circuit calculation specifies three assets, 20 steps, `Δt=1/20`, volatility bounds `0.1–0.4`, a Gaussian cutoff `w=5`, five call dates and a normalized error budget of about `2×10⁻³` [1, Section 4.2.3]. The paper describes the *form* of a call schedule and knock-in put [1, Section 5.1 and Appendix A.4]. The cited resource-estimate sections do not supply a complete numerical basket contract: the individual volatilities, pairwise correlations, risk-free rate, five dated strikes and cash payments, barrier, put strike and notional are not fixed together. Appendix A.4 gives a **different** illustrative single-asset, three-date contract. The later QSP paper reports resources for a three-asset, 20-step autocallable with a different amplitude-error target [2, Section 6]; it inherits the earlier contract description rather than publishing a machine-readable basket input. Consequently, one can reproduce the arithmetic `T-depth / 1 s`, but cannot claim a **same-contract** classical price or runtime from the papers alone. A newly chosen parameter set would be a new benchmark, not a replication of their exact pricing task.

## What would settle it

The front matter gives the reproducibility checklist. The first useful contribution is a versioned contract/model bundle; see [community task #19](https://github.com/yuchenguommm/practical-quantum-advantage/issues/19). Report both price error and business latency as curves, and keep statistical confidence, discretization bias and payoff-approximation error separate. An error-corrected schedule must state how T layers are produced and consumed; a generic Toffoli time from another architecture [3] cannot substitute for that schedule. The result could strengthen this candidate or show that classical parallelism and oracle construction absorb the query advantage.
