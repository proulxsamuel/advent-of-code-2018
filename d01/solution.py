if __name__ == "__main__":
    with open("input.txt") as file:
        numbers = [int(number) for number in file.readlines()]
    
    # part 1
    print(sum(numbers))
    
    # part 2
    frequencies = set()
    frequency = 0
    i = 0
    while True:
        frequency += numbers[i % len(numbers)]
        if frequency in frequencies:
            break
        frequencies.add(frequency)
        i += 1
    print(frequency)