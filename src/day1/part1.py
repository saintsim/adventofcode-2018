#!/usr/bin/env python3


def frequency_change(lines):
        return sum(map(int, lines))


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(frequency_change(lines)))
