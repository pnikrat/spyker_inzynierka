from PyQt4 import QtCore


class ChartListModel(QtCore.QAbstractListModel):
    def __init__(self, charts, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)

        self.charts = charts

    def rowCount(self, parent=None):
        return len(self.charts)

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            return self.charts[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return self.charts[index.row()]
