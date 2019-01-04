#!/usr/bin/env python3

from src.day15 import part2

import unittest


class TestPacmanPart2(unittest.TestCase):

    @staticmethod
    def runCase(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        return part2.elves_win_outcome(lines)

    def testInput(self):
        self.assertEqual(4988, TestPacmanPart2.runCase('../../src/day15/test_input'))

    def testInput2(self):
        self.assertEqual(29064, TestPacmanPart2.runCase('../../src/day15/test_input_2'))

    def testInput3(self):
        self.assertEqual(31284, TestPacmanPart2.runCase('../../src/day15/test_input_3'))

    def testInput4(self):
        self.assertEqual(3478, TestPacmanPart2.runCase('../../src/day15/test_input_4'))

    def testInput5(self):
        self.assertEqual(6474, TestPacmanPart2.runCase('../../src/day15/test_input_5'))

    def testInput6(self):
        self.assertEqual(1140, TestPacmanPart2.runCase('../../src/day15/test_input_6'))


if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()
