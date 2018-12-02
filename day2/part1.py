#!/usr/bin/env python3


def solve():
    # exactly two of any letter
    # exactly three of any letter
    with open('input', 'r') as file:
        exactly_two_occurences = 0
        exactly_three_occurences = 0
        lines = file.readlines()
        for line in lines:
            occurences = {}
            exactly_two_in_line = False
            exactly_three_in_line = False
            for letter in line:
                if letter in occurences:
                    occurences[letter] = occurences[letter]+1
                else:
                    occurences[letter] = 1
            for l, freq in occurences.items():
                if freq == 2:
                    exactly_two_in_line = True
                if freq == 3:
                    exactly_three_in_line = True
            if exactly_two_in_line:
                exactly_two_occurences += 1
            if exactly_three_in_line:
                exactly_three_occurences += 1
        return exactly_two_occurences * exactly_three_occurences


print('Result: ' + str(solve()))
