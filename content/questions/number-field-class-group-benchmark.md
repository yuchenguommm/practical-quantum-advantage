---
type: question
id: number-field-class-group-benchmark
title: Which number-field families yield useful class-group data with a matched classical and quantum advantage?
title_zh: 哪些数域族能在同一类群任务上产生有用的量子优势？
summary: Identify number-field families motivated by an explicit mathematical question. Compare current classical algorithms and quantum S-unit or class-group algorithms on the same input and compact output, stating ERH or GRH separately. Show that the resulting data answer a question unavailable at the same scale classically.
summary_zh: 找出有明确数学问题驱动的数域族，在相同输入和紧凑输出上比较经典与量子算法，并分别列明 ERH、GRH 假设。还须说明新增类群数据能回答什么问题，以及经典方法在哪个尺度遇到瓶颈。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Choose a public, independently motivated sequence of number fields. Specify defining polynomials, integral bases, discriminants, S, and compact output encoding. State which result needs ERH or GRH, and certify the class-group generators when possible. Benchmark the strongest classical subexponential method and its practical implementations on the same outputs; estimate the actual reversible quantum arithmetic and compare scaling on held-out fields. Explain which mathematical claim the new data would test and which precision or completeness it requires. Report a crossover only after matching all costs and outputs."
  difficulty: phd
  resolved: false
related:
  problems: [number-field-s-units-class-groups, integer-factoring-hidden-subgroup]
references:
  - {arxiv: "2510.02280", title: "An efficient quantum algorithm for computing S-units and its applications", authors: "J.-F. Biasse, F. Song", year: 2025}
  - {arxiv: "2512.01588", title: "Rigorous methods for computational number theory", authors: "K. de Boer, A. Pellet-Mary, B. Wesolowski", year: 2025}
---

## Why it matters

The S-unit theorem and the class-group corollary are mathematically substantial, but a polynomial-versus-subexponential comparison does not yet identify which fields would produce new knowledge [1, 2]. The output could extend class-number data or check a conjecture over a family. That value depends on the family and on whether the desired invariant is exactly what the quantum algorithm returns.

## What would settle it

The front matter gives the deliverables. The first milestone is an open dataset of fields with a concrete reason for studying their class groups, together with classical runtime, memory, and output certificates. The second is a quantum cost model for precisely the same compact output. Keep the given-S theorem, the GRH-dependent class-group reduction, and the ERH-dependent classical guarantee in separate columns. A scaling comparison without a useful field family remains an algorithm study; a useful family without a matched classical baseline remains a mathematical motivation.
