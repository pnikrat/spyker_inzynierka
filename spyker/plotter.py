import matplotlib as plt
import numpy as np
from matplotlib.figure import Figure


class Plotter:
    def __init__(self):
        self.datay = None
        self.datax = None
        self.figure = None

    def plot(self):
        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        a.plot(self.datax, self.datay)
        self.figure = f

    def slice_time(self, record_time):
        assert(self.datay is not None, "No data y in plotter")
        self.datax = np.linspace(0, record_time, len(self.datay))

