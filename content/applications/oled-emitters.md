---
type: application
id: oled-emitters
title: Phosphorescent OLED emitters
title_zh: OLED 磷光发光体
summary: OTI Lumionics and Samsung SAIT studied Ir/Pt phosphors used in OLEDs. Their 14-emitter T1-to-S0 benchmark reached 0.0501 eV mean absolute error with iQCC+PT on classical processors. The paper demonstrates industrial interest and a strong classical baseline; it does not state a buyer acceptance threshold or show an instance beyond classical computation.
summary_zh: OTI Lumionics 与三星 SAIT 研究了 OLED 用 Ir/Pt 磷光体。在 14 个发光体的 T1 到 S0 能隙基准上，经典处理器运行的 iQCC+PT 达到 0.0501 eV 平均绝对误差。论文说明企业关心这一问题，也给出了很强的经典基线；它没有写明买方验收门槛，也没有展示经典计算做不到的实例。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: none, note: "The published 14 Ir/Pt emitters are classically tractable, including Q1 at CAS(100,100); the authors' diagnostics describe them as predominantly single-reference. No harder, decision-relevant OLED instance is yet documented here."}
  quantum_easiness: {level: unknown, note: "The paper classically emulates iQCC; it gives no same-Hamiltonian quantum phase-estimation cost, guiding-state overlap, or hardware measurement budget."}
  willingness_to_pay: {level: first-hand, note: "OTI Lumionics and Samsung SAIT co-authored the benchmark and identify emitter prediction as an industrial task. The achieved 0.0501 eV MAE is not a stated buyer acceptance threshold; no price or procurement target is given."}
resources: {logical_qubits: "140–200 system qubits for CAS(70–100,70–100)", note: "Q1 CAS(100,100) was classically emulated; its 10.21 million abstract CNOT equivalent excludes fault tolerance. No emitter-specific compiled quantum resource estimate is available."}
related:
  problems: [ground-state-energy, excited-states]
  methods: [phase-estimation]
  questions: [dmrg-vs-qpe-cost-accuracy-oled, first-hand-payment-evidence]
references:
  - {arxiv: "2512.13657", doi: "10.1021/jacs.6c04752", title: "Towards Quantum Advantage in Chemistry", authors: "S. N. Genin, O. Kwon et al. (OTI Lumionics, Samsung SAIT)", year: 2026, note: "arXiv v2; Tables 1-2 and SI.1-2, SI.2-2, SI.3-1; journal version has a different title"}
  - {arxiv: "2111.04169", title: "Estimating Phosphorescent Emission Energies in Ir(III) Complexes using Large-Scale Quantum Computing Simulations", authors: "S. N. Genin et al.", year: 2021, note: "earlier nine-complex study, also run on classical hardware"}
---

## Who needs it

Emitter suppliers and display manufacturers need to predict phosphorescent colour and stability before synthesis. OTI Lumionics and Samsung SAIT directly participated in the published 14-compound benchmark [1]. This is evidence of industrial interest. The paper does not give the financial value of a better prediction or an explicit acceptance tolerance. Its experiments measure the 77 K photoluminescence gap of seven Ir(III) and seven Pt(II) complexes, mostly in low-dielectric solvents [1]. This page is about that phosphorescent benchmark; it does not transfer its numbers to TADF emitters or operating devices.

## Bottleneck

The benchmark compares the T1-to-S0 emission gap with experiment. Its 14-emitter mean absolute errors are 0.121 eV for TD-B3LYP, 0.220 eV for CCSD, 0.291 eV for CR-CC(2,3), and 0.0501 eV for iQCC+PT [1]. **The last number is an achieved error, not a buyer's written target.** The study omits spin-orbit coupling based on earlier work; temperature, solvent, geometry and device lifetime are separate sources of uncertainty. Q2 and Q4 needed CAS(100,100) rather than CAS(70,70) for a better fit to experiment [1].

## Computational problems

- [Ground-state energies](../problems/ground-state-energy.html) in the relevant spin sectors.
- [Excited-state and emission gaps](../problems/excited-states.html), including the state and geometry definitions used for comparison with photoluminescence.
- Device lifetime and degradation are further design tasks, not settled by an electronic energy gap.

## Best classical today

The authors ran iQCC+PT on classical processors and reached the reported 0.0501 eV mean absolute error. Their own diagnostics say this set is predominantly single-reference, and they do not present DMRG as the missing baseline for these 14 compounds [1]. For Q1, the measured gap is 1.974 eV; the classical iQCC+PT result at the benchmark active space is 1.988 eV, an absolute error of 0.014 eV. The uncorrected iQCC gap is 1.982 eV, an error of 0.008 eV. Across all 14 compounds, iQCC+PT performs better than uncorrected iQCC [1].

A [paired-error audit](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/oled_paired_error_robustness.md) of the rounded supplementary gaps finds that iQCC+PT has lower absolute error than TD-B3LYP on 12/14 named emitters, including 7/7 Ir and 5/7 Pt compounds. Its mean improvement is 0.0711 eV on this cohort; removing any one molecule leaves 0.0656–0.0832 eV. The selected molecules and possibly different input geometries limit transfer to new compounds. This is a real within-cohort gain of a classically executed algorithm over one DFT baseline, with no quantum hardware or buyer threshold involved.

An earlier, separate nine-Ir-complex benchmark used CAS(36,36), or 72 active-space qubits [2]. Its classically executed iQCC+PT reached 0.201 eV mean absolute deviation, versus 0.192 eV for its best reported tuned DFT functional, LC-wHPBE; its Pearson correlation across the nine compounds was higher, 0.762 versus 0.328 [2, Table 1]. This 72-qubit task has an industrially meaningful observable and fits a smaller quantum register, but the published comparison does not show a quantum speed or accuracy advantage over classical computation. The nine- and fourteen-compound cohorts should not be pooled into one scaling fit.

![Errors recomputed from the published 14-emitter tables](../figs/oled_genin2026_accuracy.png)

A further classical baseline is **calibration on previously measured emitters**. Our exploratory leave-one-molecule-out offset correction lowers RO-CAM-B3LYP's MAE from `0.1161` to `0.0938 eV`, and RO-ωB97X's from `0.2194` to `0.0735 eV`; iQCC+PT remains at about `0.05 eV` [1]. The latter DFT functional was picked after inspecting six options, and all 14 molecules belong to two related metal families. When we train the offset on one metal family and test on the other, RO-ωB97X gives `0.0973 eV` and iQCC+PT gives `0.0843 eV`. These are small-cohort sensitivity checks, not prospective validation or matched runtime measurements. The [benchmark question](../questions/dmrg-vs-qpe-cost-accuracy-oled.html) gives the fold rule and all results.

We also made DFT method selection part of each training fold, choosing among the six published functionals and raw, offset or affine calibration by inner leave-one-out error. This **nested** analysis gives `0.0735 eV` when holding out one molecule; it selects RO-ωB97X with an offset in every fold. Holding out an entire metal family changes the selected method and raises the error to `0.2302 eV`. The latter is a two-fold stress test on seven training molecules, not an estimate of prospective product performance. Candidate pipelines were defined after reading this publication, so even nested selection cannot remove that study-level choice. The [script and fold-level predictions](https://github.com/yuchenguommm/practical-quantum-advantage/blob/main/numerics/oled_nested_dft_selection.py) show exactly what changed.

The [script and transcribed data](https://github.com/yuchenguommm/practical-quantum-advantage/tree/main/numerics) recompute both panels from Supplementary Tables SI.1-2 and SI.1-3. The rounded source data give 0.0499 eV for iQCC+PT versus 0.0501 eV in the paper's unrounded Table 2. For Q1, Table SI.3-1 gives an uncorrected iQCC gap of 1.999 eV at CAS(50,50), an absolute error of 0.025 eV against its measured 1.974 eV gap. This model needs 100 **system** qubits before ancillas or error correction. The corresponding **singlet-state solver alone** ran for 87.02 hours; CAS(70,70) took 107.10 hours and CAS(100,100) took 199.37 hours, on 64 processes across two AMD EPYC 7702 processors [1]. These exclude the full S0/T1 workflow and are a measured classical baseline, not a quantum cost comparison. The [open benchmark question](../questions/dmrg-vs-qpe-cost-accuracy-oled.html) keeps this orbital sweep separate from the cohort statistics because the tables give different Q1 CAS(70,70) gaps.

## Verdict

Surviving as an industrial application to investigate, with **no demonstrated quantum advantage on the published emitter set**. The same paper that establishes the industrial scenario solves those named molecules classically. It does not provide a written 0.05 eV buyer threshold, a classically hard OLED instance, or a quantum run on the same Hamiltonian. A future claim needs a named emitter with public Hamiltonian or integrals, the best classical cost and error for its decision-relevant observable, a compiled quantum cost at the same error, and a buyer-defined target. The [open benchmark question](../questions/dmrg-vs-qpe-cost-accuracy-oled.html) records those missing inputs.
