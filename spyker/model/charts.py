import scipy
import scipy.io.wavfile
import numpy as np
from scikits.talkbox.features import mfcc
import scipy.signal
from spyker.utils.constants import RECS_DIR


def envelope(fs, x):
    time = np.linspace(0, float(len(x)) / fs, len(x))
    return time, abs(scipy.signal.hilbert(x))


def stft(fs, x, frame_size=0.01, hop=0.05):
    frame_samp = int(frame_size * fs)
    hop_samp = int(hop * fs)
    w = scipy.hanning(frame_samp)
    X = scipy.array([np.fft.rfft(w * x[i:i + frame_samp]) for i in range(0, len(x) - frame_samp, hop_samp)])
    return scipy.log10(scipy.absolute(X.T))


def mfcceps(fs, x):
    ceps, mspec, spec = mfcc(x)
    return ceps


def raw(fs, x):
    # time = np.linspace(0, float(len(x)) / fs, len(x))
    return x.astype(float) / 32768.0


def fft(fs, x):
    time = np.linspace(0, float(len(x)) / fs, len(x))
    # data_windowed = scipy.hanning(data)
    complex_array = np.fft.fft(x, len(x))
    freq = np.fft.fftfreq(time.shape[-1], 1.0 / fs)
    module = ((complex_array.real ** 2 + complex_array.imag ** 2) ** 0.5) / len(x)
    return freq[:(len(freq) / 2)], module[:(len(module) / 2)]


def envelope(fs, x):
    time = np.linspace(0, float(len(x)) / fs, len(x))
    env = abs(scipy.signal.hilbert(x))
    return env