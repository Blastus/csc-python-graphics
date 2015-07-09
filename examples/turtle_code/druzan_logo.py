#! /usr/bin/env python3

__version__ = 2, 0, 0
__date__ = '27 June 2015'
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__credits__ = '''Guido van Rossum, Dutch computer programmer & Python's author.
Gregor Lingl, creator of Python's turtle module that powers this program.'''

import math
import turtle


def main():
    radius = 20
    screen = turtle.Screen()
    screen.reset()
    reptile = turtle.Turtle()
    reptile.circle(radius)
    reptile.left(60)
    inv = math.pi / 180
    unit_distance = math.sin(120 * inv) * radius / math.sin(30 * inv)
    reptile.begin_fill()
    reptile.forward(unit_distance)
    reptile.left(120)
    reptile.forward(unit_distance)
    reptile.left(120)
    reptile.forward(unit_distance)
    reptile.end_fill()
    reptile.begin_fill()
    reptile.forward(unit_distance)
    reptile.right(120)
    reptile.forward(unit_distance)
    reptile.right(120)
    reptile.forward(unit_distance)
    reptile.end_fill()
    reptile.up()
    reptile.forward(unit_distance)
    reptile.down()
    reptile.begin_fill()
    reptile.forward(unit_distance)
    reptile.right(120)
    reptile.forward(unit_distance)
    reptile.right(120)
    reptile.forward(unit_distance)
    reptile.end_fill()
    reptile.up()
    reptile.forward(unit_distance)
    reptile.down()
    reptile.begin_fill()
    reptile.forward(unit_distance)
    reptile.right(120)
    reptile.forward(unit_distance)
    reptile.right(120)
    reptile.forward(unit_distance)
    reptile.end_fill()
    reptile.up()
    reptile.goto(0, 0)
    reptile.left(150)
    reptile.forward(radius)
    screen.mainloop()

if __name__ == '__main__':
    main()
