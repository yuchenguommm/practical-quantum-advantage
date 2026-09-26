---
type: question
id: jones-useful-hard-braids
title: Which mathematically useful braids remain classically hard at the Jones estimate's guaranteed precision?
title_zh: 哪类有数学价值的辫子在 Jones 估计的保证精度下仍然经典难算？
summary: Jones approximation is BQP-complete in a specified normalized additive-error formulation. A 2026 end-to-end hardware study projects a crossover near 2,800 crossings from constructed braids of at most 600 crossings, under a 1e-4 two-qubit error assumption and about 40% relative output error. Find a public family where that precision answers a concrete topological question and the best classical contraction, simplification and Monte Carlo methods fail on the same instances.
summary_zh: Jones 多项式在特定归一化加性误差定义下的逼近是 BQP 完全的。2026 年的端到端实验把最多 600 个交叉的构造辫子外推到约 2,800 个交叉的交叉点，依赖万分之一双比特门错误率，输出相对误差约 40%。需要寻找公开的辫子族，使该精度能回答具体拓扑问题，同时同实例经典收缩、化简与抽样方法都难以完成。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Name a knot/link or 3-manifold family with an independently motivated decision or numerical observable. Publish input braid words, their closures, strand counts and crossings; specify the root of unity, Jones normalization, additive and relative tolerances, and how the desired output changes a mathematical conclusion. Find simpler equivalent braid presentations and benchmark exact bracket/state-sum, MPO/tensor contraction, state-vector and randomized estimators on identical inputs. On the quantum side, compile the same braids, report circuit depth, shots, noise/mitigation bias and value uncertainty at the required precision. Fit classical scaling only within a stated family, include held-out larger instances, and report the crossover as conditional until measured."
  difficulty: phd
  resolved: false
related:
  problems: [topological-invariants]
  methods: [error-mitigation]
references:
  - {url: "https://arxiv.org/abs/quant-ph/0511096", title: "A Polynomial Quantum Algorithm for Approximating the Jones Polynomial", authors: "D. Aharonov, V. Jones, Z. Landau", year: 2006, note: "Polynomial algorithm for a specified normalized additive approximation"}
  - {url: "https://arxiv.org/abs/quant-ph/0605181", title: "The BQP-hardness of approximating the Jones Polynomial", authors: "D. Aharonov, I. Arad", year: 2006, note: "Hardness of the specified approximation, not every precision or braid family"}
  - {arxiv: "2503.05625", title: "End-to-End Quantum Algorithms for the Jones Polynomial", authors: "T. Laakkonen, E. Rinaldi, C. N. Self, E. Chertkov, M. DeCross, et al.", year: 2026, note: "Sec. IV and Figs. 10-11; constructed 10k-braid dataset to 600 crossings, extrapolated ~2,800-crossing crossover at ~40% relative error"}
---

## Why it matters

The BQP-completeness of normalized additive Jones approximation is one of the strongest algorithmic reasons to believe quantum computation can solve a fundamental mathematical task [1, 2]. Yet a theorem about *all* braids does not identify the braids knot theorists most need to understand. The output precision matters too: an additive estimate after an exponentially growing normalization may be compatible with many very different values of the unnormalized invariant. A useful demonstration should answer a specific question about a public family at the precision the quantum algorithm actually returns.

## Current evidence

The end-to-end study [3] ran small braid circuits and built an unusually careful classical MPO comparison. Its projected ~2,800-crossing crossing point uses a special constructed braid family with at most 600 crossings in the measured classical dataset, an assumed two-qubit error rate of `1e-4`, an assumed 30 ms depth-one circuit time, and a quantum output with about 40% relative error at the projected point. The paper itself notes that this extrapolation cannot certify advantage for a particular new braid. These figures should guide a follow-up benchmark, not stand in for one.

## What would settle it

The front matter states the deliverables. The first milestone is a small public collection for which a topology researcher can explain why the approximate value is informative. For each member, publish the braid word and equivalent simplified presentations, so a classical competitor can use all known diagram reductions. Then report both the normalized additive error required by the theorem and the error required by the mathematical question. Only compare runtimes where both algorithms meet the latter target. A held-out large-family test would give scaling evidence; an actual timed crossover at that target would establish an instance-level result.
