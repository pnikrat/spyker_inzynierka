import matplotlib as plt
from scikits.talkbox.features import mfcc
import scipy.io.wavfile

plt.use('TkAgg')
import numpy as np
from matplotlib.figure import Figure


class Plotter:
    def __init__(self):
        self.datay = None
        self.datax = None
        self.figure = None

    def plot(self):
        fig = Figure(figsize=(3, 3), dpi=100)  # figsize - (width,height) in inches
        ax = fig.add_subplot(111)  # nrows, ncols, plot_number
        ax.plot(self.datax, self.datay)
        self.figure = fig

    def set_datay(self, datay):
        self.datay = datay

    def slice_time(self, record_time):
        assert self.datay is not None, "No data y in plotter"
        self.datax = np.linspace(0, record_time, len(self.datay))

    def fft(self, samples):
        # if len(samples) % 2 != 0:
        #     samples = samples[:(len(samples)-1),:]
        A = np.fft.fft(samples, len(samples))
        freqaxis = np.fft.fftfreq(len(samples))
        amplitude = np.abs(A)
        phase = np.angle(A)
        self.datax = freqaxis
        self.datay = amplitude

    def plot_mfcc(self, filename):
        sample_rate, X = scipy.io.wavfile.read(filename)
        ceps, mspec, spec = mfcc(X)

        m, n = ceps.shape
        x, y = np.mgrid[0:m, 0:n]

        fig = Figure(figsize=(3, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.imshow(ceps, origin='lower', aspect='auto', extent=(x.min(), x.max(), y.min(), y.max()))
        self.figure = fig
