# Complete case: a public vehicle-option pricing ILP

This is a **same-input negative case**. It checks the public nine-variable illustrative pricing model distributed with [Sabater et al.'s DQI study](https://arxiv.org/abs/2509.08328), using the authors' [pinned input and encoder](https://github.com/BCG-X-Official/dqi/tree/8456eaddb0033fa703c169c19ff264b51ccd0711). The model is synthetic. It is not a production pricing problem or buyer acceptance test. The original weights and constraint, a direct quantum alternative, the authors' DQI encoding, exact classical answer and reproduction commands are all explicit below.

## Shared input and output contract

The [public instance](instance.json) asks for binary choices `x_0,...,x_8` maximizing

`261x0 + 286x1 + 312x2 + 218x3 + 251x4 + 275x5 + 247x6 + 376x7 + 298x8`

subject to `sum(x_i) <= 5`. Our fixed decision target is to return a **feasible** assignment with objective at least **1500**, with success probability at least 0.95. The exact optimum, 1547, is reported separately. An original pricing-unit or monetary value for this objective is not specified by the input. The choice of 1500 is ours, for a reproducible near-optimal target; it is not a buyer requirement or the threshold used in the paper's DQI conversion.

## Same-instance result

| Check | Result | Interpretation |
| --- | ---: | --- |
| Original decision variables | 9 | 512 possible assignments; 382 satisfy the capacity constraint |
| Exact classical optimum | 1547 | Choose indices 1, 2, 5, 7, 8 (zero-based) |
| Classical certificate | Sort the nine positive weights and take the largest five | `O(n log n)` time; exact for this one-cardinality-constraint family |
| Target-qualifying assignments | 9 / 512 | A uniform random assignment hits the target with probability 0.01758 |
| Ideal Grover search | 5 oracle calls; target success 0.98836 | Exact ideal two-amplitude formula, not a hardware or full-circuit sampling result |
| Our clean arithmetic phase oracle | 45 qubits; 13,439 CX; depth 25,095 | Qiskit Terra 0.23.3, unoptimized `u1/u2/u3/cx` decomposition; one oracle, not a fault-tolerant runtime |
| Full five-iteration Grover circuit | 45 qubits; 71,015 CX; depth 128,686 | Includes initialization and five diffusion operators in the same unoptimized gate basis; compiled, not executed |
| Authors' DQI encoding of this input | 827 XOR rows × 345 variables; reported generator-row minimum weight 3, `ell=1` | The encoded route exceeds 100 system qubits before decoder workspace |

The 45-qubit oracle computes the weighted sum and cardinality from the **nine input bits**, compares against 1500 and five, applies a phase on joint success, and uncomputes all workspace. Its arithmetic is not synthesized from a table of winning bit strings. The source code constructs the circuit; 32-shot matrix-product-state interference checks verify four contrasting input pairs, including a score exactly at threshold and a choice that violates the capacity constraint. The full five-iteration Grover circuit was **compiled but not run or fault-tolerantly compiled**. Its 0.98836 success value assumes ideal gates and follows from the exact Grover formula. The gate counts are not physical runtimes.

The paper's DQI route uses a different **shifted** objective `c_i = original_i - 217` and chooses `beta=285`, making its encoded objective comparison `sum(c_i x_i) >= 286`. That threshold is not our original-objective target of 1500. The paper's DQI performance plots also use downsampled matrices rather than this full encoded input, and its quantum circuit simulations use smaller random instances. This case reproduces the full encoding size and code statistic; it does **not** claim to measure DQI's output quality on the 827×345 matrix.

## Verdict and scope

The original instance is classically easy in a structural sense: sorting proves the optimum for **every** nonnegative-weight, single-cardinality-constraint input of this form. An improvement in oracle-query count over uniform random sampling has no useful crossover against this algorithm. The ideal Grover circuit serves as a fully specified under-100-qubit **alternative algorithm for the same original decision problem**, not as a reconstruction of the paper's DQI implementation. Neither circuit access nor BMW/BCG authorship supplies a buyer-defined accuracy or price threshold. This result settles this public illustrative instance only; it does not rule out advantage on richer automotive pricing ILPs.

## Reproduce

From the repository root, with Python, NumPy, SciPy, SymPy, Matplotlib, Qiskit Terra 0.23.3 and Qiskit Aer 0.11.2:

```sh
git clone https://github.com/BCG-X-Official/dqi.git .case-upstream-dqi
git -C .case-upstream-dqi checkout 8456eaddb0033fa703c169c19ff264b51ccd0711
python numerics/cases/automotive_pricing/run.py --compile --check-circuit --upstream .case-upstream-dqi --output numerics/cases/automotive_pricing/result.json
```

The resulting [machine-readable audit](result.json) records the local input hash, upstream input hash and commit, exact assignment, oracle gate counts, four circuit checks and encoding statistics. The small exact classical audit needs only the standard Python library:

```sh
python numerics/cases/automotive_pricing/run.py
```

The upstream code is imported only when `--upstream` is supplied; the case does not copy its implementation. Qiskit's basis gate count is compiler-version dependent. The exact optimum and sorted certificate are not.

## Source and arithmetic cross-check

The standard-library [checker](verify_public_input.py) downloads the ILP file from the authors' pinned Git commit, compares its three input fields with [our instance](instance.json), and independently enumerates all 512 assignments. It checks the sorting certificate, target count and ideal Grover probability against [the recorded result](result.json). Its [machine-readable receipt](verification.json) records the checks and their limits:

```sh
python numerics/cases/automotive_pricing/verify_public_input.py --output numerics/cases/automotive_pricing/verification.json
```

The source SHA-256 is `4c9578c6abec2a0fecb34da58eefa22af590a33542e8643f10e9da2384c12db4` for the **Git blob's LF bytes**. An earlier result recorded `bc1500e94eb4182935600894f620c338de24b9c95bcfef7577ab23f3a76690d5`, the hash of the same file after a Windows checkout converted its newlines to CRLF. `run.py` now hashes the canonical Git blob, and normalizes the local input's newlines before hashing. No objective, constraint or numerical result changed. The checker is a second implementation by this project, not an independent peer review; it does not verify the DQI encoder, compiled circuit or hardware performance.
