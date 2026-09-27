"""Load reproducible case manifests and check their public inputs and links."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from common import ROOT

CASE_ROOT = ROOT / "numerics" / "cases"
REQUIRED = {"id", "title", "summary", "application", "problems", "finding",
            "review_status", "input", "result", "protocol", "code", "last_checked"}


def load_cases(entries):
    ids = {"application": {e.id for e in entries if e.type == "application"},
           "problem": {e.id for e in entries if e.type == "problem"}}
    cases, errors = [], []
    for manifest in sorted(CASE_ROOT.glob("*/case.json")):
        try:
            label = manifest.relative_to(ROOT)
        except ValueError:
            label = manifest
        try:
            case = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{label}: {exc}")
            continue
        missing = REQUIRED - case.keys()
        if missing:
            errors.append(f"{label}: missing {', '.join(sorted(missing))}")
            continue
        if (not isinstance(case["id"], str) or not isinstance(case["title"], str)
                or not isinstance(case["summary"], str)
                or not isinstance(case["application"], str)
                or not isinstance(case["problems"], list)
                or not all(isinstance(p, str) for p in case["problems"])):
            errors.append(f"{label}: invalid case field types")
            continue
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", case["id"]):
            errors.append(f"{label}: invalid id")
        if case["application"] not in ids["application"]:
            errors.append(f"{label}: unknown application {case['application']}")
        for problem in case["problems"]:
            if problem not in ids["problem"]:
                errors.append(f"{label}: unknown problem {problem}")
        if case["review_status"] not in ("seed", "reviewed", "disputed"):
            errors.append(f"{label}: invalid review_status")
        try:
            date.fromisoformat(case["last_checked"])
        except (TypeError, ValueError):
            errors.append(f"{label}: invalid last_checked")
        for field in ("input", "result", "protocol", "code"):
            name = case[field]
            if not isinstance(name, str) or Path(name).name != name or not (manifest.parent / name).is_file():
                errors.append(f"{label}: missing or unsafe {field}: {name}")
        if "verification" in case:
            name = case["verification"]
            if not isinstance(name, str) or Path(name).name != name or not (manifest.parent / name).is_file():
                errors.append(f"{label}: missing or unsafe verification: {name}")
        case["folder"] = manifest.parent.name
        cases.append(case)
    seen = set()
    for case in cases:
        if case["id"] in seen:
            errors.append(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
    return cases, errors
