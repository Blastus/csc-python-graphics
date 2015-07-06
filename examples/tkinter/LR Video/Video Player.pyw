#! /usr/bin/env python3
import random, tempfile, zlib, os, bz2, time, imp, traceback
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import xml.sax as _xml_sax
import tkinter as Tkinter
import pickle as cPickle
import _thread as thread
import queue as Queue
import sys as _sys

DO_EXIT = False

_os = os

util = imp.new_module('util')
vars(util).update(vars(Tkinter))
util.os = os
util.cPickle = cPickle
class Screen3:
    IMAGE_MAP = {'^': 'you', '&': 'robot', '_': 'floor', '*': 'load', '|': 'ladder', '@': 'portal'}
util.Screen3 = Screen3

class Call:

    def __init__(self, function, *args):
        self.__function = function
        self.__args = args

    def __call__(self, *args):
        self.__function(*self.__args)

def set_theme(theme):
    global DO_EXIT
    util.Screen3.IMAGE_THEME = theme
    root.withdraw()
    DO_EXIT = False
    raise SystemExit()

def shutdown():
    global DO_EXIT
    root.destroy()
    DO_EXIT = True
    raise SystemExit()

def select_theme():
    global root
    os = util.os
    Tkinter = util
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('Main Menu')
    root.protocol('WM_DELETE_WINDOW', shutdown)
    Tkinter.Label(root, text='Choose a theme for to use during game play.', padx=5, pady=5).grid(row=0, sticky='news')
    for row, theme in enumerate(path for path in sorted(os.listdir('themes')) if os.path.isdir(os.path.join('themes', path))):
        Tkinter.Button(root, text=theme.replace('_', ' ').title(), command=Call(set_theme, theme)).grid(row=row+1, sticky='news')
    try:
        root.mainloop()
    except SystemExit:
        if DO_EXIT:
            raise

def load_images():
    Tkinter, os = util, util.os
    util.Screen3.IMAGES = dict((key, Tkinter.PhotoImage(file=os.path.join(os.getcwd(), 'themes', util.Screen3.IMAGE_THEME, util.Screen3.IMAGE_MAP[key] + '.gif'))) for key in util.Screen3.IMAGE_MAP)
    first = True
    for key in util.Screen3.IMAGES:
        image = util.Screen3.IMAGES[key]
        if first:
            first = False
            h = image.height()
            w = image.width()
        else:
            assert image.height() == h
            assert image.width() == w
    util.Screen3.IMAGE_WIDTH = w
    util.Screen3.IMAGE_HEIGHT = h

class DummyFile:
    def __getattr__(self, name):
        return self.method
    def method(self, *args, **kwargs):
        pass

class glo: pass
Demo = sounds = main = glo()
Demo.__dict__ = globals()

class Event:

    def __init__(self, *args):
        self.__args = args

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join(map(repr, self.__args)))

    def __call__(self, handler=None):
        if handler is None:
            return self.__args
        else:
            getattr(handler, self.__class__.__name__)(*self.__args)

class setDocumentLocator(Event): pass
class startDocument(Event): pass
class endDocument(Event): pass
class startPrefixMapping(Event): pass
class endPrefixMapping(Event): pass
class startElement(Event): pass
class endElement(Event): pass
class startElementNS(Event): pass
class endElementNS(Event): pass
class characters(Event): pass
class ignorableWhitespace(Event): pass
class processingInstruction(Event): pass
class skippedEntity(Event): pass

class Stream:

    def __init__(self, filename_or_stream_or_string):
        self.__stream = []
        if isinstance(filename_or_stream_or_string, bytes):
            filename_or_stream_or_string = filename_or_stream_or_string.decode()
        if isinstance(filename_or_stream_or_string, str):
            if _os.path.exists(filename_or_stream_or_string):
                _xml_sax.parse(filename_or_stream_or_string, self)
            else:
                _xml_sax.parseString(filename_or_stream_or_string.encode(), self)
        else:
            _xml_sax.parse(filename_or_stream_or_string, self)
        self.__maximized = self.__minimized = False

    def __getattr__(self, name):
        self.__dict__[name] = Method(self.__stream, name)
        return self.__dict__[name]

    def __iter__(self):
        return iter(self.__stream)

    def parse(self, handler):
        for event in self:
            event(handler)

    def maximize(self, style):
        if not self.__maximized:
            self.minimize()
            self.__minimized = False
            self.__maximized = True
            if isinstance(self.__stream[0], setDocumentLocator):
                index =  2
            else:
                index =  1
            level = 0
            cancel = False
            while True:
                event = self.__stream[index]
                if isinstance(event, (startPrefixMapping, startElement, startElementNS)):
                    self.__stream.insert(index, characters(style * level))
                    index += 2
                    if not isinstance(self.__stream[index], (endDocument, endPrefixMapping, endElement, endElementNS)):
                        self.__stream.insert(index, characters('\n'))
                        index += 1
                        level += 1
                elif isinstance(event, (endPrefixMapping, endElement, endElementNS)):
                    if not isinstance(self.__stream[index - 1], (startDocument, startPrefixMapping, startElement, startElementNS)):
                        level -= 1
                        if cancel:
                            cancel = False
                            index += 1
                        else:
                            self.__stream.insert(index, characters(style * level))
                            index += 2
                    else:
                        index += 1
                    self.__stream.insert(index, characters('\n'))
                    index += 1
                elif isinstance(event, endDocument):
                    break
                elif isinstance(event, characters):
                    del self.__stream[index - 1]
                    cancel = True

    def minimize(self):
        if not self.__minimized:
            self.__maximized = False
            self.__minimized = True
            if isinstance(self.__stream[0], setDocumentLocator):
                index = 2
            else:
                index = 1
            inside = True
            while index < len(self.__stream):
                event = self.__stream[index]
                if isinstance(event, (startPrefixMapping, startElement, startElementNS)):
                    inside = True
                    index = self.__prune(index)
                elif isinstance(event, (endDocument, endPrefixMapping, endElement, endElementNS)):
                    if inside:
                        inside = False
                        index = self.__join(index)
                    else:
                        index = self.__prune(index)
                index += 1

    def __prune(self, index):
        temp = index - 1
        event = self.__stream[temp]
        while not isinstance(event, (startDocument, startPrefixMapping, endPrefixMapping, startElement, endElement, startElementNS, endElementNS)):
            if isinstance(event, characters):
                del self.__stream[temp]
                index -= 1
            temp -= 1
            event = self.__stream[temp]
        return index

    def __join(self, index):
        temp = index - 1
        event_1 = self.__stream[temp]
        while not isinstance(event_1, (startDocument, startPrefixMapping, startElement, startElementNS)):
            if isinstance(event_1, characters):
                event_2 = self.__stream[temp - 1]
                if isinstance(event_2, characters):
                    self.__stream[temp] = characters(event_2()[0] + event_1()[0])
                    del self.__stream[temp - 1]
                    index -= 1
            temp -= 1
            event_1 = self.__stream[temp]
        return index

class Method:

    def __init__(self, stream, name):
        self.__stream = stream
        self.__name = name

    def __call__(self, *args):
        self.__stream.append(globals()[self.__name](*args))

class ConfigParser:

    def __init__(self):
        self.sounds = {}

    def __getattr__(self, name):
        return Event

    def startElement(self, name, attrs):
        if name == 'Sound':
            self.__sound = attrs.getValue('name'), attrs.getValue('data_type')
        if name == 'Theme':
            self.__parse_background(attrs)
    
    def __parse_background(self, attrs):
        self.TITLE_COLOR = attrs.getValue('title_color')
        background_type = attrs.getValue('background_type')
        if background_type == 'color':
            self.BACKGROUND_COLOR = attrs.getValue('background_fill')
        elif background_type == 'picture':
            raise Exception('Picture backgrounds are not yet supported')
        else:
            raise Exception('Unknown background type')

    def characters(self, content):
        self.sounds[self.__sound[0]] = self.__sound[1], content

try:
    import winsound
except ImportError:
    class Server:
        def __init__(self, path, history):
            stream = Stream(main.zlib.decompress(file(path, 'rb').read()))
            stream.minimize()
            parser = ConfigParser()
            stream.parse(parser)
            self.TITLE_COLOR = parser.TITLE_COLOR
            self.BACKGROUND_COLOR = parser.BACKGROUND_COLOR
        def play(self, name, block=False):
            pass
else:

    class WAV:

        def __init__(self, data, path):
            path += '.wav'
            with open(path, 'wb') as file:
                file.write(data)
            self.__path = path

        def play(self):
            winsound.PlaySound(self.__path, winsound.SND_FILENAME)

    class PIF:

        def __init__(self, data):
            data = data.split(' ')
            data = [data[index:index+3] for index in range(0, len(data), 3)]
            self.__data = [(float(secs), int(frequency), int(duration)) for secs, frequency, duration in data]

        def play(self):
            for secs, frequency, duration in self.__data:
                time.sleep(secs)
                winsound.Beep(frequency, duration)
            
    class Server:
        
        def __init__(self, path, history):
            self.__history = history
            stream = Stream(main.zlib.decompress(open(path, 'rb').read()))
            stream.minimize()
            parser = ConfigParser()
            stream.parse(parser)
            self.TITLE_COLOR = parser.TITLE_COLOR
            self.BACKGROUND_COLOR = parser.BACKGROUND_COLOR
            self.__sounds = {}
            for key in parser.sounds:
                data_type, data = parser.sounds[key]
                if data_type == 'wav':
                    path = os.path.join(os.path.dirname(path), data)
                    self.__sounds[key] = WAV(bz2.decompress(open(path, 'rb').read()), path)
                else:
                    assert data_type == 'pif'
                    self.__sounds[key] = PIF(data)
            self.__playlist = Queue.Queue()
            thread.start_new_thread(self.__safe_player, ())
        
        def play(self, name, block=False):
            cPickle.dump((name, block), self.__history, -1)
            if block:
                lock = thread.allocate_lock()
                lock.acquire()
                self.__playlist.put([name, lock])
                lock.acquire()
            else:
                self.__playlist.put([name])

        def __safe_player(self):
            try:
                self.__player()
            except:
                traceback.print_exc()

        def __player(self):
            while True:
                if self.__playlist.empty():
                    item = self.__playlist.get()
                    if item[0] in self.__sounds:
                        self.__sounds[item[0]].play()
                    if len(item) == 2:
                        item[1].release()
                else:
                    stack = []
                    while not self.__playlist.empty():
                        stack.append(self.__playlist.get())
                    while stack:
                        item = stack.pop()
                        if item[0] in self.__sounds:
                            self.__sounds[item[0]].play()
                            if len(item) == 2:
                                item[1].release()
                            break
                        elif len(item) == 2:
                            item[1].release()
                    while stack:
                        item = stack.pop()
                        if len(item) == 2:
                            item[1].release()

class Screen(Demo.util.Screen3):

    def __init__(self, start_frame, callback, root):
        height = len(start_frame)
        width = len(start_frame[0])
        self.keys = [[[None, None] for column in range(width)] for row in range(height)]
        self.hand = [[[None, None] for column in range(width)] for row in range(height)]
        self.call = callback
        self.root = Demo.util.Toplevel(root)
        self.root.overrideredirect(True)
        w = width * self.IMAGE_WIDTH + 3
        h = height * self.IMAGE_HEIGHT + 3
        x = self.root.winfo_screenwidth()
        y = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (w, h, (x - w) / 2, (y - h) / 2))
        self.root.focus_force()
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.bind_all('<Escape>', self.exit)
        self.canvas = Demo.util.Canvas(self.root, width=w, height=h)
        self.canvas.config(background=self.BACKGROUND_COLOR)
        self.canvas.pack()
        self.start(start_frame)
        self.canvas.after(125, self.after_loop)

    def exit(self, *args):
        global DO_EXIT
        self.root.destroy()
        DO_EXIT = True
        raise SystemExit()

    def start(self, frame):
        for rnum, row in enumerate(frame):
            for cnum, key in enumerate(row):
                env, act = key
                self.keys[rnum][cnum][0] = env
                if env in self.IMAGES:
                    c = self.coords(cnum, rnum)
                    handle = self.canvas.create_image(c, image=self.IMAGES[env])
                    self.hand[rnum][cnum][0] = handle
        self.canvas.update()

    def coords(self, cnum, rnum):
        x = cnum * self.IMAGE_WIDTH + self.IMAGE_WIDTH / 2 + 1
        y = rnum * self.IMAGE_HEIGHT + self.IMAGE_HEIGHT / 2 + 1
        return x, y

    def after_loop(self):
        global DO_EXIT
        try:
            self.call()
            self.canvas.after(125, self.after_loop)
        except AssertionError:
            self.root.destroy()
            DO_EXIT = False
            raise SystemExit()
        except:
            self.exit()

    def update(self, frame):
        for rnum, row in enumerate(frame):
            for cnum, key in enumerate(row):
                env, act = key
                act_key = self.keys[rnum][cnum][1]
                act_hand = self.hand[rnum][cnum][1]
                if act != act_key:
                    if act_hand is not None:
                        self.canvas.delete(act_hand)
                    if act is not None:
                        c = self.coords(cnum, rnum)
                        handle = self.canvas.create_image(c, image=self.IMAGES[act])
                        self.hand[rnum][cnum][1] = handle
                    else:
                        self.hand[rnum][cnum][1] = None
                    self.keys[rnum][cnum][1] = act
                env_key = self.keys[rnum][cnum][0]
                env_hand = self.hand[rnum][cnum][0]
                if env != env_key:
                    if env_hand is not None:
                        self.canvas.delete(env_hand)
                    if env != ' ':
                        c = self.coords(cnum, rnum)
                        handle = self.canvas.create_image(c, image=self.IMAGES[env])
                        self.hand[rnum][cnum][0] = handle
                        act_hand = self.hand[rnum][cnum][1]
                        if act_hand is not None:
                            self.canvas.tag_raise(act_hand, handle)
                    else:
                        self.hand[rnum][cnum][0] = None
                    self.keys[rnum][cnum][0] = env
        self.canvas.update()

def execute():
    Demo.select_theme()
    history = load_video()
    Demo.load_images()
    load_sounds()
    try:
        play(history)
    finally:
        history.close()

def load_video():
    filename = Demo.tkFileDialog.askopenfilename(title='Open Video', filetypes=['Audio/Video .gvb', 'Video .gva'])
    if filename:
        history = Demo.tempfile.TemporaryFile()
        data = Demo.zlib.decompress(open(filename, 'rb').read())
        history.write(data)
        del data
        history.seek(0)
        return history
    else:
        raise SystemExit

def load_sounds():
    global sound
    sound = Demo.sounds.Server(Demo.util.os.path.join(Demo.util.os.getcwd(), 'themes', Screen.IMAGE_THEME, 'theme_config.xml'), Demo.DummyFile())
    Screen.BACKGROUND_COLOR = sound.BACKGROUND_COLOR

def play(history):
    global frames, screen, c_height, c_width, frame
    frames = history
    frame = Demo.util.cPickle.load(history)
    while True:
        c_height = len(frame)
        c_width = len(frame[0])
        screen = Screen(frame, updater, Demo.root)
        try:
            screen.root.mainloop()
        except SystemExit:
            if DO_EXIT:
                break

def updater():
    global frame
    frame = Demo.util.cPickle.load(frames)
    while isinstance(frame, tuple):
        sound.play(*frame)
        frame = Demo.util.cPickle.load(frames)
    height = len(frame)
    width = len(frame[0])
    assert height == c_height and width == c_width
    screen.update(frame)

if __name__ == '__main__':
    execute()
