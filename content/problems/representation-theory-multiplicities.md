---
type: problem
id: representation-theory-multiplicities
title: Representation-theoretic multiplicities (Kronecker, plethysm, Littlewood–Richardson)
title_zh: 表示论重数（Kronecker 系数、plethysm、Littlewood–Richardson）
summary: Quantum algorithms compute certain multiplicities efficiently when representation-dimension ratios are polynomial. Panova proved classical polynomial-time exact algorithms for important Kronecker and plethysm subfamilies, refuting specific speedup conjectures. Her theorems do not cover every polynomial-ratio family; no surviving family with a proved classical separation or a demonstrated mathematical use has been identified.
summary_zh: 当表示维数之比为多项式时，量子算法可高效计算部分表示论重数。Panova 为重要的 Kronecker 和 plethysm 子族给出了经典多项式时间精确算法，推翻了具体加速猜想；其定理并未覆盖所有多项式维数比的输入族。尚未找到兼具明确经典困难证据和数学用途的剩余子族。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: unknown, note: "exact Kronecker and plethysm coefficients are #P-hard in general, but Panova gives classical polynomial algorithms on important quantum-accessible subfamilies; generic hardness does not transfer to the remaining polynomial-ratio families"}
  quantum_easiness: {level: conditional, note: "exact multiplicity algorithms are polynomial only when the relevant representation-dimension ratio is polynomial; inverse-polynomial additive estimation of a normalized Kronecker sampling probability is a separate BQP task"}
  willingness_to_pay: {level: none, note: "mathematical motivation is clear, but no buyer or concrete use for the particular normalized additive output is documented"}
related:
  problems: [topological-invariants, integer-factoring-hidden-subgroup]
  methods: [phase-estimation]
  questions: [representation-multiplicity-remaining-families]
references:
  - {arxiv: "2302.11454", title: "Quantum complexity of the Kronecker coefficients", authors: "S. Bravyi, A. Chowdhury, D. Gosset, V. Havlíček, G. Zhu", year: 2023, note: "PRX Quantum 5, 010329 (2024)"}
  - {arxiv: "2407.17649", title: "Quantum Algorithms for Representation-Theoretic Multiplicities", authors: "M. Larocca, V. Havlíček", year: 2024}
  - {arxiv: "2502.20253", title: "Polynomial time classical versus quantum algorithms for representation theoretic multiplicities", authors: "G. Panova", year: 2025, note: "v2, Theorems 1.1–1.2 and Section 7.1 delimit the classical subfamilies and remaining gap"}
  - {arxiv: "2602.08441", title: "Plethysm is in #BQP", authors: "M. Christandl, A. W. Harrow, G. Panova, P. M. Posta, M. Walter", year: 2026, note: "CCC 2026"}
---

## Best classical

The Kronecker coefficient `g(λ, μ, ν)` counts the multiplicity of one symmetric-group representation inside a tensor product of two others. Exact Kronecker and plethysm coefficients are #P-hard on general inputs [1–4]. This worst-case fact alone says nothing about a subfamily selected because a quantum algorithm runs quickly on it.

Panova's Theorem 1.1 computes the **exact** Kronecker coefficient in classical polynomial time when one of the three Specht-module dimensions satisfies `f^ν ≤ n^k` for a fixed `k`. Its stated bound is `O(D(k) n^(4k²+1) log n)`, with a large `k`-dependent constant [3]. Theorem 1.2 does the same for the special plethysm coefficient `a^λ_(d,m)` when `d` and the length of `λ` are fixed, or `f^λ ≤ n^k`. These results refute specified superpolynomial-speedup conjectures in [2]. They leave open inputs where all relevant dimensions grow superpolynomially yet their ratio is polynomial: [3, Section 7.1] explicitly says its Kronecker theorem does not cover that possibility. No well-parameterized surviving family is supplied there.

## Best quantum

There are **three different output tasks**. For exact multiplicities, the algorithms in [2] run in polynomial time only on inputs whose specified representation-dimension ratio is polynomial. For example, a Kronecker algorithm has cost depending on `f^μ f^ν / f^λ`; one small dimension is sufficient in a highlighted family, but it is not necessary for that ratio to be polynomial [2, 3]. For a normalized **additive estimate**, [1, Lemma 2] samples a distribution with probability `p(λ) = f^λ g(λ, μ, ν)/(f^μ f^ν)` and estimates a chosen probability to inverse-polynomial additive error. That estimate can be too coarse to recover an exact coefficient or decide positivity when the probability is small. Finally, putting exact multiplicities in #BQP or positivity in QMA is a complexity-class **upper bound**, not a polynomial-time algorithm that returns the exact integer on every input [1, 4].

Panova's classical theorems concern exact computation on restricted inputs. They do not, by themselves, prove a classical polynomial algorithm for the normalized additive task on **all** inputs. Conversely, a quantum additive estimate does not solve the #P-hard exact problem in general.

## What survives

One route is an explicit partition family with a polynomial quantum dimension ratio that falls outside Panova's classical theorems. Another is a normalized additive task with a demonstrated mathematical use at exactly the algorithm's precision. For the concrete small-dimension families, the classical polynomial algorithms are decisive despite potentially large exponents. For the remaining families, neither a classical lower bound nor a matching efficient classical algorithm is known here [2, 3]. Exact values, positivity and a useful formula remain distinct mathematical goals.

## Verdict

Surviving as a foundational question, with major subfamilies closed. The earlier `no-go` verdict treated Panova's restricted exact algorithms as covering every quantum-accessible family and conflated them with the separate normalized additive task. A strong case needs an explicit partition family for which the quantum dimension ratio stays polynomial, the desired output remains mathematically informative, and the strongest classical algorithms are demonstrably slower on that **same** family. No superpolynomial classical lower bound or such benchmark is known here. The [open question](../questions/representation-multiplicity-remaining-families.html) specifies what a contributor should test.
