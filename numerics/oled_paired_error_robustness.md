# How stable is the OLED cohort's accuracy gain?

The [14-emitter study](https://arxiv.org/html/2512.13657v2) reports a 0.0501 eV mean absolute error for iQCC+PT, executed on classical processors, versus 0.1209 eV for TD-B3LYP. We recomputed the **paired** per-molecule absolute-error difference from Supplementary Table SI.1-2, using its displayed gaps rounded to 0.001 eV. This checks how the reported accuracy gain is distributed across the named emitters; it does not compare quantum and classical hardware on one Hamiltonian.

| Cohort | Molecules | TD-B3LYP MAE (eV) | iQCC+PT MAE (eV) | Mean paired improvement (eV) | iQCC+PT lower error |
|---|---:|---:|---:|---:|---:|
| All | 14 | 0.1210 | 0.0499 | 0.0711 | 12/14 |
| Ir(III), Q1–Q7 | 7 | 0.1430 | 0.0426 | 0.1004 | 7/7 |
| Pt(II), Q8–Q14 | 7 | 0.0990 | 0.0571 | 0.0419 | 5/7 |

Only Q8 and Q10 favour TD-B3LYP in absolute error, by 0.016 and 0.086 eV respectively. Removing any one molecule leaves the all-cohort mean paired improvement between **0.0656 and 0.0832 eV**. A seeded, 20,000-replicate bootstrap that draws seven Ir and seven Pt pairs within their respective groups gives a **descriptive percentile range** of **0.0417–0.0997 eV** for that mean difference. The calculation keeps published predictions fixed. The data and [script](oled_paired_error_robustness.py) record the exact per-molecule differences and resampling rule.

This is credible evidence of an accuracy difference **within this selected cohort**. It cannot give a prospective error guarantee for new emitter scaffolds: the fourteen molecules are related, the group split is only Ir versus Pt, and the bootstrap does not account for systematic errors from geometry, electronic-structure choices or experiment. The source paper's DFT and iQCC workflows may also use different geometries, so even though the *molecules and measured targets* are paired, these are not necessarily the same Hamiltonians. A buyer's accuracy or throughput requirement remains undocumented. The iQCC+PT calculation itself ran on classical processors; the result demonstrates an algorithmic accuracy gain over this DFT baseline, not a quantum-computer advantage.

Reproduce from the [transcribed public table](results/oled_genin2026_si1.csv):

```bash
python numerics/oled_paired_error_robustness.py
```

The [machine-readable output](results/oled_paired_error_robustness.json) includes all fourteen paired errors. Its 0.0499 eV MAE differs slightly from the paper's 0.0501 eV because the supplement displays rounded gaps.
