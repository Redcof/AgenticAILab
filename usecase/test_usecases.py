"""# Reproduction tests for the standalone RAG worked examples

Run from the repository root:
```bash
python3 -m unittest discover -s usecase -p 'test_*.py' -v
```

Each test executes the same code as the linked examples without third-party
packages. Tests verify intended toy behavior, not production security.
"""

import importlib.util
import pathlib
import unittest
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent


def load(filename: str):
    """Import a numbered standalone module by file path."""
    import sys

    name = "usecase_" + filename.replace(".py", "").replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class UseCaseTests(unittest.TestCase):
    def test_policy_version(self):
        m = load("01_foundations.py")
        self.assertIn("30 days", m.answer("refund", date(2026, 11, 16)))
        self.assertIn("cannot verify", m.answer("warranty", date(2026, 11, 16)))

    def test_chunk_overlap(self):
        m = load("02_chunking.py")
        text = "Our annual plan offers a refund within 30 days after purchase"
        phrase = "refund within 30 days"
        self.assertFalse(any(phrase in c for c in m.chunk_words(text, 5, 0)))
        self.assertTrue(any(phrase in c for c in m.chunk_words(text, 5, 2)))

    def test_tenant_filter(self):
        m = load("03_vector_search.py")
        self.assertEqual([x[0] for x in m.search((1.0, 0.0), "A")], ["A1", "A2"])
        self.assertEqual([x[0] for x in m.search((1.0, 0.0), "B")], ["B1"])

    def test_retrieval_metrics(self):
        m = load("04_evaluation.py")
        v = m.evaluate(["d1", "d2", "d3", "d4"], {"d1", "d3", "d5", "d6", "d7"}, 4)
        self.assertAlmostEqual(v.precision, 0.5)
        self.assertAlmostEqual(v.recall, 0.4)
        self.assertAlmostEqual(v.f1, 4 / 9)

    def test_refund_gate(self):
        m = load("05_agent_authorization.py")
        svc = m.RefundService()
        self.assertTrue(svc.refund(m.TrustedContext("C2"), 1000, "k").startswith("DENIED"))
        self.assertTrue(svc.refund(m.TrustedContext("C1"), 1000, "k").startswith("APPROVED"))
        self.assertTrue(svc.refund(m.TrustedContext("C1"), 1000, "k").startswith("DUPLICATE"))

    def test_citation_check(self):
        m = load("06_grounded_citations.py")
        self.assertTrue(m.verify_days(30, "p2"))
        self.assertFalse(m.verify_days(60, "p2"))
        self.assertFalse(m.verify_days(30, "missing"))


if __name__ == "__main__":
    unittest.main()
