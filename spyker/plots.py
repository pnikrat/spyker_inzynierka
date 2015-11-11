from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from spyker.utils.constants import *
from scikits.talkbox.features import mfcc
import scipy.io.wavfile
import numpy as np


class MyCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, filename=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        self.compute_figure(filename)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_figure(self, filename): #abstract method
        pass


class MFCC(MyCanvas):
    def __init__(self, *args, **kwargs):
        super(MFCC, self).__init__(*args, **kwargs)

    def compute_figure(self, filename):
        sample_rate, X = scipy.io.wavfile.read(RECS_DIR + "/" + filename)
        ceps, mspec, spec = mfcc(X)

        m, n = ceps.shape
        x, y = np.mgrid[0:m, 0:n]

        self.axes.imshow(ceps, origin='lower', aspect='auto', extent=(x.min(), x.max(), y.min(), y.max()))
