import re
from collections import defaultdict, deque


def highest_score(player_count, last_marble):
    circle = deque([0])
    scores = defaultdict(int)
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % player_count] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return(max(scores.values()))


if __name__ == "__main__":
    numbers = re.findall(r"\d+", open("input.txt").read())
    player_count, last_marble = tuple(int(number) for number in numbers)
    
    # part 1
    print(highest_score(player_count, last_marble))

    # part 2
    print(highest_score(player_count, last_marble * 100))