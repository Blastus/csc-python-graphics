#! /usr/bin/env python3

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
        self.__h['command'] = self.__c.xview
        self.__v['command'] = self.__c.yview
        self.__s = tkinter.ttk.Sizegrip(self)
        self.__c.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.__h.grid(row=1, column=0, sticky=tkinter.EW)
        self.__v.grid(row=0, column=1, sticky=tkinter.NS)
        self.__s.grid(row=1, column=1, sticky=tkinter.NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.__last_x = self.__last_y = 0
        self.__color = 'black'
        self.__c.bind('<Button-1>', self.__xy)
        self.__c.bind('<B1-Motion>', self.__add_line)
        self.__c.bind('<B1-ButtonRelease>', self.__done_stroke)
        handle = self.__c.create_rectangle((10, 10, 30, 30), fill='red',
                                           tags=('palette', 'palettered'))
        self.__c.tag_bind(handle, '<Button-1>',
                          lambda event: self.__set_color('red'))
        handle = self.__c.create_rectangle((10, 35, 30, 55), fill='blue',
                                           tags=('palette', 'paletteblue'))
        self.__c.tag_bind(handle, '<Button-1>',
                          lambda event: self.__set_color('blue'))
        handle = self.__c.create_rectangle((10, 60, 30, 80), fill='black',
                                           tags=('palette', 'paletteblack',
                                                 'palette_selected'))
        self.__c.tag_bind(handle, '<Button-1>',
                          lambda event: self.__set_color('black'))
        self.__c.itemconfigure('palette', width=5)

    def __xy(self, event):
        self.__last_x = self.__c.canvasx(event.x)
        self.__last_y = self.__c.canvasy(event.y)

    def __set_color(self, new_color, tag='palette_selected'):
        self.__color = new_color
        self.__c.dtag(tkinter.ALL, tag)
        self.__c.itemconfigure('palette', outline='white')
        self.__c.addtag(tag, 'withtag', 'palette' + self.__color)
        self.__c.itemconfigure(tag, outline='#999999')

    def __add_line(self, event):
        x, y = self.__c.canvasx(event.x), self.__c.canvasy(event.y)
        self.__c.create_line((self.__last_x, self.__last_y, x, y),
                             fill=self.__color, width=5, tags='current_line')
        self.__last_x, self.__last_y = x, y

    def __done_stroke(self, event):
        self.__c.itemconfigure('current_line', width=1)

if __name__ == '__main__':
    main()