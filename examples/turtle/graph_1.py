#! /usr/bin/env python3
import operator
import turtle


def graph(start, end, function):
    start_y = function(start)
    end_y = function(end)
    screen = turtle.Screen()
    screen.reset()
    margin_x = (end - start) / 98
    margin_y = (end_y - start_y) / 98
    screen.setworldcoordinates(start - margin_x,
                               start_y - margin_y,
                               end + margin_x,
                               end_y + margin_y)
    reptile = turtle.Turtle()
    reptile.speed(0)
    reptile.pu()
    reptile.goto(start, start_y)
    reptile.pd()
    width = screen.canvwidth
    step = (end - start) / width
    for x in range(width + 1):
        reptile.goto(x * step + start, function(x * step + start))

# ===========================
# Example Usage Follows Below
# ===========================


def interpolate_max(years):
    m = years % 1
    people1 = [0] * 202
    people1[0] = people1[21] = 1
    for _ in range(int(years)):
        just_born = operator.getitem(people1, 1)
        new_adult = operator.getitem(people1, 20)
        to_heaven = operator.getitem(people1, 200)
        people1 = [just_born + new_adult - to_heaven] + people1[:-1]
    people2 = [people1[1] + people1[20] - people1[200]] + people1[:-1]
    people3 = [a + round((b - a) * m) for a, b in zip(people1, people2)]
    return people3[:21], people3[1:21], people3[21:-1], people3[21:]


def demo():
    # Graph through 250,000,000 Y (204.2858647 X)
    graph(204.2858, 204.2859, lambda x: sum(map(sum, interpolate_max(x))))
    # Show growth of total unmarried males.
    graph(20, 60, lambda x: sum(interpolate_max(x)[0]))
    # Example of how newborn males changes over time.
    graph(0, 80, lambda x: interpolate_max(x)[0][0])
    # Run turtle's mainloop for GUI.
    turtle.Screen().mainloop()

if __name__ == '__main__':
    demo()
