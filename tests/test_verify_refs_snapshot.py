"""The CI reference gate must work when arXiv is temporarily unavailable."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import verify_refs


class SnapshotCheck(unittest.TestCase):
    def test_committed_titles_need_no_network(self):
        with patch.object(verify_refs, "fetch_feed", side_effect=AssertionError("unexpected network lookup")):
            titles = verify_refs.fetch_titles(["2104.10653", "1504.06987"])
        self.assertIn("battery electrolyte molecules", titles["2104.10653"].lower())
        self.assertIn("monte carlo", titles["1504.06987"].lower())


if __name__ == "__main__":
    unittest.main()
