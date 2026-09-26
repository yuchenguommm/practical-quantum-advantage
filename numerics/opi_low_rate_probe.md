# A low-rate OPI baseline at 15–91 output-register qubits

The [original DQI paper](https://arxiv.org/html/2408.08292v5) highlights OPI with roughly one polynomial coefficient per ten field elements and allowed-set density near one half. It compares asymptotic DQI satisfaction 0.7179 with the Prange polynomial-time baseline 0.55. The [published block-Gibbs experiments](https://arxiv.org/html/2607.28120v1) instead use roughly one coefficient per two field elements. This note checks **elementary classical baselines at the low rate** before attempting an expensive same-instance quantum comparison. It is an original numerical probe, not a reproduction of the block-Gibbs experiment or a claim of quantum advantage.

## Fixed contract

For each prime `p`, take all `m=p−1` nonzero field elements as evaluation points, `n=round(m/10)` coefficients, and `r=floor(p/2)` allowed values per point. Each allowed set is sampled without replacement with NumPy's `default_rng(123)`, in the same row order as the [public `dqi-mcmc` generator](https://github.com/matanninio/dqi-mcmc/blob/4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b/scripts/generate_opi_rhs.py). The first, second and twentieth `p=31` sets were checked against that repository's archived `.npy` data. Our [result file](results/opi_low_rate_seed123.json) also fixes the SHA-256 of every allowed-value mask. There are 20 instances per prime, indices 0–19.

The comparison target is the integer ceiling of the original paper's formula with `ell=floor(n/2)` decodable errors:

`target = ceil(m × (sqrt((ell/m)(1−r/p)) + sqrt((r/p)(1−ell/m)))²)`.

This formula describes an **asymptotic expected DQI score**. At the finite sizes below it is a target convention, not an independently simulated finite-size DQI expectation. Requiring one output to score at least its expectation is also different from comparing two algorithms' average output quality. We deliberately retain the target's exact integer value in each result.

Each classical method receives at most 100,000 scored candidate polynomials per instance:

1. **Uniform random coefficients:** sample polynomials independently in batches of at most 512. The reported `first_hit_evaluations` counts the whole batch actually scored before inspecting it; `first_hit_position` additionally records the first successful member's place in the sequential stream.
2. **Prange-seeded coordinate ascent:** choose `n` evaluation points and allowed values, interpolate a polynomial satisfying those `n` constraints, then visit each coefficient and score all `p` substitutions, taking an improving value. Restart at a new interpolation when a sweep stops improving. Candidate scoring counts include the interpolated start and all `p` substitutions per coordinate update. Modular interpolation and instance generation add work beyond this count.
3. **Single-coordinate Gibbs:** run the [authors' `dqi-mcmc` implementation](https://github.com/matanninio/dqi-mcmc/tree/4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b) on the same masks, one chain from a random start, no burn-in, permutation sweeps, block size 1. We explicitly pass `ell=n//2`, the unique-decoding radius stated in the paper. Each update scores all `p` coefficient substitutions, so the cap permits `floor((100000−1)/p)` updates after the initial score. The [wrapper](opi_low_rate_block_gibbs.py) and [result](results/opi_low_rate_gibbs_seed123.json) pin this variant. It differs from the paper's block-size-three, high-rate experiment; it is a local Gibbs chain using the DQI-inspired weight, with no certified mixing time.

The [baseline code](opi_low_rate_probe.py) and Gibbs wrapper record the best polynomial's coefficient vector, score, first hit or censoring, and elapsed local wall time. The separate [witness checker](opi_low_rate_verify.py) re-evaluates each polynomial by modular Horner's rule. Candidate counts are useful to compare these implementations under a fixed cap. Gibbs weight precomputation, random-instance generation and Prange interpolation add uncounted work; wall times and quantum circuit costs remain incomparable.

| `p` | `n` | output qubits | formula fraction | integer target | random hits / 20 | Prange + coordinate hits / 20 | Gibbs hits / 20 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 31 | 3 | 15 | 0.6644 | 20 / 30 | 20 | 20 | 20 |
| 43 | 4 | 24 | 0.7024 | 30 / 42 | 20 | 20 | 20 |
| 61 | 6 | 36 | 0.7105 | 43 / 60 | 20 | 20 | 20 |
| 89 | 9 | 63 | 0.7032 | 62 / 88 | 20 | 19 | 11 |
| 97 | 10 | 70 | 0.7176 | 69 / 96 | 12 | 7 | 4 |
| 101 | 10 | 70 | 0.7135 | 72 / 100 | 11 | 5 | 1 |
| 109 | 11 | 77 | 0.7060 | 77 / 108 | 3 | 2 | 0 |
| 113 | 11 | 77 | 0.7025 | 79 / 112 | 11 | 6 | 1 |
| 127 | 13 | 91 | 0.7094 | 90 / 126 | 0 | 2 | 0 |

The nonmonotonic hit counts are a useful warning. Two field sizes with the same output-register qubit count can have different integer targets and different finite-sample outcomes. At 91 output-register qubits, a 100,000-evaluation failure is a **right-censored run**, not evidence that an instance is classically hard in any complexity-theoretic sense. No scaling exponent or crossover is fitted to these nine sizes. The quantum circuit would also need workspace, a coherent input oracle and fault-tolerant gates beyond this output register.

None of these three variants establishes the strongest available classical OPI cost. Prange-seeded coordinate ascent and single-coordinate Gibbs often do worse than uniform sampling under this cap. That diagnoses these local variants on these finite random instances; it neither contests Prange's asymptotic approximation guarantee nor the potential of larger Gibbs blocks, restarts, annealing or algebraic list recovery. An informative next experiment would tune and test those methods on these same allowed-set masks, compare *distributions* of score as well as first passage, and then account for coherent input access and repetitions in DQI.

## Reproduce and verify

With Python and NumPy installed:

```bash
python numerics/opi_low_rate_probe.py --primes 31 43 61 89 97 101 109 113 127 --instances 20 --budget 100000 --seed 123 --output numerics/results/opi_low_rate_seed123.json
git clone https://github.com/matanninio/dqi-mcmc.git /tmp/dqi-mcmc
git -C /tmp/dqi-mcmc checkout 4b964e9c3f716ed73c7f99c30a9d37cb9ae50d6b
python -m pip install -e /tmp/dqi-mcmc
python numerics/opi_low_rate_block_gibbs.py numerics/results/opi_low_rate_seed123.json --instances 20 --budget 100000 --seed 123 --output numerics/results/opi_low_rate_gibbs_seed123.json
python numerics/opi_low_rate_verify.py numerics/results/opi_low_rate_seed123.json --gibbs numerics/results/opi_low_rate_gibbs_seed123.json
```

The original two-method run used Python 3.9.12 and NumPy 1.24.4. The Gibbs run used Python 3.11.16, NumPy 2.4.6 and `dqi-mcmc` 0.1.1.dev1+g4b964e9c3. The result files contain 180 instance records per method and 540 best-polynomial witnesses in total, including failures to reach the target. Re-running with a different NumPy release should check the allowed-mask SHA-256 fields before comparing trajectories.
