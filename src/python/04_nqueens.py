#!/usr/bin/env python3


def valid_combination(partial_solution):
    """

    :param partial_solution:
    :return:
    """
    raise Exception("Not Implemented")


def n_queens(n, partial_solution, all_solutions):
    if len(partial_solution) == n:
        all_solutions.append(partial_solution)
    else:
        for i in range(n):
            next_partial = partial_solution[:] + [i]
            if valid_combination(next_partial):
                n_queens(n, next_partial, all_solutions)
