#!/usr/bin/env python3


def solve():
    with open('input', 'r') as file:
        return sum(map(int, file.readlines()))


print('Result: ' + str(solve()))
