#!/usr/bin/env python3

MAX_X = 10
MAX_Y = 10


def move_robot(current, dest):
    x, y = current
    if current == dest:
        return [[]]
    elif x > MAX_X or x < 0 or y > MAX_Y or y < 0:
        return []
    else:
        paths = []
        down = x, y - 1
        down_paths = move_robot(down, dest)
        if down_paths:
            down_paths_with_current = [["down", down] + p[:] for p in down_paths]
            paths.extend(down_paths_with_current)

        right = x + 1, y
        right_paths = move_robot(right, dest)
        if right_paths:
            right_paths_with_current = [["right", right] + p[:] for p in right_paths]
            paths.extend(right_paths_with_current)

        return paths


if __name__ == "__main__":
    all_paths = move_robot((3, 7), (6, 4))
    for path in all_paths:
        print(path)
