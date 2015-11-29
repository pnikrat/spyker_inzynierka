import scipy
import scipy.io.wavfile
import numpy as np
from scikits.talkbox.features import mfcc
import scipy.signal


def envelope(fs, data):
    time = np.linspace(0, float(len(data)) / fs, len(data))
    return time, abs(scipy.signal.hilbert(data))


def stft(fs, data, frame_size=0.01, hop=0.05):
    frame_samp = int(frame_size * fs)
    hop_samp = int(hop * fs)
    w = scipy.hanning(frame_samp)
    data = scipy.array(
        [np.fft.rfft(w * data[i:i + frame_samp]) for i in range(0, len(data) - frame_samp, hop_samp)])
    labels = {'xlabel': 'time', 'ylabel': 'amplitude', 'zlabel': 'dwaddddddd'}
    return scipy.log10(scipy.absolute(data.T)), None, labels


def mfcceps(fs, data):
    ceps, mspec, spec = mfcc(data)
    labels = {'xlabel': 'Coefficient number', 'ylabel': 'Frame number', 'zlabel': 'dwaddddddd'}
    return ceps, None, labels


def raw(fs, data):
    data = data.astype(float) / 32768.0
    time = np.linspace(0, float(len(data)) / fs, len(data))
    labels = {'xlabel': 'Time [s]', 'ylabel': 'Amplitude [-]'}
    return data, time, labels


def fft(fs, data):
    time = np.linspace(0, float(len(data)) / fs, len(data))
    # data_windowed = scipy.hanning(data)
    compledata_array = np.fft.fft(data, len(data))
    freq = np.fft.fftfreq(time.shape[-1], 1.0 / fs)
    module = ((compledata_array.real ** 2 + compledata_array.imag ** 2) ** 0.5) / len(data)
    labels = {'xlabel': 'Frequency [Hz]', 'ylabel': 'Amplitude [-]'}
    return module[:(len(module) / 2)], freq[:(len(freq) / 2)], labels


def envelope(fs, data):
    time = np.linspace(0, float(len(data)) / fs, len(data))
    env = abs(scipy.signal.hilbert(data))
    labels = {'xlabel': 'Time [s]', 'ylabel': 'Amplitude [-]'}
    return env, time, labels
