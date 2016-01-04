import math

import numpy as np
import numpy
import scipy
import scipy.io.wavfile
import scipy.signal
from matplotlib.mlab import specgram
from scikits.talkbox import lpc
from scikits.talkbox.features import mfcc
from scipy.signal import lfilter, hamming


def stft(fs, data, frame_size=0.05, hop=0.025):
    frame_samp = int(frame_size * fs)
    hop_samp = int(hop * fs)
    w = scipy.hanning(frame_samp)

    for i in range(0, len(data) - frame_samp, hop_samp):
        print i

    data = scipy.array([np.fft.rfft(w * data[i:i + frame_samp])
                        for i in range(0, len(data) - frame_samp, hop_samp)])
    labels = {'xlabel': 'Time frames [-]', 'ylabel': 'Frequency [Hz]', 'zlabel': 'Amplitude'}
    return {'y_vector': scipy.log10(scipy.absolute(data.T)), 'x_vector': None, 'labels': labels}


def fft2(fs, data, frame_size=0.05, hop=0.025):
    frame_samp = int(frame_size * fs)
    hop_samp = int(hop * fs)
    w = scipy.hanning(frame_samp)

    data = scipy.array([np.fft.rfft(w * data[i:i + frame_samp])
                        for i in range(0, len(data) - frame_samp, hop_samp)])
    data = scipy.absolute(data.T)
    ans = [sum(i) / len(i) for i in data]
    labels = {'xlabel': 'Frequency [Hz]', 'ylabel': 'Amplitude [-]'}
    return {'y_vector': ans, 'x_vector': range(0, len(ans)), 'labels': labels}


def mfccoefs(fs, data, nwin=256, nfft=512, nceps=13):
    print fs, data, nwin, nfft, nceps
    ceps, mspec, spec = mfcc(data, nwin, nfft, fs, nceps)
    labels = {'xlabel': 'Coefficient number', 'ylabel': 'Frame number', 'zlabel': ''}
    return {'y_vector': ceps, 'x_vector': None, 'labels': labels}


def raw(fs, data):
    data = data.astype(float) / 32768.0
    # We then split the file into chunks, where the number of chunks depends on how finely you want to measure the volume:

    # Finally, we compute the volume of each chunk:

    # chunks = np.array_split(data, numchunks)
    time = np.linspace(0, float(len(data)) / fs, len(data))
    # time = range(0, int(numchunks), 1)
    # dbs = [20 * log10(sqrt(mean(chunk ** 2))) for chunk in chunks]

    labels = {'xlabel': 'Time [s]', 'ylabel': 'Amplitude [-]'}
    return {'y_vector': data, 'x_vector': time, 'labels': labels}


def fft(fs, data):
    time = np.linspace(0, float(len(data)) / fs, len(data))
    window = scipy.signal.hamming(len(data), False)
    data = data * window
    compledata_array = np.fft.rfft(data)
    module = ((compledata_array.real ** 2 + compledata_array.imag ** 2) ** 0.5) / len(data)
    freq = np.fft.rfftfreq(time.shape[-1], 1.0 / fs)
    # module = module[:(len(module) / 2)]
    # freq = freq[:(len(freq) / 2)]
    labels = {'xlabel': 'Frequency [Hz]', 'ylabel': 'Amplitude [-]'}
    return {'y_vector': module[:6000], 'x_vector': freq[:6000], 'labels': labels}


def envelope(fs, data):
    fftdict = fft(fs, data)

    env = abs(scipy.signal.hilbert(fftdict['y_vector']))
    labels = {'xlabel': 'Time [s]', 'ylabel': 'Amplitude [-]'}
    return {'y_vector': env[:1000], 'x_vector': fftdict['x_vector'][:1000], 'labels': labels}


def formant_freqs_on_fft(fs, data):
    return dict(fft(fs, data).items() + {'cursors': formant_freqs(fs, data)}.items())


    # na usrednionym widmie gestosci mocy


def formant_freqs(fs, data):
    N = len(data)
    w = numpy.hamming(N)

    # Apply window and high pass filter.
    x1 = data * w
    x1 = lfilter([1], [1., 0.63], x1)

    ncoeff = 2 + fs / 1000
    A, e, k = lpc(x1, ncoeff)

    # Get roots.
    rts = numpy.roots(A)
    rts = [r for r in rts if numpy.imag(r) >= 0]

    # Get angles.
    angs = numpy.arctan2(numpy.imag(rts), numpy.real(rts))

    # Get frequencies.
    frqs = sorted(angs * (fs / (2 * math.pi)))
    return frqs[:5]


def stft3d(fs, data):
    (spectrum, freqs, t) = specgram(data, Fs=fs, NFFT=512, sides='onesided', mode='magnitude')
    spectrum = spectrum / len(data)
    freqs = freqs[:58]
    spectrum = spectrum[:58, :]
    dimR, dimC = spectrum.shape
    time = np.linspace(0, float(len(data)) / fs, dimC)

    time, freqs = np.meshgrid(time, freqs, sparse=True)

    labels = {'xlabel': 'Frequency [Hz]', 'ylabel': 'Time [s]', 'zlabel': 'Amplitude [-]'}
    return {'y_vector': spectrum, 'x_vector': time, 'z_vector': freqs, 'labels': labels}
