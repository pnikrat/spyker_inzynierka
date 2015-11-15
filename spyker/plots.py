from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scikits.talkbox.features import mfcc
import numpy as np
import scipy
import scipy.io.wavfile

from spyker.utils.constants import *


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

    def compute_figure(self, filename):  # abstract method
        pass


class MFCC(MyCanvas):
    def __init__(self, *args, **kwargs):
        super(MFCC, self).__init__(*args, **kwargs)

    def compute_figure(self, filename):
        sample_rate, X = scipy.io.wavfile.read(RECS_DIR + "/" + filename)
        ceps, mspec, spec = mfcc(X)

        m, n = ceps.shape
        x, y = np.mgrid[0:m, 0:n]
        return ceps


def mfccoef(x):
    ceps, mspec, spec = mfcc(x)
    return ceps


def stft(x, fs):
    frame_size = 0.050  # with a frame size of 50 milliseconds
    hop = 0.025  # and hop size of 25 milliseconds.
    frame_samp = int(frame_size * fs)
    hop_samp = int(hop * fs)
    w = scipy.hanning(frame_samp)
    X = scipy.array([scipy.fft(w * x[i:i + frame_samp])
                     for i in range(0, len(x) - frame_samp, hop_samp)])
    return X
