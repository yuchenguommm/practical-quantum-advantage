---
type: method
id: dqi
title: Decoded quantum interferometry (DQI)
title_zh: 解码量子干涉（DQI）
summary: Maps max-LINSAT through a Fourier transform to decoding the dual code. On optimal polynomial intersection, DQI reaches a satisfaction fraction beyond known polynomial-time classical algorithms, but no classical superpolynomial lower bound is proved. The algorithm needs a decodable dual code; a published industrial ILP encoding does not retain the Reed–Solomon structure.
summary_zh: 经傅里叶变换把 max-LINSAT 转化为对偶码解码。对最优多项式相交问题，DQI 的满足比例超过已知经典多项式算法，但经典超多项式下界并未证明。算法需要可高效解码的对偶码；已发表的工业整数规划编码没有保留 Reed–Solomon 结构。
status: seed
last_verified: 2026-09-26
verdict: surviving
dimensions:
  classical_hardness: {level: empirical, note: "balanced OPI has no known polynomial-time classical algorithm matching the DQI fraction; MCMC ~1.1^n is an empirical fit on tested instances; no unrestricted lower bound or standard-assumption reduction is known"}
  quantum_easiness: {level: conditional, note: "polynomial time given an efficient decoder for the dual code B^T with decoding radius near m/2; nearly linear-time circuits exist for OPI"}
  willingness_to_pay: {level: none, note: "the published automotive pricing study has industry coauthors but no buyer-defined advantage target; its gadget encoding has distance 3 independent of size and does not beat Gurobi"}
related:
  problems: [combinatorial-optimization, optimal-polynomial-intersection]
  applications: [automotive-pricing-integer-programming, cryptanalysis]
  methods: [grover-amplitude-estimation]
  questions: [dqi-industrial-encoding-crossover]
references:
  - {arxiv: "2408.08292", title: "Optimization by Decoded Quantum Interferometry", authors: "S. P. Jordan, N. Shutty, M. Wootters, A. Zalcman, A. Schmidhuber, R. King, S. V. Isakov, R. Babbush", year: 2025, note: "Nature 646, 831"}
  - {arxiv: "2509.14509", title: "Spin Glass Transitions Obstruct Decoded Quantum Interferometry", authors: "E. R. Anschuetz, D. Gamarnik, B. Lu", year: 2025}
  - {arxiv: "2509.14443", title: "On the Complexity of Decoded Quantum Interferometry", authors: "K. Marwaha, B. Fefferman, A. Gheorghiu, V. Havlíček", year: 2025}
  - {arxiv: "2603.04540", title: "Tight inapproximability of max-LINSAT and implications for decoded quantum interferometry", authors: "M. J. Kramer, D. Schubert, J. Eisert", year: 2026}
  - {arxiv: "2604.09533", title: "On Worst-Case Optimal Polynomial Intersection", authors: "Y. Sun, M. Wootters", year: 2026}
  - {arxiv: "2601.15171", title: "A nearly linear-time Decoded Quantum Interferometry algorithm for the Optimal Polynomial Intersection problem", authors: "A. Rosmanis", year: 2026}
  - {arxiv: "2509.08328", title: "Towards solving industrial integer linear programs with Decoded Quantum Interferometry", authors: "F. Sabater et al.", year: 2026, note: "Quantum Sci. Technol. 11, 025054"}
  - {arxiv: "2607.28120", title: "Approximate sampling from decoded quantum interferometry via Markov chain Monte Carlo methods", authors: "E. Gil-Fuster et al.", year: 2026}
  - {arxiv: "2607.16541", title: "Efficient Exact Quantum Sampling from the Sun-Wootters Distribution for Optimal Polynomial Intersection", authors: "S. Jo", year: 2026}
---

## How it works

Max-LINSAT asks, for a matrix B ∈ F_p^{m×n} and subsets F_i ⊂ F_p, for an x maximising the number of rows i with (Bx)_i ∈ F_i. DQI prepares a superposition weighted by a polynomial in the objective, whose Fourier transform is a superposition over low-weight error patterns; decoding the dual code C^⊥ = ker B^T coherently uncomputes the error register and leaves a state concentrated on good x [1]. With a decoder of radius ℓ, the expected satisfied fraction follows the semicircle law ⟨s⟩/m = (√[(ℓ/m)(1 − r/p)] + √[(r/p)(1 − ℓ/m)])², where r = |F_i|. The flagship instance is optimal polynomial intersection (OPI): B is a Vandermonde matrix, the dual code is Reed–Solomon, Berlekamp–Massey decodes up to ℓ = ⌊(m − n)/2⌋, and at rate n/p ≈ 1/10 DQI reaches a fraction 0.7179 against 0.55 for the best classical algorithm the authors tried (Prange). Rosmanis gives a nearly linear-time circuit for OPI [6].

## Preconditions

1. **A decodable dual code.** B^T must generate a code with an efficient decoder; the advantage grows with the decoding radius, which must approach m/2 for a large gap.
2. **Instances that are not random-local.** The structure must come from algebra (Reed–Solomon, algebraic-geometry codes), not from a random sparse constraint graph.
3. **Classical hardness of the same instances.** For OPI this is the conjecture that Reed–Solomon list recovery with p/2 candidates per point is hard; there is no reduction to a standard assumption.

## Known limits

- **Unstructured instances are blocked.** Anschuetz, Gamarnik and Lu show that on random LDPC-type max-k-XOR-SAT the overlap-gap property obstructs DQI: the spin-glass transition prevents it from beating classical local algorithms asymptotically [2]. Kramer, Schubert and Eisert prove that beating the trivial r/q fraction on general max-LINSAT by a constant is NP-hard, so any advantage must come from structure [4].
- **Complexity status is intermediate.** Marwaha et al. show the DQI output distribution can be sampled in low levels of the polynomial hierarchy, so sampling-hardness arguments of the RCS type do not apply, while the task of finding high-value outputs resists relativizing dequantization [3].
- **The quantum guarantee has advanced at higher rates.** Sun and Wootters prove that for balanced prime-field OPI at limiting rate from 0.6225 solutions beating DQI's semicircle value exist, and from 0.7496 nearly perfect solutions exist [5]. A later quantum algorithm attains the improvement under specified coherent-oracle and list-decoding conditions [9]. This does not prove classical hardness. The original low-rate 0.7179 comparison remains a separate regime. Classical block-Gibbs MCMC reached DQI-like quality on tested OPI instances with an **empirical** runtime fit around 1.1ⁿ [8]; this is neither a polynomial-time algorithm nor a worst-case lower bound.
- **The published industrial encoding has not retained the favourable code structure.** The automotive option-package pricing study converts an ILP to max-XORSAT through gadgets. Repeating rows naively would give distance 2; the construction actually used has distance 3 independent of size [7, Sections 5.1 and 5.3]. The smallest relevant encoded example has 827 constraints and 345 variables. Gurobi solves every tested, smaller matrix optimally; the better BP2 decoder in the performance plots has no coherent circuit in the paper. See the [encoding crossover question](../questions/dqi-industrial-encoding-crossover.html). Code-based cryptography such as HQC and BIKE uses random codes without publicly available efficient decoders.

## Verdict

Surviving. DQI has a proved algorithmic guarantee on [OPI](../problems/optimal-polynomial-intersection.html), beyond the best cited polynomial-time classical baseline, and no known classical polynomial-time match in its balanced low-rate regime. There is no proof of superpolynomial classical hardness. The 2021 Chen–Liu–Zhandry quantum optimization result predates DQI [1, Section 1]. No documented industrial problem has retained the required dual-code structure after encoding. What would strengthen the case: a mathematically useful OPI family with a matched classical comparison, an explicit hardness assumption or restricted-model lower bound, or an industrial objective mapped without destructive gadgets.
