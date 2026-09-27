"""Check that every arXiv ID in the content resolves and that its title matches
the title written in the entry (fuzzy). Guards against fabricated references.

Usage:  python tools/verify_refs.py [--strict]
Known titles are checked against the committed snapshot in data/arxiv_titles.json.
New IDs require network access; use --refresh to recheck the full snapshot.
"""
from __future__ import annotations

import difflib
import json
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from common import ROOT, load_all

CACHE = ROOT / ".cache" / "arxiv.json"
SNAPSHOT = ROOT / "data" / "arxiv_titles.json"
API = "https://export.arxiv.org/api/query?id_list={ids}&max_results={n}"
NS = {"a": "http://www.w3.org/2005/Atom"}
HEADERS = {"Accept": "application/atom+xml", "User-Agent": "practical-quantum-advantage-refcheck/1.0 (https://github.com/yuchenguommm/practical-quantum-advantage)"}


def fetch_feed(url: str) -> str:
    try:
        response = requests.get(url, timeout=25, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        # Some proxies reject requests while accepting curl's TLS transport.
        curl = shutil.which("curl")
        if not curl:
            raise
        result = subprocess.run(
            [curl, "--fail", "--silent", "--show-error", "--location",
             "--max-time", "45", "--retry", "2", "--retry-delay", "3",
             "--header", "Accept: application/atom+xml", url],
            capture_output=True, text=True, encoding="utf-8", timeout=150, check=True,
        )
        return result.stdout


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def fetch_titles(ids: list[str], refresh: bool = False) -> dict[str, str]:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8")) if SNAPSHOT.exists() else {}
    cache = {} if refresh else (json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {})
    titles = {} if refresh else {**cache, **snapshot}
    todo = ids if refresh else [i for i in ids if not titles.get(i)]
    for k in range(0, len(todo), 20):
        chunk = todo[k : k + 20]
        print(f"Fetching references {k + 1}–{k + len(chunk)} of {len(todo)}", flush=True)
        root = ET.fromstring(fetch_feed(API.format(ids=",".join(chunk), n=len(chunk))))
        for ent in root.findall("a:entry", NS):
            eid = ent.find("a:id", NS).text.rsplit("/", 1)[-1]
            eid = re.sub(r"v\d+$", "", eid)
            title = " ".join(ent.find("a:title", NS).text.split())
            titles[eid] = title
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(titles, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(3)  # arXiv API etiquette
    if refresh:
        missing = [i for i in ids if i not in titles]
        if missing:
            raise ValueError(f"arXiv refresh did not resolve: {', '.join(missing)}")
        SNAPSHOT.parent.mkdir(exist_ok=True)
        SNAPSHOT.write_text(json.dumps(titles, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return titles


def main() -> int:
    strict = "--strict" in sys.argv
    wanted: dict[str, list[tuple[Path, str]]] = {}
    for e in load_all():
        for ref in e.meta.get("references") or []:
            if ref.get("arxiv"):
                aid = re.sub(r"v\d+$", "", ref["arxiv"])
                wanted.setdefault(aid, []).append((e.path, ref.get("title", "")))
    titles = fetch_titles(sorted(wanted), refresh="--refresh" in sys.argv)
    bad = 0
    for aid, uses in wanted.items():
        real = titles.get(aid)
        if real is None:
            print(f"UNRESOLVED arXiv:{aid}  used in {uses[0][0].name}")
            bad += 1
            continue
        for path, claimed in uses:
            ratio = difflib.SequenceMatcher(None, norm(real), norm(claimed)).ratio()
            if ratio < 0.6:
                print(f"TITLE MISMATCH arXiv:{aid} in {path.name}\n   entry : {claimed}\n   arXiv : {real}")
                bad += 1
    print(f"{len(wanted)} arXiv ids checked, {bad} problems")
    return 1 if (bad and strict) else 0


if __name__ == "__main__":
    sys.exit(main())
