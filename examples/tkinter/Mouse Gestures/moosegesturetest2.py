#! /usr/bin/env python3
"""
MooseGesture Test application
Al Sweigart al@coffeeghost.net
http://coffeeghost.net/2011/05/09/moosegesture-python-mouse-gestures-module

Run the app and then draw by dragging the mouse. When you release the mouse
button, the gesture you drew will be identified.


This script requires the MooseGesture library, which you can download from here:
http://coffeeghost.net/moosegesture.py

Copyright 2011, BSD-license.
"""

import tkinter.font
import moosegesture

class Test(tkinter.Canvas):

    # setup constants
    WINDOWWIDTH = 400
    WINDOWHEIGHT = 400
    FPS = 40
    
    color = '#{:02X}{:02X}{:02X}'

    TEXTCOLOR = color.format(255, 255, 255) # white
    BACKGROUNDCOLOR = color.format(0, 0, 0) # black
    POINTSCOLOR = color.format(255, 0, 0)   # red
    LINECOLOR = color.format(255, 165, 0)   # orange
    CARDINALCOLOR = color.format(0, 255, 0) # green
    DIAGONALCOLOR = color.format(0, 0, 255) # blue

    del color
    
    ########################################################################

    @classmethod
    def main(cls):
        # set up tkinter, the window, and the mouse cursor
        tkinter._tkinter.setbusywaitinterval(round(1000 / cls.FPS))
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('Mouse Gesture Test')
        root.bind_all('<Escape>', lambda event: root.quit())
        surface = cls()
        surface.grid()
        root.mainloop()

    def __init__(self):
        # Draw the window.
        super().__init__(width=self.WINDOWWIDTH, height=self.WINDOWHEIGHT,
                         background=self.BACKGROUNDCOLOR, highlightthickness=0)
        self.points = []
        self.font = tkinter.font.Font(size=24)
        # handle all tkinter events
        self.bind('<ButtonPress-1>', self.mouse_button_down)
        self.bind('<ButtonRelease-1>', self.mouse_button_up)
        self.bind('<Motion>', self.mouse_motion)

    def mouse_button_down(self, event):
        # on mouse down, erase the previous line and start drawing a new one
        self.delete(tkinter.ALL)
        self.points = [(event.x, event.y)]
        self.draw_point(self.POINTSCOLOR, 2)
        
    def draw_point(self, color, radius):
        x, y = self.points[-1]
        self.create_oval(x - radius, y - radius, x + radius, y + radius,
                         fill=color, outline=color)

    def mouse_button_up(self, event):
        # try to identify the gesture when the mouse dragging stops
        gesture = MooseGesture(self.points)
        self.points = []
        # draw the identified strokes of the last line
        self.create_text(10, self.WINDOWHEIGHT - 30, font=self.font,
                         text=gesture.strokeText, fill=self.TEXTCOLOR,
                         anchor=tkinter.NW)
        # draw the identified strokes
        self.delete('line')
        segNum = 0
        curColor = self.LINECOLOR
        # START
        for p in range(len(gesture.points) - 1):
            if segNum < len(gesture.segments) and gesture.segments[segNum][0] == p:
                # start of new stroke
                if gesture.strokes[segNum] & 1:
                    curColor = self.DIAGONALCOLOR
                else:
                    curColor = self.CARDINALCOLOR
            self.draw_line(curColor, *gesture.points[p:p+2])
            # end of a stroke
            if segNum < len(gesture.segments) and gesture.segments[segNum][1] == p:
                curColor = self.LINECOLOR
                segNum += 1\

    def mouse_motion(self, event):
        if self.points:
            # draw the line if the mouse is dragging
            self.points.append((event.x, event.y))
            self.draw_point(self.POINTSCOLOR, 2)
            # draw strokes as unidentified while dragging the mouse
            self.draw_line(self.LINECOLOR, *self.points[-2:])
            
    def draw_line(self, color, start, stop):
        (a, b), (c, d) = start, stop
        self.create_line(a, b, c, d, fill=color, tag='line')
        
################################################################################
        
class MooseGesture:

    def __init__(self, points):
        self.__points = tuple(points)
        self.__strokes = None
        self.__segments = None
        self.__strokeText = None

    @property
    def points(self):
        return self.__points
        
    @property
    def strokes(self):
        if self.__strokes is None:
            self.__strokes = moosegesture.getGesture(self.__points)
        return self.__strokes
        
    @property
    def segments(self):
        if self.__segments is None:
            self.__segments = moosegesture.getSegments(self.__points)
        return self.__segments
        
    @property
    def strokeText(self):
        if self.__strokeText is None:
            self.__strokeText = moosegesture.getGestureStr(self.strokes)
        return self.__strokeText

if __name__ == '__main__':
    Test.main()
