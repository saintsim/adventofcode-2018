#!/usr/bin/env python3

import copy

STARS = []
CONSTELLATIONS = []


class Star:
    def __init__(self, x, y, z, t):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.t = int(t)

    def __str__(self):
        return str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ',' + str(self.t)


def manhattan_distance(star1, star2):
    return abs(star1.x - star2.x) + abs(star1.y - star2.y) + abs(star1.z - star2.z) + abs(star1.t - star2.t)


def parse(lines):
    for line in lines:
        clean_line = line.split('\n')
        x, y, z, t = clean_line[0].split(',')
        STARS.append(Star(x, y, z, t))


def process():
    global CONSTELLATIONS
    for star in STARS:
        new_constellations = []
        new_constellation = []
        for idx, constellation in enumerate(CONSTELLATIONS):
            match = False
            for coords in constellation:
                if manhattan_distance(star, coords) < 4:
                    match = True
                    break
            if match:
                constellation.append(star)
                new_constellation = new_constellation + constellation
            else:
                # not a match for this star so just add
                new_constellations.append(constellation)
        if new_constellation:
            # add this new combined bucket
            new_constellations.append(new_constellation)
        else:
            # add star to a new bucket since it doesn't match any others
            new_constellation.append(star)
            new_constellations.append(new_constellation)
        CONSTELLATIONS = copy.deepcopy(new_constellations)


def constellation(lines):
    parse(lines)
    process()
    return len(CONSTELLATIONS)

# 597 is too high
# 426 is too high


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(constellation(lines)))
