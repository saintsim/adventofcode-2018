#!/usr/bin/env python3

from src.day2 import part2

import unittest


class TestCommonLetters(unittest.TestCase):
    def test_common_letters(self):
        boxes = [
            "abcde",
            "fghij",
            "klmno",
            "pqrst",
            "fguij",
            "axcye",
            "wvxyz"
        ]
        self.assertEqual('fgij', part2.common_letters(boxes))
