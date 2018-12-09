#!/usr/bin/env python3
# Day 8: Memory Maneuver


def metadata_sum(entries, metaentries_sum):
    number_of_children = entries[0]
    number_of_entries = entries[1]
    if number_of_children == 0:
        for i in range(2, 2+number_of_entries):
            metaentries_sum += entries[i]
            print(str(entries[i]) + ' + ')
        if len(entries) > 2+number_of_entries:
            return metadata_sum(entries[2+number_of_entries:], metaentries_sum)
        else:
            return metaentries_sum
    else:
        print(str(entries[(-1 * number_of_entries):]) + ' + ')
        metaentries_sum += sum(entries[(-1 * number_of_entries):])
        try:
            return metadata_sum(entries[2:-1 * number_of_entries], metaentries_sum)
        except IndexError:
            pass


if __name__ == '__main__':
    with open('test_input2', 'r') as file:
        lines = file.readlines()
        entries = list(map(int, lines[0].split()))
        print('Result: ' + str(metadata_sum(entries, 0)))
