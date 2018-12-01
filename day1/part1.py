#!/usr/bin/env python3


def solve():
    with open('input', 'r') as file:
        data = file.readlines()
        return sum(map(int, data))


print('Result: ' + str(solve()))
