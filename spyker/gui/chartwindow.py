import inspect

import matplotlib.pyplot as plt
import scipy.io.wavfile
import scipy.signal
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

from spyker.gui.entrylayout import EntryLayout
from spyker.utils.constants import RECS_DIR
from spyker.utils.pltutils import *
from spyker.utils.utils import get_kwargs


class ChartWindow(QtGui.QDialog):
    def __init__(self, function, filename, fname, parent=None):
        super(ChartWindow, self).__init__(parent)
        self.function = function
        self.fname = fname
        self.filename = filename
        self.init_figure()
        self.init_ui()

    def init_ui(self):
        self.init_layout()
        self.init_plot()
        self.resize(1000, 600)
        self.setWindowTitle('Recording "' + str(self.filename) + '" : ' + str(self.fname))

    def init_layout(self):
        self.layout = QtGui.QHBoxLayout()
        self.init_plot_layout()
        self.init_controls_layout()

        self.setLayout(self.layout)

    def init_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.vline = self.ax.axvline(color='r')
        self.hline = self.ax.axhline(color='y')

        # cursor = Cursor(ax)
        # cursor = SnaptoCursor(ax, t, s)
        # plt.connect('motion_notify_event', cursor.mouse_move)

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

        self.x_cursor_layout = EntryLayout('x cursor', )
        self.y_cursor_layout = EntryLayout('y cursor')

        self.cursors_layout.addLayout(self.x_cursor_layout)
        self.cursors_layout.addLayout(self.y_cursor_layout)

        self.controls_layout.addLayout(self.cursors_layout)

    def init_cursors(self):
        self.x_cursor_layout.button.clicked.connect(
                lambda: plt_single(self.fig, self.data, self.x_cursor_layout.slider.value(), 'x'))
        self.x_cursor_layout.button.clicked.connect(self.canvas.draw)

        self.y_cursor_layout.button.clicked.connect(
                lambda: plt_single(self.fig, self.data, self.y_cursor_layout.slider.value(), 'y'))
        self.y_cursor_layout.button.clicked.connect(self.canvas.draw)



    def init_plot(self):
        self.replot()
        if len(self.data['labels']) == 3:
            self.init_cursors_layout()
            self.init_cursors()
            self.update_sliders()

    def replot(self):
        self.data = self.function(*self.get_args())
        plot_function(self.fig, self.data)

        if hasattr(self, 'x_cursor_layout'):
            self.update_sliders()

        self.canvas.draw()

    def update_sliders(self):
        self.x_cursor_layout.set_maximum(len(self.data['y_vector'][0]) - 1)
        self.y_cursor_layout.set_maximum(len(self.data['y_vector']) - 1)

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
        fs, data = scipy.io.wavfile.read(RECS_DIR + '/' + self.filename)
        args = [fs, data]
        for kwarg_edit in self.kwarg_edits:
            args.append(float(kwarg_edit.text()))
        return args

# class Cursor(object):
#     def __init__(self, ax):
#         self.ax = ax
#         self.lx = ax.axhline(color='k')  # the horiz line
#         self.ly = ax.axvline(color='k')  # the vert line
#
#         # text location in axes coords
#         # self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
#
#     def mouse_move(self, event):
#         if not event.inaxes:
#             return
#
#         x, y = event.xdata, event.ydata
#         # update the line positions
#         self.lx.set_ydata(y)
#         self.ly.set_xdata(x)
#
#         # self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
#         plt.draw()
