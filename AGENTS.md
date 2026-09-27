# Instructions for contributors (humans and agents)

This repository is a catalogue of quantum-computing application candidates. Every page is a
Markdown file with YAML front matter under `content/`. The site at
https://yuchenguommm.github.io/practical-quantum-advantage/ is built from these files; there is
no other database. To change a verdict, change the file and open a pull request.
The [contributor guide](CONTRIBUTING.md) gives the routes for proposing pages and evidence,
the review criteria, and the commands for creating a draft. Agents can read the full catalogue
from `index.json` or `llms.txt` on the published site; write changes through issues or PRs.
The [review queue](https://yuchenguommm.github.io/practical-quantum-advantage/review-queue.json)
lists pages awaiting first review, disputed pages and pages older than 180 days.

## What a page is

Five page types live in five folders:

| folder | type | what it describes | example |
|---|---|---|---|
| `content/applications/` | application | a scenario that a company or lab would pay for | electrolyte design, OLED emitters, derivative pricing |
| `content/problems/` | problem | the computational task behind one or more applications | ground-state energy, PDE solving, Monte Carlo expectation |
| `content/methods/` | method | a quantum (or hybrid) algorithmic approach | phase estimation, SQD, DQI, embedding |
| `content/claims/` | claim | one published "quantum advantage" claim and whether it was refuted | IBM 127-qubit utility experiment |
| `content/questions/` | question | a concrete unanswered question someone could take on | does ideal SQD sampling beat classical selection? |

The distinction between application and problem is the point of the site. Industry says
"weather forecasting is an application"; algorithm papers say "PDE solving is an application".
Both layers are kept, and linked through `related.problems` / `related.applications`.

## Three dimensions and the verdict

Every application, problem and method carries a verdict and three graded dimensions.

Verdicts: `no-go` (a stated task and input/output model has a decisive obstruction), `uneconomic`
(the studied route does not beat the relevant classical baseline under stated cost assumptions),
`surviving` (no decisive obstruction, but the evidence does not yet support either a practical or
a strong algorithmic case), `promising` (the practical or foundational evidence meets the rule
below), `unassessed`. These labels do not by themselves assert an unconditional classical lower
bound. Keep the three dimension grades visible beside the verdict.

`dimensions.classical_hardness.level`: `reduction` (BQP- or QMA-hardness), `crypto`
(cryptographic assumption), `lower-bound` (low-degree, overlap-gap, or similar), `empirical`
(best known classical methods are slow), `none`, `unknown`.

`dimensions.quantum_easiness.level`: `proven` (polynomial-time algorithm with verified
preconditions), `conditional` (polynomial time if a stated precondition holds, e.g. overlap
≥ 1/poly, adiabatic gap ≥ 1/poly, decodable dual code), `heuristic`, `unknown`, `no`.

`dimensions.willingness_to_pay.level`: `first-hand` (a company or agency has documented its
interest directly, for example through a written target or co-authored study), `second-hand`
(a plausible argument in the literature), `none`, `unknown`. Co-authorship alone does not
establish a quantitative buyer requirement or a commitment to pay; state those separately.

There are two routes to `promising`, reflecting the site's two layers. An **application** needs a
named decision, a credible classical bottleneck on the same task, an end-to-end quantum route,
and first-hand evidence of a buyer's requirement. A **foundational computational problem** can
qualify without a buyer when it has a polynomial-time quantum algorithm with its preconditions
met, a credible classical-hardness argument or a standard cryptographic assumption, and an
independently important output. State the exact missing theorem: for factoring, quantum
polynomial time is proved while a superpolynomial classical lower bound is not. Methods inherit
neither route automatically; judge whether their required instance family has been established.
Do not treat `crypto`, `lower-bound` and `reduction` as an ordered scale or promote a page from
generic NP-hardness of a broader family.

## File format

```markdown
---
type: problem
id: ground-state-energy            # must equal the filename without .md
title: Ground-state energy of molecules and materials
title_zh: 分子与材料的基态能量
summary: One or two sentences in English, 20 to 600 characters. Shown in lists and search.
summary_zh: 可选的中文摘要。
status: seed                       # seed | reviewed | disputed
# Add last_verified only after checking the cited sources and claims.
verdict: surviving
dimensions:
  classical_hardness: {level: empirical, note: "DMRG and SHCI reach chemical accuracy up to ~100 orbitals"}
  quantum_easiness:   {level: conditional, note: "needs initial-state overlap ≥ 1/poly; not guaranteed for strongly correlated systems"}
  willingness_to_pay: {level: first-hand, note: "industrial co-authors studied OLED emitters; the reported 0.0501 eV is achieved cohort error, not a buyer target"}
resources: {logical_qubits: "140–200", gates: "1e9–1e10 T", note: "for CAS(70–100)"}
related:
  applications: [oled-emitters, homogeneous-catalysis]
  methods: [phase-estimation, sqd]
  claims: [ibm-sqd-2024]
  questions: [ideal-sqd-vs-classical-selection]
references:
  - {arxiv: "2208.02199", title: "Is there evidence for exponential quantum advantage in quantum chemistry?", authors: "S. Lee et al.", year: 2023}
---

## Best classical
...

## Best quantum
...

## Verdict
...
```

Required body sections (checked by CI):

- application: `## Who needs it`, `## Bottleneck`, `## Computational problems`, `## Verdict`
- problem: `## Best classical`, `## Best quantum`, `## Verdict`
- method: `## Preconditions`, `## Known limits`, `## Verdict`
- claim: `## Claim`, `## Refutation`
- question: `## Why it matters`, `## What would settle it`

You may add further sections. Keep pages under about 1,200 words. Write in English; a Chinese
`title_zh` and `summary_zh` are welcome.

## Rules for evidence

1. Every application, problem, method and claim page cites at least one reference. Prefer arXiv
   IDs; CI checks IDs and titles against the committed, previously verified arXiv title
   snapshot. New IDs are fetched from the arXiv API; commit the refreshed snapshot after
   adding a reference. A fabricated ID or wrong title fails the build.
2. Numbers (qubit counts, gate counts, runtimes, prices) must be traceable to a reference or to a
   script under `numerics/`. State the assumptions the number depends on. Do not cite private or
   unpublished notes; if a number is your own estimate, say so and show the arithmetic.
3. Figures from `numerics/` go in `numerics/figs/` and are embedded as `![caption](../figs/name.png)`;
   the build copies that folder to the site. Commit the script and the JSON results next to the figure.
4. `willingness_to_pay: first-hand` needs a citation to a document in which the industrial or
   agency participant speaks (a co-authored paper, a public RFP, a written accuracy target).
   Record whether it states an actual requirement or only interest. A survey's opinion is
   `second-hand`.
5. When you change a verdict, say in the PR description which dimension changed and what
   evidence changed it. Do not silently soften wording.
6. Refutations are as valuable as claims. If a classical simulation reproduces a claimed
   advantage, add it to the claim page and set `refuted: true`.
7. A literature refresh needs both supporting and contrary searches. Record the search date,
   exact claims checked, sources read and remaining uncertainty in the PR. Change
   `last_verified` only after that check; do not mark a page `reviewed` by adding a citation.

## Workflow

```
python tools/validate.py       # schema, required sections, cross-links
python tools/verify_refs.py --strict    # check titles against the verified snapshot
python tools/verify_refs.py --strict --refresh    # recheck all IDs online and update the snapshot
python tools/build.py          # writes ./site
```

Dependencies: `pip install -r requirements.txt` (PyYAML, jsonschema, markdown, jinja2, requests).

Branch from `main`, one topic per pull request. Agent-authored PRs are welcome; label them
`agent` and list the sources consulted. A maintainer merges after checking the evidence, not the
prose.

For a research task, start with one page ID from `review-queue.json` or one question ID from
`index.json`. Search the latest primary literature, compare the best classical and quantum
methods on the same instance and accuracy, and say explicitly when the evidence does not
settle the verdict. Run `validate.py`, `verify_refs.py --strict`, `build.py`, and
`check_site.py` before opening a PR. The agent should never publish a new scientific result
solely as a catalogue edit; release a citable preprint, paper or reproducible public report
first, then link it from the page.

To create a draft for any of the five types, run
`python tools/new_entry.py problem my-problem --title "My problem"`. Replace all placeholders,
add references where required, and check the schema before opening a PR. A `seed` page has not
completed source review. Mark a page `reviewed` only after the PR records a source and claim
check; use `disputed` for a documented live challenge to its conclusion.

## Skills for Claude Code users

`.claude/skills/` contains four skills you can invoke from a Claude Code session opened in this
repo:

- `/survey <topic>` — research a candidate and write or update its page.
- `/challenge <claim-id>` — search for classical reproductions of an advantage claim.
- `/score <page-id>` — fill in or contest the three dimensions with cited evidence.
- `/verify-refs` — run the reference checker and fix mismatches.

## Things not to do

- Do not add an application, problem or method page without a verdict and at least one reference.
- Do not add a claim page without a reference. Questions may be submitted before a reference is found.
- Do not add marketing language ("revolutionary", "game-changing"). State what was measured.
- Do not copy abstracts verbatim; paraphrase and cite.
- Do not delete a refuted claim. Refuted claims are the most useful part of the record.
