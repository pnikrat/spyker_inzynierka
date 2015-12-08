import inspect

from PyQt4 import QtGui
from PyQt4.uic.properties import QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
import matplotlib.pyplot as plt
import scipy.signal
import scipy.io.wavfile

from spyker.utils.constants import RECS_DIR
from spyker.utils.pltutils import plot_function
from spyker.utils.utils import get_kwargs


class ChartWindow(QtGui.QDialog):
    def __init__(self, function, filename, parent=None):
        super(ChartWindow, self).__init__(parent)

        self.kwarg_edits = []
        self.function = function
        self.filename = filename
        self.fig = plt.figure()

        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.replot)

        self.plot_layout = QtGui.QVBoxLayout()
        self.plot_layout.addWidget(self.canvas)
        self.plot_layout.addWidget(self.toolbar)

        self.data_layout = QtGui.QVBoxLayout()
        self.arg_edits = []
        self.add_kwarg_fields()
        self.data_layout.addWidget(self.button)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addLayout(self.plot_layout)
        self.layout.addLayout(self.data_layout)

        self.replot()
        self.setLayout(self.layout)
        self.resize(700, 500)

    def replot(self):
        data = self.function(*self.get_args())
        plot_function(self.fig, data)
        self.canvas.draw()

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

                self.data_layout.addLayout(h_box_layout)

    def get_args(self):
        fs, data = scipy.io.wavfile.read(RECS_DIR + '/' + self.filename)
        args = [fs, data]
        for kwarg_edit in self.kwarg_edits:
            args.append(float(kwarg_edit.text()))
        return args