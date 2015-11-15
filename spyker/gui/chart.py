from PyQt4 import QtGui
from spyker.plots import MFCC, Raw


class CanvasWindow(QtGui.QWidget):
    def __init__(self, recname, plotnumber):
        super(CanvasWindow, self).__init__()

        self.plotnumber = plotnumber #plotnumber will determine which object we create
        #ob = MFCC(self, filename=recname)
        ob = Raw(self, filename=recname)
        grid = QtGui.QGridLayout()
        grid.addWidget(ob, 0, 0)
        self.setLayout(grid)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('MFCC')
