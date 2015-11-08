import os
import pyaudio
import wave


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

    def open_stream(self):
        self.stream = self.handle.open(format=self.format,
                                       channels=self.channels,
                                       rate=self.rate,
                                       input=True,
                                       frames_per_buffer=self.chunk)

    def record(self, num_of_seconds):
        self.num_of_seconds = num_of_seconds
        self.frames = []
        for i in range(0, int(self.rate / self.chunk * num_of_seconds)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.handle.terminate()

    def save_to_file(self, file_name):
        if not os.path.exists("records"):
            os.makedirs("records")
        wf = wave.open("records/" + str(file_name), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.handle.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))  # bytestring join
        wf.close()
