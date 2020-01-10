from collections import defaultdict
from copy import deepcopy

if __name__ == "__main__":
    steps = set()
    requirements = defaultdict(list)
    for line in open("input.txt"):
        step = line[36]
        prerequisite = line[5]
        steps.add(step)
        steps.add(prerequisite)
        requirements[step].append(prerequisite)

    # part 1
    order = []
    contraints = deepcopy(requirements)
    remaining = deepcopy(steps)
    while len(remaining) > 0:
        next_step = min(step for step in remaining
                        if len(contraints[step]) == 0)
        remaining.remove(next_step)
        for prerequisites in contraints.values():
            try:
                prerequisites.remove(next_step)
            except ValueError:
                pass
        order.append(next_step)
    print(''.join(order))

    # part 2
    completed = set()
    workers = [(None, 0) for _ in range(5)]
    second = 0
    while True:
        for i in range(len(workers)):
            step, time = workers[i]
            if step is not None and time == 0:
                completed.add(step)
                workers[i] = (None, 0)
        for i in range(len(workers)):
            try:
                next_step = next(step for step in order
                                 if all(step in completed
                                        for step in requirements[step]))
            except StopIteration:
                break
            step, time = workers[i]
            if step is None:
                workers[i] = (next_step, 60 + ord(next_step) - ord('A') + 1)
                order.remove(next_step)
        for i in range(len(workers)):
            step, time = workers[i]
            if step is not None:
                workers[i] = (step, time - 1)
        if len(order) == 0 and all(step is None for step, time in workers):
            break
        second += 1
    print(second)