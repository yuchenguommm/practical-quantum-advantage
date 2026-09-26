---
type: problem
id: combinatorial-optimization
title: Combinatorial optimization (QUBO, CSP, integer programming)
title_zh: 组合优化（QUBO、约束满足、整数规划）
summary: Unstructured search has at most a quadratic Grover speedup, while QAOA lacks established scaling advantage. On algebraic optimal polynomial intersection instances, DQI beats known polynomial-time classical approximation algorithms, with no classical superpolynomial lower bound. Spin-glass obstructions apply to specified random sparse CSP families. Generic local-Hamiltonian ground energy is QMA-complete.
summary_zh: 无结构搜索最多有 Grover 的二次加速，QAOA 尚无确定的标度优势。在代数结构明确的最优多项式相交实例上，DQI 超过已知经典多项式逼近算法，但没有经典超多项式下界。自旋玻璃阻碍适用于特定随机稀疏约束族。一般局域哈密顿量基态能是 QMA 完全问题。
status: seed
last_verified: 2026-09-26
verdict: uneconomic
dimensions:
  classical_hardness: {level: empirical, note: "NP-hard in general, which is irrelevant to speedup; for DQI on OPI there is no known classical polynomial algorithm and no reduction; random CSPs are blocked for quantum too by the overlap-gap property"}
  quantum_easiness: {level: proven, note: "Grover and amplitude amplification give exactly quadratic speedup; DQI runs in polynomial time when the dual code is efficiently decodable; QAOA is heuristic with no scaling evidence"}
  willingness_to_pay: {level: second-hand, note: "optimization buyers are everywhere, but the only public industrial DQI case study (automotive option pricing ILP) claims no advantage over Gurobi; no company has written a target that classical solvers miss"}
resources: {logical_qubits: "~900", gates: "~1e15", note: "JPMorgan end-to-end estimate for a quartic planted-inference speedup (tensor problems); quadratic Grover speedups need 5e5–6e7 iterations to break even at Toffoli ≈ 170 μs"}
related:
  applications: [automotive-pricing-integer-programming, derivative-pricing]
  problems: [ground-state-energy, integer-factoring-hidden-subgroup, monte-carlo-expectation, optimal-polynomial-intersection]
  methods: [dqi, grover-amplitude-estimation, vqe]
  claims: [dwave-beyond-classical-2025, bluequbit-peaked-circuits-2025]
  questions: [first-hand-payment-evidence, dqi-industrial-encoding-crossover]
references:
  - {arxiv: "2011.04149", title: "Focus beyond quadratic speedups for error-corrected quantum advantage", authors: "R. Babbush, J. R. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven", year: 2021, note: "PRX Quantum 2, 010103"}
  - {arxiv: "2408.08292", title: "Optimization by decoded quantum interferometry", authors: "S. P. Jordan, N. Shutty, M. Wootters, A. Zalcman, A. Schmidhuber, R. King, S. V. Isakov, T. Khattar, R. Babbush", year: 2025, note: "Nature 646, 831"}
  - {arxiv: "2509.14509", title: "Spin glass transitions obstruct decoded quantum interferometry", authors: "E. R. Anschuetz, D. Gamarnik, S. Lu", year: 2025}
  - {arxiv: "2603.04540", title: "Tight inapproximability of max-LINSAT and implications for decoded quantum interferometry", authors: "M. J. Kramer, C. Schubert, J. Eisert", year: 2026}
  - {arxiv: "2509.08328", title: "Towards solving industrial integer linear programs with decoded quantum interferometry", authors: "F. Sabater et al.", year: 2026, note: "Quantum Sci. Technol. 11, 025054"}
  - {arxiv: "2403.03087", title: "Bounding speedup of quantum-enhanced Markov chain Monte Carlo", authors: "A. Orfi, D. Sels", year: 2024, note: "Phys. Rev. A 110, 052414"}
  - {arxiv: "2406.19378", title: "Quartic quantum speedups for planted inference", authors: "A. Schmidhuber, R. O'Donnell, R. Kothari, R. Babbush", year: 2024, note: "Phys. Rev. X 15, 021077"}
  - {arxiv: "2508.09422", title: "A classical quadratic speedup for planted kXOR", authors: "M. Gupta, W. He, R. O'Donnell, N. Singer", year: 2025}
  - {arxiv: "2510.07273", title: "End-to-end quantum algorithms for tensor problems", authors: "E. Fontana et al.", year: 2025}
  - {title: "The complexity of the local Hamiltonian problem", authors: "J. Kempe, A. Kitaev, O. Regev", year: 2006, doi: "10.1137/S0097539704445226", note: "SIAM J. Comput. 35, 1070; QMA-completeness of ground-state energy"}
---

## Best classical

Branch-and-bound mixed-integer solvers (Gurobi, CPLEX, SCIP), local search and simulated annealing, and for spin-glass-like instances tensor-network and parallel-tempering samplers. Two facts frame the comparison. First, NP-hardness is about worst cases and says nothing about speedup: quantum computers are not expected to solve NP-hard problems in polynomial time, and the ground-state energy of a local Hamiltonian, the physicist's version of QUBO, is QMA-complete [10], which is at least as hard. "Quantum computers find ground states" is a misconception. Second, the overlap-gap property that blocks classical local algorithms on random constraint satisfaction problems blocks stable quantum algorithms too: Anschuetz, Gamarnik and Lu show that spin-glass transitions obstruct DQI on random sparse max-k-XOR-SAT [3], and Orfi and Sels prove that quantum-enhanced Markov chain Monte Carlo with any unitary proposal has no worst-case spectral-gap speedup [6].

Hardware claims have a half-life of months: D-Wave's 2025 annealing observables and Kipu's and Q-CTRL's 2025–2026 optimization and simulation claims were each matched by tensor networks, simulated bifurcation or GPU heuristics within weeks (see the claim pages).

## Best quantum

- Unstructured: Grover and amplitude amplification give a quadratic speedup and BBBV proves that is optimal. Babbush et al. price it under surface-code overhead: with code distance 30 and a Toffoli every ~170 μs, break-even needs 5×10⁵ to 6×10⁷ iterations, that is 2.4 hours to 320 days of single-core classical time per instance, and parallel classical hardware pushes the crossover to years or worse [1]. Magic-state cultivation, qLDPC codes and algorithmic fault tolerance since 2024 buy roughly 10³ in total, moving "years" to "days"; the verdict does not flip.
- QAOA: heuristic, no instance family with evidence of scaling advantage, and its expectation values on the Sherrington–Kirkpatrick model are semiclassical.
- DQI: Jordan et al. map max-LINSAT to decoding the dual code and reach the "semicircle law" fraction of satisfied constraints; on [optimal polynomial intersection](../problems/optimal-polynomial-intersection.html), the reported quantum fraction is about 0.7179 versus 0.55 for their polynomial-time Prange baseline at degree-to-field ratio near 1/10 [2]. No lower bound excludes an improved classical algorithm. Kramer, Schubert and Eisert show that beating the random-assignment baseline r/q on general max-LINSAT is NP-hard, so any efficient method must exploit structure [4]. The published automotive option-package pricing ILP needs gadgets that inflate variables. Its actual encoding has code distance 3 independent of size; Gurobi optimally solves every tested matrix, and no quantum advantage is claimed [5]. The [industrial encoding benchmark](../questions/dqi-industrial-encoding-crossover.html) remains open.
- Planted inference: Schmidhuber et al. obtain a near-quartic speedup over the Kikuchi method for planted noisy kXOR [7], but Gupta, He, O'Donnell and Singer's classical quadratic improvement reduces it to quadratic at large k [8]. The JPMorgan end-to-end estimate for a related tensor problem is about 900 logical qubits and 10¹⁵ gates at depth 10¹², roughly four months of runtime against one exaflop-day classically [9].

## What survives

Instances whose objective is a max-LINSAT with an efficiently decodable dual code and a sufficiently large decoding radius. [OPI over prime fields](../problems/optimal-polynomial-intersection.html) is the clearest mathematical candidate. No documented industrial encoding preserves the required structure.

## Verdict

Uneconomic for the broad industrial optimization tasks currently assessed here. Unstructured search has only a quadratic query advantage, and specified random sparse families have DQI obstructions. The separate OPI page remains a foundational candidate with a quantum guarantee beyond known classical algorithms, but no classical hardness proof or buyer. An industrial objective retaining a decodable dual code after encoding, or a classical polynomial algorithm matching DQI on balanced OPI, would change the relevant verdict.
