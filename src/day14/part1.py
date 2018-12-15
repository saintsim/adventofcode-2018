#!/usr/bin/env python3


def add_new_recipe(recipes, elf1_current, elf2_current):
    new_recipe = recipes[elf1_current] + recipes[elf2_current]
    for i in str(new_recipe):
        recipes.append(int(i))
    return recipes


def recipe_scores(after_recipes, last_recipes):
    elf_current = [0, 1]
    recipes = [3, 7]
    recipes = add_new_recipe(recipes, elf_current[0], elf_current[1])
    # now move, 1 + current recipe amount
    i = 0
    while len(recipes) < (after_recipes + last_recipes):
        recipes = add_new_recipe(recipes, elf_current[0], elf_current[1])
        for elf in range(2):
            elf_move = 1 + recipes[elf_current[elf]]
            elf_new_index = elf_current[elf] + elf_move
            if elf_new_index >= len(recipes):
                elf_new_index = elf_new_index % (len(recipes))
            elf_current[elf] = elf_new_index
        print(str(i))
        i += 1
        # print(elf_current)
        # for idx, r in enumerate(recipes):
        #     if elf_current[0] == idx:
        #         print('(' + str(r) + ') ', end='')
        #     elif elf_current[1] == idx:
        #         print('[' + str(r) + '] ', end='')
        #     else:
        #         print(str(r) + ' ', end='')
        # print('\n', end='')
        # print('-----')
    result_list = recipes[after_recipes:after_recipes+last_recipes]
    result = ''
    for r in result_list:
        result += str(r)
    return result


if __name__ == '__main__':
    print('Result: ' + str(recipe_scores(323081, 10)))
