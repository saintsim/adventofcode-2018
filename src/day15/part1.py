#!/usr/bin/env python3

import copy
import datetime

GAME_BOARD = []
PLAYERS = []  # Unit object + row/col of each player in this round
ROUND = 1  # round number
PATH_HISTORY = []
PATHS_VISITED = []


class Unit:
    def __init__(self, unit_type):
        self.unit_type = unit_type  # E or G
        self.hit_points = 200

    def __str__(self):
        return self.unit_type


class Paths:
    def __init__(self, current, visited, limit):
        self.current = current
        self.visited = visited
        self.limit = limit


def get_date_time():
    return str(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] '))


def move(player):
    print(get_date_time() + 'finding targets...')
    targets = get_targets(player)
    print(get_date_time() + 'finding in range...')
    in_range = get_in_range(targets)
    print(get_date_time() + 'finding reachable...')
    reachable = get_reachable(player, in_range)
    print(get_date_time() + 'finding nearest...')
    nearest = get_nearest(reachable)
    print(get_date_time() + 'finding chosen...')
    chosen = get_chosen(nearest)
    if chosen:
        # make the move
        old_row, old_col = chosen[1][0]
        new_row, new_col = chosen[1][1]
        print(get_date_time() + 'Moving to: (' + str(new_row) + ', ' + str(new_col) + ')')
        GAME_BOARD[new_row][new_col] = GAME_BOARD[old_row][old_col]
        player[1] = new_row
        player[2] = new_col
        GAME_BOARD[old_row][old_col] = '.'
    else:
        print(get_date_time() + 'no move!')


# get targets
def get_targets(player):
    targets = []
    target_type = 'E' if player[0].unit_type == 'G' else 'G'
    for row_idx, row in enumerate(GAME_BOARD):
        for col_idx, cell in enumerate(row):
            if isinstance(cell, Unit) and cell.unit_type == target_type:
                targets.append([cell, row_idx, col_idx])
    return targets


def get_in_range(targets):
    in_range = []
    for target in targets:
        target_obj, target_row, target_col = target
        in_range = is_in_range(in_range, target_obj, target_row-1, target_col)  # top
        in_range = is_in_range(in_range, target_obj, target_row+1, target_col)  # bottom
        in_range = is_in_range(in_range, target_obj, target_row, target_col-1)  # left
        in_range = is_in_range(in_range, target_obj, target_row, target_col+1)  # right
    return in_range


def is_in_range(in_range, obj, row, col):
    if GAME_BOARD[row][col] == '.':
        in_range.append([obj, row, col])
    return in_range


def get_reachable(player, in_range):
    global PATH_HISTORY, PATHS_VISITED
    limit = 1
    PATH_HISTORY = []
    PATHS_VISITED = []
    while True:
        existing_paths = copy.deepcopy(PATH_HISTORY)
        PATH_HISTORY = []
        find_reachable_paths(player[1], player[2], limit, existing_paths)
        reachable = get_reachable_paths(in_range)
        # check if any of the paths match the in_range, break if they do match at least
        # exit loop if we have a path or no progress has been made so time to give up
        if reachable:
            break
        if not PATH_HISTORY:
            print('no progress made')
            break
        limit += 1
        # print('Limit: ' + str(limit))
    return reachable


def get_reachable_paths(dest_coords):
    paths = []
    for dest_coord in dest_coords:
        for path in PATH_HISTORY:
            current_row, current_col = path.current[-1]
            if dest_coord[1] == current_row and dest_coord[2] == current_col:
                paths.append(path)
    return paths


def find_reachable_paths(from_row, from_col, limit, existing_paths):
    # re-use the most recent paths if they exist
    if len(existing_paths):
        for idx, existing_path in enumerate(existing_paths):
            new_path = Paths(existing_path.current, existing_path.visited, limit)
            get_path(new_path.current[-1][0], new_path.current[-1][1], new_path)
    else:
        new_path = Paths([], [], limit)
        get_path(from_row, from_col, new_path)


def update_history(path):
    PATH_HISTORY.append(path)


def get_path(current_row_a, current_col_a, path):
    global PATHS_VISITED
    # need to check this so when we come back in, we don't keep adding back the same coord
    if [current_row_a, current_col_a] not in path.current:
        path.visited.append([current_row_a, current_col_a])
        path.current.append([current_row_a, current_col_a])

    if len(path.current) > path.limit:
        # print('!! skipping too long: ' + str(path))
        if path.limit > 1:
            pass
        update_history(copy.deepcopy(path))
        return path

    # coords in reading order -> up, left right, down
    coords = [[current_row_a-1, current_col_a],
              [current_row_a, current_col_a-1],
              [current_row_a, current_col_a + 1],
              [current_row_a+1, current_col_a]]

    for coord in coords:
        if GAME_BOARD[coord[0]][coord[1]] == '.':
            if ([coord[0], coord[1]] not in path.visited) and ([coord[0], coord[1]] not in PATHS_VISITED):
                PATHS_VISITED.append([coord[0], coord[1]])
                path = get_path(coord[0], coord[1], path)
                path.current.pop()
                path.visited.remove([coord[0], coord[1]])

    return path


def get_nearest(reachable):
    nearest = []
    shortest_length = 100000
    for candidate in reachable:
        length = len(candidate.current)
        if length < shortest_length:
            nearest = [[candidate.current[0], candidate.current]]
            shortest_length = length
        elif length == shortest_length:
            nearest.append([candidate.current[0], candidate.current])
    return nearest


def get_unit_coords_around_me(row, col):
    up = [row-1, col]
    left = [row, col-1]
    right = [row, col+1]
    down = [row+1, col]
    return [up, left, right, down]


def get_chosen(nearest):
    # we decide ties based upon reading order of the next step, we don't care about future steps
    if not nearest:
        return []
    nearest_chosen = nearest[0]
    for near in nearest:
        if near == nearest_chosen[0]:
            continue
        if near[1][-1][0] < nearest_chosen[1][-1][0] or (near[1][-1][0] == nearest_chosen[1][-1][0] and near[1][-1][1] < nearest_chosen[1][-1][1]):
            nearest_chosen = near
    return nearest_chosen


def attack(player):
    # any enemy around them?
    unit_to_attack = []
    unit_to_attack_hit_points = 300
    target_type = 'E' if player[0].unit_type == 'G' else 'G'
    for coords_around_me in get_unit_coords_around_me(player[1], player[2]):
            cell = GAME_BOARD[coords_around_me[0]][coords_around_me[1]]
            if isinstance(cell, Unit) and cell.unit_type == target_type:
                if cell.hit_points < unit_to_attack_hit_points:
                    unit_to_attack = [cell, coords_around_me[0], coords_around_me[1]]
                    unit_to_attack_hit_points = cell.hit_points
    if unit_to_attack:
        # time to shoot
        GAME_BOARD[unit_to_attack[1]][unit_to_attack[2]].hit_points -= 3
        print(get_date_time() + ' attacked!')
        if unit_to_attack_hit_points - 3 < 1:
            killed(unit_to_attack[1], unit_to_attack[2])
        return True
    return False


def killed(row, col):
    GAME_BOARD[row][col] = '.'


def targets_remaining():
    elves_count = 0
    goblins_count = 0
    for player in PLAYERS:
        if player[0].hit_points > 0:
            if player[0].unit_type == 'E':
                elves_count += 1
            else:
                goblins_count += 1
    return elves_count > 0 and goblins_count > 0


def init_game_board(lines):
    for line in lines:
        row = []
        for cell in line.split()[0]:
            if cell == 'E' or cell == 'G':
                row.append(Unit(cell))
            else:
                row.append(str(cell))
        GAME_BOARD.append(row)


def print_game_board():
    for row in GAME_BOARD:
        for cell in row:
            print(cell.unit_type if isinstance(cell, Unit) else cell, end='')
        print()


def init_players():
    global PLAYERS
    PLAYERS = []
    for row_idx, row in enumerate(GAME_BOARD):
        for col_idx, cell in enumerate(row):
            if isinstance(cell, Unit):
                PLAYERS.append([cell, row_idx, col_idx])


def calcuate_outcome():
    init_players()
    remaining_score = 0
    for player in PLAYERS:
        remaining_score += player[0].hit_points
    print('Result: ' + str(remaining_score) + ' * ' + str(ROUND) + ' = ')
    return remaining_score * ROUND


def init():
    global GAME_BOARD, PLAYERS, ROUND, PATH_HISTORY, PATHS_VISITED
    GAME_BOARD = []
    PLAYERS = []  # Unit object + row/col of each player in this round
    ROUND = 1  # round number
    PATH_HISTORY = []
    PATHS_VISITED = []


def play_pacman(lines):
    global ROUND
    init()
    init_game_board(lines)
    print_game_board()
    init_players()
    while True:
        print(get_date_time() + '== Round: ' + str(ROUND) + ' ==')
        print(str(len(PLAYERS)) + ' players')
        i = 0
        last_player_attacked = False
        for player in PLAYERS:
            attacked = False
            if player[0].hit_points > 0:
                print(get_date_time() + 'Players turn: ' + str(i) + ' (' + str(player[1]) + ', ' + str(player[2]) + ')')
                if attack(player):
                    attacked = True
                else:
                    move(player)
                    attacked = attack(player)
            if player == PLAYERS[-1] and attacked:
                last_player_attacked = True
            i += 1
        print_game_board()
        init_players()
        if not targets_remaining():
            # we didn't finish that round, so it wasn't a full round
            if not last_player_attacked:
                ROUND -= 1
            break
        ROUND += 1
    return calcuate_outcome()


if __name__ == '__main__':
    with open('test_input_8', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(play_pacman(lines)))
