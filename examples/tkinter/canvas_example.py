#! /usr/bin/env python3

__version__ = 2, 0, 0
__date__ = '8 July 2015'
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__credits__ = 'Anonymous, whoever happened to write the original code first.'

import tkinter
import tkinter.ttk


def main():
    tkinter.NoDefaultRoot()
    app = Application()
    app.mainloop()


class Application(tkinter.Tk):

    def __init__(self, screen_name=None, base_name=None, class_name='Tk',
                 use_tk=1, sync=0, use=None):
        super().__init__(screen_name, base_name, class_name, use_tk, sync, use)
        self.__h = tkinter.ttk.Scrollbar(self, orient=tkinter.HORIZONTAL)
        self.__v = tkinter.ttk.Scrollbar(self, orient=tkinter.VERTICAL)
        self.__c = tkinter.Canvas(self, scrollregion=(0, 0, 1000, 1000),
                                  xscrollcommand=self.__h.set,
                                  yscrollcommand=self.__v.set)
        self.__s = tkinter.ttk.Sizegrip(self)
        self.__last_x = self.__last_y = 0
        self.__color = None
        self.__setup_widgets()
        self.__create_palette()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
    def __setup_widgets(self):
        self.__h['command'] = self.__c.xview
        self.__v['command'] = self.__c.yview
        self.__c.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.__h.grid(row=1, column=0, sticky=tkinter.EW)
        self.__v.grid(row=0, column=1, sticky=tkinter.NS)
        self.__s.grid(row=1, column=1, sticky=tkinter.NSEW)
        self.__c.bind('<Button-1>', self.__xy)
        self.__c.bind('<B1-Motion>', self.__add_line)
        self.__c.bind('<B1-ButtonRelease>', self.__done_stroke)
        
    def __create_palette(self):
        change = self.__set_color
        red = (10, 10, 30, 30), 'red', ('color', 'color_red')
        handle = self.__rectangle(*red)
        self.__c.tag_bind(handle, '<Button-1>', lambda event: change('red'))
        blue = (10, 35, 30, 55), 'blue', ('color', 'color_blue')
        handle = self.__rectangle(*blue)
        self.__c.tag_bind(handle, '<Button-1>', lambda event: change('blue'))
        black = (10, 60, 30, 80), 'black', ('color', 'color_black', 'selected')
        handle = self.__rectangle(*black)
        self.__c.tag_bind(handle, '<Button-1>', lambda event: change('black'))
        self.__set_color('black')
        self.__c.itemconfigure('color', width=5)
        
    def __rectangle(self, corners, fill, tags):
        return self.__c.create_rectangle(corners, fill=fill, tags=tags)

    def __xy(self, event):
        self.__last_x = self.__c.canvasx(event.x)
        self.__last_y = self.__c.canvasy(event.y)

    def __set_color(self, new_color):
        self.__color = new_color
        self.__c.dtag(tkinter.ALL, 'selected')
        self.__c.itemconfigure('color', outline='white')
        self.__c.addtag('selected', 'withtag', 'color_' + new_color)
        self.__c.itemconfigure('selected', outline='#999999')

    def __add_line(self, event):
        x, y = self.__c.canvasx(event.x), self.__c.canvasy(event.y)
        self.__c.create_line((self.__last_x, self.__last_y, x, y),
                             fill=self.__color, width=5, tags='current_line')
        self.__last_x, self.__last_y = x, y

    def __done_stroke(self, _):
        self.__c.itemconfigure('current_line', width=1)

if __name__ == '__main__':
    main()
