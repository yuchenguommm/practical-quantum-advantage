---
type: problem
id: integer-factoring-hidden-subgroup
title: Integer factoring, discrete logarithms and abelian hidden subgroup problems
title_zh: 整数分解、离散对数与交换群隐子群问题
summary: Shor proves polynomial-time quantum factoring and discrete logarithms; no superpolynomial classical lower bound is known. Pilatte proved correctness of a later factoring algorithm, and Gidney estimated a conditional RSA-2048 circuit with fewer than one million physical qubits. NIST's post-quantum migration is evidence of defensive demand, not a buyer of quantum attacks.
summary_zh: Shor 算法已证明量子计算机可在多项式时间内分解整数、求离散对数，但经典算法的超多项式下界尚未证明。Pilatte 证明了后续分解算法的正确性，Gidney 给出在特定硬件条件下以不到一百万物理比特分解 RSA-2048 的估计。NIST 的后量子迁移说明防御需求存在，不能证明有人采购量子攻击。
status: seed
last_verified: 2026-09-27
verdict: promising
dimensions:
  classical_hardness: {level: crypto, note: "best known general classical factoring algorithms are subexponential; no superpolynomial lower bound against classical algorithms is known"}
  quantum_easiness: {level: proven, note: "Shor 1994; Regev's O(n^3/2)-gate variant proven correct unconditionally by Pilatte; this grade is for factoring and discrete logs, not the separately assessed number-field class-group task"}
  willingness_to_pay: {level: unknown, note: "NIST's post-quantum standard documents defensive migration; no public procurement or price for quantum factoring itself is cited"}
resources: {logical_qubits: "~1,400 active (RSA-2048)", gates: "~6.5e9 Toffoli", note: "Gidney 2025 conditional engineering estimate: under 1e6 physical qubits and under one week at 0.1% physical error, 1 μs code cycles and 10 μs control reaction; the same estimate does not apply to class groups"}
related:
  applications: [cryptanalysis]
  problems: [combinatorial-optimization, representation-theory-multiplicities, number-field-s-units-class-groups]
  methods: [phase-estimation, dqi]
  questions: [first-hand-payment-evidence]
references:
  - {arxiv: "2308.06572", title: "An Efficient Quantum Factoring Algorithm", authors: "O. Regev", year: 2023}
  - {arxiv: "2310.00899", title: "Space-Efficient and Noise-Robust Quantum Factoring", authors: "S. Ragavan, V. Vaikuntanathan", year: 2023}
  - {arxiv: "2404.16450", title: "Unconditional correctness of recent quantum algorithms for factoring and computing discrete logarithms", authors: "C. Pilatte", year: 2024, note: "Forum Math. Pi 14, e5 (2026)"}
  - {arxiv: "2505.15917", title: "How to factor 2048 bit RSA integers with less than a million noisy qubits", authors: "C. Gidney", year: 2025}
  - {arxiv: "2510.02280", title: "An efficient quantum algorithm for computing S-units and its applications", authors: "J.-F. Biasse, F. Song", year: 2025}
  - {title: "Module-Lattice-Based Key-Encapsulation Mechanism Standard (FIPS 203)", authors: "National Institute of Standards and Technology", year: 2024, doi: "10.6028/NIST.FIPS.203"}
---

## Best classical

The general number field sieve factors an n-bit integer in subexponential time, and no 2048-bit RSA modulus has been factored classically. Prime-field discrete logarithms also have subexponential classical algorithms. Generic elliptic-curve discrete logarithms require square-root search in the group size. None of these observations proves a superpolynomial classical lower bound; cryptography relies on the practical hardness of selected parameter sizes.

Number-field class groups and S-units have different assumptions and input models. See their [separate assessment](../problems/number-field-s-units-class-groups.html). The RSA-2048 circuit estimate does not transfer to those tasks.

## Best quantum

Shor's algorithm factors and takes discrete logarithms in quantum polynomial time through period finding. Regev's later construction uses Õ(n^{3/2}) gates per run, with multiple runs and a number-theoretic correctness condition [1]. Ragavan and Vaikuntanathan reduced its space requirement [2]; Pilatte proved the correctness condition, without proving a classical lower bound or a practical circuit advantage [3]. Gidney's 2025 RSA-2048 estimate uses fewer than one million noisy physical qubits and under a week under specified error and timing assumptions [4].

Beyond factoring, quantum algorithms for [number-field S-units and class groups](../problems/number-field-s-units-class-groups.html) connect continuous hidden-subgroup methods with computational number theory [5]. The given-S theorem and the GRH-dependent class-group corollary are assessed separately on that page.

## Who pays

Intelligence and security agencies are potential users of cryptanalysis, but this page has no public procurement record or price for a quantum factoring computation. NIST's FIPS 203 explains why organisations are migrating to post-quantum key encapsulation [6]. That is direct evidence for defensive migration, which can proceed without a quantum computer. Computational number theory supplies a research motivation; a commercial customer for those calculations is not documented here.

## Verdict

Promising as a **foundational computational problem**. Factoring and discrete logarithms have independently important outputs, quantum polynomial time is proved, and the best known classical algorithms have much worse scaling. The superpolynomial classical lower bound remains unproved, so this verdict does not assert an unconditional separation. Gidney's RSA-2048 engineering model has about 1,400 active logical qubits and billions of Toffoli gates [4]; those are conditional estimates. The linked [cryptanalysis application](../applications/cryptanalysis.html) remains `surviving` because direct willingness to pay for a quantum attack is undocumented. Number-field class-group and S-unit tasks have their [own assessment](../problems/number-field-s-units-class-groups.html) and do not inherit this verdict.
