from copy import deepcopy


class Cell:
    pass


class Wall(Cell):
    def __repr__(self):
        return '#'


class Cavern(Cell):
    def __repr__(self):
        return '.'


class Unit(Cell):
    def __init__(self):
        self.health = 200
        self.attack = 3
        self.position = (0, 0)

    def is_alive(self):
        return self.health > 0

    def damage(self, amount):
        self.health -= amount

    def move(self, position, map):
        current = map.at(position)
        assert(isinstance(current, Cavern))
        map.set(self.position, current)
        map.set(position, self)
        self.position = position


class Elf(Unit):
    def __init__(self):
        super().__init__()

    def can_target(self, cell):
        return isinstance(cell, Goblin)

    def __repr__(self):
        return 'E'


class Goblin(Unit):
    def __init__(self):
        super().__init__()

    def can_target(self, cell):
        return isinstance(cell, Elf)

    def __repr__(self):
        return 'G'


class Map:
    def __init__(self, grid):
        self._grid = grid

    @classmethod
    def parse(cls, grid):
        def parse_char(char):
            if char == '#': return Wall()
            if char == 'E': return Elf()
            if char == 'G': return Goblin()
            assert(char == '.')
            return Cavern()
        new_grid = []
        for (y, row) in enumerate(grid):
            new_row = []
            for (x, char) in enumerate(row):
                cell = parse_char(char)
                if isinstance(cell, Unit):
                    cell.position = (x, y)  
                new_row.append(cell)
            new_grid.append(new_row)
        return cls(new_grid)

    def copy(self):
        return Map(deepcopy(self._grid))

    def at(self, position):
        x, y = position
        return self._grid[y][x]

    def set(self, position, cell):
        x, y = position
        self._grid[y][x] = cell

    def __iter__(self):
        for (y, row) in enumerate(self._grid):
            for (x, cell) in enumerate(row):
                yield ((x, y), cell)

    def __repr__(self):
        string = ''
        for row in self._grid:
            row_units = []
            for cell in row:
                string += repr(cell)
                if isinstance(cell, Unit):
                    row_units.append(cell)
            if len(row_units) != 0:
                string += '   '
                string += ', '.join(f'{repr(unit)}({unit.health})' for unit in row_units)
            string += '\n'
        return string


def add(position, offset):
    xi, yi = position
    xo, yo = offset
    return (xi + xo, yi + yo)


def try_attack(unit, map):
    def attack(target):
        target.damage(unit.attack)
        if not target.is_alive():
            map.set(target.position, Cavern())
    adjacent = (map.at(add(unit.position, offset)) for offset in [(0, -1), (-1, 0), (1, 0), (0, 1)])
    targets = (cell for cell in adjacent if unit.can_target(cell))
    targets = list(sorted(targets, key = lambda unit: unit.health))
    if len(targets) == 0:
        return False
    if len(targets) > 1 and targets[0].health == targets[1].health:
        targets = list(target for target in targets if target.health == targets[0].health)
        targets = list(sorted(sorted(targets, key = lambda unit: unit.position[0]), key = lambda unit: unit.position[1]))
    attack(targets[0])
    return True


def try_move(unit, targets, map):
    targets = (add(target.position, offset) for target in targets for offset in [(0, -1), (-1, 0), (1, 0), (0, 1)])
    targets = [target for target in targets if isinstance(map.at(target), Cavern)]
    distances = {unit.position: 0}
    origins = {}
    adjacent = (add(unit.position, offset) for offset in [(0, -1), (-1, 0), (1, 0), (0, 1)])
    adjacent = [position for position in adjacent if isinstance(map.at(position), Cavern) and position not in distances]
    for position in adjacent:
        distances[position] = 1
        origins[position] = unit.position
    i = 2
    while len(adjacent) > 0:
        next_adjacent = []
        for position in adjacent:
            for offset in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                next_position = add(position, offset)
                if next_position not in next_adjacent and isinstance(map.at(next_position), Cavern) and next_position not in distances:
                    next_adjacent.append(next_position)
                    distances[next_position] = i
                    origins[next_position] = position
        adjacent = next_adjacent
        i += 1
    targets = (target for target in targets if target in distances)
    targets = list(sorted(targets, key = lambda target: distances[target]))
    if len(targets) == 0:
        return False
    if len(targets) > 1 and distances[targets[0]] == distances[targets[1]]:
        targets = list(target for target in targets if distances[target] == distances[targets[0]])
        targets = list(sorted(sorted(targets, key = lambda position: position[0]), key = lambda position: position[1]))
    target = targets[0]
    while origins[target] != unit.position:
        target = origins[target]
    unit.move(target, map)
    return True


class NoTargetException(Exception):
    pass


def simulate_combat(map):
    i = 0
    try:
        while True:
            #print(f'\nAfter {i} round:' if i != 0 else 'Initially:')
            #print(repr(map))
            turn_order = [cell for _, cell in map if isinstance(cell, Unit)]
            for unit in turn_order:
                if not unit.is_alive():
                    continue
                targets = [cell for _, cell in map if unit.can_target(cell)]
                if len(targets) == 0:
                    raise NoTargetException()
                if not try_attack(unit, map) and try_move(unit, targets, map):
                    try_attack(unit, map)
                #print(f'\nAfter unit {turn_order.index(unit)}:')
                #print(repr(map))
            i += 1
    except NoTargetException:
        #print('\nFinal:')
        #print(repr(map))
        return i * sum(cell.health for _, cell in map if isinstance(cell, Unit))


def optimize_attack(map):
    elf_count = sum(1 for _, cell in map if isinstance(cell, Elf))
    i = 4
    while True:
        new_map = map.copy()
        for _, cell in new_map:
            if isinstance(cell, Elf):
                cell.attack = i
        outcome = simulate_combat(new_map)
        if sum(1 for _, cell in new_map if isinstance(cell, Elf)) != elf_count:
            i += 1
            continue
        return outcome


if __name__ == "__main__":
    with open('input.txt') as file:
        map = Map.parse([[char for char in line.strip()] for line in file])

    print(simulate_combat(map.copy()))
    print(optimize_attack(map))