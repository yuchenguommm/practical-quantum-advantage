---
type: question
id: ideal-sqd-vs-classical-selection
title: Can a useful quantum sampler find compact CI subspaces that classical methods miss?
title_zh: 量子采样能否找到经典方法难以发现的紧凑 CI 子空间？
summary: Exact-ground-state sampling scales poorly on studied lattice models; that distribution need not be optimal for discovering an energy-accurate CI subspace. Test whether an efficiently prepared quantum distribution finds a compact useful subspace at lower total cost than matched classical selection and circuit simulation. A hard-to-sample circuit without a compact subspace, or a compact subspace already found by HCI, would not establish an advantage.
summary_zh: 在已研究的晶格模型上，精确基态采样的标度不利，但这一采样分布未必最适合寻找能量准确的 CI 子空间。需要测试能否制备一种经典难以复现的采样分布，并以低于同实例经典选择与电路模拟的总成本找到紧凑、有用的子空间。单有难采样线路或单有紧凑子空间都不够。
status: seed
last_verified: 2026-10-01
question:
  what_would_settle_it: "Fix a public Hamiltonian family, basis, target energy error, symmetry sector, number of shots and classical/quantum total-cost model. Compare exact-ground-state sampling as an idealised diagnostic; feasible circuits with explicit classical initialisation; top-probability selection when exact amplitudes are available; HCI/CIPSI and strong classical circuit or sampler simulations. Measure energy error against K, unique configurations against shots, classical diagonalisation work and circuit preparation/noise cost over at least three growing sizes. Test alternative circuits at identical budgets, reporting classical simulability and whether a compact subspace remains useful as size grows. A scaling gap over the strongest classical route would be evidence; failure of finitely many families would not prove a universal no-go."
  difficulty: phd
  resolved: false
related:
  methods: [sqd]
  problems: [ground-state-energy]
references:
  - {arxiv: "2605.02494", title: "A Critical Assessment of the Sample-Based Quantum Diagonalization for Heisenberg and Hubbard Models", authors: "C. Gaberle, M. S. Jattana", year: 2026, note: "exact-ground-state sampling requires exponentially many selected configurations in tested lattice families"}
  - {arxiv: "2509.02525", title: "Towards Compact Wavefunctions from Quantum-Selected Configuration Interaction", authors: "T. Weaving, A. Mingare, A. Ralli, P. V. Coveney", year: 2025, note: "time-evolved QSCI on SiH4; HCI reaches similar compactness at convergence"}
  - {arxiv: "2607.21337", title: "Efficient classical simulation of large-scale unitary cluster Jastrow circuits", authors: "K. Belagali et al.", year: 2026, note: "classical energy algorithm for single-layer LUCJ, including the IBM 77-qubit circuit"}
  - {arxiv: "2504.12893", title: "Hardness of classically sampling quantum chemistry circuits", authors: "A. Hafid, H. Iwakiri, K. Tsubouchi, N. Yoshioka, M. Kohda", year: 2025, note: "worst-case UCJ sampling hardness; no useful-instance guarantee"}
---

## Why it matters

SQD underlies IBM's quantum-centric supercomputing programme and its large protein demonstration. For a computational advantage, quantum sampling must help find a useful low-energy subspace **more cheaply than the best classical strategy**, including preparation, measurement and diagonalisation. Sampling the exact ground state isolates one idealised distribution, but a task-designed circuit could sample another. The research question is whether such a circuit can be both useful for selection and genuinely hard to replace classically.

## What is known

- Our 4×3 half-filled Hubbard test (`numerics/sqd_ideal_test.py`) found similar energy-vs-K curves for exact-ground-state sampling, top-probability selection and HCI at U/t = 4 and 8. At U/t = 4, selecting 16% of the full space still leaves 0.04 t per site of error. This is one small system, not a no-go theorem.
- Exact-ground-state sampling on the tested Hubbard and Heisenberg families needs exponentially growing K at fixed energy accuracy, even if determinants are included by decreasing exact probability [1]. Top-probability selection maximises captured probability mass at fixed K; it need not minimise the projected Hamiltonian's energy error.
- A 42-qubit time-evolved QSCI calculation on stretched SiH4 found over 200-fold fewer configurations than one conventional SCI selection criterion at comparable energy, but reported compactness similar to HCI at convergence [2]. Its classical expansion heuristic also uses Hamiltonian-connected excitations. The quantum-specific benefit over the strongest classical selector has not been isolated.
- A single-layer LUCJ energy algorithm has an efficient classical implementation [3], while general UCJ sampling has a worst-case hardness result under a complexity assumption [4]. Neither establishes an advantage for a physical Hamiltonian family.

## What would settle it

See the front matter. The first experiment should compare exact-state samples with samples from a **feasible circuit**, then vary circuit structure, depth and preparation rule. A classical seed can be supplied, but its construction cost and the improvement provided by the quantum circuit must be recorded separately. Circuit or initialisation search, including automated search, is a research technique to test against classical selectors; it supplies no advantage by itself. Report K(ε, N), unique useful configurations per shot, diagonalisation cost and classical simulation cost for the same Hamiltonian. A candidate circuit whose output is hard to sample globally may still yield an easy-to-find useful subset; test the downstream selection task directly.

## Who could take it

Electronic-structure and quantum-algorithm researchers working together. The exact-state diagnostic can be reproduced on a workstation; a growing-size, same-cost circuit benchmark needs substantially more work. A negative result for a specified circuit family is valuable if its scope is stated precisely.
