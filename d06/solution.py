import re
from collections import defaultdict

def distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x2 - x1) + abs(y2 - y1)

if __name__ == "__main__":
    coords = [tuple(int(match) for match in re.findall(r"\d+", line))
              for line in open("input.txt")]
    min_x, max_x = min(x for x, y in coords), max(x for x, y in coords)
    min_y, max_y = min(y for x, y in coords), max(y for x, y in coords)
    
    areas = defaultdict(int)
    infinite = set()
    safe = set()
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            position = (i, j)
            distances = {coord: distance(coord, position) for coord in coords}
            
            # part 1
            shortest = min(distances.values())
            matches = [coord for coord, distance in distances.items()
                       if distance == shortest]
            if len(matches) == 1:
                match = matches[0]
                areas[match] += 1
                if i == min_x or i == max_x or j == min_y or j == max_y:
                    infinite.add(match)
            
            # part 2
            total_distance = sum(distances.values())
            if total_distance < 10000:
                safe.add(position)

    print(max(area for coord, area in areas.items() if coord not in infinite))
    print(len(safe))