from PyQt4 import QtGui


class FileListView(QtGui.QListView):
    def __init__(self, model):
        super(FileListView, self).__init__()

        self.setModel(model)

