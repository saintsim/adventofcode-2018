#!/usr/bin/env python3

import re


class Node:
    def __init__(self, key):
        self.key = key
        self.before = list()

    def add_dep(self, dep):
        self.before.append(dep)
        return self


def build_nodes(input):
    nodes = dict()
    for instruction in input:
        # Step U must be finished before step Y can begin.
        _, step1, step2, _ = re.split('Step ([A-Z]) must be finished before step ([A-Z]) can begin.', instruction)
        if step2 in nodes:
            nodes[step2] = nodes.get(step2).add_dep(step1)
        else:
            nodes[step2] = Node(step2).add_dep(step1)
        if step1 not in nodes:
            nodes[step1] = Node(step1)
    return nodes


def find_next(nodes):
    candidates = list()
    for key, node in nodes.items():
        if len(node.before) == 0:
            candidates.append(key)
    if len(candidates) == 0:
        return ''
    candidates.sort()
    winner = candidates[0]
    return winner


def remove_node(nodes, node_to_remove):
    if node_to_remove in nodes:
        del nodes[node_to_remove]
    for key, node in nodes.items():
        if node_to_remove in node.before:
            node.before.remove(node_to_remove)
    return nodes


def node_order(lines):
    nodes = build_nodes(lines)
    prev_node = None
    order = ''
    while True:
        next_node = find_next(nodes)
        if next_node == prev_node or next_node == '':
            return order
        order += next_node
        nodes = remove_node(nodes, next_node)
        prev_node = next_node


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(node_order(lines)))
