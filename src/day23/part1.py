#!/usr/bin/env python3

import re

NODES = []


class Bot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __str__(self):
        return "(" + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + '), r=' + str(self.r)


def parse(lines):
    for instruction in lines:
        # pos=<17979522,-36670256,7942228>, r=58950833
        _, x, y, z, r, _ = re.split('pos=<(.*),(.*),(.*)>, r=(.*)', instruction.split('\n')[0])
        NODES.append(Bot(int(x), int(y), int(z), int(r)))


def get_max_r_node():
    max_node = None
    max_r_value = 0
    for node in NODES:
        if node.r > max_r_value:
            max_r_value = node.r
            max_node = node
    return max_node


def manhattan_distance(from_x, from_y, from_z, to_x, to_y, to_z):
    return abs(from_x - to_x) + abs(from_y - to_y) + abs(from_z - to_z)


def get_number_in_range(from_node):
    count = 0
    for node in NODES:
        distance = manhattan_distance(from_node.x, from_node.y, from_node.z, node.x, node.y, node.z)
        if distance <= from_node.r:
            print('close: ' + str(node))
            count += 1
    return count


def nanobots(lines):
    parse(lines)
    max_node = get_max_r_node()
    return get_number_in_range(max_node)


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(nanobots(lines)))