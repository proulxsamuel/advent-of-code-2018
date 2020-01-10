from collections import Counter

if __name__ == "__main__":
    with open("input.txt") as file:
        boxes = [line.strip() for line in file]
    letters = len(boxes[0])
    
    # part 1
    doubles = set()
    triples = set()
    for box in boxes:
        counter = Counter(box)
        for count in counter.values():
            if count == 2:
                doubles.add(box)
            elif count == 3:
                triples.add(box)
    print(len(doubles) * len(triples))

    # part 2
    def common():
        for i in range(0, len(boxes) - 1):
            for j in range(i + 1, len(boxes)):
                matches = len([x for x, y in zip(boxes[i], boxes[j]) if x == y])
                if matches == letters - 1:
                    return ''.join(x for x, y in zip(boxes[i], boxes[j]) if x == y)
    print(common())