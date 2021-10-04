#!/usr/bin/env python3


def power_set(set_elements):
    if not set_elements:
        return [[]]
    else:
        all_results = []

        this = set_elements[:1]
        rest = set_elements[1:]

        power_set_for_rest = power_set(rest)
        with_this = [this + x for x in power_set_for_rest]
        without_this = power_set_for_rest

        all_results.extend(with_this)
        all_results.extend(without_this)

        return all_results


if __name__ == "__main__":
    for i, r in enumerate(power_set([1, 2, 3, 4]), 1):
        print(i, "   ", r)

