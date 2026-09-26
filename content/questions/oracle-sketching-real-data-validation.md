---
type: question
id: oracle-sketching-real-data-validation
title: Does quantum oracle sketching win on the same real-data task after memory, samples and runtime are all counted?
title_zh: 同一真实数据任务计入存储、样本和时间后，量子 oracle sketching 仍有优势吗？
summary: The unconditional space lower bounds for quantum oracle sketching use constructed task distributions. Its public real-data sweeps plot classical ridge/PCA performance against a formula-derived quantum memory size, without running the quantum learner on those data. A reproducible same-task Pareto comparison must execute or validate the quantum output and test stronger low-memory classical sketches at matched accuracy, sample count and wall time.
summary_zh: 量子 oracle sketching 的无条件空间下界针对构造的任务分布。公开的真实数据扫描将经典 ridge/PCA 性能与按公式计算的量子存储量配对，没有在这些数据上运行量子学习器。需要在相同精度、样本量与时间下核对量子输出，并与更强的低存储经典方法比较。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Pin one public dataset and its train/test split. Run the paper's quantum oracle-sketching and readout pipeline, or a justified small-size exact simulation, to measure prediction/PCA error versus logical memory, samples, shots and total gates. Measure matched classical streaming, feature hashing, sparse JL and adaptive sketches with actual peak memory and wall time, including data preprocessing. For larger sizes, state precisely which quantum quantities are extrapolated, validate them against small sizes and separately report physical error-correction and input-interface costs. Repeat on an independent dataset and obtain a user-defined accuracy/latency/memory target."
  difficulty: phd
  resolved: false
related:
  problems: [streaming-classical-data-memory, classical-data-machine-learning]
  methods: [hhl-qsvt]
references:
  - {arxiv: "2604.07639", title: "Exponential quantum advantage in processing massive classical data", authors: "H. Zhao, A. Zlokapa, H. Neven, R. Babbush, J. Preskill, J. R. McClean, H.-Y. Huang", year: 2026, note: "Fig. 2 and Theorems 1-4; theoretical and empirical evidence concern different instance families"}
  - {url: "https://github.com/haimengzhao/quantum-oracle-sketching/tree/a3fe8d6fe777750749f5e90131180e016088bdaf/real_datasets", title: "Pinned public real-dataset experiment scripts", authors: "H. Zhao and collaborators", note: "Classification accuracy from sklearn; formula-based quantum memory; multiple classical sketch modes available"}
  - {arxiv: "2609.13549", title: "Practical Considerations for Processing Massive Classical Data via Quantum Oracle Sketching", authors: "S. Markidis", year: 2026, note: "Offline phase-oracle case study identifies circuit-depth and interactive-runtime obstacles without challenging the online space theorem"}
---

## Why it matters

This is one of the few claims of a *proved* quantum advantage for processing ordinary classical data, with ideal logical memory below 100 qubits [1]. Its theorem establishes an information-theoretic space separation for specified constructed tasks and sample budgets. The same paper presents real-data plots for sentiment and single-cell analysis, but the public scripts compute their accuracy with classical estimators and assign the quantum memory coordinate analytically [2]. The plot does not directly test whether the quantum circuit attains that accuracy on those datasets. Keeping the theorem and the empirical extrapolation separate prevents both an unjustified practical claim and an unjustified dismissal of the theorem.

## Current reproducibility starting point

The pinned code revision [2] includes `imdb_svm.py`, `pbmc68k_svm.py`, `imdb_pca.py`, `pbmc68k_pca.py`, and `sweep_utils.py`. Classification uses `RidgeClassifier` cross-validation; the quantum size function counts ideal logical qubits from data dimensions and sparsity. The code offers feature hashing, sparse Johnson-Lindenstrauss projections and adaptive classical sketches. An independent *offline* phase-oracle case study found deep compiled circuits and described the need for an interactive quantum runtime; it does not test the online theorem [3]. A useful first contribution is a table for one dataset separating **measured** test accuracy, measured peak memory, derived logical qubits, sample count and wall time. A point calculated from a formula should remain labelled an estimate.

## What would settle it

The front matter gives the matched test. Success would show the quantum pipeline's output at the same target accuracy with a reproducible sample and runtime budget, then a space advantage over tuned classical streaming methods on held-out data. Failure could arise from quantum approximation error, classical feature compression, state-preparation cost or simply a throughput target that a small-memory classical method already meets. Either result would sharpen the verdict for the [parent problem](../problems/streaming-classical-data-memory.html) without altering the proved lower bound for the paper's constructed instances.
