#!/usr/bin/env python3

from src.day1 import part2

import unittest


class TestChecksum(unittest.TestCase):
    def test_repeating_frequency(self):
        cases = [
            (['+1', '-1'], 1),
            (['+3', '+3', '+4', '-2', '-4'], 10),
            (['-6', '+3', '+8', '+5', '-6'], 5),
            (['+7', '+7', '-2', '-7', '-4'], 14)
        ]

        for case in cases:
            self.assertEqual(case[1], part2.repeating_frequency(case[0]))
