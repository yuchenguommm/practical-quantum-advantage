---
type: question
id: dmrg-vs-qpe-cost-accuracy-oled
title: Same-instance classical and quantum cost–accuracy curve for an OLED emitter
title_zh: 对同一 OLED 发光体测量经典与量子计算的成本和误差
summary: The published 14-emitter benchmark already reaches 0.0501 eV mean absolute error on classical processors. For one public, decision-relevant emitter Hamiltonian, can a fault-tolerant quantum algorithm beat the best classical workflow at the same accuracy and total cost? No such comparison is reported for the named emitters, and no buyer-defined acceptance threshold is documented.
summary_zh: 已发表的 14 个发光体基准在经典处理器上达到 0.0501 eV 平均绝对误差。对于一个公开、与实际决策有关的发光体哈密顿量，容错量子算法能否在相同精度和完整成本下超过最强经典流程？现有论文没有这样的同实例比较，也没有给出买方验收门槛。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Publish one emitter's geometry, basis, orbitals, integrals and observable definition. At several accuracy levels, compare measured wall time and hardware cost for the best classical methods (including iQCC+PT and whichever of CC, DMRG, SHCI and AFQMC is competitive) against a compiled fault-tolerant quantum algorithm on that same Hamiltonian. Include preparation overlap, repetitions, ancillas, logical gates, and state/geometry error. Obtain a buyer's written accuracy, throughput or price target. Report the full cost–error Pareto curves and all missing inputs."
  difficulty: phd
  resolved: false
related:
  applications: [oled-emitters]
  problems: [ground-state-energy, excited-states]
  methods: [phase-estimation]
  questions: [first-hand-payment-evidence]
references:
  - {arxiv: "2512.13657", doi: "10.1021/jacs.6c04752", title: "Towards Quantum Advantage in Chemistry", authors: "S. N. Genin, O. Kwon et al.", year: 2026, note: "arXiv v2, Table 2 and SI.1-2, SI.2-2, SI.3-1; journal version titled Large-Scale Quantum Computing Emulation for Accurate Triplet States of Ir(III) and Pt(II) Phosphorescent Emitters"}
  - {arxiv: "2208.02199", title: "Is there evidence for exponential quantum advantage in quantum chemistry?", authors: "S. Lee et al.", year: 2023}
  - {arxiv: "2111.04169", title: "Estimating Phosphorescent Emission Energies in Ir(III) Complexes using Large-Scale Quantum Computing Simulations", authors: "S. N. Genin et al.", year: 2022, note: "nine Ir emitters at CAS(36,36), or 72 active-space qubits; classical iQCC+PT and DFT comparison"}
---

## Why it matters

An OLED emitter is an industrially meaningful molecule, but the published Ir/Pt set does not establish a quantum advantage. OTI Lumionics and Samsung SAIT used classical processors to emulate iQCC+PT and obtained a 0.0501 eV mean absolute error on 14 measured T1-to-S0 emission gaps [1]. The paper's 0.05 eV is an **observed cohort error**, not a written buyer threshold. The authors regard these molecules as predominantly single-reference and classically tractable up to CAS(100,100) [1]. Thus a DMRG-only baseline would be incomplete; the group's own classical iQCC implementation must also be beaten.

Our [reanalysis script](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/oled_genin_benchmark.py) transcribes the public supplementary gaps and recomputes the five reported method errors. It does not run an electronic-structure solver. On Q1, the measured gap is 1.974 eV and iQCC+PT at the benchmark active space gives 1.988 eV, a 0.014 eV error. Q1's CAS(70,70) **singlet solver alone** took 107.10 hours; CAS(100,100) took 199.37 hours [1]. These timings are not the full gap cost. The paper gives no same-Hamiltonian quantum phase-estimation estimate, and the geometry and integral files needed for an independent solver comparison are not provided in the tables we used.

The [paired-error sensitivity calculation](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/oled_paired_error_robustness.md) finds that iQCC+PT improves on TD-B3LYP for 12 of these 14 named emitters. The all-cohort mean absolute-error difference is 0.0711 eV from the rounded supplement, with a 0.0656–0.0832 eV range after leaving out any single molecule. This supports a within-cohort accuracy gain of the classically run iQCC+PT workflow. It does not establish prospective performance on a new scaffold, an identical Hamiltonian across methods, or a quantum-hardware gain.

## What is known

| Evidence | Result | What it does not establish |
|---|---|---|
| 14-compound classical iQCC+PT [1] | Reported MAE 0.0501 eV | A buyer's acceptance threshold or quantum advantage |
| Q1 classical iQCC+PT [1] | 0.014 eV absolute gap error at benchmark active space | Error on an unseen emitter or total screening throughput |
| Q1 classical iQCC timing [1] | 107.10 h for one CAS(70,70) singlet solver run | Full S0/T1 workflow time or quantum crossover |
| Q1 CAS(100,100) [1] | 199.37 h for one singlet solver run | A hard correlated state; the authors' diagnostics favour a single-reference picture |

Supplementary Table SI.3-1 lists an active-space sweep for Q1's uncorrected iQCC gap, while Table SI.2-2 gives the **singlet-state solver** times on the same named molecule [1]. The [reanalysis data](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/results/oled_genin2026_reanalysis.json) combine those reported quantities without calling the result a full cost–error curve:

| Q1 active space | System qubits | SI.3-1 gap (eV) | Absolute gap error (eV) | Singlet solver (h) |
|---|---:|---:|---:|---:|
| CAS(50,50) | 100 | 1.999 | 0.025 | 87.02 |
| CAS(70,70) | 140 | 1.988 | 0.014 | 107.10 |
| CAS(100,100) | 200 | 1.932 | 0.042 | 199.37 |

The 100-system-qubit row is a concrete starting point for a near-term experiment. Those 100 qubits exclude ancillas and error correction; the 87.02 hours exclude the triplet solver, Hamiltonian generation and other workflow costs. The errors are non-monotone with active-space size. Table SI.1-2 also reports 1.982 eV for the benchmark's uncorrected Q1 iQCC result, rather than SI.3-1's 1.988 eV at CAS(70,70). That discrepancy needs clarification before joining the sweep to the 14-emitter benchmark. We have kept the two series separate in the figure.

**Sensitivity to classical calibration.** The paper's headline method comparison uses raw calculated gaps [1]. A screening team with measured emitters could fit a simple systematic-bias correction on prior compounds. We transcribed all six DFT columns in SI.1-3 and, for each of the 14 molecules, fitted a one-parameter additive offset on the other 13 before predicting the held-out measurement. We also trained on all seven Ir compounds and tested on the seven Pt compounds, then reversed the direction. The [data and reproducible calculation](https://github.com/yuchenguommm/practical-quantum-advantage/tree/main/numerics) report every method, including CC and iQCC, with offset and affine fits. Selected rows are:

| Method [1] | Raw MAE (eV) | Leave-one-molecule-out offset MAE | Ir/Pt-family holdout offset MAE |
|---|---:|---:|---:|
| RO-CAM-B3LYP | 0.1161 | 0.0938 | 0.1544 |
| RO-ωB97X | 0.2194 | 0.0735 | 0.0973 |
| CCSD | 0.2201 | 0.0965 | 0.0986 |
| iQCC+PT, run classically | 0.0499 from rounded SI rows | 0.0505 | 0.0843 |

The paper reports `0.0501 eV` for iQCC+PT from its unrounded values; our `0.0499 eV` uses the displayed three-decimal gaps. The iQCC+PT result remains the lowest MAE in these selected comparisons. Calibration narrows the **observed** gap to some conventional methods, especially for a functional with a large systematic offset. RO-ωB97X was selected for this table *after inspecting six functionals*, so its cross-validated number has method-selection bias. Fourteen related molecules are too few for a prospective error guarantee, and the Ir/Pt holdout trains on only seven cases. DFT and iQCC may also use different geometries [1, SI.1-3]. This check changes the classical comparison that a buyer should test; it does not produce a quantum cost or prove a commercially usable calibrated DFT model.

**Nested method selection.** To prevent a held-out experimental value from selecting its own DFT baseline, we compared all six published DFT columns under three fixed fitting rules within each outer training set: raw, additive offset and affine. Inner leave-one-molecule-out MAE selected the method and rule; they were then fitted on all outer-training molecules. The [script, 14 predictions and selected pipelines](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/results/oled_genin2026_nested_dft_selection.json) give:

| Outer test | Inner-selected DFT pipeline | Outer MAE (eV) | What this tests |
|---|---|---:|---|
| One molecule, repeated 14 times | RO-ωB97X + offset in all 14 folds | `0.0735` | Transfer among related emitters within this cohort |
| Ir family, then Pt family | TD-B3LYP + affine for Ir; TD-B3LYP + offset for Pt | `0.2302` | Two-fold transfer across metal families with seven training molecules |

For perspective, the paper's classically run iQCC+PT has `0.0499 eV` raw MAE from rounded rows on the complete cohort, and its *separately fitted* Ir/Pt offset holdout has `0.0843 eV`. These are descriptive contrasts, not a single competition with identical training and selection protocols. The nested method choice removes **within-fold** target leakage; the 18 candidate pipelines and this analysis were devised after seeing the study, so retrospective analysis still cannot establish an unseen-molecule error. The large family-holdout error also rules out claiming that the `0.0735 eV` number transfers reliably between Ir and Pt chemistries. A new external cohort is the next meaningful test.

A smaller alternative is the earlier nine-complex Ir benchmark at CAS(36,36), which maps to 72 active-space qubits [3]. Its iQCC+PT and fine-tuned DFT mean absolute deviations were 0.201 and 0.192 eV, respectively [3, Table 1]. A 72-qubit demonstration would still need to beat a measured classical baseline on the same molecular Hamiltonian; reproducing the already classically simulated circuit would only verify implementation. The older cohort has different molecules and methods, so its accuracy figures cannot be combined with Q1's active-space sweep.

## Input availability audit

The 2026 study has a [published JACS version](https://doi.org/10.1021/jacs.6c04752). Its [open supplementary package](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13523740/supplementaryFiles) contains one PDF and image files. The PDF provides the reported gap, active-space and timing tables, plus the geometry-optimization and orbital-selection protocol [1]. It does **not** include Cartesian coordinate files for the named S0/T1 structures, selected orbital coefficients, or the one- and two-electron integral arrays. The paper says a modified GAMESS program generated those integrals; method details alone do not fix the same numerical Hamiltonian [1, Methods]. The older arXiv study describes its 72-qubit CAS(36,36) construction but likewise supplies no coordinate or integral arrays in its arXiv text and supplement [3]. This audit is about the inspected public files; it does not claim that the authors cannot provide further data.

| Needed for a matched solver run | Currently public | Missing deliverable |
|---|---|---|
| Experimental target and named molecule | Gap tables and molecular labels [1, 3] | A buyer-defined error or throughput target |
| Geometry and basis | Optimization functional, ECP and basis protocol [1] | Coordinates of the triplet-optimized geometry used for the gap, exact basis/ECP versions and charge/spin conventions; singlet geometry if reproducing TDDFT too |
| Active-space Hamiltonian | Electron/orbital counts and selection rule [1, 3] | Orbital coefficients or the exact one- and two-electron integrals, frozen-core energy and integral ordering |
| Classical runtime | Q1 singlet iQCC timings at three CAS sizes [1] | Full gap workflow time, machine allocation and challenger solver convergence at each accuracy |
| Quantum cost | Active-space system-register sizes [1, 3] | State-preparation overlap, compiled circuit, logical ancillas, repetitions and fault-tolerant schedule |

The first reproducibility milestone is a public, versioned Hamiltonian bundle for one emitter and both spin sectors, with checksums and a script that regenerates the reported classical gap. A new Hamiltonian generated from a similar geometry would be a useful independent benchmark, but its results could not be labelled a reproduction of the published Q1 calculation.

The [community task for a public emitter Hamiltonian](https://github.com/yuchenguommm/practical-quantum-advantage/issues/14) lists the file inventory and acceptance checks. Contributors can point to an existing public bundle or submit a new, clearly labelled benchmark through a pull request.

## What would settle it

The front matter states the full benchmark. Start by obtaining public geometry, basis, selected orbitals and Hamiltonian for one emitter. Reproduce the reported classical result and measure the full S0/T1 workflow time, then test the strongest competing classical solvers on the same instance and accuracy. Only then compile phase estimation or another fault-tolerant method for that Hamiltonian, including state preparation, repeated runs and error correction. Display cost versus error for both approaches and add a written buyer requirement. The current evidence does not support an arbitrary 0.05 eV crossover line or a universal T-gate budget.
