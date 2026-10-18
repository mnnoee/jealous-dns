"""Unit-тесты парсера DNS-записей."""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dnsparse.core import DNSParser

SAMPLE = """mnnoee.ru.
3600
A (адрес Internet v4)
127.0.0.1
mail.mnnoee.ru.
3600
MX (почтовый сервер)
mx.example.com
priority = 10
"""


class ParserTest(unittest.TestCase):
    def test_basic(self):
        recs = DNSParser.parse(SAMPLE)
        self.assertEqual(len(recs), 2)
        self.assertEqual(recs[0]["type"], "A")
        self.assertEqual(recs[0]["value"], "127.0.0.1")
        self.assertEqual(recs[1]["type"], "MX")
        self.assertEqual(recs[1]["priority"], "10")

    def test_empty(self):
        self.assertEqual(DNSParser.parse(""), [])
        self.assertEqual(DNSParser.parse("   \n  "), [])


if __name__ == "__main__":
    unittest.main()
