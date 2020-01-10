from string import ascii_lowercase


def react(polymer):
    i = 0
    while i < len(polymer) - 1:
        x = polymer[i]
        y = polymer[i + 1]
        if x != y and x.lower() == y.lower():
            polymer = polymer[:i] + polymer[i+2:]
            i = max(0, i - 1)
            continue
        i += 1
    return polymer


def remove(polymer, unit):
    return polymer.replace(unit, '').replace(unit.upper(), '')


if __name__ == "__main__":
    polymer = open("input.txt").read()

    # part 1
    print(len(react(polymer)))
    
    # part 2
    print(min(len(react(remove(polymer, char))) for char in ascii_lowercase))