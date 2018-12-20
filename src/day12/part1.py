#!/usr/bin/env python3

import re

PLANTS = ""
PLANTS_START = 5
RULES = {}


def parse(lines):
    global PLANTS, PLANTS_START
    _, init_state, _ = re.split('initial state: (.*)', lines[0])
    PLANTS = '.....' + init_state + '...'
    for line in lines:
        tokens = re.split('(.*) => (.*)', line)
        if len(tokens) > 1:
            _, rule, result, _ = tokens
            RULES[rule] = result


def run_simulation():
    global PLANTS
    new_gen = ["."]*(len(PLANTS)+3)
    for idx in range(0, len(PLANTS)-3):
        if idx < 2:
            rule_candidate = '.'*(2-idx) + PLANTS[0:idx + 3]
        else:
            rule_candidate = PLANTS[idx-2:idx+3]
        if rule_candidate in RULES:
            new_gen[idx] = RULES[rule_candidate]
    PLANTS = "".join(new_gen)


def print_plants():
    print(PLANTS)


def count_plants():
    total = 0
    for idx in range(0, len(PLANTS) - 3):
        if PLANTS[idx] == '#':
            total += idx-PLANTS_START
    return total


MODEL = [
    '...#..#.#..##......###...###...........',
    '...#...#....#.....#..#..#..#...........',
    '...##..##...##....#..#..#..##..........',
    '..#.#...#..#.#....#..#..#...#..........',
    '...#.#..#...#.#...#..#..##..##.........',
    '....#...##...#.#..#..#...#...#.........',
    '....##.#.#....#...#..##..##..##........',
    '...#..###.#...##..#...#...#...#........',
    '...#....##.#.#.#..##..##..##..##.......',
    '...##..#..#####....#...#...#...#.......',
    '..#.#..#...#.##....##..##..##..##......',
    '...#...##...#.#...#.#...#...#...#......',
    '...##.#.#....#.#...#.#..##..##..##.....',
    '..#..###.#....#.#...#....#...#...#.....',
    '..#....##.#....#.#..##...##..##..##....',
    '..##..#..#.#....#....#..#.#...#...#....',
    '.#.#..#...#.#...##...#...#.#..##..##...',
    '..#...##...#.#.#.#...##...#....#...#...',
    '..##.#.#....#####.#.#.#...##...##..##..',
    '.#..###.#..#.#.#######.#.#.#..#.#...#..',
    '.#....##....#####...#######....#.#..##.'
]

def verify(i):
    match = True
    for idx in range(min(len(PLANTS),len(MODEL[i]))):
        if MODEL[i][idx] != PLANTS[idx]:
            match = False

    if match:
        print(str(i) + ' - matches')
    else:
        print(str(i) + ' - mismatch')
        print(str(i) + '~ ', end='')
        print(MODEL[i][:len(PLANTS)])

def plant_simulation(lines, verify_test_input):
    parse(lines)
    print('0: ', end='')
    if verify_test_input:
        verify(0)
    print_plants()
    for i in range(20):
        run_simulation()
        if verify_test_input:
            verify(i+1)
        print(str(i+1) + ': ', end='')
        print_plants()
    return count_plants()


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(plant_simulation(lines, False)))