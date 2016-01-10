import inspect

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile
import scipy.signal
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QHBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

from spyker.gui.entrylayout import EntryLayout
from spyker.utils.constants import RECS_DIR, ChartType
from spyker.utils.pltutils import plt_single, plot_function, plot_3d
from spyker.utils.utils import get_kwargs


class ChartWindow(QtGui.QMainWindow):
    def __init__(self, function, file_name, function_name, file_list_model, parent=None):
        super(ChartWindow, self).__init__(parent)
        self.function = function
        self.function_name = function_name
        self.file_name = file_name
        self.file_list_model = file_list_model
        self.fs, self.data = scipy.io.wavfile.read(RECS_DIR + '/' + self.file_name)

        self.init_figure()
        self.init_ui()

    def init_ui(self):
        self.init_layout()
        self.init_plot()
        self.showMaximized()
        self.setWindowTitle('Recording "' + str(self.file_name) + '" : ' + str(self.function_name))

    def init_layout(self):
        self.layout = QtGui.QHBoxLayout()
        self.init_plot_layout()
        self.init_controls_layout()

        window = QtGui.QWidget()
        window.setLayout(self.layout)
        self.setCentralWidget(window)

    def init_figure(self):
        self.fig = plt.figure()
        self.second_fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.vline = self.ax.axvline(color='r')
        self.hline = self.ax.axhline(color='y')

    def init_plot_layout(self):

        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.plot_layout = QtGui.QVBoxLayout()
        self.plot_layout.addWidget(self.canvas)
        self.plot_layout.addWidget(self.toolbar)
        self.layout.addLayout(self.plot_layout, 3)

    def init_controls_layout(self):
        self.controls_layout = QtGui.QVBoxLayout()
        self.init_params_layout()
        self.layout.addLayout(self.controls_layout, 2)

    def init_params_layout(self):
        self.params_layout = QtGui.QVBoxLayout()
        self.params_layout.setAlignment(Qt.AlignTop)

        self.kwarg_edits = []
        self.add_kwarg_fields()

        self.button = QtGui.QPushButton('Plot main recording')
        self.button.clicked.connect(lambda: self.replot(self.function(*self.get_args())))
        self.params_layout.addWidget(self.button)

        if is_two_d(self.function_name):
            plot_next_layout = ComboLayout("Plot next: ", self.file_list_model, self.plot_next)
            self.params_layout.addLayout(plot_next_layout)

        plot_difference_layout = ComboLayout("Plot difference: ", self.file_list_model, self.plot_difference)
        self.params_layout.addLayout(plot_difference_layout)
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
                lambda: plt_single(self.second_fig, self.plotted_data, self.x_cursor_layout.slider.value(), 'x'
                                   , self.fig, is_gca(self.function_name)))

        self.x_cursor_layout.button.clicked.connect(self.second_canvas.draw)
        self.x_cursor_layout.button.clicked.connect(self.canvas.draw)

        self.y_cursor_layout.button.clicked.connect(
                lambda: plt_single(self.second_fig, self.plotted_data, self.y_cursor_layout.slider.value(), 'y'
                                   , self.fig, is_gca(self.function_name)))

        self.y_cursor_layout.button.clicked.connect(self.second_canvas.draw)
        self.y_cursor_layout.button.clicked.connect(self.canvas.draw)

    def init_second_canvas(self):
        self.second_canvas_layout = QtGui.QVBoxLayout()
        self.second_canvas = FigureCanvas(self.second_fig)
        self.second_toolbar = NavigationToolbar2QT(self.second_canvas, self)
        self.second_canvas_layout.addWidget(self.second_canvas)
        self.second_canvas_layout.addWidget(self.second_toolbar)
        self.controls_layout.addLayout(self.second_canvas_layout)

    def init_plot(self):

        self.replot(self.function(*self.get_args()))
        if not is_two_d(self.function_name):
            self.init_second_canvas()
            self.init_cursors_layout()
            self.init_cursors()
            self.plot_sliders()

    def replot(self, data_to_plot):
        if 'z_vector' in data_to_plot:
            plot_3d(self.fig, data_to_plot)
        else:
            data_to_plot['legend'] = self.file_name
            plot_function(self.fig, data_to_plot)

        if hasattr(self, 'x_cursor_layout'):
            self.plot_sliders()

        self.canvas.draw()
        self.plotted_data = data_to_plot

    def get_args(self):
        args = [self.fs, self.data] + self.get_kwargs()
        return args

    def get_kwargs(self):
        kwargs = []
        for kwarg_edit in self.kwarg_edits:
            kwargs.append(float(kwarg_edit.text()))
        return kwargs

    def plot_next(self, index):
        additional_recording = self.file_list_model.file_paths[index]
        fs, data = scipy.io.wavfile.read(RECS_DIR + "/" + additional_recording)
        plot_data = self.function(fs, data)
        plot_data['legend'] = additional_recording
        plot_function(self.fig, plot_data, clear=False)
        self.canvas.draw()

    def plot_difference(self, index):
        recording_to_subtract = self.file_list_model.file_paths[index]
        file_to_subtract_fs, file_to_subtract_data = scipy.io.wavfile.read(RECS_DIR + '/' + recording_to_subtract)

        data_copy = np.ndarray.copy(self.data)

        if data_copy.shape > file_to_subtract_data.shape:
            data_copy.resize(file_to_subtract_data.shape)
        elif data_copy.shape < file_to_subtract_data.shape:
            file_to_subtract_data.resize(data_copy.shape)

        args = [self.fs, self.data] + self.get_kwargs()
        data_to_plot = self.function(*args)
        minuend_y_vector = data_to_plot['y_vector']

        subtrahend_args = [file_to_subtract_fs, file_to_subtract_data] + self.get_kwargs()
        subtrahend_y_vector = self.function(*subtrahend_args)['y_vector']

        y_vector_to_plot = minuend_y_vector - subtrahend_y_vector

        data_to_plot['y_vector'] = y_vector_to_plot
        self.replot(data_to_plot)

    def plot_sliders(self):
        x_slider_max = len(self.plotted_data['y_vector'][0]) - 1
        x_real_max = self.plotted_data['xticks']['labels'][-1]
        self.x_cursor_layout.set_maximum(x_slider_max, x_real_max)

        y_slider_max = len(self.plotted_data['y_vector']) - 1
        y_real_max = self.plotted_data['yticks']['labels'][-1]
        self.y_cursor_layout.set_maximum(y_slider_max, y_real_max)

    def add_kwarg_fields(self):
        if inspect.getargspec(self.function).defaults is not None:
            for k, v in get_kwargs(self.function).iteritems():
                edit_layout = QtGui.QGridLayout()

                edit_layout.setColumnStretch(0, 1)
                edit_layout.setColumnStretch(1, 2)
                label = QtGui.QLabel(k)
                kwarg_edit = QtGui.QLineEdit(str(v))
                edit_layout.addWidget(label, 0, 0)
                edit_layout.addWidget(kwarg_edit, 0, 1)
                self.kwarg_edits.append(kwarg_edit)

                self.params_layout.addLayout(edit_layout)


def is_two_d(function_name):
    return function_name != ChartType.STFT3D and function_name != ChartType.STFT \
           and function_name != ChartType.MFCC


def is_gca(function_name):
    return function_name == ChartType.STFT3D


class ComboLayout(QtGui.QHBoxLayout):
    def __init__(self, name, model, fun_to_call):
        QHBoxLayout.__init__(self)

        label = QtGui.QLabel(name)

        combo = QtGui.QComboBox()
        combo.setModel(model)

        button = QtGui.QPushButton("Plot")
        button.clicked.connect(lambda: fun_to_call(combo.currentIndex()))

        self.addWidget(label)
        self.addWidget(combo)
        self.addWidget(button)
