import matplotlib as plt
import numpy as np


class Plotter:
    def __init__(self):
        self.datay = None
        self.datax = None

    def plot(self):
        figure = plt.plot(self.datax, self.datay)


    def slice_time(self, record_time):
        assert(self.datay is not None, "No data y in plotter")
        self.datax = np.linspace(0, record_time, len(self.datay))

