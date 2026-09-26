---
type: problem
id: number-field-s-units-class-groups
title: S-unit groups and ideal class groups of number fields
title_zh: 数域的 S-unit 群与理想类群
summary: Given a number field and prime ideals, a quantum algorithm computes its S-unit group in compact representation in polynomial time. The class-group corollary assumes GRH. A classical result gives probabilistic subexponential class- and unit-group algorithms under ERH; practical advantage needs a matched task.
summary_zh: 给定数域和素理想集合，量子算法可以用多项式时间输出 S-unit 群的紧凑表示。推到理想类群时需要 GRH。经典算法已在 ERH 假设下取得概率性次指数复杂度；讨论实际优势前，还须统一输入和输出表示。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: empirical, note: "best known general classical class- and unit-group algorithms are probabilistic subexponential under ERH; no superpolynomial classical lower bound is known"}
  quantum_easiness: {level: conditional, note: "S-units for a supplied S have a polynomial-time quantum algorithm with compact output; class-group computation in the cited corollary assumes GRH"}
  willingness_to_pay: {level: unknown, note: "computational number theory has an independent research use, but no documented buyer requirement or priced task is cited"}
related:
  problems: [integer-factoring-hidden-subgroup]
  questions: [number-field-class-group-benchmark]
references:
  - {arxiv: "2510.02280", title: "An efficient quantum algorithm for computing S-units and its applications", authors: "J.-F. Biasse, F. Song", year: 2025, note: "Theorem 1 and Corollary 1, v2"}
  - {arxiv: "2512.01588", title: "Rigorous methods for computational number theory", authors: "K. de Boer, A. Pellet-Mary, B. Wesolowski", year: 2025, note: "v2, 2026; classical probabilistic subexponential result under ERH"}
  - {url: "https://eprint.iacr.org/2025/1825", title: "Quantumly Computing S-unit Groups in Quantified Polynomial Time and Space", authors: "K. de Boer, J. Felderhoff", year: 2025, note: "Revised 2026; quantified quantum analysis under GRH"}
---

## The task

The S-unit group consists of field elements whose associated principal ideal factors only over a supplied finite set S of prime ideals. For S empty it is the ordinary unit group. The ideal class group records fractional ideals modulo principal ideals. Computing these structures supports class-number tables and the study of conjectures about how class groups vary across field families [1]. A larger table can test a conjecture or reveal a pattern; it is not by itself a proof of that conjecture.

An instance must specify the field and its representation, its ring of integers, and S if relevant. The quantum theorem outputs generators in **compact representation**, a compressed product of field elements [1, Theorem 1]. Requiring fully expanded coordinates is a different output task and can erase a polynomial-time statement when the expansion itself is large.

## Best classical

Classical algorithms for arbitrary number fields historically depended on heuristic smoothness arguments. A 2026 revision of a recent result gives a probabilistic subexponential algorithm for class groups and unit groups of arbitrary number fields **under ERH**, removing those earlier smoothness heuristics [2]. ERH remains an assumption. This is the relevant asymptotic classical comparison for those two outputs, not the integer-factoring record or a restricted field family. No superpolynomial classical lower bound for these tasks is known.

## Best quantum

For a supplied S, Theorem 1 of [1] computes the S-unit group in compact representation in time polynomial in the field degree, log absolute discriminant, size of S, and largest log norm of a prime ideal in S. The theorem is stated without GRH. Its reduction uses a continuous hidden-subgroup problem; it should not be summarized merely as an application of the finite abelian hidden-subgroup theorem.

The ideal class-group algorithm in Corollary 1 of [1] **assumes GRH**. The reduction needs a small, effectively available set of prime ideals that generates the class group. The same corollary separately lists the Principal Ideal Problem without GRH; these claims should not be conflated. A later independent quantum analysis quantifies polynomial gate and memory complexity under GRH [3]. The 2025 revision of [1] also corrects a misleading coefficient-size dependence in its earlier theorem statement and supplies a bit-complexity argument. This exchange warrants checking the exact algorithm and assumptions, not dismissing the problem or treating all versions as interchangeable [1, 3].

## Verdict

Surviving as a foundational computational problem. The unconditional given-S theorem has a meaningful algebraic output; the class-group consequence has an explicit GRH condition. The best current general classical comparison is subexponential under ERH. These facts suggest an asymptotic algorithmic opportunity, while a superpolynomial classical lower bound, a matched public benchmark family, and an end-to-end crossover are absent. The [benchmark question](../questions/number-field-class-group-benchmark.html) specifies the next useful test. No logical-qubit estimate from RSA factoring is transferred here.
