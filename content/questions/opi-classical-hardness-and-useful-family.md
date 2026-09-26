---
type: question
id: opi-classical-hardness-and-useful-family
title: Can balanced OPI retain its DQI gap on a mathematically useful, classically tested instance family?
title_zh: 平衡 OPI 能否在有数学价值的实例族上保留 DQI 优势？
summary: At the balanced prime-field parameters where DQI reaches about 0.7179 satisfaction and the original Prange baseline reaches 0.55, seek either a stronger classical algorithm or a meaningful hardness result, and identify a public OPI family tied to a coding-theoretic question. Compare input access, quality and runtime on the same instances.
summary_zh: 在 DQI 约达 0.7179、原经典 Prange 基线约达 0.55 的平衡有限域参数下，寻找更强的经典算法或有意义的困难性结论，并找到与编码理论问题相关的公开实例族。双方须在相同输入、解质量和成本定义下比较。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Fix a public sequence of prime-field OPI instances with explicit evaluation points and allowed sets, coefficient-to-field ratio near 0.1 and density near 1/2, and explain what the resulting polynomial reveals about a separate coding-theoretic question. Publish the polynomial and achieved fraction for each run. Compare Prange, algebraic list-recovery ideas, tuned block-Gibbs MCMC and other competitive classical solvers against DQI at the same fraction and input-access cost, using held-out sizes. The published block-Gibbs experiments use coefficient-to-field ratio near 0.5 and cannot serve as this matched low-rate comparison. Either produce a classical polynomial-time algorithm meeting the DQI guarantee, prove a credible restricted-model lower bound or reduction under an explicit assumption, or report a robust matched scaling gap without presenting it as an unconditional separation."
  difficulty: phd
  resolved: false
related:
  problems: [optimal-polynomial-intersection, combinatorial-optimization]
  methods: [dqi]
references:
  - {arxiv: "2408.08292", title: "Optimization by Decoded Quantum Interferometry", authors: "S. P. Jordan et al.", year: 2025}
  - {arxiv: "2607.28120", title: "Approximate sampling from decoded quantum interferometry via Markov chain Monte Carlo methods", authors: "E. Gil-Fuster et al.", year: 2026}
---

## Why it matters

The DQI theorem establishes a polynomial-time quantum output-quality guarantee on OPI, while the published classical gap is relative to known algorithms [1]. OPI is related to Reed-Solomon list recovery, a basic coding-theoretic task, but the balanced large-list regime used for quantum advantage is not automatically useful in a cryptographic system or an industrial optimization model. A family tied to a concrete mathematical question would make the output valuable independently of the speedup claim.

## What would settle it

The front matter specifies the shared instance and output contract. A classical algorithm reaching the DQI satisfaction fraction in polynomial time would close the proposed asymptotic gap for this task. A restricted-model lower bound or explicit hardness assumption would strengthen the case without pretending to prove a general BPP-versus-BQP separation. The published block-Gibbs study [2] is a useful implementation baseline, but its coefficient-to-field ratio is near 0.5. The [public-data audit](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/opi_mcmc_archive_audit.md) makes that difference and its first-passage counts explicit. Rerun it, and any improved algebraic solver, near ratio 0.1 on the same held-out fields and target fraction. A quantum circuit's input-oracle construction and all repetitions belong in the time comparison.

A [seeded low-rate dataset](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/opi_low_rate_probe.md) now provides 180 explicit random instances and polynomial witnesses for two simple classical baselines. The next comparison can reuse its allowed-set hashes, but should include block Gibbs, stronger annealing or algebraic methods and held-out field sizes. Since the DQI expression is an expected score, report the actual finite-size output-score distributions rather than equating one classical threshold crossing to a quantum sample.
