from PyQt4 import QtGui

from spyker.plots import MFCC, Raw, FFT, STFT, STFT3D, Envelope
from spyker.utils.constants import ChartType


class CanvasWindow(QtGui.QWidget):
    def __init__(self, recname, plotnumber):
        super(CanvasWindow, self).__init__()

        self.plotnumber = plotnumber #plotnumber will determine which object we create
        self.plotobj = [Raw, MFCC, FFT, STFT, STFT3D, Envelope]

        self.plotnames = [ChartType.RAW, ChartType.MFCC, ChartType.FFT, ChartType.STFT, ChartType.STFT3D, ChartType.ENVELOPE]
        ob = self.plotobj[self.plotnumber](self, filename=recname)
        grid = QtGui.QGridLayout()
        grid.addWidget(ob, 0, 0)
        self.setLayout(grid)
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle(self.plotnames[self.plotnumber] + ' for recording: ' + recname)
