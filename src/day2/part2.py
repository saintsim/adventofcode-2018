#!/usr/bin/env python3


def common_letters(sequences):
    for index, item in enumerate(sequences):
        item_stripped = item.strip()
        for other_index, other_item in enumerate(sequences):
            if index == other_index:
                continue
            diffs = 0
            in_common = ''
            for letter_index, letter in enumerate(item_stripped):
                if item_stripped[letter_index] != other_item[letter_index]:
                    diffs += 1
                else:
                    in_common += item_stripped[letter_index]
            if diffs == 1:
                return in_common


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(common_letters(lines)))
