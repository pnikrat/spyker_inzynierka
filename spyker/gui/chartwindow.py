import inspect

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile
import scipy.signal
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

from spyker.gui.entrylayout import EntryLayout
from spyker.gui.filepicker import FilePicker
from spyker.listeners.filepickerlistener import FilePickerListener
from spyker.utils.constants import RECS_DIR
from spyker.utils.pltutils import *
from spyker.utils.utils import get_kwargs


class ChartWindow(QtGui.QMainWindow, FilePickerListener):
    def __init__(self, function, file_name, function_name, file_list_model, parent=None):
        super(ChartWindow, self).__init__(parent)
        self.function = function
        self.function_name = function_name
        self.file_name = file_name
        self.additional_file = None
        self.file_list_model = file_list_model
        self.fs, self.data = scipy.io.wavfile.read(RECS_DIR + '/' + self.file_name)

        self.init_figure()
        self.init_ui()

    def init_ui(self):
        self.init_layout()
        self.init_plot()
        self.resize(1000, 600)
        self.setWindowTitle('Recording "' + str(self.file_name) + '" : ' + str(self.function_name))

    def init_layout(self):
        self.layout = QtGui.QHBoxLayout()
        self.init_plot_layout()
        self.init_controls_layout()
        self.init_menu()

        window = QtGui.QWidget()
        window.setLayout(self.layout)
        self.setCentralWidget(window)

    def init_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.vline = self.ax.axvline(color='r')
        self.hline = self.ax.axhline(color='y')

    def init_plot_layout(self):

        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.plot_layout = QtGui.QVBoxLayout()
        self.plot_layout.addWidget(self.canvas)
        self.plot_layout.addWidget(self.toolbar)
        self.layout.addLayout(self.plot_layout, 2)

    def init_controls_layout(self):
        self.controls_layout = QtGui.QVBoxLayout()
        self.init_params_layout()
        self.layout.addLayout(self.controls_layout, 1)

    def init_params_layout(self):
        self.params_layout = QtGui.QVBoxLayout()
        self.params_layout.setAlignment(Qt.AlignTop)

        self.kwarg_edits = []
        self.add_kwarg_fields()

        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.replot)
        self.params_layout.addWidget(self.button)
        self.controls_layout.addLayout(self.params_layout)

    def init_cursors_layout(self):
        self.cursors_layout = QtGui.QVBoxLayout()
        self.cursors_layout.setAlignment(Qt.AlignTop)

        self.x_cursor_layout = EntryLayout('x cursor')
        self.y_cursor_layout = EntryLayout('y cursor')

        self.cursors_layout.addLayout(self.x_cursor_layout)
        self.cursors_layout.addLayout(self.y_cursor_layout)

        self.controls_layout.addLayout(self.cursors_layout)

    def init_cursors(self):
        self.x_cursor_layout.button.clicked.connect(
                lambda: plt_single(self.fig, self.plot_data, self.x_cursor_layout.slider.value(), 'x'))
        self.x_cursor_layout.button.clicked.connect(self.canvas.draw)

        self.y_cursor_layout.button.clicked.connect(
                lambda: plt_single(self.fig, self.plot_data, self.y_cursor_layout.slider.value(), 'y'))
        self.y_cursor_layout.button.clicked.connect(self.canvas.draw)

    def init_menu(self):

        addAction = QtGui.QAction('&Add', self)
        addAction.setShortcut('Ctrl+A')
        addAction.setStatusTip('Add signal')
        addAction.triggered.connect(lambda: self.pick_file(1))

        subtractAction = QtGui.QAction('&Subtract', self)
        subtractAction.setShortcut('Ctrl+S')
        subtractAction.setStatusTip('Subtract signal')
        subtractAction.triggered.connect(lambda: self.pick_file(-1))

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(addAction)
        fileMenu.addAction(subtractAction)
        fileMenu.addAction(exitAction)

    def init_plot(self):
        self.replot()
        if len(self.plot_data['labels']) == 3:
            self.init_cursors_layout()
            self.init_cursors()
            self.update_sliders()

    def replot(self):
        self.plot_data = self.function(*self.get_args())
        plot_function(self.fig, self.plot_data)

        if hasattr(self, 'x_cursor_layout'):
            self.update_sliders()

        self.canvas.draw()

    def update_sliders(self):
        self.x_cursor_layout.set_maximum(len(self.plot_data['y_vector'][0]) - 1)
        self.y_cursor_layout.set_maximum(len(self.plot_data['y_vector']) - 1)

    def add_kwarg_fields(self):
        if inspect.getargspec(self.function).defaults is not None:
            for k, v in get_kwargs(self.function).iteritems():
                h_box_layout = QtGui.QHBoxLayout()
                label = QtGui.QLabel(k)
                label.setMinimumWidth(50)
                h_box_layout.addWidget(label)

                kwarg_edit = QtGui.QLineEdit(str(v))
                h_box_layout.addWidget(kwarg_edit)
                self.kwarg_edits.append(kwarg_edit)

                self.params_layout.addLayout(h_box_layout)

    def get_args(self):
        if self.additional_file is not None:
            fs, file_data = scipy.io.wavfile.read(RECS_DIR + '/' + self.additional_file)

            if self.data.shape > file_data.shape:
                file_data.resize(self.data.shape)
            elif self.data.shape < file_data.shape:
                self.data.resize(file_data.shape)

            self.data = self.data + self.multiplier * file_data

        print self.data
        args = [self.fs, self.data]
        for kwarg_edit in self.kwarg_edits:
            args.append(float(kwarg_edit.text()))
        return args

    def pick_file(self, multiplier):
        self.pick_file_dialog = FilePicker(self.file_list_model, self)
        self.pick_file_dialog.show()
        self.multiplier = multiplier

    def file_picked(self, picked_file):
        self.additional_file = picked_file
