if __name__ == "__main__":
    recipe_count = open("input.txt").read().strip()

    # part 1
    scores = "37"
    elfs = [0, 1]
    remaining_recipes = int(recipe_count) + 10
    while remaining_recipes > 0:
        new_recipe = str(sum(int(scores[elf]) for elf in elfs))
        scores += new_recipe
        remaining_recipes -= len(new_recipe)
        for i in range(len(elfs)):
            elfs[i] = (elfs[i] + 1 + int(scores[elfs[i]])) % len(scores)
    print(scores[int(recipe_count):int(recipe_count) + 10])

    # part 2
    scores = "37"
    elfs = [0, 1]
    while recipe_count not in scores[-10:]:
        scores += str(sum(int(scores[elf]) for elf in elfs))
        for i in range(len(elfs)):
            elfs[i] = (elfs[i] + 1 + int(scores[elfs[i]])) % len(scores)
    print(scores.index(recipe_count, -10))