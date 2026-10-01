---
type: method
id: sqd
title: Sample-based quantum diagonalization (SQD / QSCI)
title_zh: 采样式量子对角化（SQD / QSCI）
summary: Sample bitstrings from a quantum circuit, then diagonalise in their subspace classically. Exact-ground-state sampling scales poorly on studied Hubbard and Heisenberg models, and a flagship single-layer LUCJ result has a fast classical reproduction. A time-evolved QSCI chemistry study finds more compact subspaces than one conventional selection rule, but similar compactness to HCI at convergence. No tested family establishes that the quantum samples outperform the strongest classical route at matched accuracy and total cost.
summary_zh: 用量子电路采样比特串，再在采样子空间内经典对角化。精确基态采样在已测试的 Hubbard、Heisenberg 模型上标度不利，单层 LUCJ 实验也有快速经典复现。一项时间演化 QSCI 化学研究得到了比某种传统选择规则更小的子空间，但收敛时与 HCI 接近。目前尚无同精度、同总成本下量子采样超过最强经典方法的实例族。
status: seed
last_verified: 2026-10-01
verdict: surviving
dimensions:
  classical_hardness: {level: unknown, note: "single-layer LUCJ energy evaluation has a polynomial-time classical algorithm; worst-case UCJ sampling hardness does not establish hardness of a useful chemistry circuit or of finding its selected subspace"}
  quantum_easiness: {level: unknown, note: "needs a feasible circuit that yields an accurate, classically hard-to-discover compact subspace at polynomial sample and diagonalisation cost; neither exact-ground-state sampling nor published time-evolved QSCI establishes this combination"}
  willingness_to_pay: {level: unknown, note: "inherits the application; no buyer specific to the method"}
related:
  problems: [ground-state-energy]
  claims: [ibm-sqd-2024]
  questions: [ideal-sqd-vs-classical-selection]
references:
  - {arxiv: "2405.05068", title: "Chemistry beyond the scale of exact diagonalization on a quantum-centric supercomputer", authors: "J. Robledo-Moreno et al.", year: 2025}
  - {arxiv: "2501.07231", title: "Critical limitations in quantum-selected configuration interaction methods", authors: "P. Reinholdt et al.", year: 2025}
  - {arxiv: "2605.02494", title: "A Critical Assessment of the Sample-Based Quantum Diagonalization for Heisenberg and Hubbard Models", authors: "C. Gaberle, M. S. Jattana", year: 2026, note: "exact-ground-state sampling on Heisenberg/Hubbard lattices; required configurations grow exponentially even with optimal ordering"}
  - {arxiv: "2607.21337", title: "Efficient classical simulation of large-scale unitary cluster Jastrow circuits", authors: "K. Belagali et al.", year: 2026}
  - {arxiv: "2509.02525", title: "Towards Compact Wavefunctions from Quantum-Selected Configuration Interaction", authors: "T. Weaving, A. Mingare, A. Ralli, P. V. Coveney", year: 2025, note: "42-qubit time-evolved QSCI on stretched SiH4; 200-fold compactness relative to a conventional SCI criterion, similar to HCI at convergence"}
  - {arxiv: "2504.12893", title: "Hardness of classically sampling quantum chemistry circuits", authors: "A. Hafid, H. Iwakiri, K. Tsubouchi, N. Yoshioka, M. Kohda", year: 2025, note: "worst-case UCJ sampling hardness under a polynomial-hierarchy assumption, not a physical-instance hardness result"}
---

## How it works

Prepare an approximate ground state on the device (typically a local unitary cluster Jastrow, LUCJ, circuit), sample computational-basis bitstrings, correct them for particle-number and spin symmetry ("configuration recovery"), and diagonalise the Hamiltonian in the span of the sampled determinants on a classical computer. Iterate: the classical eigenvector's occupation numbers steer the next round of recovery. Demonstrated on N₂ and [2Fe-2S]/[4Fe-4S] clusters with 77 qubits [1], and in 2026 extended, via embedding, to a 12,635-atom protein–ligand complex.

## Preconditions

1. The selected basis subspace must attain the target energy with a manageable number of configurations. The state sampled by the circuit need not equal the exact ground state; the two distributions require separate tests.
2. A feasible, classically initialised circuit must find that subspace with manageable shots and preparation cost. Selection, symmetry recovery and diagonalisation costs count on both sides.
3. Quantum samples must improve the **same-instance, same-error end-to-end cost** over strong classical selectors and any efficient classical simulation of the preparation circuit. Hardness of sampling arbitrary UCJ circuits alone does not certify this.

## Known limits

- **Exact-state sampling is costly on tested lattices.** Gaberle and Jattana sample exact ground states of Heisenberg and Hubbard lattices and find exponential growth in the configurations needed for fixed accuracy, even under ordering by exact probability [3]. This is evidence about those model families and this sampling distribution, not a theorem for every useful circuit-generated distribution.
- **Our small-model test finds no benefit.** For the 4×3 half-filled Hubbard model, exact-ground-state sampling, top-probability selection and HCI have similar energy-vs-K curves at the tested couplings (`numerics/sqd_ideal_test.py`). At U/t = 4, selecting 16% of the space still leaves 0.04 t per site of error. Two rounds of classical configuration recovery starting from uniform random bitstrings reach similar accuracy in this test. One size cannot establish asymptotic scaling or a universal no-go.
- **A chemistry counterexample deserves a matched check.** Time-evolved QSCI on stretched SiH4 used 42 hardware qubits and produced a subspace more than 200 times smaller than one conventional SCI criterion at comparable energy, but similar compactness to HCI at convergence [5]. The workflow also uses classical Hamiltonian-connected excitation selection. It does not isolate a growing, end-to-end advantage of the quantum samples over HCI or other classical samplers.
- **Systematic errors.** Reinholdt et al. document biases in QSCI energies and non-variational behaviour under realistic sampling budgets [2].
- **The flagship circuit has a classical reproduction.** A polynomial-time classical energy algorithm for single-layer LUCJ reproduced the 77-qubit experiment on a laptop in under a minute [4]. A separate worst-case hardness result for general UCJ sampling [6] does not establish hardness for that particular circuit or for useful selected-configuration outputs.

![Ideal-limit SQD test](../figs/fig5_sqd_ideal.png)

## Verdict

Surviving as a research direction, without a demonstrated quantum advantage. The tested exact-state sampling route is weak on strongly correlated lattice models; the flagship shallow LUCJ route has a strong classical counterexample. The time-evolved chemistry study leaves open whether a **different, efficiently prepared distribution** can reveal a compact useful subspace that strong classical methods cannot find as cheaply. The [open question](../questions/ideal-sqd-vs-classical-selection.html) separates the ideal-sampler limit from that practical circuit-and-selection test. A growing advantage needs matched energy error, subspace size, total shots, circuit and classical costs, and a classical simulation challenge on the same instance family.
