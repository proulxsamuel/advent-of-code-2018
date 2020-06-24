import re


class Grid:
    def __init__(self, scan, spring=500):
        coordinates = []
        for axis, (position, start, end) in scan:
            for i in range(start, end + 1):
                coordinate = (position, i) if axis == 'x' else (i, position)
                coordinates.append(coordinate)
        self._xi = min(x for x, _ in coordinates) - 1
        self._xf = max(x for x, _ in coordinates) + 1
        self._yi = min(y for _, y in coordinates)
        self._yf = max(y for _, y in coordinates)
        self._width = self._xf - self._xi + 1
        self._height = self._yf - self._yi + 1
        self.grid = [['.' for _ in range(self._width)] for _ in range(self._height)]
        for x, y in coordinates:
            self.set(x, y, '#')
        self.spring = spring

    def at(self, x, y):
        return self.grid[y - self._yi][x - self._xi]

    def set(self, x, y, value):
        self.grid[y - self._yi][x - self._xi] = value

    def simulate(self):
        def fill(x, y):
            pass

        def spill(x, y):
            xi, yi = x, y
            while True:
                x -= 1
                if self.at(x, y) == '#':
                    left_wall = True
                    break
                if self.at(x, y + 1) == '.':
                    flow(x, y)
                else:
                    self.set(x, y, '|')
            x = xi
            while True:
                x += 1
                if self.at(x, y) == '#':
                    right_wall = True
                    break
                if self.at(x, y + 1) == '.':
                    flow(x, y)
                else:
                    self.set(x, y, '|')
            if left_wall and right_wall:
                fill(xi, yi)

        def flow(x, y):
            while y <= self._yf and self.at(x, y) == '.':
                self.set(x, y, '|')
                y += 1
            spill(x, y - 1)

        flow(self.spring, 1)

    def __repr__(self):
        first = ''.join('+' if i == self.spring - self._xi else '.' for i in range(self._width))
        return first + '\n' + '\n'.join(''.join(row) for row in self.grid)


if __name__ == "__main__":
    regex = re.compile(r'\d+')
    with open('input.txt') as file:
        scan = [(line[0], tuple(int(number) for number in regex.findall(line)))
                for line in file]
    grid = Grid(scan)
    #grid.simulate()
    print(grid)