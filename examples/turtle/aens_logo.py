import math
import turtle


def main():
    radius = 50.0
    screen = turtle.Screen()
    screen.reset()
    reptile = turtle.Turtle()
    reptile.speed('fastest')
    # draw outer circle
    reptile.up()
    other_radius = radius + radius * math.sqrt(3) / 2 + radius / 3 + radius
    reptile.goto(0, other_radius)
    reptile.setheading(180)
    reptile.color('blue')
    reptile.down()
    reptile.begin_fill()
    reptile.circle(other_radius)
    reptile.end_fill()
    # draw middle circle
    # Note: technique courtesy of Tim Hansen
    reptile.up()
    other_radius = radius + radius * math.sqrt(3) / 2 + radius / 3
    reptile.goto(0, other_radius)
    reptile.setheading(180)
    reptile.color('white')
    reptile.down()
    reptile.begin_fill()
    reptile.circle(other_radius)
    reptile.end_fill()
    # draw inner circle
    reptile.up()
    reptile.goto(0, radius)
    reptile.setheading(180)
    reptile.color('green')
    reptile.down()
    reptile.begin_fill()
    reptile.circle(radius)
    reptile.end_fill()
    # draw the arrows
    for arrow in range(8):
        # setup triangle
        reptile.up()
        reptile.goto(0, 0)
        reptile.setheading(arrow * 45)
        reptile.forward(radius)
        reptile.right(30)
        reptile.color('red')
        reptile.down()
        # draw triangle
        reptile.begin_fill()
        reptile.forward(radius)
        reptile.left(120)
        reptile.forward(radius)
        reptile.left(120)
        reptile.forward(radius)
        reptile.end_fill()
        # setup box
        reptile.up()
        reptile.goto(0, 0)
        reptile.setheading(arrow * 45)
        reptile.forward(radius + radius * math.sqrt(3) / 2)
        reptile.right(90)
        reptile.forward(radius / 6)
        reptile.left(90)
        reptile.down()
        # draw box
        reptile.begin_fill()
        reptile.forward(radius / 3)
        reptile.left(90)
        reptile.forward(radius / 3)
        reptile.left(90)
        reptile.forward(radius / 3)
        reptile.end_fill()
    # cleanup the view
    reptile.up()
    reptile.goto(0, 0)
    reptile.color('green')
    screen.mainloop()

if __name__ == '__main__':
    main()
