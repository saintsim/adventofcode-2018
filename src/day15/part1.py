#!/usr/bin/env python3

GAME_BOARD = []
PLAYERS = []  # Unit object + row/col of each player in this round
ROUND = 0  # round number

VALID_PATHS = []
SHORTEST_PATH = 100000


class Unit:
    def __init__(self, unit_type):
        self.unit_type = unit_type  # E or G
        self.hit_points = 200

    def __str__(self):
        return self.unit_type


def move(player):
    global SHORTEST_PATH
    SHORTEST_PATH = 100000
    print('finding targets...')
    targets = get_targets(player)
    print('finding in range...')
    in_range = get_in_range(targets)
    # optimise to only look at the closer ones
    close_range = get_in_close_range(player, in_range)
    print('finding reachable...')
    reachable = get_reachable(player, close_range)
    print('finding nearest...')
    nearest = get_nearest(reachable)
    print('finding chosen...')
    chosen = get_chosen(player, nearest)
    if chosen:
        # make the move
        old_row, old_col = chosen[1][0]
        new_row, new_col = chosen[1][1]
        GAME_BOARD[new_row][new_col] = GAME_BOARD[old_row][old_col]
        player[1] = new_row
        player[2] = new_col
        GAME_BOARD[old_row][old_col] = '.'


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
        in_range = is_in_range(in_range, target_obj, target_row-1, target_col) # top
        in_range = is_in_range(in_range, target_obj, target_row+1, target_col)  # bottom
        in_range = is_in_range(in_range, target_obj, target_row, target_col-1)  # left
        in_range = is_in_range(in_range, target_obj, target_row, target_col+1)  # right
    return in_range


def is_in_range(in_range, obj, row, col):
    if GAME_BOARD[row][col] == '.':
        in_range.append([obj, row, col])
    return in_range


def get_in_close_range(player, in_range):
    # drop half
    by_range = {}
    in_close_range = []
    from_row = player[1]
    from_col = player[2]
    in_range_points_count = 0
    for in_range_details in in_range:
        distance = manhattan_distance(from_row, from_col, in_range_details[1], in_range_details[2])
        if distance in by_range:
            by_range[distance].append(in_range_details)
        else:
            by_range[distance] = [in_range_details]
        in_range_points_count += 1
    number_to_include = max(10, round(in_range_points_count/2))
    i = 0
    for key in sorted(by_range):
        if i > number_to_include:
            break
        for entry in by_range[key]:
            in_close_range.append(entry)
            i += 1
    return in_close_range


def manhattan_distance(from_row, from_col, to_row, to_col):
    return abs(from_row - to_row) + abs(from_col - to_col)


def get_reachable(player, in_range):
    reachable = []
    for in_range_cell in in_range:
        paths = find_reachable_paths(player[1], player[2], in_range_cell[1], in_range_cell[2])
        if paths:
            reachable.append([in_range_cell, paths])
    return reachable


def find_reachable_paths(from_row, from_col, dest_row, dest_col):
    global VALID_PATHS
    VALID_PATHS = []
    get_path(from_row, from_col, dest_row, dest_col, [], [])
    return VALID_PATHS


def get_path(current_row_a, current_col_a, dest_row, dest_col, visited, path):
    visited.append([current_row_a, current_col_a])
    path.append([current_row_a, current_col_a])

    if len(path) > SHORTEST_PATH:
        return path

    if len(path) > 25:
        return path

    if current_row_a == dest_row and current_col_a == dest_col:
        global SHORTEST_PATH
        if len(path) < SHORTEST_PATH:
            SHORTEST_PATH = len(path)
        VALID_PATHS.append(path.copy())
        return path

    # go down
    if GAME_BOARD[current_row_a+1][current_col_a] == '.':
        if [current_row_a+1, current_col_a] not in visited:
            get_path(current_row_a+1, current_col_a, dest_row, dest_col, visited, path)
            path.pop()
            visited.remove([current_row_a+1, current_col_a])

    # go up
    if GAME_BOARD[current_row_a-1][current_col_a] == '.':
        if [current_row_a-1, current_col_a] not in visited:
            get_path(current_row_a-1, current_col_a, dest_row, dest_col, visited, path)
            path.pop()
            visited.remove([current_row_a-1, current_col_a])

    # go right
    if GAME_BOARD[current_row_a][current_col_a + 1] == '.':
        if [current_row_a, current_col_a + 1] not in visited:
            get_path(current_row_a, current_col_a + 1, dest_row, dest_col, visited, path)
            path.pop()
            visited.remove([current_row_a, current_col_a + 1])
    # go left
    if GAME_BOARD[current_row_a][current_col_a-1] == '.':
        if [current_row_a, current_col_a-1] not in visited:
            get_path(current_row_a, current_col_a-1, dest_row, dest_col, visited, path)
            path.pop()
            visited.remove([current_row_a, current_col_a-1])


def get_nearest(reachable):
    nearest = []
    shortest_length = 100000
    for candidate in reachable:
        for candidate_paths in candidate[1]:
            length = len(candidate_paths)
            if length < shortest_length:
                nearest = [[candidate[0], candidate_paths]]
                shortest_length = length
            elif length == shortest_length:
                nearest.append([candidate[0], candidate_paths])
    return nearest


def get_unit_coords_around_me(row, col):
    up = [row-1, col]
    left = [row, col-1]
    right = [row, col+1]
    down = [row+1, col]
    return [up, left, right, down]


def get_chosen(player, nearest):
    # we decide ties based upon reading order of the next step, we don't care about future steps
    for preferred_move in get_unit_coords_around_me(player[1], player[2]):
        for nearest_candiate in nearest:
            if nearest_candiate[1][1] == preferred_move:
                return nearest_candiate
    return []


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
    return remaining_score * ROUND


def play_pacman(lines):
    init_game_board(lines)
    print_game_board()
    init_players()
    while targets_remaining():
        global ROUND
        ROUND += 1
        print('== Round: ' + str(ROUND) + ' ==')
        print(str(len(PLAYERS)) + ' players')
        i=0
        for player in PLAYERS:
            if i == 11:
                print('11')
                pass
            if player[0].hit_points > 0:
                print('Players turn: ' + str(i) + ' (' + str(player[1]) + ', ' + str(player[2]) + ')')
                if not attack(player):
                    move(player)
                    attack(player)
            i += 1
        print_game_board()
        init_players()
    return calcuate_outcome()


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(play_pacman(lines)))
