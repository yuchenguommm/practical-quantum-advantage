# Auditing the public OPI block-Gibbs trajectories

This is a reanalysis of the data released with Gil-Fuster et al., [*Approximate sampling from decoded quantum interferometry via Markov chain Monte Carlo methods*](https://arxiv.org/abs/2607.28120). It is not a new quantum calculation or a rerun of their sampler. The primary data and Apache-2.0 code are in [`matanninio/dqi-mcmc`](https://github.com/matanninio/dqi-mcmc), pinned here to commit [`4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b`](https://github.com/matanninio/dqi-mcmc/tree/4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b). This report uses `paper-data/opi/base_sample/gibbs3_p*_no_warmup.jsonl`; no source data are copied into this repository.

## What is compared

For each field prime `p`, the archive has 100 random allowed-set instances. It takes `m=p-1` evaluation points, `n=p//2` polynomial coefficients, allowed-set size `r=p//2`, and Gibbs block size 3. The output register contains `n ceil(log2 p)` qubits. This is an *output-register equivalent*, excluding workspace, a coherent input oracle and error correction.

For each recorded trajectory, we take the **first** step at which the satisfied-constraint count exceeds `floor(predicted_fraction × m)`. We then report the maximum of those 100 first-passage counts, reproducing the paper's finite-sample worst-instance statistic. This maximum is not a guarantee over all OPI inputs. The archive's `resume_state.tau_k` equals the *last* score improvement; for two `p=13` trajectories it occurs after the first target crossing. The script deliberately reads `trajectory` rather than treating `tau_k` as a first-passage time.

### Decoder-radius discrepancy in the pinned implementation

[The paper's OPI setup](https://arxiv.org/html/2607.28120v1) specifies `ell=floor(n/2)` correctable errors for the Reed–Solomon code of distance `d=n+1`. The pinned [implementation defaults to `ell=(n+1)//2`](https://github.com/matanninio/dqi-mcmc/blob/4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b/dqi_mcmc/api/maxlinsat/max_opi_problem.py#L248-L252). These agree for even `n`; for odd `n`, the code uses one more error than the guaranteed unique-decoding radius `floor((d−1)/2)=floor(n/2)`. The archived `predicted_fraction` values match the code default to numerical precision. Five of the ten archived sizes have odd `n`: `p=19, 23, 31, 43, 47`. For example, at `p=31, n=15`, the archived formula fraction is 0.93446 with `ell=8`; using the paper's `ell=7` gives 0.91413. The integer threshold `score > floor(fraction × m)` changes from `>28` to `>27` there.

This does **not** invalidate the archived classical trajectories. It limits their interpretation as a matched comparison against the stated worst-case DQI decoding guarantee. The Gibbs sampling weights themselves depend on `ell`, so lowering only the success threshold in an existing trajectory would not reproduce the paper-specified distribution. A matched finite-size rerun must set `ell` explicitly in both the weight construction and the target formula. The fitting result below describes the **archived code-default experiment**.

| `p` | coefficients `n` | output qubits | DQI expected fraction | first-passage median | maximum of 100 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 6 | 24 | 0.9125 | 12 | 119 |
| 17 | 8 | 40 | 0.9176 | 73 | 395 |
| 19 | 9 | 45 | 0.9356 | 91.5 | 675 |
| 23 | 11 | 55 | 0.9351 | 510 | 5,237 |
| 29 | 14 | 70 | 0.9241 | 1,075.5 | 9,347 |
| 31 | 15 | 75 | 0.9345 | 15,267 | 103,376 |
| 37 | 18 | 108 | 0.9261 | 28,208.5 | 201,589 |
| 41 | 20 | 120 | 0.9268 | 207,737 | 1,599,720 |
| 43 | 21 | 126 | 0.9340 | 455,797.5 | 2,780,290 |
| 47 | 23 | 138 | 0.9339 | 264,715.5 | 2,402,819 |

All 100 instances per listed size crossed their archived integer target. An ordinary least-squares fit to `log(maximum steps)` against output qubits across these ten sizes has base **1.09628** per output qubit and log-space `R²=0.9562`. Leaving out one size at a time changes the fitted base to **1.0940–1.1021**. These are descriptive fits over a changing prime, coefficient count and success threshold. The three published sizes within 50–100 output qubits are 55, 70 and 75; there is no measurement at 100. The archive lacks the `p=53`, 156-output-qubit trajectories mentioned as the largest size in the paper, so these calculations cannot independently check that final data point. The paper reports a base of 1.096 for its own fit.

The original DQI paper's headline comparison, [0.7179 quantum versus 0.55 Prange](https://arxiv.org/html/2408.08292v5), instead takes `n/p≈0.1` and `r/p≈0.5`. The archived MCMC runs take `n/p≈0.5`, with target fraction above 0.9 and the decoder-radius discrepancy above for odd `n`. They test the same *problem definition* at different rate parameters, not the headline 0.7179 instance family. Neither the archived step counts nor this fit establish a classical cost for matching DQI at rate 0.1. Step counts also omit the per-step work, input generation and any quantum implementation cost.

## Reproduce

```bash
git clone https://github.com/matanninio/dqi-mcmc.git /tmp/dqi-mcmc
git -C /tmp/dqi-mcmc checkout 4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b
python numerics/opi_mcmc_archive_audit.py /tmp/dqi-mcmc --output numerics/results/opi_mcmc_archive_audit.json
```

The [script](opi_mcmc_archive_audit.py) uses only the Python standard library. Its [machine-readable result](results/opi_mcmc_archive_audit.json) records every size and the limitations above. A useful next comparison would hold the **rate near 0.1**, allowed-set density, explicit instances and target fraction fixed for Prange, tuned block Gibbs, stronger classical algebraic solvers and DQI. It would count the quantum input oracle and success repetitions separately.
