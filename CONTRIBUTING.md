# Contribute to Practical Quantum Advantage

You can suggest a change without writing code. Community changes go through a GitHub pull request; proposals and corrections are welcome before a full page is ready.

The [review queue](https://yuchenguommm.github.io/practical-quantum-advantage/review-queue.html) lists seed, disputed and stale pages. Its [JSON export](https://yuchenguommm.github.io/practical-quantum-advantage/review-queue.json) is a task list for agents. A monthly workflow updates one [catalogue review issue](https://github.com/yuchenguommm/practical-quantum-advantage/issues) so older conclusions remain visible to contributors.
It also rebuilds the site so the age-based queue stays current. GitHub can disable scheduled workflows on public repositories after 60 days without activity; maintainers can run the workflow manually from Actions or re-enable it when that happens.

## Choose a route

| You have | Use |
|---|---|
| A new application, computational problem or method | [Propose a candidate](https://github.com/yuchenguommm/practical-quantum-advantage/issues/new?template=new-candidate.md) |
| A new published advantage claim or classical reproduction | [Report a claim](https://github.com/yuchenguommm/practical-quantum-advantage/issues/new?template=claim-refuted.md) |
| A paper, correction, benchmark or changed conclusion for an existing page | [Submit evidence](https://github.com/yuchenguommm/practical-quantum-advantage/issues/new?template=evidence-update.md) |
| A documented accuracy or speed target from a buyer | [Submit buyer evidence](https://github.com/yuchenguommm/practical-quantum-advantage/issues/new?template=payment-evidence.md) |
| A concrete question with a measurable resolution | [Propose a research question](https://github.com/yuchenguommm/practical-quantum-advantage/issues/new?template=research-question.md) |
| A plan or result for an existing open question | [Take it on or report progress](https://github.com/yuchenguommm/practical-quantum-advantage/issues/new?template=research-progress.md) |
| A correction you can make yourself | Use **Edit this page** on the entry, then open a pull request |

GitHub currently requires an account for these routes. Issues are proposals, not published catalogue entries. They receive a public discussion; a maintainer checks the sources and merges a page change before it appears on the website. If you have a substantial new scientific result, first publish a citable preprint or paper and then link it in an issue or pull request.

## Add a page by pull request

1. Search the [catalogue](https://yuchenguommm.github.io/practical-quantum-advantage/) and [open issues](https://github.com/yuchenguommm/practical-quantum-advantage/issues) to avoid duplicates. Choose one of the five types in [AGENTS.md](AGENTS.md): application, problem, method, claim or question. A scenario with a decision maker is an **application**; an algorithmic task shared by scenarios is a **problem**.
2. Fork the repository, create a branch, and run `python tools/new_entry.py application example-id --title "Example title"` from the repository root. Replace the type and ID as needed. The ID becomes the permanent URL slug, so choose it carefully. The script refuses to overwrite an existing page.
3. Replace all placeholder text. Add public references in the YAML front matter. For an application, problem or method, grade each of the three dimensions and explain the verdict. Link existing entries in `related:` by ID. A new cross-link can be added once both new files are in the same pull request.
4. Run the checks below. The generated draft intentionally has no fabricated references or `last_verified` date and contains placeholder text; it will fail validation until the placeholders are replaced and a source is added for an application, problem, method or claim. Set `last_verified` only after checking the sources; a `seed` page may leave it absent.
5. Open one focused pull request. Use the PR template to state exactly which claims, grades or verdicts change and why. An agent-authored PR should say which sources it consulted and which it rejected. A maintainer reviews the evidence before merging.

```sh
python -m pip install -r requirements.txt
python tools/validate.py
python tools/verify_refs.py --strict
python tools/build.py
python tools/check_site.py
```

The reference check uses `data/arxiv_titles.json`, a committed snapshot of titles already
checked against arXiv. A new arXiv ID triggers an online lookup; commit the updated snapshot
with your PR. Run `python tools/verify_refs.py --strict --refresh` to recheck every ID online.
If arXiv is unavailable, leave the new reference unverified and retry rather than inventing a
title. The offline snapshot keeps unrelated PRs independent of arXiv API availability.

**Review standard.** arXiv title matching checks that a cited identifier exists; it does not show that the paper supports a sentence. Reviewers check the cited passage, the numerical assumptions, the best classical comparison and the quantum algorithm's preconditions. The `seed` status means these checks are not complete. Use `reviewed` only after a maintainer has recorded the source and claim checks in the pull request. Use `disputed` when a published conclusion has a documented live challenge. Updating an older page should update `last_verified` to the date of the new source check.

For a review PR, give the entry ID, the date searched, the sources checked, the exact claims checked, and any remaining uncertainty. The reviewer should check both confirming and contrary papers. A fresh date or an added citation by itself does not make a page `reviewed`; a scheduled reminder does not change a verdict automatically. Keep disputed and refuted pages in the catalogue with their history.

**Credit and rights.** Contributors retain copyright in their original writing and contribute it under CC BY 4.0; code is MIT licensed. Cite and paraphrase third-party work, and include scripts plus results for new figures. See [LICENSE](LICENSE). Do not add private notes or personal contact details to public entries.

## Use an agent

Give an agent the repository and [AGENTS.md](AGENTS.md), then ask for a specific page or evidence task. For example: “Investigate whether classical impurity solvers change the verdict on `rare-earth-permanent-magnets`; cite primary sources, update the relevant page and open a PR with the evidence.” The complete public catalogue is available as [index.json](https://yuchenguommm.github.io/practical-quantum-advantage/index.json) and a compact [llms.txt](https://yuchenguommm.github.io/practical-quantum-advantage/llms.txt). These are read-only; agents submit changes through the same issue and PR process as people.

An agent can start from a queue ID or open question, gather primary sources, propose a focused edit, run the checks and open a PR. The PR must identify agent assistance, sources it rejected, and what remains uncertain. Human review is required before publication; no agent can change the live catalogue through the JSON export.

Four optional Claude Code skills live in `.claude/skills/`. The repository instructions and JSON export work with other agents as well. The catalogue has no remote write API or automatic research bot.
