---
type: problem
id: optimal-polynomial-intersection
title: Optimal polynomial intersection over finite fields
title_zh: 有限域上的最优多项式相交问题
summary: Given a finite field, evaluation points and allowed value sets, find a low-degree polynomial that hits as many sets as possible. DQI achieves a worst-case satisfaction fraction beyond known polynomial-time classical algorithms, and later quantum work improves it at high rates. No classical superpolynomial lower bound, industrial encoding or practical crossover is known.
summary_zh: 给定有限域、取值点和各点允许的取值集合，寻找命中集合最多的低次多项式。DQI 在最坏情形下达到超过已知经典多项式算法的满足比例，较高码率还有后续量子改进。经典超多项式下界、工业问题的直接编码和实际交叉点均未确立。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: empirical, note: "at balanced prime-field parameters, no known classical polynomial-time algorithm reaches the DQI worst-case satisfaction fraction; the MCMC ~1.1^n observation is empirical and no unrestricted lower bound is proved"}
  quantum_easiness: {level: proven, note: "for explicit prime-field OPI inputs, DQI uses efficiently decodable Reed-Solomon dual codes and attains its semicircle-law fraction in polynomial time; later quantum algorithms improve high-rate guarantees under their stated oracle and decoding conditions"}
  willingness_to_pay: {level: none, note: "OPI is a coding-theoretic and algebraic computational problem; no public buyer requirement or natural industrial instance with this balanced parameter regime is documented"}
related:
  problems: [combinatorial-optimization]
  methods: [dqi]
  questions: [opi-classical-hardness-and-useful-family, dqi-industrial-encoding-crossover]
references:
  - {arxiv: "2408.08292", title: "Optimization by Decoded Quantum Interferometry", authors: "S. P. Jordan et al.", year: 2025, note: "v5; OPI and classical comparison"}
  - {arxiv: "2601.15171", title: "A nearly linear-time Decoded Quantum Interferometry algorithm for the Optimal Polynomial Intersection problem", authors: "A. Rosmanis", year: 2026}
  - {arxiv: "2607.28120", title: "Approximate sampling from decoded quantum interferometry via Markov chain Monte Carlo methods", authors: "E. Gil-Fuster et al.", year: 2026}
  - {arxiv: "2604.09533", title: "On Worst-Case Optimal Polynomial Intersection", authors: "Y. Sun, M. Wootters", year: 2026}
  - {arxiv: "2607.16541", title: "Efficient Exact Quantum Sampling from the Sun-Wootters Distribution for Optimal Polynomial Intersection", authors: "S. Jo", year: 2026}
---

## The task and why it matters

An instance supplies distinct points `a_i` in a finite field and an allowed set `S_i` for each point. Return a polynomial `Q` of degree below `n` that maximizes the fraction of indices with `Q(a_i) ∈ S_i`. This is a structured form of constraint satisfaction and is closely related to Reed-Solomon list recovery. It is an independent algebraic problem even without an industrial buyer. The quantum candidate concerns **balanced** allowed sets of size about half the prime field; older noisy-polynomial cryptographic proposals used a different, small-list and planted-solution regime, so their assumptions and attacks do not transfer automatically [1, Section 11.6–11.7].

The output is a concrete polynomial whose satisfaction fraction can be verified classically. A meaningful comparison fixes the same field sizes, degree/rate, allowed sets, target fraction and input-access model for both algorithms.

## Best classical

At degree-to-field ratio near `1/10` and allowed-set density near `1/2`, the original paper reports `0.55` satisfied for its polynomial-time Prange baseline versus approximately `0.7179` for DQI [1]. No known classical polynomial-time algorithm guarantees the latter fraction in the same parameter regime. This is a comparison with **known algorithms**, not a lower bound against all classical algorithms.

A newer block-Gibbs study reached DQI-like quality on tested OPI instances up to 156 **output-register equivalent** qubits, with observed search-step scaling around `1.096^n` [3]. Its parameter family has `n≈p/2` polynomial coefficients, allowed-set density about one half and a target fraction above 0.9. The `0.7179` versus `0.55` comparison above instead has `n≈p/10`. The MCMC result is therefore **not a classical run on the headline low-rate instances**. Its fitted exponential law is empirical, and its maximum over 100 random inputs is not a worst-case lower bound. Our [audit of the public trajectories](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/opi_mcmc_archive_audit.md) finds 5,237, 9,347 and 103,376 steps for the slowest of 100 inputs at 55, 70 and 75 output-equivalent qubits respectively; the archive does not include the paper's 156-qubit trajectories. A reproducible crossover needs classical solvers and DQI to meet the *same* satisfaction target at the same rate on a public held-out family.

An initial [low-rate classical probe](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/opi_low_rate_probe.md) fixes `n≈(p−1)/10` and publishes 180 seeded random OPI instances, scored witnesses and a 100,000-candidate cap for uniform search and Prange-seeded coordinate ascent. At 63 output-equivalent qubits, uniform search reached the formula-based DQI score target on all 20 tested instances; at 91, it reached 0/20 and the coordinate heuristic reached 2/20. The finite-size integer target varies across fields, the cap censors failures, and the DQI formula is an expected score rather than a per-sample quantum guarantee. This is a baseline sanity check; stronger classical solvers and a matched quantum implementation remain to be tested.

## Best quantum

DQI maps the objective to coherent decoding of a Reed-Solomon dual code and returns a polynomial meeting its semicircle-law satisfaction guarantee in polynomial time [1]. Rosmanis later gave a nearly linear-time version **given random access to the input** [2]. The random-access condition matters for an end-to-end input-loading comparison.

At higher rates, Sun and Wootters proved that solutions beating DQI's semicircle value exist for balanced prime-field OPI from limiting rate `0.6225`, with asymptotically perfect solutions from rate `0.7496` [4]. This was an existence result. A later algorithm efficiently samples a distribution realizing the improvement for specified Reed-Solomon parameters and coherent membership-oracle access [5]. These high-rate advances do not establish classical hardness and do not settle the balanced low-rate case used for the `0.7179` comparison.

## Verdict

Surviving as a foundational computational problem. OPI has a checkable algebraic output and a proved quantum algorithm with a striking gap over published polynomial-time classical baselines. It lacks an unrestricted classical lower bound or a standard cryptographic reduction for this parameter regime. Its links to coding theory give it mathematical interest, while no natural industrial instance or buyer requirement has been demonstrated. The [classical-hardness and useful-family question](../questions/opi-classical-hardness-and-useful-family.html) states what a stronger claim would need. The automotive ILP encoding belongs to a separate application test; its gadgetized constraints do not inherit OPI's Reed-Solomon structure.
