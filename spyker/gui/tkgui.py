from tkinter import *
from tkinter import ttk
from spyker.recording import *
from spyker.plotter import *
from spyker.decoding import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


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
        self.chartframes = [Frame(self, borderwidth=1, relief="sunken", width=480, height=384),
                            Frame(self, borderwidth=1, relief="sunken", width=480, height=384)]

        self.namelabel = Label(self.nameframe, text="Name")
        self.nameentry = Entry(self.nameframe)

        self.timelabel = Label(self.timeframe, text="Time")
        self.timeentry = Entry(self.timeframe)

        self.savebutton = Button(self.buttonframe, text="Record")
        self.savebutton.bind("<Button-1>", self.record_sound)
        self.loadbutton = Button(self.buttonframe, text="Load")
        self.playbutton = Button(self.buttonframe, text="Play")

        self.plotters = [Plotter(), Plotter()]
        self.canvas = [None, None]

        self.createnameframe()
        self.createtimeframe()
        self.createbuttonframe()
        self.createchartframe(col=1, row=0, colspan=3, rowspan=3, padx=5, pady=5, which_chart=0)
        self.createchartframe(1, 3, 3, 3, 5, 5, 1)

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

    def createchartframe(self, col, row, colspan, rowspan, padx, pady, which_chart):

        self.chartframes[which_chart].grid(column=col, row=row, columnspan=colspan, rowspan=rowspan, sticky=NSEW,
                                          padx=padx, pady=pady)

    def bind_figure_to_char(self, index):
        self.canvas[index] = FigureCanvasTkAgg(self.plotters[index].figure, master = self.chartframes[index])
        self.canvas[index].show()
        self.canvas[index].get_tk_widget().grid(column=1, row=index*3, sticky=NSEW)

    def record_sound(self, event):
        stream = SoundStream(1024, pyaudio.paInt16, 2, 44100)
        stream.open_stream()
        stream.record(int(self.timeentry.get()))
        stream.close_stream()
        self.configure_plots_fft(stream)
        stream.save_to_file(str(self.nameentry.get()))

    def configure_plots_raw(self, stream):
        temp = bytestring_to_intarray(stream.get_frames())
        ind = 0
        for plotter in self.plotters:
            plotter.set_datay(temp[:, ind])
            plotter.slice_time(stream.get_num_of_seconds())
            plotter.plot()
            self.bind_figure_to_char(ind)
            ind += 1

    def configure_plots_fft(self, stream):
        temp = bytestring_to_intarray(stream.get_frames())
        self.plotters[0].fft(temp[:, 0])
        self.plotters[0].plot()
        self.bind_figure_to_char(0)


