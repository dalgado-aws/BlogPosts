#!/usr/bin/env python3


def change(amount, options):
    if not amount:  # zero amount left. We have a valid solution path
        return [[]]
    elif amount < 0:
        return []
    else:
        solutions = []
        for i, option in enumerate(options):  # consider every option
            option = options[i]
            rest = options[i+1:]
            for option_amount in range(option, amount + 2, option):  # generate option x 0, option x 1, option x2 ....
                remaining_amount = amount - option_amount
                change_for_remaining = change(remaining_amount, rest)

                this_plus = [x[:] + ["${}x{}".format(option, int(option_amount/option))] for x in change_for_remaining]

                solutions.extend(this_plus)

        return solutions


if __name__ == "__main__":
    solutions = change(10, [2, 3, 5])
    for solution in solutions:
        print(solution)

