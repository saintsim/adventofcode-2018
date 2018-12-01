#!/usr/bin/env python3


def solve():
    with open('input', 'r') as file:
        data = file.readlines()
        total = sum([int(x) for x in data])
    print('Result: ' + str(total))


solve()
