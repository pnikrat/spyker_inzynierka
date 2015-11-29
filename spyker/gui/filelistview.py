import os
from os import listdir
from os.path import isfile, join

from PyQt4 import QtGui

from spyker.utils.constants import RECS_DIR


class FileListView(QtGui.QListView):
    def __init__(self, model):
        super(FileListView, self).__init__()

        self.setModel(model)

        if os.path.exists(RECS_DIR):
            for f in listdir(RECS_DIR):
                if isfile(join(RECS_DIR, f)):
                    self.model().insertRows(f)
