#!/usr/bin/env python3

from src.day2 import part1

import unittest


class TestChecksum(unittest.TestCase):
    def test_checksum(self):
        lines = [
            "abcdef",
            "bababc",
            "abbcde",
            "abcccd",
            "aabcdd",
            "abcdee",
            "ababab"
        ]
        self.assertEqual(12, part1.checksum(lines))
