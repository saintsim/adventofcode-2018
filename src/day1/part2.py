#!/usr/bin/env python3


def repeating_frequency(lines):
    totals_found = set()
    total = 0
    while True:
        for x in lines:
            total += int(x)
            if total in totals_found:
                return total
            totals_found.add(total)


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(repeating_frequency(lines)))
