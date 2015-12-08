import os
import pyaudio
import wave
import numpy as np
from spyker.utils.constants import RECS_DIR


class SoundStream:
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
        #file = wave.open(RECS_DIR + "/" + str(file_name), "rb")
        data = dataframes.pop(0)
        while len(dataframes) != 0:
            self.stream.write(data)
            data = dataframes.pop(0)
        self.close_stream()

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.handle.terminate()

    def save_to_file(self, file_name):
        if not os.path.exists(RECS_DIR):
            os.makedirs(RECS_DIR)
        wf = wave.open(RECS_DIR + "/" + str(file_name), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.handle.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))  # bytestring join
        wf.close()

def autotrimalgo(data_to_trim):
    datacopy = np.copy(data_to_trim)
    datacopy = datacopy / 32768.0
    indexlist = []
    indexback, indexfront, index = (0, 0, 0)
    for x in datacopy:
        if x < 0.01: #change to noise amplitude ?? how to find it out ?
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