#!/usr/bin/env python3


def solve():
    with open('input', 'r') as file:
        data = file.readlines()
        totals_found = set()
        total = 0
        while True:
            for x in data:
                total += int(x)
                if total in totals_found:
                    return total
                totals_found.add(total)


print('Result: ' + str(solve()))
