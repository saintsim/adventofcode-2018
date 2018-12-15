#!/usr/bin/env python3


def add_new_recipe(recipes, elf1_current, elf2_current):
    new_recipe = recipes[elf1_current] + recipes[elf2_current]
    for i in str(new_recipe):
        recipes.append(int(i))
    return recipes


def find_number_in_sequence(recipes, number_to_find):
    print('checking...')
    for idx, r in enumerate(recipes):
        match = True
        if len(recipes)-idx < len(number_to_find):
            return 'Can\'t find it'
        for to_find_idx, num in enumerate(number_to_find):
            if recipes[idx+to_find_idx] != int(num):
                match = False
                break
        if match is True:
            return idx


def recipe_scores(search_amount, number_to_find):
    elf_current = [0, 1]
    recipes = [3, 7]
    recipes = add_new_recipe(recipes, elf_current[0], elf_current[1])
    # now move, 1 + current recipe amount
    while len(recipes) < search_amount:
        recipes = add_new_recipe(recipes, elf_current[0], elf_current[1])
        for elf in range(2):
            elf_move = 1 + recipes[elf_current[elf]]
            elf_new_index = elf_current[elf] + elf_move
            if elf_new_index >= len(recipes):
                elf_new_index = elf_new_index % (len(recipes))
            elf_current[elf] = elf_new_index
    return find_number_in_sequence(recipes, number_to_find)


if __name__ == '__main__':
    number_of_recipes = 30000000
    string_to_find = '323081'
    print('Result: ' + str(recipe_scores(number_of_recipes, string_to_find)))
