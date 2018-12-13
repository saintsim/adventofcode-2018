#!/usr/bin/env python3

import re
from collections import Counter
import statistics


class Node:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def one_move(self):
        self.x += self.vx
        self.y += self.vy


def parse(lines):
    # position=< 9,  1> velocity=< 0,  2>
    nodes = []
    for line in lines:
        _, x, y, vx, vy, _ = re.split('position=<(.*[0-9]+),(.*[0-9]+)> velocity=<(.*[0-9]+),(.*[0-9]+)>', line.split('\n')[0])
        nodes.append(Node(int(x), int(y), int(vx), int(vy)))
    return nodes


def print_pic(nodes):
    for y in range(100, 300):
        for x in range(100, 300):
            res = '.'
            for node in nodes:
                if node.x == x and node.y == y:
                    res = '#'
                    break
            print(res, end='')
        print('')
    print('DONE')


def run(lines):
    nodes = parse(lines)
    sd_small = 10000000
    sd_iter = None

    for iters in range(1, 15000):
        for node in nodes:
            node.one_move()

        x_lined_up = Counter()
        xs = []
        for node in nodes:
            xs.append(node.y)
            x_lined_up[str(node.y)] += 1
        sd = statistics.stdev(xs)
        if sd < sd_small:
            sd_small = sd
            sd_iter = iters
        #if iters == 10086:
        #    print_pic(nodes)

    print(sd_small)
    print(sd_iter)


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(run(lines)))
