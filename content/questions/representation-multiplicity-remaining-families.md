---
type: question
id: representation-multiplicity-remaining-families
title: Which multiplicity families remain quantum-accessible after Panova's classical
  algorithms?
title_zh: Panova 的经典算法之后，还有哪些表示论重数族值得研究？
summary: Find a public family of partitions with a polynomial quantum dimension ratio outside Panova's proven classical subfamilies. Match exact or normalized-additive output on both sides, identify a mathematical use for that output, and test the strongest classical formulas without claiming a lower bound from the absence of one.
summary_zh: 找到量子算法的维数比为多项式、又不落入 Panova 已证明经典易解子族的公开划分族。在相同输出定义下比较经典与量子方法，并说明所得重数或近似值能回答什么数学问题。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Give an explicit indexed partition family, state the input encoding and prove the relevant quantum dimension ratio is polynomial. Check whether Panova Theorems 1.1–1.2 or another classical formula applies. Fix exact coefficient, positivity, relative error or normalized additive error as the common output; compare matched algorithms and show why that precision answers an independently stated mathematical question. A classical upper bound would close the proposed family; a hardness reduction for the matched approximation task would strengthen it. Generic #P-hardness of unrestricted exact coefficients is insufficient."
  difficulty: phd
  resolved: false
related:
  problems: [representation-theory-multiplicities]
references:
  - {arxiv: "2407.17649", title: "Quantum Algorithms for Representation-Theoretic Multiplicities", authors: "M. Larocca, V. Havlíček", year: 2024, note: "v5, polynomial dimension-ratio algorithms"}
  - {arxiv: "2502.20253", title: "Polynomial time classical versus quantum algorithms for representation theoretic multiplicities", authors: "G. Panova", year: 2025, note: "v2, Theorems 1.1–1.2 and open Questions 1–2"}
---

## Why it matters

Kronecker and plethysm coefficients encode concrete multiplicities in representation theory and appear in geometric complexity theory [1, 2]. Panova computed important quantum-accessible subfamilies classically in polynomial time, but explicitly left open a potential regime where all relevant dimensions are superpolynomial while their ratio is polynomial [2, Section 7.1]. Finding an explicit family there would turn a verbal loophole into a testable problem. A small normalized sampling probability may still be useless at additive inverse-polynomial precision, so output quality matters as much as runtime.

## What would settle it

The front matter lists the needed proof and benchmark. As an initial contribution, tabulate a proposed family of partitions, its Specht dimensions, the quantum ratio, Panova's applicable conditions, and the exact mathematical quantity sought. Then publish a classical implementation or bound on that same family. The site will not infer a quantum separation from a ratio alone or from the #P-hardness of unrestricted coefficients.
