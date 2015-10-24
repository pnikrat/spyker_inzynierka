import matplotlib as plt
plt.use('TkAgg')
import numpy as np
from matplotlib.figure import Figure


class Plotter:
    def __init__(self):
        self.datay = None
        self.datax = None
        self.figure = None

    def plot(self):
        fig = Figure(figsize=(5,4), dpi=100) #figsize - (width,height) in inches
        ax = fig.add_subplot(111) #nrows, ncols, plot_number
        ax.plot(self.datax, self.datay)
        self.figure = fig

    def set_datay(self, datay):
        self.datay = datay

    def slice_time(self, record_time):
        assert self.datay is not None, "No data y in plotter"
        self.datax = np.linspace(0, record_time, len(self.datay))

