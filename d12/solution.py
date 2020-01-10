import re


def grow(state, rules):
    previous_sum = sum(state)
    generation = 1
    while True:
        next_state = set()
        start = min(state) - 2 if len(state) > 0 else -2
        end = max(state) + 2 if len(state) > 0 else 2
        for i in range(start, end + 1):
            for rule in rules:
                far_left, left, center, right, far_right = rule
                if ((i - 2 in state) == far_left
                        and (i - 1 in state) == left
                        and (i in state) == center
                        and (i + 1 in state) == right
                        and (i + 2 in state) == far_right):
                    next_state.add(i)
                    break
        state = next_state
        current_sum = sum(state)
        yield generation, current_sum, current_sum - previous_sum
        previous_sum = current_sum
        generation += 1


if __name__ == "__main__":
    rules = []
    for line in open("input.txt"):
        line = line.strip()
        if line.startswith("initial state"):
            initial_state = set()
            for i in range(15, len(line)):
                if line[i] == '#':
                    initial_state.add(i - 15)
        elif line != "":
            match = re.match(r"([\.#]{5}) => ([\.#])", line)
            configuration = tuple(pot == '#' for pot in match.group(1))
            outcome = match.group(2)
            if outcome == '#':
                rules.append(configuration)

    # part 1
    growth = grow(initial_state, rules)
    for _ in range(20):
        generation, total, difference = next(growth)
    print(total)

    # part 2
    growth = grow(initial_state, rules)
    generations = []
    for _ in range(500):
        generations.append(next(growth))
    for i in range(len(generations)):
        generation, total, difference = generations[i]
        if all(d == difference for g, t, d in generations[i + 1:]):
            break
    print(total + (50000000000 - generation) * difference)