#!/usr/bin/env python3


def permute(choices):
    if not choices:
        return [[]]
    else:
        all_results = []
        for i, this in enumerate(choices):
            rest = [choices[j] for j in range(len(choices)) if j != i]
            permute_rest = permute(rest)
            this_and_permutations = [[this] + permute_rest[k] for k in range(len(permute_rest))]
            all_results.extend(this_and_permutations)
    return all_results


if __name__ == "__main__":
    permutations = permute("abc")
    for r in permutations:
        print(r)

