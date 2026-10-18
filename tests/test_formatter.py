"""Unit-тесты форматтера DNS-записей."""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dnsparse.formatter import DNSFormatter


class FormatterTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(DNSFormatter().format([]), "")

    def test_wrapped(self):
        recs = [{"name": "a.example.", "type": "A", "value": "1.2.3.4", "priority": ""}]
        out = DNSFormatter(is_pretty=False).format(recs)
        self.assertTrue(out.startswith("```"))
        self.assertTrue(out.endswith("```"))
        self.assertIn("a.example.", out)

    def test_mx_priority(self):
        recs = [{"name": "m.example.", "type": "MX", "value": "mx.example.", "priority": "5"}]
        out = DNSFormatter(is_pretty=False).format(recs)
        self.assertIn("(приоритет 5)", out)


if __name__ == "__main__":
    unittest.main()
