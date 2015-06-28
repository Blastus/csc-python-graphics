#! /usr/bin/env python3
import itertools
import math
import turtle

DEFAULT = ((501, 248),
           (104, 952),
           (996, 1262),
           (1091, 826),
           (1193, 952),
           (2242, 1394),
           (1628, 1726),
           (1298, 1664),
           (1072, 1868),
           (977, 2696),
           (811, 2668),
           (351, 3072))

ALT1 = ((501, 248),
        (104, 952),
        (1091, 826),
        (1193, 952),
        (996, 1262),
        (2242, 1394),
        (1628, 1726),
        (1298, 1664),
        (1072, 1868),
        (977, 2696),
        (811, 2668),
        (351, 3072))

ALT2 = ((501, 248),
        (104, 952),
        (1193, 952),
        (1091, 826),
        (996, 1262),
        (2242, 1394),
        (1628, 1726),
        (1298, 1664),
        (1072, 1868),
        (977, 2696),
        (811, 2668),
        (351, 3072))

COORDINATES = DEFAULT


def main():
    screen = turtle.Screen()
    screen.reset()
    height, width = screen.window_height(), screen.window_width()
    screen.setworldcoordinates(0, height, width, 0)
    margin = 10
    x_scale = (width - margin) / max(c[0] for c in COORDINATES)
    y_scale = (height - margin) / max(c[1] for c in COORDINATES)
    reptile = turtle.Turtle()
    reptile.penup()
    x, y = COORDINATES[0]
    reptile.goto(x * x_scale, y * y_scale)
    reptile.pendown()
    for x, y in COORDINATES:
        reptile.goto(x * x_scale, y * y_scale)
        reptile.dot()
    reptile.hideturtle()
    screen.mainloop()


def test():
    assert min(COORDINATES, key=lambda c: c[1]) == COORDINATES[0]
    assert next(iter(best_path())) == COORDINATES


def best_path():
    best_length, results = float('inf'), set()
    for p in permute_paths():
        total = total_length(p)
        if total < best_length:
            best_length, results = total, {p}
        elif total == best_length:
            results.add(p)
    return results


def permute_paths():
    for p in itertools.permutations(COORDINATES[1:]):
        yield (COORDINATES[0],) + p


def total_length(path):
    return sum(length(path[i], path[i + 1]) for i in range(len(path) - 1))


def length(p1, p2):
    # return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

if __name__ == '__main__':
    main()
