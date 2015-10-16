from tkinter import *
from tkinter import ttk
from spyker.recording import *


class MenuBar(Menu):
    parent = None

    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent

        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        editmenu = Menu(self, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)

        self.add_cascade(label="File", menu=filemenu)
        self.add_cascade(label="Edit", menu=editmenu)
        self.add_cascade(label="Help", menu=helpmenu)

    def quit(self):
        sys.exit(0)

    def donothing(self):
        filewin = Toplevel(self.parent)
        button = Button(filewin, text="Do nothing button")
        button.pack()


class MainFrame(ttk.Frame):
    def __init__(self, parent, **kw):
        ttk.Frame.__init__(self, parent, **kw)
        self.parent = parent

        self.grid(column=0, row=0, sticky=(N, S, E, W))

        self.nameframe = Frame(self)
        self.timeframe = Frame(self)
        self.buttonframe = Frame(self)
        self.chartframe = Frame(self, borderwidth=1, relief="sunken", width=200, height=100)

        self.namelabel = Label(self.nameframe, text="Name")
        self.nameentry = Entry(self.nameframe)

        self.timelabel = Label(self.timeframe, text="Time")
        self.timeentry = Entry(self.timeframe)

        self.savebutton = Button(self.buttonframe, text="Record")
        self.savebutton.bind("<Button-1>", self.recordSound)
        self.loadbutton = Button(self.buttonframe, text="Load")
        self.playbutton = Button(self.buttonframe, text="Play")

        self.createnameframe()
        self.createtimeframe()
        self.createbuttonframe()
        self.createchartframe()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def createnameframe(self):
        self.namelabel.grid(column=0, row=0, columnspan=1, sticky=W, padx=5)
        self.nameentry.grid(column=0, row=1, columnspan=1, sticky=EW, padx=5)

        self.nameframe.grid(column=0, row=0, columnspan=1, sticky=EW, padx=5, pady=5)
        self.nameframe.columnconfigure(0, weight=1)
        self.nameframe.rowconfigure(0, weight=1)
        self.nameframe.rowconfigure(1, weight=1)

    def createtimeframe(self):
        self.timelabel.grid(column=0, row=0, columnspan=1, sticky=W, padx=5)
        self.timeentry.grid(column=0, row=1, columnspan=1, sticky=EW, padx=5)

        self.timeframe.grid(column=0, row=1, columnspan=1, sticky=EW, padx=5, pady=5)
        self.timeframe.columnconfigure(0, weight=1)
        self.timeframe.rowconfigure(0, weight=1)
        self.timeframe.rowconfigure(1, weight=1)

    def createbuttonframe(self):
        self.savebutton.grid(column=0, row=0, columnspan=1, sticky=EW, padx=5, pady=5)
        self.loadbutton.grid(column=0, row=1, columnspan=1, sticky=EW, padx=5, pady=5)
        self.playbutton.grid(column=0, row=2, columnspan=1, sticky=EW, padx=5, pady=5)

        self.buttonframe.grid(column=0, row=2, columnspan=1, sticky=EW, padx=5, pady=5)

        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.rowconfigure(0, weight=1)
        self.buttonframe.rowconfigure(1, weight=1)
        self.buttonframe.rowconfigure(2, weight=1)

    def createchartframe(self):
        self.chartframe.grid(column=1, row=0, columnspan=3, rowspan=3, sticky=NSEW, padx=5, pady=5)

    def recordSound(self, event):
        stream = SoundStream(1024, pyaudio.paInt16, 2, 44100)
        stream.open_stream()
        stream.record(int(self.timeentry.get()))
        stream.close_stream()
        stream.save_to_file(str(self.nameentry.get()))

