---
type: question
id: cfd-drag-same-instance-crossover
title: Can a quantum lattice-Boltzmann solver estimate cylinder drag faster at matched error?
title_zh: 同一圆柱绕流实例中，量子格子玻尔兹曼方法能否更快算出阻力？
summary: A published quantum lattice-Boltzmann algorithm includes a boundary-drag measurement cost, but its numerical Carleman-error tests use periodic flows without obstacles. The public DFG cylinder benchmarks supply a geometry, boundary conditions and drag references. Matching the drag error and total cost of classical and quantum routes on one of those cases remains open.
summary_zh: 已发表的量子格子玻尔兹曼算法计入了边界阻力的读出成本，但其 Carleman 误差测试采用无障碍物的周期流。公开的 DFG 圆柱绕流基准给出了几何、边界条件和阻力参考值。量子与经典方法尚未在同一实例、同一阻力误差下完成总成本比较。
status: seed
last_verified: 2026-09-27
question:
  what_would_settle_it: "Use the public DFG 2D-1 cylinder (Re=20) as a correctness gate and DFG 2D-2 (Re=100) as the unsteady test. Fix geometry, inflow/outflow, no-slip walls, viscosity, initialisation, drag-coefficient convention and target error. Compare validated classical FEM, optimised D2Q9 lattice Boltzmann and, whenever accurate enough, a classical solver for the same low-order Carleman approximation. Implement the published shifted lattice-Boltzmann Carleman truncations on those exact boundary conditions; report drag error versus truncation order, mesh and time step, separating LBM model error from Carleman error. Only after drag accuracy is established should a quantum resource estimate count input and wall-state preparation, condition number, block encoding, all solver repetitions, drag readout and error correction on the same instance. Publish inputs, code, raw outputs and a matched classical-versus-quantum cost curve. State a decision-maker's required tolerance and latency separately."
  difficulty: phd
  resolved: false
related:
  applications: [turbulence-cfd]
  problems: [pde-solving, sparse-linear-systems]
  questions: [first-hand-payment-evidence]
references:
  - {arxiv: "2512.03758", doi: "10.1103/xysy-q3fp", title: "An end-to-end quantum algorithm for nonlinear fluid dynamics with bounded quantum advantage", authors: "D. Jennings, K. Korzekwa, M. Lostaglio, R. Ashworth, E. Marsili, S. Rolston", year: 2026, note: "PRX Quantum 7, 033060; Secs. VI D, VII A and VIII, and Data Availability"}
  - {url: "https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/flow/dfg_benchmark1_re20.html", title: "DFG flow around cylinder benchmark 2D-1, laminar case (Re=20)", authors: "FeatFlow, TU Dortmund", note: "Public geometry, conditions and stationary drag reference"}
  - {url: "https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/flow/dfg_benchmark2_re100.html", title: "DFG flow around cylinder benchmark 2D-2, time-periodic case (Re=100)", authors: "FeatFlow, TU Dortmund", note: "Public unsteady drag curves, mesh and time-step data; use updated reference archive"}
---

## Why it matters

Aircraft design uses drag as an engineering output. Airbus Operations Ltd coauthored the published quantum fluid-algorithm study [1], which establishes direct industrial research interest. It does not publish a required drag tolerance, turnaround time or procurement target. A scalar force avoids the cost of reading an entire flow field, but it still requires accurate boundary dynamics and enough measurements to resolve the force.

## What is known

| Evidence | What it establishes | What it leaves open |
|---|---|---|
| Published quantum algorithm [1, Sec. VI D] | An incompressible shifted lattice-Boltzmann construction and a boundary-drag observable; its readout adds a factor O(Re^{3/8}) at the paper's resolution choice | Drag accuracy on a specified obstacle and the total cost at a specified error |
| Numerical convergence study [1, Sec. VII A] | For periodic D1Q3 and D2Q9 flows **without walls**, Carleman truncation improves below a model-dependent Reynolds threshold and can worsen above it | Transfer of that threshold and error to cylinder drag |
| Scaling analysis [1, Sec. VIII] | With numerical condition-number exponents, 2D drag retains favourable Re scaling only for truncation order NC=1, by a factor Re^{0.287}; a higher order can remove the gain | Whether NC=1 meets a useful drag tolerance, and whether asymptotic gains beat constants |
| Classical comparison [1, Sec. VIII] | Counts updates of the full classical LBE state and compares their scaling with quantum queries and drag readout | A measured classical solver for the same low-order approximation if NC=1 already meets the target |
| DFG reference cases [2, 3] | Public cylinder geometry, boundary conditions and drag outputs at Re=20 and Re=100 | Quantum data, code and a matched resource comparison |

The published paper states that no research data or software supporting it are publicly available [1, Data Availability]. Its drag extraction is derived for a wall, while the reported numerical convergence tests assume periodic boundaries and no wall [1, Sec. VII A]. Treating the drag formula and the convergence plots as an already validated single instance would combine different experiments.

### Proposed public instance

Start with DFG 2D-1 [2]: a `2.2 × 0.41` channel with a cylinder of radius `0.05` centred at `(0.2, 0.2)`, density `1`, viscosity `0.001`, no-slip top/bottom/cylinder, parabolic inflow with maximum velocity `0.3`, and the benchmark's do-nothing outflow. Its mean inflow is `0.2`, giving Re=20. The stationary drag coefficient reference is `5.57953523384` under the DFG convention [2]. This is a correctness check at low Re, not a commercially hard flow.

Move to DFG 2D-2 [3] with the same geometry and viscosity, inflow maximum `1.5` and Re=100. Measure drag over one developed shedding cycle after the documented spin-up. The official page provides drag curves and updated higher-quality reference data; specify the exact archive and mesh/time-step refinement used. The cases are public **Navier–Stokes benchmarks**, while the quantum proposal uses D2Q9 lattice Boltzmann. Validate the lattice-Boltzmann modelling and boundary error against DFG before comparing algorithmic costs.

## What would settle it

The front-matter checklist defines the comparison. Report errors in the **drag coefficient**, including discretisation, boundary treatment, Carleman truncation and quantum readout. A low error in the bulk velocity field alone would not establish a low drag error. Publish the fixed input, classical solver versions and timing hardware. For each truncation order, report whether increasing order actually improves drag at both Reynolds numbers. A condition-number fit obtained on a periodic flow cannot be inserted into the cylinder cost calculation without checking it on the cylinder operator.

The first decisive result can be negative: if no truncation order with favourable cost scaling reaches the chosen drag tolerance, this route fails the benchmark even before fault-tolerant gate costs matter. If NC=1 is accurate enough, a classical solver for that same linearised approximation joins the baseline; comparing quantum NC=1 only with a full nonlinear classical evolution would leave an avoidable gap. If accuracy and condition-number scaling survive, compile the whole quantum path and compare it with the best classical route on the same drag error. Re=20 and Re=100 alone do not establish scaling; a further Reynolds sweep would need a consistently defined family of geometries, grids and target errors.
