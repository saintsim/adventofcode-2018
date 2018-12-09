import re
import operator


class SleepingData:
    def __init__(self, hour, min, instruction):
        self.hour = int(hour)
        self.min = int(min)
        self.instruction = instruction
        if instruction.startswith("Guard"):
            self.state = 1
            self.guard_id = re.split('Guard #([0-9]+)', instruction)[1]
            pass
        elif instruction == 'falls asleep':
            self.state = 2
        else:
            self.state = 3 # wakes up


# year-month-day hour:minute format
# [1518-11-01 00:00] Guard #10 begins shift
# [1518-11-01 00:05] falls asleep
# [1518-11-01 00:25] wakes up
def parse(line):
    result = re.split('\[[0-9]{4}-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\][\s]*(.*)', line)
    data = SleepingData(result[3], result[4], result[5])
    return data


def gen_empty_array():
    arr = []
    for i in range(0,60):
        arr.append(0)
    return arr


def get_slept_most(sleeping):
    slept_most_mins = 0
    slept_most_id = 0

    for key, value in sleeping.items():
        asleep_mins = sum(value)
        if asleep_mins > slept_most_mins:
            slept_most_mins = asleep_mins
            slept_most_id = key

    return slept_most_id


def get_asleep_most_min(sleeping_mins):
    slept_most = 0
    slept_most_min = 0
    for idx, mins in enumerate(sleeping_mins):
        if mins > slept_most:
            slept_most = mins
            slept_most_min = idx

    return slept_most_min


def max_min(sleeping):
    slept_most_mins = 0
    slept_most_id = 0
    slept_most_min = 0

    for key, value in sleeping.items():
        slept_most_min_candidate, asleep_mins = max(enumerate(value), key=operator.itemgetter(1))
        if asleep_mins > slept_most_mins:
            slept_most_mins = asleep_mins
            slept_most_id = key
            slept_most_min = slept_most_min_candidate

    return int(slept_most_id) * slept_most_min


def guard_sleeping_solution(lines):
    instructions = []
    lines.sort()
    for line in lines:
        instructions.append(parse(line))

    sleeping = dict()
    guard_id = 0
    sleep_at = 0
    for instruction in instructions:
        if instruction.state == 1:
            guard_id = instruction.guard_id
        elif instruction.state == 2:
            sleep_at = instruction.min
        else:
            if sleeping.get(guard_id) is None:
                sleeping_mins = gen_empty_array()
            else:
                sleeping_mins = sleeping.get(guard_id)
            for asleep_min in list(range(sleep_at,instruction.min)):
                sleeping_mins[asleep_min] += 1
            sleeping[guard_id] = sleeping_mins

    slept_most_id = get_slept_most(sleeping)
    asleep_most_min = get_asleep_most_min(sleeping[slept_most_id])
    max_answer = max_min(sleeping)

    return int(slept_most_id) * asleep_most_min


if __name__ == '__main__':
    with open('input', 'r') as file:
        lines = file.readlines()
        print('Result: ' + str(guard_sleeping_solution(lines)))