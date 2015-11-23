from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure
import scipy.io.wavfile
import numpy as np
from PyQt4 import QtGui
from scikits.talkbox.features import mfcc
from matplotlib.mlab import specgram
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
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

        self.axes.imshow(ceps, origin='lower', aspect='auto', extent=(x.min(), x.max(), y.min(), y.max()))
        self.axes.set_xlabel('Frame number')
        self.axes.set_ylabel('Coefficient number')


class Raw(MyCanvas):
    def __init__(self, *args, **kwargs):
        super(Raw, self).__init__(*args, **kwargs)

    def compute_figure(self, filename):
        sample_rate, data = scipy.io.wavfile.read(RECS_DIR + "/" + filename)
        time = np.linspace(0, float(len(data)) / sample_rate, len(data))
        data = self.rescale(data)
        self.axes.plot(time, data)
        self.axes.set_xlabel('Time [s]')
        self.axes.set_ylabel('Amplitude [-]')

    def rescale(self, data):
        # rescale in place
        data = data.astype(float) / 32768.0
        return data


class STFT3D(MyCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, filename=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.gca(projection='3d')

        self.compute_figure(filename)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_figure(self, filename):
        sample_rate, data = scipy.io.wavfile.read(RECS_DIR + "/" + filename)
        (spectrum, freqs, t) = specgram(data, NFFT=256, Fs=sample_rate)
        print freqs.shape, t.shape
        t, freqs = np.meshgrid(t, freqs)
        print freqs.shape, t.shape, spectrum.shape
        surf = self.axes.plot_surface(freqs, t, spectrum, rstride=3, cstride=3, cmap=cm.coolwarm,  linewidth=0)
        self.fig.colorbar(surf)


class FFT(MyCanvas):
    def __init__(self, *args, **kwargs):
        super(FFT, self).__init__(*args, **kwargs)

    def compute_figure(self, filename):
        sample_rate, data = scipy.io.wavfile.read(RECS_DIR + '/' + filename)
        time = np.linspace(0, float(len(data)) / sample_rate, len(data))
        #data_windowed = scipy.hanning(data)
        complex_array = np.fft.fft(data, len(data))
        freq = np.fft.fftfreq(time.shape[-1], 1.0 / sample_rate)
        module = ((complex_array.real**2 + complex_array.imag**2)**0.5) / len(data)
        self.axes.plot(freq[:(len(freq) / 2)], module[:(len(module) / 2)], 'g')
        self.axes.set_xlabel('Frequency [Hz]')
        self.axes.set_ylabel('Amplitude [-]')


class STFT(MyCanvas):
    def __init__(self, *args, **kwargs):
        super(STFT, self).__init__(*args, **kwargs)

    def compute_figure(self, filename):
        fs, x = scipy.io.wavfile.read(RECS_DIR + '/' + filename)
        frame_size = 0.050  # with a frame size of 50 milliseconds
        hop = 0.025  # and hop size of 25 milliseconds.
        frame_samp = int(frame_size * fs)
        hop_samp = int(hop * fs)
        w = scipy.hanning(frame_samp)
        X = scipy.array([scipy.fft(w * x[i:i + frame_samp])
                         for i in range(0, len(x) - frame_samp, hop_samp)])

        self.axes.imshow(scipy.absolute(X.T), origin='lower', aspect='auto', interpolation='nearest', norm=LogNorm())
        self.axes.set_xlabel('Frame number [-]')
        self.axes.set_ylabel('Frequency [Hz]')

