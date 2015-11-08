import os
from PyQt4 import QtGui
import pyaudio
from spyker.model.recording import SoundStream


class RecordWindow(QtGui.QWidget):
    def __init__(self, model):
        super(RecordWindow, self).__init__()

        self.stream = SoundStream(1024, pyaudio.paInt16, 2, 44100)
        self.record_name = None
        self.model = model

        self.name_label = QtGui.QLabel('Name')
        self.name_edit = QtGui.QLineEdit()

        self.length_label = QtGui.QLabel('Length')
        self.length_edit = QtGui.QLineEdit()

        self.record_button = QtGui.QPushButton('Record')
        self.record_button.clicked.connect(lambda: self.record())
        self.play_button = QtGui.QPushButton('Play')
        self.play_button.clicked.connect(self.close)

        self.ok_button = QtGui.QPushButton('Ok')
        self.ok_button.clicked.connect(lambda: self.add_new_file())
        self.cancel_button = QtGui.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.name_edit, 0, 1)

        grid.addWidget(self.length_label, 1, 0)
        grid.addWidget(self.length_edit, 1, 1)

        grid.addWidget(self.record_button, 2, 0)
        grid.addWidget(self.play_button, 2, 1)

        grid.addWidget(self.ok_button, 3, 0)
        grid.addWidget(self.cancel_button, 3, 1)

        self.setLayout(grid)
        self.setGeometry(200, 200, 200, 200)
        self.setWindowTitle('Add new record')

    def add_new_file(self):
        if self.record_name is not None:
            self.stream.save_to_file(self.record_name)
            self.model.insertRows(self.record_name)
        self.close()

    def record(self):
        self.record_name = self.name_edit.text()
        self.ok_button.setEnabled(False)
        self.stream.open_stream()
        self.stream.record(int(self.length_edit.text()))
        self.stream.close_stream()
        self.ok_button.setEnabled(True)

