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

The [code](opi_low_rate_probe.py) records the best polynomial's coefficient vector, score, first hit or censoring, and elapsed local wall time. The separate [witness checker](opi_low_rate_verify.py) re-evaluates each polynomial by modular Horner's rule. Candidate counts are useful to compare these two implementations under a fixed cap, while wall times and quantum circuit costs remain incomparable.

| `p` | `n` | output qubits | formula fraction | integer target | random hits / 20 | Prange + coordinate hits / 20 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 31 | 3 | 15 | 0.6644 | 20 / 30 | 20 | 20 |
| 43 | 4 | 24 | 0.7024 | 30 / 42 | 20 | 20 |
| 61 | 6 | 36 | 0.7105 | 43 / 60 | 20 | 20 |
| 89 | 9 | 63 | 0.7032 | 62 / 88 | 20 | 19 |
| 97 | 10 | 70 | 0.7176 | 69 / 96 | 12 | 7 |
| 101 | 10 | 70 | 0.7135 | 72 / 100 | 11 | 5 |
| 109 | 11 | 77 | 0.7060 | 77 / 108 | 3 | 2 |
| 113 | 11 | 77 | 0.7025 | 79 / 112 | 11 | 6 |
| 127 | 13 | 91 | 0.7094 | 90 / 126 | 0 | 2 |

The nonmonotonic hit counts are a useful warning. Two field sizes with the same output-register qubit count can have different integer targets and different finite-sample outcomes. At 91 output-register qubits, a 100,000-evaluation failure is a **right-censored run**, not evidence that an instance is classically hard in any complexity-theoretic sense. No scaling exponent or crossover is fitted to these nine sizes. The quantum circuit would also need workspace, a coherent input oracle and fault-tolerant gates beyond this output register.

Neither method is the strongest available classical OPI solver. In particular, this is not a low-rate run of the published block-Gibbs sampler, a tuned annealer, or an algebraic list-recovery method. The Prange-seeded coordinate heuristic often does worse than uniform sampling under this scoring cap; that says something about this local heuristic, not about Prange's asymptotic approximation guarantee. An informative next experiment would run those stronger methods on these same allowed-set masks, compare *distributions* of score as well as first passage, and then account for coherent input access and repetitions in DQI.

## Reproduce and verify

With Python and NumPy installed:

```bash
python numerics/opi_low_rate_probe.py --primes 31 43 61 89 97 101 109 113 127 --instances 20 --budget 100000 --seed 123 --output numerics/results/opi_low_rate_seed123.json
python numerics/opi_low_rate_verify.py numerics/results/opi_low_rate_seed123.json
```

The committed run used Python 3.9.12 and NumPy 1.24.4. The result file contains 180 instance records and 360 best-polynomial witnesses, including failures to reach the target. Re-running with a different NumPy release should check the allowed-mask SHA-256 fields before comparing trajectories.
