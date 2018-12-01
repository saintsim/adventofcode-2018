def solve():
    with open('input', 'r') as file:
        data = file.readlines()
        totals_found = set([])
        total = 0
        while True:
            for x in data:
                total = total + int(x)
                if total in totals_found:
                    return total
                else:
                    totals_found.add(total)


result = solve()
print('Result: ' + str(result))
