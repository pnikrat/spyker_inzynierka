from PyQt4 import QtGui
import pyaudio
import winsound

from spyker.model.recording import SoundStream
from spyker.utils.constants import RECS_DIR
import spyker.utils.utils as utils


class RecordWindow(QtGui.QWidget):
    def __init__(self, model):
        super(RecordWindow, self).__init__()

        self.record_name = None
        self.record_duration = None
        self.stream = None
        self.model = model

        self.name_label = QtGui.QLabel('Name')
        self.name_edit = QtGui.QLineEdit()

        self.length_label = QtGui.QLabel('Length')
        self.length_edit = QtGui.QLineEdit()

        self.record_button = QtGui.QPushButton('Record')
        self.record_button.clicked.connect(lambda: self.record())
        self.play_button = QtGui.QPushButton('Play')
        self.play_button.clicked.connect(lambda: self.play())

        self.ok_button = QtGui.QPushButton('Ok')
        self.ok_button.clicked.connect(lambda: self.save_new_record())
        self.cancel_button = QtGui.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.error_label = QtGui.QLabel()

        grid = QtGui.QGridLayout()
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.name_edit, 0, 1)

        grid.addWidget(self.length_label, 1, 0)
        grid.addWidget(self.length_edit, 1, 1)

        grid.addWidget(self.record_button, 2, 0)
        grid.addWidget(self.play_button, 2, 1)

        grid.addWidget(self.error_label, 3, 0, 1, 2)

        grid.addWidget(self.ok_button, 4, 0)
        grid.addWidget(self.cancel_button, 4, 1)

        self.setLayout(grid)
        self.setGeometry(200, 200, 200, 200)
        self.setWindowTitle('Add new record')

    def save_new_record(self):
        if self.record_name is not None:
            self.stream.save_to_file(self.record_name)
            self.model.insertRows(self.record_name)
        self.close()

    def record(self):
        if self.is_data_valid():
            self.record_duration = int(self.length_edit.text())
            self.record_name = self.name_edit.text()
            self.stream = SoundStream(1024, pyaudio.paInt16, 1, 44100)
            self.stream.open_stream()
            self.set_buttons_enabled(False)
            self.stream.record(self.record_duration)
            self.stream.close_stream()
            self.set_buttons_enabled(True)

    def play(self):
        if self.record_name is not None:
            winsound.PlaySound(RECS_DIR + '/' + str(self.record_name), winsound.SND_FILENAME)
        else:
            self.error_label.setText("<font color=\"red\">* Record the file first</font>")

    def set_buttons_enabled(self, enabled):
        self.ok_button.setEnabled(enabled)
        self.record_button.setEnabled(enabled)
        self.play_button.setEnabled(enabled)

    def is_data_valid(self):
        if utils.is_valid_path(str(self.name_edit.text())):
            if utils.is_number(self.length_edit.text()):
                self.error_label.setText("")
                return True
            else:
                self.error_label.setText("<font color=\"red\">* Length must be a valid integer</font>")
        else:
            self.error_label.setText("<font color=\"red\">* Name must be a valid file name</font>")
            return False
