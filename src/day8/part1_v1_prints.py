#!/usr/bin/env python3
# Day 8: Memory Maneuver

# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# A----------------------------------
#     B----------- C-----------
#                      D-----
# In this example, each node of the tree is also marked with an underline starting with a letter for easier
# identification. In it, there are four nodes:
#
# A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
# B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
# C, which has 1 child node (D) and 1 metadata entry (2).
# D, which has 0 child nodes and 1 metadata entry (99).
#


def get_child_size(entries):
    if len(entries) < 2:
        return 0
    number_of_children = entries[0]
    number_of_entries = entries[1]
    if number_of_children == 0:
        return 2+number_of_entries
    else:
        return 2+number_of_entries + get_child_size(entries[2:(-1*number_of_entries)])


def metadata_sum(entries, metaentries_sum):
    number_of_children = entries[0]
    number_of_entries = entries[1]
    if number_of_children == 0:
        for i in range(2, 2+number_of_entries):
            print(str(entries[i]) + ' + ')
            metaentries_sum += entries[i]
        return metaentries_sum
    else:
        print('kid count: ' + str(number_of_children))
        total = sum(entries[(-1 * number_of_entries):])
        print(str(entries[(-1 * number_of_entries):]) + ' (foo) + ')
        # one per a kid
        kid_entries = entries[2:-1*number_of_entries]
        print('my kids: ' + str(kid_entries))
        next_min = 2
        for i in range(number_of_children):
            print('child ' + str(i) + ' of ' + str(number_of_children))
            print('get next child of: ' + str(entries[next_min:-1 * number_of_entries]))
            if len(entries[next_min:-1 * number_of_entries]) == 0:
                print('empty')
                pass
            next_child_length = get_child_size(entries[next_min:-1 * number_of_entries])
            print('next child length: ' + str(next_child_length))
            next_max = next_min + next_child_length
            total += metadata_sum(entries[next_min:next_max], 0)
            next_min = next_max
        return metaentries_sum + total


if __name__ == '__main__':
    with open('test_input2', 'r') as file:
        lines = file.readlines()
        entries = list(map(int, lines[0].split()))
        print(str(len(entries)))
        print('Result: ' + str(metadata_sum(entries, 0)))
