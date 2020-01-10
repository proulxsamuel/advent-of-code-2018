def find_neighbors(area, x, y):
    neighbors = []
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if not (i == y and j == x) and not (i < 0 or j < 0):
                try:
                    neighbors.append(area[i][j])
                except IndexError:
                    pass
    return neighbors


def grow(area):
    previous_value = (sum(len([acre for acre in row if acre == '|']) for row in area)
            * sum(len([acre for acre in row if acre == '#']) for row in area))
    minute = 1
    while True:
        updated_area = [['' for acre in row] for row in area]
        for y, row in enumerate(area):
            for x, acre in enumerate(row):
                neighbors = find_neighbors(area, x, y)
                if acre == '.':
                    if len([n for n in neighbors if n == '|']) >= 3:
                        updated_area[y][x] = '|'
                    else:
                        updated_area[y][x] = '.'
                elif acre == '|':
                    if len([n for n in neighbors if n == '#']) >= 3:
                        updated_area[y][x] = '#'
                    else:
                        updated_area[y][x] = '|'
                elif acre == '#':
                    if (len([n for n in neighbors if n == '#']) >= 1
                            and len([n for n in neighbors if n == '|']) >= 1):
                        updated_area[y][x] = '#'
                    else:
                        updated_area[y][x] = '.'
                else:
                    raise ValueError
        area = updated_area
        value = (sum(len([acre for acre in row if acre == '|']) for row in area)
            * sum(len([acre for acre in row if acre == '#']) for row in area))
        yield (minute, value, value - previous_value)
        previous_value = value
        minute += 1


if __name__ == "__main__":
    area = [[acre for acre in row.strip()] for row in open("input.txt")]

    # part 1
    growth = grow(area)
    for _ in range(10):
        minute, value, difference = next(growth)
    print(value)

    # part 2
    growth = grow(area)
    minutes = []
    for _ in range(600):
        minutes.append(next(growth))
        try:
            previous = next(m for m, v, d in minutes[:-1] if v == minutes[-1][1])
            other = next(m for m, v, d in minutes[:-2] if v == minutes[-2][1])
            if other == previous - 1:
                break
        except StopIteration:
            pass
    start = other
    end = minutes[-3][0]
    values = [v for m, v, d in minutes if 477 <= m <= 504]
    print(values[(1000000000 - start) % (end - start + 1)])