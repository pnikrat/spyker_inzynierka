from tkinter import *
import sys


class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        file_menu = Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=file_menu)
        file_menu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)


class Input(Entry):
    def __init__(self, parent):
        Entry.__init__(self, parent)


class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        frame = Frame(self)
        frame.pack()

        bottomframe = Frame(self)
        bottomframe.pack(side=BOTTOM)

        redbutton = Button(frame, text="Red", fg="red")
        redbutton.pack(side=LEFT)

        greenbutton = Button(frame, text="Brown", fg="brown")
        greenbutton.pack(side=LEFT)

        bluebutton = Button(frame, text="Blue", fg="blue")
        bluebutton.pack(side=LEFT)

        blackbutton = Button(bottomframe, text="Black", fg="black")
        blackbutton.pack(side=BOTTOM)

        menu_bar = MenuBar(self)
        self.config(menu=menu_bar)
