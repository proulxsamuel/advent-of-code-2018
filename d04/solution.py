import re
from collections import defaultdict

if __name__ == "__main__":

    records = defaultdict(lambda: defaultdict(int))
    for line in sorted(line.strip() for line in open("input.txt")):
        time = int(line[15:17])
        state = line[19:]

        if state.startswith("Guard"):
            guard = int(re.search("\d+", state).group())
        elif state.startswith("falls asleep"):
            start = time
        elif state.startswith("wakes up"):
            for minute in range(start, time):
                records[guard][minute] += 1

    # part 1
    sleep = {guard: sum(minutes.values())
             for guard, minutes in records.items()}
    guard = max(sleep, key=sleep.get)
    minute = max(records[guard], key=records[guard].get)
    print(guard * minute)

    # part 2
    sleep = {guard: max(minutes, key=minutes.get)
             for guard, minutes in records.items()}
    guard = max(sleep, key=lambda i: records[i][sleep[i]])
    minute = sleep[guard]
    print(guard * minute)