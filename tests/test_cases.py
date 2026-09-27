"""A contributed case must link real catalogue pages and local public files."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from common import load_all  # noqa: E402
import cases  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "numerics" / "cases" / "automotive_pricing"))
import run as automotive_run  # noqa: E402
import verify_public_input  # noqa: E402


class CasesTest(unittest.TestCase):
    def test_automotive_public_input_arithmetic(self):
        receipt = verify_public_input.verify(download=False)
        self.assertEqual(receipt["optimum"], 1547)
        self.assertEqual(receipt["feasible_assignments"], 382)
        self.assertEqual(receipt["qualifying_assignments"], 9)

    def test_automotive_input_hash_is_checkout_independent(self):
        source = Path(automotive_run.HERE / "instance.json").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "instance.json"
            copy.write_bytes(source.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
            self.assertEqual(automotive_run.portable_sha256(copy),
                             automotive_run.portable_sha256(automotive_run.HERE / "instance.json"))

    def test_published_case_is_valid(self):
        found, errors = cases.load_cases(load_all())
        self.assertEqual(errors, [])
        self.assertTrue(any(c["id"] == "automotive-pricing-public-9" for c in found))

    def test_invalid_case_cannot_escape_its_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "bad"
            folder.mkdir()
            manifest = {"id": "bad", "title": "Bad case", "summary": "Test case",
                        "application": "not-an-application", "problems": ["not-a-problem"],
                        "finding": "baseline", "review_status": "seed",
                        "input": "../private.json", "result": "result.json",
                        "protocol": "README.md", "code": "run.py", "last_checked": "2026-09-27"}
            (folder / "case.json").write_text(json.dumps(manifest), encoding="utf-8")
            with patch.object(cases, "CASE_ROOT", Path(directory)):
                _, errors = cases.load_cases(load_all())
        self.assertTrue(any("unsafe input" in error for error in errors))
        self.assertTrue(any("unknown application" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
