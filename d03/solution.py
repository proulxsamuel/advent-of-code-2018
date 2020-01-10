import re
from collections import defaultdict

if __name__ == "__main__":
    
    claims = defaultdict(list)
    squares = defaultdict(list)
    for line in open("input.txt"):
        n, l, t, w, h = tuple(int(match) for match in re.findall(r"\d+", line))
        for x in range(l, l + w):
            for y in range(t, t + h):
                position = (x, y)
                claims[n].append(position)
                squares[position].append(n)
    
    # part 1
    print(len([square for square in squares.values() if len(square) > 1]))
    
    # part 2
    print(next(number for number, claim in claims.items()
               if all(len(squares[position]) == 1 for position in claim)))