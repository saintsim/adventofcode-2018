#!/usr/bin/env python3
# Day 8: Memory Maneuver


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
            metaentries_sum += entries[i]
        return metaentries_sum
    else:
        metaentries_sum += sum(entries[(-1 * number_of_entries):])
        next_min = 2
        for i in range(number_of_children):
            next_child_length = get_child_size(entries[next_min:-1 * number_of_entries])
            next_max = next_min + next_child_length
            metaentries_sum += metadata_sum(entries[next_min:next_max], 0)
            next_min = next_max
        return metaentries_sum


if __name__ == '__main__':
    with open('test_input', 'r') as file:
        lines = file.readlines()
        entries = list(map(int, lines[0].split()))
        print('Result: ' + str(metadata_sum(entries, 0)))
