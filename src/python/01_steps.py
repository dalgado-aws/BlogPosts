#!/usr/bin/env python


def steps_1(remaining_steps, partial_path, all_paths):
    # partial path gets added to all_paths
    # all_paths will contain the final result
    if remaining_steps < 0:
        pass
    elif remaining_steps == 0:
        all_paths.append(partial_path)
    else:
        steps_1(remaining_steps - 1, partial_path[:] + [1], all_paths)
        steps_1(remaining_steps - 2, partial_path[:] + [2], all_paths)
        steps_1(remaining_steps - 3, partial_path[:] + [3], all_paths)
    return all_paths


def steps_2(remaining_steps, partial_path):
    # still using partial paths, but no all_paths
    all_paths = []
    if remaining_steps < 0:
        pass
    elif remaining_steps == 0:
        all_paths.append(partial_path)
    else:
        all_paths.extend(steps_2(remaining_steps - 1, partial_path[:] + [1]))
        all_paths.extend(steps_2(remaining_steps - 2, partial_path[:] + [2]))
        all_paths.extend(steps_2(remaining_steps - 3, partial_path[:] + [3]))
    return all_paths


def steps_3(remaining):
    all_paths = []
    if not remaining:
        all_paths.extend([[]])
    elif remaining < 0:
        pass
    else:
        one_paths = steps_3(remaining - 1)
        five_paths = steps_3(remaining - 2)
        ten_paths = steps_3(remaining - 3)

        all_paths.extend(list(map(lambda x: x[:] + [1], one_paths)))
        all_paths.extend(list(map(lambda x: x[:] + [2], five_paths)))
        all_paths.extend(list(map(lambda x: x[:] + [3], ten_paths)))

    return all_paths


if __name__ == "__main__":
    results = steps_1(5, [], [])
    for i, result in enumerate(results):
        print(i,  result)

    results = steps_2(5, [])
    for i, result in enumerate(results):
        print(i, result)

    results = steps_3(5)
    for i, result in enumerate(results):
        print(i, result)
