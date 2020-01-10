class Cart:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.turns = 0


if __name__ == "__main__":
    tracks = [line.strip('\n') for line in open("input.txt")]
    carts = []
    for y in range(len(tracks)):
        row = tracks[y]
        for x in range(len(row)):
            square = row[x]
            if square in "^<v>":
                orientation, track = {
                    '^': ((0, -1), '|'),
                    '<': ((-1, 0), '-'),
                    'v': ((0, 1), '|'),
                    '>': ((1, 0), '-'),
                }[square]
                tracks[y] = tracks[y][:x] + track + tracks[y][x + 1:]
                carts.append(Cart((x, y), orientation))
    number_of_carts = len(carts)
    
    i = 1
    while len(carts) > 1:
        for cart in sorted(carts, key=lambda cart: cart.position):
            x, y = cart.position
            dx, dy = cart.orientation
            nx, ny = (x + dx, y + dy)
            cart.position = (nx, ny)
            track = tracks[ny][nx]
            if track == '\\':
                cart.orientation = tuple(reversed(cart.orientation))
            elif track == '/':
                cart.orientation = tuple(map(lambda n: -n, reversed(cart.orientation)))
            elif track == '+':
                if cart.turns % 3 == 0:
                    cart.orientation = {
                        (0, -1): (-1, 0),
                        (-1, 0): (0, 1),
                        (0, 1): (1, 0),
                        (1, 0): (0, -1),
                    }[cart.orientation]
                elif cart.turns % 3 == 2:
                    cart.orientation = {
                        (0, -1): (1, 0),
                        (-1, 0): (0, -1),
                        (0, 1): (-1, 0),
                        (1, 0): (0, 1),
                    }[cart.orientation]
                cart.turns += 1
            for other in carts:
                if other is not cart and other.position == cart.position:
                    if len(carts) == number_of_carts:
                        print(f"{nx},{ny}")
                    carts.remove(cart)
                    carts.remove(other)
                    break
        i += 1
    x, y = carts[0].position
    print(f"{x},{y}")