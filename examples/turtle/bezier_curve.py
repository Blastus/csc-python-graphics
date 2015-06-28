#! /usr/bin/env python3

__version__ = 2, 0, 0
__date__ = '27 June 2015'
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__credits__ = '''Guido van Rossum, Dutch computer programmer & Python's author.
Gregor Lingl, creator of Python's turtle module that powers this program.
http://en.wikipedia.org/wiki/Bezier_curve, for inspiring the following code.'''

import itertools


def bezier_curve(t, *p):
    if not 0 <= t <= 1:
        raise ValueError('t must be between 0 and 1 inclusive')
    s = len(p)
    if s < 2:
        raise ValueError('p must have at least two values')
    a = 1 - t
    return _bezier_curve(t, p, s, a)


def _bezier_curve(t, p, s, a):
    if s == 2:
        p0, p1 = p
        return complex(p0.real * a + p1.real * t, p0.imag * a + p1.imag * t)
    p = (_bezier_curve(t, p, 2, a) for p in pairwise(p))
    return _bezier_curve(t, p, s - 1, a)


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

###############################################################################

import turtle


def main():
    curve = (0+0j, 50+100j, 100+25j, 150+75j, 200+50j, 150+25j, 200-100j,
             300-100j, 300+0j, 100+200j)
    screen = turtle.Screen()
    graph(screen, curve)
    screen.mainloop()


def graph(screen, curve):
    screen.reset()
    screen.mode('logo')
    reptile = turtle.Turtle()
    reptile.speed('fastest')
    reptile.hideturtle()
    reptile.penup()
    plot_points(reptile, curve)
    position = curve[0]
    reptile.setposition(position.real, position.imag)
    plot_line(reptile, curve, 100)


def plot_points(reptile, curve):
    for position in curve:
        reptile.setposition(position.real, position.imag)
        reptile.dot()


def plot_line(reptile, curve, steps):
    reptile.pendown()
    for t in range(steps):
        position = bezier_curve((t + 1) / steps, *curve)
        reptile.setposition(position.real, position.imag)

if __name__ == '__main__':
    main()
