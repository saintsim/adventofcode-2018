#!/usr/bin/env python3

import re

ARMIES = []
ARMIES_PICKED_TO_ATTACK = []
ARMIES_PICKED_TO_TARGET = []


class Army:
    def __init__(self, group_num, group_type, num_of_units, hit_points, weak_to, immune_to,
                 attack_damage_type, attack_damage_hit_points, attack_damage_initiative):
        self.group_num = int(group_num)  # e.g. 1
        self.group_type = group_type  # e.g. Immune system or infection
        self.num_of_units = int(num_of_units)  # e.g. 17
        self.hit_points = int(hit_points)  # e.g. 5390
        self.weak_to = weak_to  # e.g. ['radiation', 'bludgeoning']
        self.immune_to = immune_to  # e.g. ['fire']
        self.attack_damage_type = attack_damage_type  # 'fire'
        self.attack_damage_hit_points = int(attack_damage_hit_points)  # e.g. 4507
        self.attack_damage_initiative = int(attack_damage_initiative)  # e.g. 3
        self.effective_power = self.num_of_units * self.attack_damage_hit_points

    def update_num_of_units(self, num_of_units):
        self.num_of_units = int(num_of_units)
        self.effective_power = self.num_of_units * self.attack_damage_hit_points


def parse(lines, boost):
    group_num = 1
    group_type = ''
    for line in lines:
        if line == '\n':
            continue
        weak_to = immune_to = []
        # group type
        tokens = line.split('\n')
        if tokens[0] == 'Immune System:' or tokens[0] == 'Infection:':
            group_type = tokens[0][:-1]
            continue
        if '(' in tokens[0]:
            _, num_of_units, hit_points, weak_immune_to, attack_damage_hit_points, attack_damage_type, \
            attack_damage_initiative, _ = re.split('([0-9]+) units each with ([0-9]+) hit points \((.+)\) '
                                                   'with an attack that does ([0-9]+) (.+) '
                                                   'damage at initiative (.*)', tokens[0])
            weak_to, immune_to = parse_weak_immune_details(weak_immune_to)
        else:
            _, num_of_units, hit_points, attack_damage_hit_points, attack_damage_type, \
            attack_damage_initiative, _ = re.split('([0-9]+) units each with ([0-9]+) hit points '
                                                   'with an attack that does ([0-9]+) (.+) '
                                                   'damage at initiative (.*)', tokens[0])
        if group_type == 'Immune System':
            attack_damage_hit_points = int(attack_damage_hit_points) + boost
        ARMIES.append(Army(group_num, group_type, num_of_units, hit_points, weak_to, immune_to,
                           attack_damage_type, attack_damage_hit_points, attack_damage_initiative))
        group_num += 1


def parse_weak_immune_details(weak_immune_to):
    # weak to radiation
    # weak to radiation, bludgeoning
    # weak to radiation; immune to fire, cold
    # immune to radiation
    # immune to radiation; weak to fire, cold
    # immune to fire; weak to bludgeoning, slashing
    weak_to = []
    immune_to = []
    tokens = weak_immune_to.split('; ')
    for token in tokens:
        if token.startswith('weak to'):
            weak_to_tokens = re.split('weak to (.+)', token)
            weak_to = weak_to_tokens[1].split(', ')
            continue
        if token.startswith('immune to'):
            immune_to_tokens = re.split('immune to (.+)', token)
            immune_to = immune_to_tokens[1].split(', ')
    return weak_to, immune_to


def who_goes_first():
    effective_power_highest = -1
    winner = None
    for army in ARMIES:
        if army in ARMIES_PICKED_TO_ATTACK:
            continue
        if army.effective_power > effective_power_highest:
            effective_power_highest = army.effective_power
            winner = army
        elif army.effective_power == effective_power_highest:
            if army.attack_damage_initiative > winner.attack_damage_initiative:
                winner = army
    ARMIES_PICKED_TO_ATTACK.append(winner)
    return winner


def get_damage_amount(attacker, target):
    attacker_latest = get_latest_army(attacker.group_type, attacker.group_num)
    damage_amount = attacker_latest.effective_power
    if attacker.attack_damage_type in target.immune_to:
        return 0
    if attacker.attack_damage_type in target.weak_to:
        return damage_amount*2
    return damage_amount


def find_army_to_target(next_attacking_army):
    most_damage = -1
    winner = None
    for army_candidate in ARMIES:
        if army_candidate == next_attacking_army:
            continue
        # cannot attack more than once
        if army_candidate in ARMIES_PICKED_TO_TARGET:
            continue
        if next_attacking_army.group_type == army_candidate.group_type:
            continue
        damage_amount = get_damage_amount(next_attacking_army, army_candidate)
        if damage_amount == 0:
            continue
        if damage_amount > most_damage:
            most_damage = damage_amount
            winner = army_candidate
        elif damage_amount == most_damage:
            if army_candidate.effective_power > winner.effective_power:
                winner = army_candidate
            elif army_candidate.effective_power == winner.effective_power:
                if army_candidate.attack_damage_initiative > winner.attack_damage_initiative:
                    winner = army_candidate
    ARMIES_PICKED_TO_TARGET.append(winner)
    return winner


def target_selection():
    next_attacking_army = who_goes_first()
    target = find_army_to_target(next_attacking_army)
    return next_attacking_army, target


def kill_units(target, how_many_killed):
    global ARMIES
    num_of_units_after = target.num_of_units - how_many_killed
    for idx, army in enumerate(ARMIES):
        if army == target:
            army.update_num_of_units(num_of_units_after)
            ARMIES[idx] = army
            break


def get_latest_army(type, number):
    for army in ARMIES:
        if type == army.group_type and number == army.group_num:
            return army
    return None


def attack(attack_groups):
    attack_groups.sort(key=lambda x: x[0].attack_damage_initiative, reverse=True)
    were_units_killed = False
    for attack_group in attack_groups:
        attacker = attack_group[0]
        target = attack_group[1]
        damage = get_damage_amount(attacker, target)
        damage_remaining = damage % target.hit_points
        units_killed = min(target.num_of_units, int((damage - damage_remaining)/target.hit_points))
        if units_killed > 0:
            were_units_killed = True
        kill_units(target, units_killed)
        # print('will kill: ' + str(units_killed) + ' units')
    return were_units_killed


def remove_dead():
    global ARMIES
    armies_alive = []
    for army in ARMIES:
        if army.num_of_units > 0:
            armies_alive.append(army)
    ARMIES = armies_alive


def get_winner():
    immune_count = 0
    infection_count = 0
    winner = None
    for army in ARMIES:
        if army.group_type == 'Infection':
            infection_count += 1
        if army.group_type == 'Immune System':
            immune_count += 1
    if immune_count == 0 or infection_count == 0:
        return "Infection" if infection_count > 0 else "Immune System"
    return winner


def get_outcome():
    outcome = 0
    for army in ARMIES:
        outcome += army.num_of_units
    return outcome


def run_one_simulation(lines, boost):
    global ARMIES, ARMIES_PICKED_TO_ATTACK, ARMIES_PICKED_TO_TARGET
    ARMIES = []
    parse(lines, boost)
    # round counter
    # do this for all
    i = 0
    winner = None
    while True:
        attack_groups = []
        ARMIES_PICKED_TO_ATTACK = []
        ARMIES_PICKED_TO_TARGET = []
        for _ in range(len(ARMIES)):
            next_attacking_army, target = target_selection()
            if target is not None:
                attack_groups.append([next_attacking_army, target])
        # attack
        were_units_killed = attack(attack_groups)
        if not were_units_killed:
            break
        remove_dead()
        winner = get_winner()
        if winner is not None:
            break
        i += 1
        # print('-------: ' + str(i))
    return winner, get_outcome()


def immune_system_simulator(lines):
    boost = 1
    while True:
        print('Boost: ' + str(boost))
        winner, outcome = run_one_simulation(lines, boost)
        if winner == "Immune System":
            return outcome
        boost += 1


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(immune_system_simulator(lines)))
