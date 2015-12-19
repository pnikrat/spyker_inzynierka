import pyaudio
import numpy as np
import wave
import matplotlib.pyplot as plt
import spyker.model.charts as plots
from spyker.utils.pltutils import plot_function
from spyker.utils.constants import f_sampling, RECS_DIR
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT


class SoundStream(object):
    def __init__(self, chunk, format, channels, rate):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.handle = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.num_of_seconds = None

    def get_frames(self):
        return self.frames

    def get_num_of_seconds(self):
        return self.num_of_seconds

    def open_stream(self, mode):
        if mode == "in":
            self.stream = self.handle.open(format=self.format,
                                            channels=self.channels,
                                            rate=self.rate,
                                            input=True,
                                            frames_per_buffer=self.chunk)
        elif mode == "out":
            self.stream = self.handle.open(format=self.format,
                                            channels=self.channels,
                                            rate=self.rate,
                                            output=True)

    def record(self, num_of_seconds):
        self.num_of_seconds = num_of_seconds
        self.frames = []
        for i in range(0, int(self.rate / self.chunk * num_of_seconds)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def play_recording(self, dataframes):
        data = dataframes.pop(0)
        while len(dataframes) != 0:
            self.stream.write(data)
            data = dataframes.pop(0)
        self.close_stream()

    def play_wav_recording(self, filename):
        file = wave.open(RECS_DIR + "/" + str(filename), "rb")
        data = file.readframes(self.chunk)
        while data != "":
            self.stream.write(data)
            data = file.readframes(self.chunk)
        self.close_stream()

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.handle.terminate()


class TrimCanvas(QtGui.QWidget):
    def __init__(self):
        super(TrimCanvas, self).__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.frames = None
        self.data = None
        self.handles = None
        self.timedata = None
        self.interval = None

    def replot(self, mode):
        data = plots.raw(f_sampling, self.data)
        self.timedata = data['x_vector']
        if mode == 'm':
            data['sliders'] = (self.timedata[-1]*0.1, self.timedata[-1]*0.1 + self.interval, self.interval)
        self.handles = plot_function(self.figure, data)
        self.canvas.draw()

    def clear_data(self):
        self.figure.clear()
        self.canvas.draw()
        self.frames = None
        self.data = None

    def data2frames(self):
        bytes = self.data.tobytes()
        self.frames = [bytes[i:i+2048] for i in range(0, len(bytes), 2048)]


def autotrimalgo(data_to_trim):
    datacopy = np.copy(data_to_trim)
    datacopy = datacopy / 32768.0
    indexlist = []
    indexback, indexfront, index = (0, 0, 0)
    for x in datacopy:
        if x < 0.05: #change to noise amplitude ?? how to find it out ?
            indexlist.append(index)
        index += 1
    for i in range(0, len(indexlist)):
        diff = indexlist[i+1] - indexlist[i]
        if diff != 1:
            indexfront = i
            break
    for i in range(len(indexlist)-1, 0, -1):
        diff = indexlist[i] - indexlist[i-1]
        if diff != 1:
            indexback = i
            break
    cutfront = indexlist[:indexfront]
    cutback = indexlist[indexback:]
    cut = cutfront + cutback
    new_data = np.delete(data_to_trim, cut)
    return new_data

def findindex(numpyarray, coord):
    'finds index using bisection'
    return np.nonzero(abs(numpyarray-coord) <= 0.00002) #distance between samples if 44100hz sampling recording is used


def manualtrimalgo(data_to_trim, timedata, timecoords):
    'assumes timecoords are already sorted'
    begin, end = timecoords

    beginindex = findindex(timedata, begin) #return tuple of arrays
    endindex = findindex(timedata, end)

    beginindex = beginindex[0][0] #array in a tuple can have more than one sample matching condition in findindex func
    endindex = endindex[0][0]
    return data_to_trim[beginindex:endindex]