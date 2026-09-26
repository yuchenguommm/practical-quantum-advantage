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
  what_would_settle_it: "Fix a public sequence of prime-field OPI instances with explicit evaluation points and allowed sets, rate near 0.1 and density near 1/2, and explain what the resulting polynomial reveals about a separate coding-theoretic question. Publish the polynomial and achieved fraction for each run. Compare Prange, algebraic list-recovery ideas, tuned block-Gibbs MCMC and other competitive classical solvers against DQI at the same fraction and input-access cost, using held-out sizes. Either produce a classical polynomial-time algorithm meeting the DQI guarantee, prove a credible restricted-model lower bound or reduction under an explicit assumption, or report a robust matched scaling gap without presenting it as an unconditional separation."
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

The front matter specifies the shared instance and output contract. A classical algorithm reaching the DQI satisfaction fraction in polynomial time would close the proposed asymptotic gap for this task. A restricted-model lower bound or explicit hardness assumption would strengthen the case without pretending to prove a general BPP-versus-BQP separation. Numerical comparisons should use the newer block-Gibbs result [2] and any improved algebraic solver, and report the same target fraction on held-out fields. A quantum circuit's input-oracle construction and all repetitions belong in the time comparison.
