---
type: problem
id: topological-invariants
title: Topological invariants (Jones polynomial, Turaev–Viro, Witten–Reshetikhin–Turaev)
title_zh: 拓扑不变量（Jones 多项式、Turaev–Viro、Witten–Reshetikhin–Turaev）
summary: Additive approximation of the Jones polynomial at roots of unity (plat closure) and of Turaev–Viro 3-manifold invariants is BQP-complete. A Quantinuum study demonstrated a small end-to-end braid pipeline; its ~2,800-crossing crossover is extrapolated from braids of at most 600 crossings, at about 40% relative error and an assumed 1e-4 two-qubit error rate. A mathematically useful hard braid family at the guaranteed output precision remains unidentified.
summary_zh: 单位根处 Jones 多项式（plat 闭包）与 Turaev–Viro 三维流形不变量的加性逼近是 BQP 完全的。Quantinuum 已演示小规模端到端辫子算法；约 2,800 个交叉的交叉点来自最多 600 个交叉的样本外推，并对应约 40% 相对误差及假设的万分之一双比特门错误率。尚未找到在算法保证精度下具有数学价值的经典难辫子族。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: reduction, note: "BQP-complete for plat-closure Jones at roots of unity and for Turaev–Viro invariants; DQC1-complete for trace closure; exact evaluation #P-hard"}
  quantum_easiness: {level: proven, note: "Aharonov–Jones–Landau polynomial-time algorithm for the specified additive approximation; small end-to-end circuits run on H2-2. The ~2,800-crossing crossover is an empirical extrapolation, not a demonstration."}
  willingness_to_pay: {level: none, note: "no buyer or precise mathematical use for the guaranteed normalized additive estimate has been identified; this does not imply every additive estimate is useless"}
resources: {logical_qubits: "about 100 in the paper's extrapolated noisy-device scenario", gates: "per-shot circuit depth grows with braid size; shots depend on precision", note: "~2,800-crossing estimated crossover assumes two-qubit error 1e-4, 30 ms depth-one layer and ~40% relative error; fitted from a special braid dataset up to 600 crossings, not a completed run"}
related:
  problems: [representation-theory-multiplicities, quench-dynamics]
  methods: [error-mitigation]
  claims: [google-random-circuit-sampling]
  questions: [jones-useful-hard-braids]
references:
  - {url: "https://arxiv.org/abs/quant-ph/0511096", title: "A Polynomial Quantum Algorithm for Approximating the Jones Polynomial", authors: "D. Aharonov, V. Jones, Z. Landau", year: 2006}
  - {url: "https://arxiv.org/abs/quant-ph/0605181", title: "The BQP-hardness of approximating the Jones Polynomial", authors: "D. Aharonov, I. Arad", year: 2006}
  - {arxiv: "0707.2831", title: "Estimating Jones polynomials is a complete problem for one clean qubit", authors: "P. W. Shor, S. P. Jordan", year: 2008}
  - {arxiv: "1003.0923", title: "Approximating Turaev-Viro 3-manifold invariants is universal for quantum computation", authors: "G. Alagic, S. P. Jordan, R. Koenig, B. W. Reichardt", year: 2010}
  - {arxiv: "2503.05625", title: "End-to-End Quantum Algorithms for the Jones Polynomial", authors: "T. Laakkonen, E. Rinaldi, C. N. Self, E. Chertkov, M. DeCross, et al.", year: 2026, note: "PRX Quantum 7, 020355; Quantinuum H2-2"}
  - {arxiv: "2512.19028", title: "Classical and Quantum Algorithms for Topological Invariants of Torus Bundles", authors: "N. A. Colón Vargas, C. Ortiz Marrero", year: 2025}
---

## Best classical

Exact evaluation of the Jones polynomial of a link at a generic root of unity is #P-hard (Jaeger, Vertigan and Welsh 1990), with the known exceptions at the trivial points t ∈ {±1, ±i, e^{±2πi/3}, e^{±πi/3}} where it is polynomial. Practical knot software (Kauffman-bracket state sums, tensor-network contractions of the braid representation) handles knots with tens to a few hundred crossings depending on treewidth; the cost is exponential in the cut width of the diagram, not in the number of crossings, so knots with low-width diagrams remain easy at any size. For 3-manifold invariants the picture is the same: Turaev–Viro and Witten–Reshetikhin–Turaev invariants are #P-hard exactly, and their approximation under topological restrictions (for example torus bundles) can fall back to classical algorithms; Colón Vargas and Ortiz Marrero give both an O(log N)-qubit quantum algorithm and an O(N²) classical one for the torus-bundle case [6], illustrating that the hardness is fragile under restriction.

## Best quantum

Aharonov, Jones and Landau gave a polynomial-time quantum algorithm for the additive approximation of the Jones polynomial at roots of unity, by representing the braid group in the Temperley–Lieb algebra and estimating a matrix element with a Hadamard test [1]. Aharonov and Arad showed the plat-closure version is BQP-complete [2], and Shor and Jordan that the trace-closure version is complete for DQC1, the one-clean-qubit class [3]. Alagic, Jordan, Koenig and Reichardt showed that approximating Turaev–Viro 3-manifold invariants is BQP-complete as well [4]. These are unconditional reductions: a classical polynomial algorithm for plat-closure Jones at these precisions would imply BPP = BQP.

Laakkonen et al. compiled a braid-to-circuit pipeline and ran small instances on Quantinuum H2-2, using topologically equivalent braids as a consistency check [5]. Their stronger crossover estimate concerns **Markov-closed braids** and a comparison with an MPO classical method, not an executed 2,800-crossing knot calculation. They fitted classical cost on 10,000 constructed braids with at most 600 crossings and 10–30 strands, then extrapolated along the dataset's principal component. With an assumed two-qubit error rate `1e-4` and a 30 ms depth-one circuit time, their model puts a possible crossover near 2,800 crossings, where the quantum value would have about **40% relative error** [5, Sec. IV]. The authors explicitly note that the braid family has special construction and that larger benchmark instances are needed to establish a same-instance advantage. A different error rate, braid family, precision target or classical algorithm can shift the boundary.

## What survives

The complexity proof and small-device algorithm are real; precision and independent scientific use remain open. The algorithm guarantees additive error after a normalisation that grows exponentially with the number of strands. Such a guarantee need not resolve the absolute invariant or a topological distinction on a given knot. The reported ~40% **relative** error at the projected crossover is a separate empirical estimate under a noise model, not the general BQP approximation guarantee [5]. Exact polynomials and structural theorems remain important in knot theory; no published family here links the quantum output's specific precision to a question those tools cannot already answer. The connection to Chern–Simons theory, quantum groups and conformal field theory supplies mathematical motivation, but it does not identify that family automatically. Restricted manifold classes where the invariant is classically tractable [6] show that input structure matters.

## Verdict

Surviving as a foundational complexity result. BQP-completeness settles the **general approximation problem**, while the most concrete hardware study supplies an extrapolated, noisy same-family crossover rather than a realized one [5]. The unresolved step is to specify a mathematically useful family and precision target, then show that the relevant classical methods cannot meet it. The [open question](../questions/jones-useful-hard-braids.html) records that benchmark.
