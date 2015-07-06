#! /usr/bin/env python3
import itertools
import time
import tkinter
import vector

################################################################################

def inherited(method):
    "Tests if a bound method was inherited from a base class."
    f = method.__func__
    return f is getattr(type(method.__self__).__base__, f.__name__, None)

################################################################################

class Polygon:

    "Polygon(*vertices) -> Polygon"

    __slots__ = 'vertices'

    def __init__(self, *vertices):
        "Initializes polygon with a list of vertices."
        self.vertices = vertices

    def translate(self, offset):
        "Moves the polygon by the specified offset."
        for vertex in self.vertices:
            vertex += offset

    def rotate(self, direction):
        "Rotates the polygon by a vector's direction."
        for vertex in self.vertices:
            vertex.direction += direction

    def scale(self, factor):
        "Increases or decreases size of the polygon."
        for vertex in self.vertices:
            vertex *= factor

    def copy(self):
        "Copies the polygon by copying its vertices."
        return Polygon(*(vertex.copy() for vertex in self.vertices))

################################################################################

class Graphics:

    "Graphics(canvas) -> Graphics"

    __slots__ = 'canvas'

    def __init__(self, canvas):
        "Initializes graphics by wrapping a canvas."
        self.canvas = canvas

    def draw(self, polygon, fill, outline):
        "Draws a polygon on the underlying canvas."
        self.canvas.create_polygon(*itertools.chain(*polygon.vertices),
                                   fill=fill, outline=outline)

    def write(self, x, y, text, fill):
        "Writes the text to bottom-left of location."
        self.canvas.create_text(x, y, text=text, fill=fill, anchor=tkinter.NW)

    def clear(self):
        "Clears canvas of all objects shown on it."
        self.canvas.delete(tkinter.ALL)

    def fill(self, background):
        "Fills in the canvas with the given color."
        self.canvas.configure(background=background)

################################################################################

class Process(tkinter.Frame):

    "Process(master, width, height) -> Process"

    FRAMESKIP = 5   # How many frames should skip before issuing speed warning?
    RENDER_PER_SECOND = 15  # How often should the DISPLAY be updated / second?
    THINK_PER_SECOND = 30   # How often should the THOUGHT be updated / second?
    MOVE_PER_SECOND = 30    # How often should the PHYSICS be updated / second?

    @classmethod
    def main(cls, width, height):
        "Creates a process in a window and executes it."
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        root.title('Processing 1.2')
        root.resizable(False, False)
        view = cls(root, width, height)
        view.grid()
        root.mainloop()

    ########################################################################

    def __init__(self, master, width, height):
        "Initializes process and starts simulation loops."
        super().__init__(master)
        canvas = tkinter.Canvas(self, width=width, height=height,
                                background='white', highlightthickness=0)
        if not inherited(self.mouse):
            canvas.bind('<Button>', self.mouse)
        if not inherited(self.keyboard):
            canvas.bind('<Key>', self.keyboard)
            canvas.focus_force()
        canvas.grid()
        graphics = Graphics(canvas)
        self.setup(graphics.fill)
        # Start the loops that have been implemented by a child class.
        render, think, move = 1 / self.RENDER_PER_SECOND, \
                              1 / self.THINK_PER_SECOND, \
                              1 / self.MOVE_PER_SECOND
        if not inherited(self.render):
            self.__loop(lambda: self.render(graphics), render, time.clock(), 0)
        if not inherited(self.think):
            self.__loop(self.think, think, time.clock(), 0)
        if not inherited(self.move):
            self.__loop(lambda: self.move(move), move, time.clock(), 0)

    def __loop(self, method, interval, target, errors):
        "Runs the method after each interval has passed."
        method()
        target += interval
        ms = int((target - time.clock()) * 1000)
        if ms >= 0:
            self.after(ms, self.__loop, method, interval, target, 0)
        elif errors == self.FRAMESKIP:
            self.warning()
            self.after_idle(self.__loop, method, interval, target, 0)
        else:
            self.after_idle(self.__loop, method, interval, target, errors + 1)

    ########################################################################

    def setup(self, background):
        "This method is called before entering the main loops."
        raise NotImplementedError()

    def render(self, graphics):
        "This method is called when the screen should be updated."
        raise NotImplementedError()

    def think(self):
        "This method is called when AI routines should be executed."
        raise NotImplementedError()

    def move(self, interval):
        "This method is called when the physics should be updated."
        raise NotImplementedError()

    def mouse(self, event):
        "This method is called when a mouse button has been pressed."
        raise NotImplementedError()

    def keyboard(self, event):
        "This method id called when a keyboard button has been pressed."
        raise NotImplementedError()

    def warning(self):
        "This method is called when a loop runs slower than it should."
        raise NotImplementedError()
