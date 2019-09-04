# e.g.
# steps = [0,1,0,2,1,0,1,3,2,1,2,1]
# ponding = 6


def calc_total_ponding(steps):
    ponding = 0
    start = 0
    while start < len(steps):
        left_half = if_decreasing(steps, start)
        left_length = len(left_half)
        start += left_length
        if left_length <= 1:
            continue
        else:
            right_half = if_increasing(steps, start - 1)
            right_half = right_half[1:]
            right_length = len(right_half)
            start += right_length - 1
            if right_length == 0:
                continue
            else:
                pit = left_half + right_half
                ponding += calc_pit_ponding(pit)
    return ponding


def if_decreasing(steps, start):
    total = len(steps)
    for index in range(start, total - 1):
        if steps[index] <= steps[index + 1]:
            return steps[start:(index + 1)]
    return [-1]


def if_increasing(steps, start):
    steps += [0]
    total = len(steps)
    for index in range(start, total - 1):
        if steps[index] >= steps[index + 1]:
            return steps[start:(index + 1)]
    return [-1]


def calc_pit_ponding(pit):
    ponding = 0
    low_step = min(pit[0], pit[-1])
    for step in pit:
        if step < low_step:
            ponding += low_step - step
    return ponding


print(calc_total_ponding([0,1,0,2,1,0,1,3,2,1,2,1]))
