import turtle


def overlap(degrees):
    screen = turtle.Screen()
    screen.reset()
    reptile = turtle.Turtle()
    # draw right side
    reptile.up()
    reptile.setheading(90)
    reptile.right(180 - degrees / 2.0)
    reptile.forward(100)
    reptile.left(90)
    reptile.color('#FF0000')
    reptile.down()
    reptile.begin_fill()
    reptile.circle(100, 180)
    reptile.end_fill()
    # draw left side
    reptile.up()
    reptile.goto(0, 0)
    reptile.setheading(90)
    reptile.right(degrees / 2.0)
    reptile.forward(100)
    reptile.left(90)
    reptile.color('#0000FF')
    reptile.down()
    reptile.begin_fill()
    reptile.circle(100, 180)
    reptile.end_fill()
    # draw overlap
    reptile.up()
    reptile.goto(0, 0)
    reptile.begin_fill()
    reptile.setheading(90)
    reptile.right(degrees / 2.0)
    reptile.forward(100)
    reptile.left(90)
    reptile.color('#FF00FF')
    reptile.down()
    reptile.circle(100, degrees)
    reptile.end_fill()
    reptile.up()
    reptile.hideturtle()
    screen.mainloop()

if __name__ == '__main__':
    overlap(120)
