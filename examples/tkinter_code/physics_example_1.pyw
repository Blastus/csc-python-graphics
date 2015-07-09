#! /usr/bin/env python3

__version__ = 2, 0, 0
__date__ = '8 July 2015'
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__credits__ = 'James Mulvihill, for checking that my code works correctly.'

import itertools
import random
import time
import tkinter
import traceback

import physics


def main():
    physics_example = Example()
    physics_example.mainloop()


class Example(tkinter.Tk):

    BALLS = 10                      # number of simulated balls
    BALL_RADIUS = 5                 # radius of ball in pixels
    START_SPACE = 20                # side offset in pixels
    SCREEN_WIDTH = 400              # width of screen in pixels
    SCREEN_HEIGHT = 400             # height of screen in pixels
    WALL_SPACE = 50                 # width of walls in pixels
    FLOOR_SPACE = 25                # height of floor in pixels
    BACKGROUND = 'white'            # color of background
    BALL_COLOR = 'red'              # color of balls
    FLOOR_COLOR = 'blue'            # color of floor
    FORCE_COLOR = 'light green'     # color of force field
    FPS = 60                        # frames per second
    SPEED_LIMIT = 500               # pixels per second
    WALL_FORCE = 500                # pixels per second
    GRAVITY_RATE = 400              # pixels per second
    FRICTION_RATE = 7 / 8           # velocity per second

    def __init__(self, screen_name=None, base_name=None, class_name='Tk',
                 use_tk=1, sync=0, use=None):
        """Initialize the example so that it can run on the computer."""
        super().__init__(screen_name, base_name, class_name, use_tk, sync, use)
        self.__balls = []
        self.__x = (self.winfo_screenwidth() - self.SCREEN_WIDTH) >> 1
        self.__y = (self.winfo_screenheight() - self.SCREEN_HEIGHT) >> 1
        self.__screen = tkinter.Canvas(self, width=self.SCREEN_WIDTH,
                                       height=self.SCREEN_HEIGHT,
                                       background=self.BACKGROUND)
        self.__lock = True
        self.__start = time.perf_counter()
        self.__frame = 1
        self.__simulators = (self.__wall, self.__floor, self.__gravity,
                             self.__friction, self.__governor)
        self.__continue_setup()
        self.__draw_walls_and_floor()
        self.resizable(False, False)
        self.title('Bouncy Balls')
        self.geometry('{}x{}+{}+{}'.format(self.SCREEN_WIDTH,
                                           self.SCREEN_HEIGHT,
                                           self.__x, self.__y))
        self.bind_all('<Escape>', lambda event: event.widget.quit())
        self.bind('<Configure>', self.__move)
        self.after(1000 // self.FPS, self.__update)
        self.after(10000 // self.FPS, self.__unlock)

    def __continue_setup(self):
        """Build balls and prepare GUI."""
        x_min = -self.START_SPACE
        x_max = self.START_SPACE + self.SCREEN_WIDTH
        y_min = self.BALL_RADIUS
        y_max = self.SCREEN_HEIGHT - self.FLOOR_SPACE - self.BALL_RADIUS
        for _ in range(self.BALLS):
            x = x_min if random.randint(0, 1) else x_max
            y = random.randint(y_min, y_max)
            self.__balls.append(physics.Ball(x, y, self.BALL_RADIUS))
        self.__screen.grid()

    def __draw_walls_and_floor(self):
        """Put representations of the walls and floor on the screen."""
        floor_height = self.SCREEN_HEIGHT - self.FLOOR_SPACE + 2
        width = self.SCREEN_WIDTH
        corners = 0, 0, self.WALL_SPACE - 1, floor_height
        self.__screen.create_rectangle(corners, fill=self.FORCE_COLOR)
        corners = width - self.WALL_SPACE + 1, 0, width, floor_height
        self.__screen.create_rectangle(corners, fill=self.FORCE_COLOR)
        corners = 0, floor_height, width, floor_height
        self.__screen.create_line(corners, width=3, fill=self.FLOOR_COLOR)

    def __move(self, event):
        """Simulate the movement of the screen."""
        if not self.__lock:
            difference = physics.Vector(self.__x - event.x, self.__y - event.y)
            self.__screen.move('animate', difference.x, difference.y)
            floor = self.SCREEN_HEIGHT - self.FLOOR_SPACE - self.BALL_RADIUS
            for ball in self.__balls:
                ball.pos += difference
                if ball.pos.y >= floor:
                    ball.vel.y += difference.y * self.FPS
                    self.__floor(ball)
            self.__x, self.__y = event.x, event.y

    def __update(self):
        """Run physics on balls and update the screen."""
        try:
            for simulate in self.__simulators:
                for ball in self.__balls:
                    simulate(ball)
            for b1, b2 in itertools.combinations(self.__balls, 2):
                b1.crash(b2)
            for ball in self.__balls:
                ball.correct()
                ball.move(self.FPS)
            self.__screen.delete('animate')
            for ball in self.__balls:
                corners = (ball.pos.x - ball.rad, ball.pos.y - ball.rad,
                           ball.pos.x + ball.rad, ball.pos.y + ball.rad)
                self.__screen.create_oval(corners,
                                          fill=self.BALL_COLOR,
                                          tag='animate')
            self.__frame += 1
            self.after(int((self.__start + self.__frame / self.FPS -
                            time.perf_counter()) * 1000), self.__update)
        except ArithmeticError:
            self.__screen.delete(tkinter.ALL)
            self.__screen.create_text(
                (self.SCREEN_WIDTH >> 1, self.SCREEN_HEIGHT >> 1),
                text=traceback.format_exc(),
                font='Courier 10',
                fill='red',
                tag='animate')

    def __wall(self, ball):
        """Simulate a wall acting on a ball."""
        space = self.WALL_SPACE + self.BALL_RADIUS
        force = self.WALL_FORCE / self.FPS
        if ball.pos.x <= space:
            ball.vel.x += force
        elif ball.pos.x >= self.SCREEN_WIDTH - space:
            ball.vel.x -= force

    def __floor(self, ball):
        """Simulate a floor acting on a ball."""
        floor = self.SCREEN_HEIGHT - self.FLOOR_SPACE - self.BALL_RADIUS
        if ball.pos.y >= floor:
            ball.pos.y = floor
            ball.vel.y *= -1

    def __gravity(self, ball):
        """Simulate gravity acting on a ball."""
        ball.vel.y += self.GRAVITY_RATE / self.FPS

    def __friction(self, ball):
        """Simulate friction slowing a ball down over time."""
        ball.vel *= self.FRICTION_RATE ** (1 / self.FPS)

    def __governor(self, ball):
        """Simulate a governor on the ball's speed."""
        if abs(ball.vel) > self.SPEED_LIMIT:
            ball.vel = ball.vel.unit() * self.SPEED_LIMIT

    def __unlock(self):
        """Unlock the move function so that it begins to operate."""
        self.__lock = False

if __name__ == '__main__':
    main()
