import re


class Point:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position = tuple(map(sum, zip(self.position, self.velocity)))


if __name__ == "__main__":

    points = []
    for line in open("input.txt"):
        n = [int(number) for number in re.findall(r"-?\d+", line)]
        points.append(Point((n[0], n[1]), (n[2], n[3])))
    
    for i in range(0, 100000):
        positions = set(point.position for point in points)
        min_y = min(y for x, y in positions)
        max_y = max(y for x, y in positions)
        
        # draw
        if max_y - min_y <= 10:
            min_x = min(x for x, y in positions)
            max_x = max(x for x, y in positions)
            
            # part 1
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    print('#' if (x, y) in positions else '.', end='')   
                print()
            
            # part 2
            print(i)

            break
        
        # update
        for point in points:
            point.update()