#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

import matplotlib
import numpy as np
import scipy
import scipy.io.wavfile
import scipy.signal
from matplotlib.mlab import specgram
from scikits.talkbox import lpc
from scikits.talkbox.features import mfcc
from scipy.signal import lfilter

NUMBER_OF_TICKS = 10


def get_freqs_ticks(fs, data_length, ans_length, max_freq=None):
    time = np.linspace(0, float(data_length) / fs, data_length)
    freq = np.fft.rfftfreq(time.shape[-1], 1.0 / fs)
    locs = np.arange(0, ans_length + 0.0001, float(ans_length) / NUMBER_OF_TICKS)
    if max_freq is None:
        max_freq = int(freq[-1])
    labels = np.arange(0, max_freq + 0.0001, float(max_freq) / NUMBER_OF_TICKS).astype(np.int, copy=False)
    ticks = {'locs': locs, 'labels': labels}
    return ticks


def get_time_ticks(fs, data_length, ans_length):
    locs = np.arange(0, ans_length + 0.0001, float(ans_length) / NUMBER_OF_TICKS)
    max_time = round(float(data_length) / fs, 1)
    labels = np.arange(0, max_time + 0.0001, float(max_time) / NUMBER_OF_TICKS)
    ticks = {'locs': locs, 'labels': labels}
    return ticks


def get_unchanged_ticks(ans_length):
    locs = np.arange(0, ans_length)
    labels = np.arange(0, ans_length)
    ticks = {'locs': locs, 'labels': labels}
    return ticks


def stft(fs, data, frame_size=0.05, hop=0.025):
    frame_samp = int(frame_size * fs)
    hop_samp = int(hop * fs)
    w = scipy.hamming(frame_samp)
    ans = scipy.array([np.fft.rfft(w * data[i:i + frame_samp])
                       for i in range(0, len(data) - frame_samp, hop_samp)])
    ans = scipy.log10(scipy.absolute(ans.T))
    labels = {'xlabel': 'Czas [s]', 'ylabel': u'Częstotliwość [Hz]', 'zlabel': 'Amplituda'}

    return {'y_vector': ans, 'x_vector': None, 'labels': labels, 'yticks': get_freqs_ticks(fs, len(data), len(ans)),
            'xticks': get_time_ticks(fs, len(data), len(ans.T))}


def formant_freqs(fs, data):
    max_freq = 5000

    ncoeff = 2 + fs / 1000

    a, e, k = lpc(data, ncoeff)
    w, h = scipy.signal.freqz(1, a, worN=512)
    freqs = fs * w / (2 * np.pi)
    ans = 20 * np.log10(abs(h))
    rts = np.roots(a)
    rts = [r for r in rts if np.imag(r) >= 0]
    angs = np.arctan2(np.imag(rts), np.real(rts))

    formants = sorted(angs * (fs / (2 * math.pi)))
    formants = filter(lambda formant: formant != 0 and formant < max_freq, formants)
    freqs = [freq for freq in freqs if freq < max_freq]
    ans = ans[:len(freqs)]
    labels = {'xlabel': u'Częstotliwość [Hz]', 'ylabel': 'Wzmocnienie [dB]'}
    return {'y_vector': ans, 'x_vector': freqs, 'labels': labels, 'cursors': formants}


def fft(fs, data):
    max_freq = 5000

    ncoeff = 2 + fs / 1000

    a, e, k = lpc(data, ncoeff)
    w, h = scipy.signal.freqz(1, a, worN=512)
    freqs = fs * w / (2 * np.pi)
    ans = 20 * np.log10(abs(h))

    freqs = [freq for freq in freqs if freq < max_freq]
    ans = ans[:len(freqs)]

    labels = {'xlabel': u'Częstotliwość [Hz]', 'ylabel': 'Wzmocnienie [dB]'}
    return {'y_vector': ans, 'x_vector': freqs, 'labels': labels}


def mfccoefs(fs, data, nwin=256, nfft=512, nceps=13):
    ceps, mspec, spec = mfcc(data, nwin, nfft, fs, nceps)
    labels = {'xlabel': u'Numer współczynnika [-]', 'ylabel': 'Czas [s]', 'zlabel': ''}
    return {'y_vector': ceps, 'x_vector': None, 'labels': labels,
            'yticks': get_time_ticks(fs, len(data), len(ceps)),
            'xticks': get_unchanged_ticks(len(ceps.T))}


def raw(fs, data):
    data = data.astype(float) / 32768.0
    time = np.linspace(0, float(len(data)) / fs, len(data))
    labels = {'xlabel': 'Czas [s]', 'ylabel': 'Amplituda [-]'}
    return {'y_vector': data, 'x_vector': time, 'labels': labels}


def stft3d(fs, data):
    (spectrum, freqs, t) = specgram(data, Fs=fs, NFFT=512, sides='onesided', mode='magnitude', noverlap=256)
    spectrum = spectrum / len(data)

    max_freq = 5000
    max_freq_index = next(i for i, v in enumerate(freqs) if v > max_freq)
    freqs = freqs[:max_freq_index]
    spectrum = spectrum[:max_freq_index, :]
    dimR, dimC = spectrum.shape
    time = np.linspace(0, float(len(data)) / fs, dimC)

    time, freqs = np.meshgrid(time, freqs, sparse=True)

    labels = {'xlabel': u'Częstotliwość [Hz]', 'ylabel': 'Czas [s]', 'zlabel': 'Amplituda [-]'}
    return {'y_vector': spectrum, 'x_vector': time, 'z_vector': freqs, 'labels': labels,
            'yticks': get_freqs_ticks(fs, len(data), len(spectrum), freqs[-1]),
            'xticks': get_time_ticks(fs, len(data), len(spectrum.T))}


def psd(fs, data):
    Pxx, freqs = matplotlib.mlab.psd(data, NFFT=512, Fs=44100, detrend=matplotlib.mlab.detrend_none,
                                     window=matplotlib.mlab.window_hanning, noverlap=256, pad_to=None,
                                     sides='default', scale_by_freq=None)
    labels = {'xlabel': u'Częstotliwość [Hz]', 'ylabel': ''}
    return {'y_vector': 20 * np.log10(Pxx), 'x_vector': freqs, 'labels': labels}
