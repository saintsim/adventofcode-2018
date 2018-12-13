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


def find_next(nodes, in_use_nodes):
    candidates = list()
    for key, node in nodes.items():
        if len(node.before) == 0:
            candidates.append(key)
    if len(candidates) == 0:
        return ''
    candidates.sort()
    for candidate in candidates:
        if candidate not in in_use_nodes:
            return candidate
    return ''


def remove_node(nodes, node_to_remove):
    if node_to_remove in nodes:
        del nodes[node_to_remove]
    for key, node in nodes.items():
        if node_to_remove in node.before:
            node.before.remove(node_to_remove)
    return nodes


# -64 so A=1, B=2, +60 for the 60secs added on to each step
def node_value(node):
    return ord(node) - 4


def node_order(lines, num_of_workers):
    nodes = build_nodes(lines)
    time_taken = 0
    workers = []
    node_working_on = []
    for _ in range(num_of_workers):
        workers.append(0)
        node_working_on.append('')
    while True:
        for idx, worker in enumerate(workers):
            if worker == 0:
                if node_working_on[idx] != '':
                    nodes = remove_node(nodes, node_working_on[idx])
                    node_working_on[idx] = ''
                next_node = find_next(nodes, node_working_on)
                if next_node != '':
                    workers[idx] = node_value(next_node)
                    node_working_on[idx] = next_node
        for idx, worker in enumerate(workers):
            if worker != 0:
                workers[idx] -= 1
        if nodes == dict() and sum(workers) == 0:
            return time_taken-1
        print(str(time_taken) + ' : ' + str(node_working_on))
        time_taken += 1


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(node_order(lines, 5)))
