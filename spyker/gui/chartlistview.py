from PyQt4 import QtGui


class ChartListView(QtGui.QListView):
    def __init__(self, model):
        super(ChartListView, self).__init__()
        self.setModel(model)
