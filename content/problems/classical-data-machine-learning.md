---
type: problem
id: classical-data-machine-learning
title: Machine learning on classical data (kernels, QNNs, low-rank linear algebra)
title_zh: 经典数据上的机器学习（核方法、量子神经网络、低秩线性代数）
summary: Low-rank linear algebra with sample-and-query access and broad kernel-model families have classical counterparts, so their earlier exponential time claims do not survive matched access assumptions. This verdict concerns those tasks. A separate 2026 result proves an unconditional space separation for constructed classical-data streams; its real-dataset performance comparison remains an empirical open question.
summary_zh: 在相同数据访问条件下，低秩线性代数及多类量子核模型已有经典算法，早期的指数级时间优势主张站不住脚。本页的判断只针对这些任务。另一项 2026 年结果对构造的经典数据流任务证明了无条件空间分离，其真实数据性能仍需独立检验。
status: seed
last_verified: 2026-09-27
verdict: no-go
dimensions:
  classical_hardness: {level: none, note: "low-rank linear algebra with sample access is classically polynomial and broad kernel/QSVM/QNN predictions have random-feature dequantizations; this grade excludes the separate streaming-space model"}
  quantum_easiness: {level: no, note: "for the specified low-rank and kernel time-advantage routes, input loading and classical counterparts remove the claimed exponential gain; the separate streaming-space algorithm has a proved ideal-memory advantage"}
  willingness_to_pay: {level: none, note: "ML buyers are abundant but none has stated a task that classical ML fails and quantum ML meets"}
related:
  problems: [learning-from-quantum-experiments, sparse-linear-systems, sorting-fft-storage, streaming-classical-data-memory]
  methods: [hhl-qsvt, qram, vqe]
references:
  - {arxiv: "1910.06151", title: "Sampling-based sublinear low-rank matrix arithmetic framework for dequantizing quantum machine learning", authors: "N.-H. Chia, A. Gilyén, T. Li, H.-H. Lin, E. Tang, C. Wang", year: 2020, note: "STOC 2020"}
  - {arxiv: "2505.15902", title: "On dequantization of supervised quantum machine learning via random Fourier features", authors: "M. Sahebi, A. Barthe, Y. Suzuki, Z. Holmes, M. Grossi", year: 2025}
  - {arxiv: "2010.02174", title: "A rigorous and robust quantum speed-up in supervised machine learning", authors: "Y. Liu, S. Arunachalam, K. Temme", year: 2021, note: "Nature Physics 17, 1013; discrete-log-based dataset"}
  - {arxiv: "2604.07639", title: "Exponential quantum advantage in processing massive classical data", authors: "H. Zhao, A. Zlokapa, H. Neven, R. Babbush, J. Preskill, J. R. McClean, H.-Y. Huang", year: 2026}
  - {arxiv: "2510.19928", title: "Mind the gaps: the fraught road to quantum advantage", authors: "J. Eisert, J. Preskill", year: 2025}
  - {arxiv: "2305.10310", title: "QRAM: A Survey and Critique", authors: "S. Jaques, A. G. Rattew", year: 2025, note: "Quantum 9, 1922"}
---

## Best classical

For the linear-algebra family (recommendation systems, principal component analysis, support-vector machines, low-rank regression), Tang's 2018 recommendation-system algorithm and the general framework of Chia, Gilyén, Li, Lin, Tang and Wang show that whenever the quantum algorithm assumes low rank and sample-and-query access to the data, a classical algorithm with the same access runs in time polynomial in rank and precision and independent of dimension [1]. That removed the exponential claims of HHL-based QML. What remains of HHL survives only for sparse, well-conditioned matrices with compactly preparable inputs and scalar outputs, which are not typical data-science conditions.

For kernel and variational models, Sahebi et al. show that predictions of quantum kernel machines, QSVMs and many quantum neural networks are reproduced by classical random-Fourier-feature models with polynomial resources [2]; a growing body of work makes the pairing precise: the parameter regimes in which variational circuits are trainable (no barren plateau) are the regimes in which they are classically simulable. Eisert and Preskill's 2025 assessment describes the surviving QML advantages as "cherry-picked examples" [5].

## Best quantum

- The input bottleneck is fundamental. Loading N classical numbers into amplitudes costs Ω(N) without a QRAM, and Jaques and Rattew's survey argues that a fault-tolerant, actively error-corrected QRAM has an opportunity cost comparable to just doing the classical computation, while a cheap passive QRAM is "unlikely" [6].
- A conditional time separation exists on constructed data. Liu, Arunachalam and Temme build a classification task from discrete logarithm on which a quantum kernel classifier succeeds under a classical hardness assumption [3]. The claim that this is the *only* provable separation for classical-data learning is too broad.
- A different, unconditional separation counts **space under a sample budget**. Zhao and colleagues prove classical memory lower bounds for constructed streaming linear-system and classification tasks while their quantum oracle-sketching algorithm uses polylogarithmic ideal logical memory [4]. Their real-dataset plots pair classical ridge/PCA accuracy with a formula-derived quantum memory count; the public code does not execute the quantum learner on those datasets. See the [separate streaming-space problem](../problems/streaming-classical-data-memory.html). The result does not reinstate an exponential *time* advantage for the low-rank and kernel routes on this page.

## What survives

Almost nothing on the "learn from classical data faster" axis for the low-rank and kernel proposals considered here. Two distinct tasks survive: learning from quantum data with quantum memory, and [classical-data streams under a memory limit](../problems/streaming-classical-data-memory.html). The latter has an unconditional space theorem [4].

## Verdict

No-go **for the specified exponential time-advantage claims in low-rank linear algebra and broad kernel models** under matched data access. This is not a verdict on all learning from classical data. The [streaming-space entry](../problems/streaming-classical-data-memory.html) keeps the unconditional result [4] visible with its different memory/sample model and open real-data test.
