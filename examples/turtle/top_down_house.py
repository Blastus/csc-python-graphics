#! /usr/bin/env python3
import turtle

DISTANCE = 50


def main():
    screen = turtle.Screen()
    reptile = turtle.Turtle()
    reptile.reset()
    screen.mode('logo')
    # reptile.speed('fastest')
    reptile.right(45)
    make_drawing(reptile)
    reptile.hideturtle()
    screen.mainloop()


def make_drawing(reptile):
    reptile.penup()
    start = reptile.position()
    # reptile.dot()
    tier1 = []
    for _ in range(4):
        trace_wall(reptile, False, tier1)
        reptile.goto(start)
        reptile.right(90)
    tier2 = []
    for point in tier1:
        reptile.goto(point)
        reptile.left(45)
        trace_wall(reptile, True, tier2)
        reptile.goto(point)
        reptile.right(90)
        trace_wall(reptile, True, tier2)
        reptile.right(45)
    tier3 = []
    for point in tier2:
        reptile.goto(point)
        reptile.right(45)
        trace_wall(reptile, False, tier3)
    tier4 = []
    for i, point in enumerate(tier3):
        draw = not i & 1
        reptile.goto(point)
        reptile.left(45)
        trace_wall(reptile, draw, tier4)
        if not draw:
            reptile.right(180)
            trace_wall(reptile, True, [], 4 + 2 ** 0.5)
            reptile.right(180)
        reptile.goto(point)
        reptile.right(90)
        trace_wall(reptile, draw, tier4)
    # Main Circle
    reptile.goto(start)
    reptile.setheading(reptile.towards(tier4[0]))
    reptile.goto(tier4[0])
    reptile.left(90)
    reptile.pendown()
    reptile.circle(reptile.distance(start))
    reptile.penup()
    # Water Falls
    reptile.goto(start)
    reptile.color('blue')
    reptile.pensize(3)
    arc = reptile.towards(tier4[6]) - reptile.towards(tier4[3])
    for i in range(4):
        point = tier4[2 + i * 4]
        reptile.setheading(reptile.towards(point))
        radius = reptile.distance(point) * 1.05
        reptile.forward(radius)
        reptile.left(90)
        reptile.pendown()
        reptile.circle(radius, arc)
        reptile.penup()
        reptile.goto(start)


def trace_wall(reptile, draw, tier, times=1):
    if draw:
        reptile.pendown()
    reptile.forward(DISTANCE * times)
    if draw:
        reptile.penup()
    reptile.dot()
    tier.append(reptile.position())

if __name__ == '__main__':
    main()
