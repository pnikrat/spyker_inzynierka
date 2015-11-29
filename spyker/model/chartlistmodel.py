from PyQt4 import QtCore


class ChartListModel(QtCore.QAbstractListModel):
    def __init__(self, chart_dict, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)

        self.chart_dict = chart_dict

    def rowCount(self, parent=None):
        return len(self.chart_dict)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.chart_dict.keys()[index.row()]
        elif role == QtCore.Qt.UserRole:
            return self.chart_dict.items()[index.row()]
