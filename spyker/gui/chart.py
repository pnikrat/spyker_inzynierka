from PyQt4 import QtGui
from spyker.plots import MFCC, Raw, STFT


class CanvasWindow(QtGui.QWidget):
    def __init__(self, recname, plotnumber):
        super(CanvasWindow, self).__init__()

        self.plotnumber = plotnumber #plotnumber will determine which object we create
        self.plotobj = [Raw, MFCC, None, STFT]
        self.plotnames = ['.wav signal', 'MFCC', None, 'STFT']
        ob = self.plotobj[self.plotnumber](self, filename=recname)
        grid = QtGui.QGridLayout()
        grid.addWidget(ob, 0, 0)
        self.setLayout(grid)
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle(self.plotnames[self.plotnumber] + ' for recording: ' + recname)
