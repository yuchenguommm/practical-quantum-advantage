---
type: problem
id: streaming-classical-data-memory
title: Space-limited learning from streams of classical data
title_zh: 有存储限制的经典数据流学习
summary: Quantum oracle sketching proves an unconditional space separation for constructed streaming linear-system and classification tasks. Its 2026 paper also plots large memory savings on real text and single-cell datasets, but the public real-data code measures classical ridge/PCA performance and assigns a formula-derived quantum memory size; it does not execute the quantum learner on those datasets. Total runtime includes processing at least roughly linear numbers of samples.
summary_zh: 量子 oracle sketching 对构造的数据流线性方程与分类任务证明了无条件的空间分离。2026 年论文还在文本和单细胞数据上展示很大的存储量差距，但公开的真实数据代码运行的是经典 ridge/PCA，并按公式计算量子存储量；它没有在这些数据上执行量子学习器。总运行时间仍需处理至少近线性数量的样本。
status: seed
last_verified: 2026-09-27
verdict: surviving
dimensions:
  classical_hardness: {level: lower-bound, note: "Information-theoretic classical space/sample lower bounds hold for constructed random-sample tasks under a specified memory and sample budget; they do not lower-bound classical memory for IMDb or PBMC data."}
  quantum_easiness: {level: proven, note: "Quantum oracle sketching uses polylogarithmic logical memory and roughly linear sample access in the paper's model. This is a space separation; finite-data quantum accuracy, full time, fault-tolerant overhead and sample-interface costs remain unmeasured."}
  willingness_to_pay: {level: second-hand, note: "Sentiment and single-cell analyses are real tasks, but no buyer-defined memory, accuracy, throughput or price requirement is documented for the quantum workflow."}
resources: {logical_qubits: "fewer than 60 in the paper's real-dataset formula-based comparisons", note: "Ideal logical-memory accounting; classical input pipeline, error correction, time and physical-qubit footprint are not included in the plotted machine-size comparison"}
related:
  problems: [classical-data-machine-learning, sparse-linear-systems, sorting-fft-storage]
  methods: [hhl-qsvt]
  questions: [oracle-sketching-real-data-validation]
references:
  - {arxiv: "2604.07639", title: "Exponential quantum advantage in processing massive classical data", authors: "H. Zhao, A. Zlokapa, H. Neven, R. Babbush, J. Preskill, J. R. McClean, H.-Y. Huang", year: 2026, note: "Theorems 1-4; Fig. 2; discussion of near-linear input processing and runtime caveat"}
  - {url: "https://github.com/haimengzhao/quantum-oracle-sketching/tree/a3fe8d6fe777750749f5e90131180e016088bdaf/real_datasets", title: "Quantum oracle sketching public real-dataset code, pinned revision", authors: "H. Zhao and collaborators", note: "imdb_svm.py and pbmc68k_svm.py use sklearn RidgeClassifier for accuracy; sweep_utils.py assigns a formula-derived quantum machine size. The repository also offers feature-hashing, sparse JL and adaptive classical baselines."}
  - {arxiv: "2609.13549", title: "Practical Considerations for Processing Massive Classical Data via Quantum Oracle Sketching", authors: "S. Markidis", year: 2026, note: "Independent offline phase-oracle implementation on DNA fingerprinting; compiled circuits too deep for current hardware. Offline formulation does not directly implement the original online space guarantee."}
---

## Best classical

A streaming classical learner can process samples without storing the entire data matrix. Feature hashing, sparse random projections and online updates further reduce its working memory. The relevant comparison fixes *both* a task accuracy and a sample/time budget: allowing unlimited extra samples can let a small-memory classical learner trade time for space. The paper's unconditional lower bounds apply to constructed random-sample tasks with those budgets [1, Theorems 1-4]. They do not prove that a classical model needs one floating-point number per feature on IMDb sentiment or single-cell RNA data. The authors' public repository includes classical feature-hashing, sparse JL and adaptive-sketch variants for empirical comparisons [2].

## Best quantum

Quantum oracle sketching builds approximate coherent queries incrementally from classical samples and combines them with quantum linear algebra and classical-shadow readout. For constructed linear-system and binary-classification tasks, the paper proves that a polylogarithmic-size quantum machine can succeed using roughly linear numbers of samples while a classical machine with sublinear memory cannot achieve the specified performance under the same sample budget [1, Theorems 1-4]. The result is information-theoretic, so it does not depend on a conjecture such as `BPP != BQP`. The hard-task construction is a theorem about those task distributions, not a lower bound for every data-analysis workload.

The real-dataset figure in [1, Fig. 2] compares machine size against classification accuracy or PCA variance on IMDb and PBMC data, among others. Its memory unit counts one logical qubit and one classical floating-point number as one unit; classical streaming is initially charged at least the feature dimension. The paper explicitly assumes enough samples and computation time to isolate *space*. Inspection of the pinned public code [2] shows that `imdb_svm.py` and `pbmc68k_svm.py` obtain the accuracy axis from scikit-learn's classical `RidgeClassifier` cross-validation. `sweep_utils.qos_machine_size` computes the quantum point's memory coordinate from sample count, feature count and sparsity. Thus the figure demonstrates classical task performance **paired with a proposed quantum-space formula**. It is not a same-data execution of the quantum algorithm or a measurement of its prediction errors, shots or runtime.

The paper gives fewer than 60 logical qubits for its selected real-data comparisons and claims four to six orders of magnitude in *machine size* against its specified baselines [1, Fig. 2]. It also states that data loading uses about `N` samples and that extrapolating to larger devices while ignoring exponential runtime overhead is only suggestive [1, Discussion]. The 60-qubit figure excludes the full input interface, error-correction hardware and wall-clock cost. An independent offline QOS implementation for DNA fingerprinting found that its compiled phase-oracle circuits were too deep for current hardware and stressed the need for online control and shorter-depth synthesis [3]. This offline variant does not test the original online theorem. The classical-space theorem remains valid under its model; the claimed practical magnitude requires a matched empirical benchmark.

## Verdict

Surviving as a **space-limited computational problem** with a genuine unconditional separation on constructed inputs. It corrects the blanket statement that all quantum learning from classical data has been dequantized. It is not yet a practical memory saving for sentiment or single-cell analysis: the real-data plot uses a classical performance proxy, its classical competitors depend on the chosen memory model, and no buyer target or full cost curve is supplied. The [open validation task](../questions/oracle-sketching-real-data-validation.html) specifies what to measure next.
