#!/usr/bin/env python3

from src.day15 import part1

import unittest


class TestPacman(unittest.TestCase):

    @staticmethod
    def runCase(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        return part1.play_pacman(lines)

    def testInput(self):
        self.assertEqual(27730, TestPacman.runCase('../../src/day15/test_input'))

    def testInput2(self):
        self.assertEqual(36334, TestPacman.runCase('../../src/day15/test_input_2'))

    def testInput3(self):
        self.assertEqual(39514, TestPacman.runCase('../../src/day15/test_input_3'))

    def testInput4(self):
        self.assertEqual(27755, TestPacman.runCase('../../src/day15/test_input_4'))

    def testInput5(self):
        self.assertEqual(28944, TestPacman.runCase('../../src/day15/test_input_5'))

    def testInput6(self):
        self.assertEqual(18740, TestPacman.runCase('../../src/day15/test_input_6'))

    def testInput7(self):
        self.assertEqual(5300, TestPacman.runCase('../../src/day15/test_input_7'))

if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()
