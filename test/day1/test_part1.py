#!/usr/bin/env python3

from src.day1 import part1

import unittest


class TestChecksum(unittest.TestCase):
    def test_frequency_change(self):
        cases = [
            (['+1', '-2', '+3', '+1'], 3),
            (['+1', '+1', '+1'], 3),
            (['-1', '-2', '-3'], -6)
        ]

        for case in cases:
            self.assertEqual(case[1], part1.frequency_change(case[0]))
