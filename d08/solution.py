class Node:
    def __init__(self, numbers):
        children_count = next(numbers)
        metadata_count = next(numbers)
        self.children = [Node(numbers) for _ in range(children_count)]
        self.metadata = [next(numbers) for _ in range(metadata_count)]

    def recursive_metadata_sum(self):
        return (sum(self.metadata)
            + sum(child.recursive_metadata_sum() for child in self.children))

    def recursive_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        else:
            return sum(self.children[i - 1].recursive_value()
                       for i in self.metadata if i - 1 < len(self.children))


if __name__ == "__main__":
    numbers = (int(number) for number in open("input.txt").read().split(' '))
    root = Node(numbers)
    
    # part 1
    print(root.recursive_metadata_sum())

    # part 2
    print(root.recursive_value())