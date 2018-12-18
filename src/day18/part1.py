#!/usr/bin/env python3

import copy

MAP = []


def parse_input(lines):
    for row in lines:
        new_row = []
        for col in row.split()[0]:
            new_row.append(col)
        MAP.append(new_row)


def print_map():
    for row in MAP:
        for cell in row:
            print(cell, end='')
        print('')
    print('')
    print('')


def get_adj_cells(row_idx, col_idx):
    #  1 2 3
    #  4   5
    #  6 7 8
    cells_by_type = {'|': 0, '#': 0}
    for row_offset in range(-1, 2):
        check_row_idx = row_idx + row_offset
        if check_row_idx > len(MAP)-1 or check_row_idx < 0:
            continue
        for col_offset in range(-1, 2):
            check_col_idx = col_idx + col_offset
            if row_offset == 0 and col_offset == 0:
                continue
            if check_col_idx > len(MAP[0])-1 or check_col_idx < 0:
                continue
            cell = MAP[check_row_idx][check_col_idx]
            if cell == '|' or cell == '#':
                cells_by_type[cell] += 1
    return cells_by_type


def run_simulation(mins):
    global MAP
    for i in range(10):
        new_map = copy.deepcopy(MAP)
        for row_idx, row in enumerate(MAP):
            for col_idx, cell in enumerate(row):
                # [1] An open acre will become filled with trees if three or more adjacent acres contained trees.
                #     Otherwise, nothing happens.
                if cell == '.':
                    cells_by_type = get_adj_cells(row_idx, col_idx)
                    if cells_by_type['|'] > 2:
                        new_map[row_idx][col_idx] = '|'
                # [2] An acre filled with trees will become a lumberyard if three or more adjacent acres
                # were lumberyards. Otherwise, nothing happens.
                elif cell == '|':
                    cells_by_type = get_adj_cells(row_idx, col_idx)
                    if cells_by_type['#'] > 2:
                        new_map[row_idx][col_idx] = '#'
                # [3] An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one
                # other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
                elif cell == '#':
                    cells_by_type = get_adj_cells(row_idx, col_idx)
                    if cells_by_type['#'] > 0 and cells_by_type['|'] > 0:
                        pass
                    else:
                        new_map[row_idx][col_idx] = '.'
        MAP = copy.deepcopy(new_map)
        print_map()


def compute_outcome():
    cells_by_type = {'|': 0, '#': 0}
    for row in MAP:
        for cell in row:
            if cell == '|' or cell == '#':
                cells_by_type[cell] += 1
    return cells_by_type['#']*cells_by_type['|']


def lumber_simulation(lines):
    parse_input(lines)
    print_map()
    run_simulation(10)
    return compute_outcome()


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(lumber_simulation(lines)))