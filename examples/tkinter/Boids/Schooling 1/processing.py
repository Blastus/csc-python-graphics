#! /usr/bin/env python3
import itertools
import time
import tkinter.ttk
import vector

################################################################################

class Process(tkinter.ttk.Frame):

    FRAMES_PER_SECOND = 10
    UPDATES_PER_SECOND = 20

    @classmethod
    def main(cls):
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        root.title('Processing 1.0')
        root.resizable(False, False)
        view = cls(root)
        view.grid()
        root.mainloop()

    ########################################################################

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.setup()
        self.__canvas = tkinter.Canvas(self,
                                       width=self.__width,
                                       height=self.__height,
                                       background=self.__color,
                                       highlightthickness=0)
        self.__canvas.bind('<1>', self.mouse_pressed)
        self.__canvas.grid()
        self.__context = GraphicsContext(self.__canvas)
        self.__schedule(self.__pre_render, time.clock(),
                        1 / self.FRAMES_PER_SECOND)
        interval = 1 / self.UPDATES_PER_SECOND
        self.__schedule(lambda: self.update(interval), time.clock(), interval)

    def __schedule(self, callback, target, interval):
        callback()
        target += interval
        ms = round((target - time.clock()) * 1000)
        if ms > 0:
            self.after(ms, self.__schedule, callback, target, interval)
        else:
            self.after_idle(self.__schedule, callback, target, interval)
            self.speed_warning()

    def __pre_render(self):
        self.__canvas.delete(tkinter.ALL)
        self.render(self.__context)
    
    def display(self, width, height, color):
        self.__width = width
        self.__height = height
        self.__color = color

    def setup(self):
        raise NotImplementedError()

    def render(self, context):
        raise NotImplementedError()

    def update(self, interval):
        raise NotImplementedError()

    def mouse_pressed(self, event):
        raise NotImplementedError()

    def speed_warning(self):
        raise NotImplementedError()

################################################################################

class GraphicsContext:

    def __init__(self, canvas):
        self.__canvas = canvas
        self.__stack = []

    def write(self, x, y, text, color):
        self.__canvas.create_text(x, y, text=text, fill=color)

    def push_matrix(self):
        self.__stack.append(self.__Matrix(self.__canvas))

    def begin_shape(self):
        self.__stack[-1].begin_shape()

    def fill(self, color):
        self.__stack[-1].fill(color)

    def stroke(self, color):
        self.__stack[-1].stroke(color)

    def vertex(self, x, y):
        self.__stack[-1].vertex(x, y)

    def end_shape(self):
        self.__stack[-1].end_shape()

    def rotate(self, direction):
        self.__stack[-1].rotate(direction)

    def translate(self, offset):
        self.__stack[-1].translate(offset)
    
    def pop_matrix(self):
        matrix = self.__stack.pop()
        matrix.render()

    def render(self):
        while self.__stack:
            matrix = self.__stack.pop()
            matrix.render()

    def push_shape(self, shape):
        self.__stack[-1].push_shape(shape)

    ########################################################################

    class __Matrix:

        def __init__(self, canvas):
            self.__canvas = canvas
            self.__shapes = []
            self.__shape = None

        def begin_shape(self):
            assert self.__shape is None, 'Shape Is Being Constructed!'
            self.__shape = Shape()

        def fill(self, color):
            self.__shape.fill(color)

        def stroke(self, color):
            self.__shape.stroke(color)

        def vertex(self, x, y):
            self.__shape.vertex(x, y)

        def end_shape(self):
            self.__shapes.append(self.__shape)
            self.__shape = None

        def rotate(self, direction):
            for shape in self.__shapes:
                shape.rotate(direction)

        def translate(self, offset):
            for shape in self.__shapes:
                shape.translate(offset)

        def render(self):
            assert self.__shape is None, 'Shape Is Being Constructed!'
            for shape in self.__shapes:
                shape.render(self.__canvas)

        def push_shape(self, shape):
            self.__shapes.append(shape.ngon_copy())

################################################################################

class Shape:

    def __init__(self):
        self.__vertex = []
        self.__stroke = ''
        self.__fill = ''

    def fill(self, color):
        self.__fill = color

    def stroke(self, color):
        self.__stroke = color

    def vertex(self, x, y):
        self.__vertex.append(vector.Vector2(x, y))

    def rotate(self, direction):
        for vertex in self.__vertex:
            vertex.direction += direction

    def translate(self, offset):
        for vertex in self.__vertex:
            vertex += offset

    def render(self, canvas):
        canvas.create_polygon(*itertools.chain(*self.__vertex),
                              outline=self.__stroke,
                              fill=self.__fill)

    def ngon_copy(self):
        copy = Shape()
        copy.__vertex = tuple(v.copy() for v in self.__vertex)
        copy.__stroke, copy.__fill = self.__stroke, self.__fill
        return copy

################################################################################

import recipe576904; recipe576904.bind_all(globals())
