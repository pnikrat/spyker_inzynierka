from tkinter import *
from tkinter import ttk
from spyker.recording import *
from spyker.plotter import *
from spyker.decoding import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        self.chartframe = Frame(self, borderwidth=1, relief="sunken", width=400, height=200)
        self.chartframe2 = Frame(self, borderwidth=1, relief="sunken", width=400, height=200)

        self.namelabel = Label(self.nameframe, text="Name")
        self.nameentry = Entry(self.nameframe)

        self.timelabel = Label(self.timeframe, text="Time")
        self.timeentry = Entry(self.timeframe)

        self.savebutton = Button(self.buttonframe, text="Record")
        self.savebutton.bind("<Button-1>", self.recordSound)
        self.loadbutton = Button(self.buttonframe, text="Load")
        self.playbutton = Button(self.buttonframe, text="Play")

        self.plotter1 = Plotter()
        self.plotter2 = Plotter() # prawdopodobnie niepotrzebne, tylko dla testow i porownania danych z dwoch kanalow
        # w przyszlosci prezentowane fft danych z .wav
        self.canvas = None

        self.createnameframe()
        self.createtimeframe()
        self.createbuttonframe()
        self.createchartframe(1, 0, 3, 3, 5, 5)
        self.createchartframe2(1, 3, 3, 3, 5, 5)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=3)

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

    def createchartframe(self, col, row, colspan, rowspan, padx, pady):
        self.chartframe.grid(column=col, row=row, columnspan=colspan, rowspan=rowspan, sticky=NSEW, padx=padx,
                             pady=pady)

    def createchartframe2(self, col, row, colspan, rowspan, padx, pady):
        self.chartframe2.grid(column=col, row=row, columnspan=colspan, rowspan=rowspan, sticky=NSEW, padx=padx,
                              pady=pady)

    def bind_figure_to_char(self):
        self.canvas = FigureCanvasTkAgg(self.plotter1.figure, master=self.parent)
        self.chartframe = self.canvas
        self.canvas.show()

    def recordSound(self, event):
        stream = SoundStream(1024, pyaudio.paInt16, 2, 44100)
        stream.open_stream()
        stream.record(int(self.timeentry.get()))
        stream.close_stream()
        # wrzucic do osobnej funkcji
        temp = bytestring_to_intarray(stream.get_frames())
        self.plotter1.datay = temp[:, 0]
        self.plotter2.datay = temp[:, 1]
        self.plotter1.slice_time(2)
        self.plotter2.slice_time(2)
        self.plotter1.plot()
        self.bind_figure_to_char()
        print(self.plotter1.datax)
        stream.save_to_file(str(self.nameentry.get()))

