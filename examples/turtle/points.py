#! /usr/bin/env python3
import colorsys
import random
import turtle


def graph_2d():
    screen = turtle.Screen()
    screen.screensize(1000, 1000, 'black')
    screen.setworldcoordinates(0, 1000, 1000, 0)
    reptile = turtle.Turtle()
    reptile.speed('fastest')
    reptile.up()
    points = tuple(eval(line) for line in open('3D.txt') if line)
    for a, b, c in random.sample(points, 1000):
        reptile.color(colorsys.hsv_to_rgb((a - 1) / 999, 1, 1))
        reptile.goto(b, c)
        reptile.down()
        reptile.circle(1)
        reptile.up()
    screen.mainloop()

# def graph_3d():
#     import visual
#     locals().update(vars(visual))
#     points = tuple(eval(line) for line in open('3D.txt') if line)
#     points = tuple(tuple(array[index] for index in indices)
#                    for array in points
#                    for indices in itertools.permutations(range(3)))
#     for pos in random.SystemRandom().sample(points, 2000 // 6):
#         sphere(pos=pos, radius=10, color=color.red)

if __name__ == '__main__':
    graph_2d()
