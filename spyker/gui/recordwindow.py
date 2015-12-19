import tempfile

import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import scipy.io.wavfile
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

import spyker.model.charts as plots
from spyker.model.recording import *
from spyker.utils.constants import RECS_DIR
import spyker.utils.utils as utils
from spyker.model.recording import SoundStream, autotrimalgo
from spyker.utils.constants import RECS_DIR
from spyker.utils.constants import f_sampling
from spyker.utils.pltutils import plot_function
import scipy.io.wavfile
import numpy as np


class RecordWindow(QtGui.QDialog):
    def __init__(self, model):
        super(RecordWindow, self).__init__()

        self.record_name = None
        self.record_duration = None
        self.currently_playing = False
        self.stream = None
        self.model = model
        self.trim = 'n'

        self.initUI()

    def initUI(self):
        self.before = TrimCanvas()
        self.after = TrimCanvas()

        self.record_name_label = QtGui.QLabel('Name')
        self.record_name_edit = QtGui.QLineEdit()

        self.record_duration_label = QtGui.QLabel('Recording length')
        #self.record_duration_edit = QtGui.QLineEdit()
        self.record_duration_spin = QtGui.QSpinBox()
        self.record_duration_spin.setValue(2)
        self.record_duration_spin.setRange(2, 4)
        self.record_duration_spin.valueChanged.connect(lambda: self.rec_spin())

        self.interval_label = QtGui.QLabel('Trim interval length')
        self.interval_spin = QtGui.QSpinBox()
        self.interval_spin.setValue(1)
        self.interval_spin.setRange(1, 1)
        self.interval_spin.valueChanged.connect(lambda : self.int_spin())

        self.record_button = QtGui.QPushButton('Record')
        self.record_button.clicked.connect(lambda: self.record())

        self.play_button_before = QtGui.QPushButton('Play signal before trimming')
        self.play_button_before.clicked.connect(lambda: self.play('b'))

        self.play_button_after = QtGui.QPushButton('Play signal after trimming')
        self.play_button_after.clicked.connect(lambda: self.play('a'))

        self.trim_button = QtGui.QPushButton('Trim')
        self.trim_button.clicked.connect(lambda: self.trim_recording())

        self.cancel_button = QtGui.QPushButton('Cancel all data')
        self.cancel_button.clicked.connect(lambda : self.cancel_recording())

        self.apply_button = QtGui.QPushButton('Apply and save recording')
        self.apply_button.clicked.connect(lambda : self.save_new_record())

        self.trim_options_group = QtGui.QButtonGroup(self)
        self.trim_none = QtGui.QRadioButton("None")
        self.trim_none.setChecked(True) #default option is no trim at all
        self.trim_auto = QtGui.QRadioButton("Auto")
        self.trim_manual = QtGui.QRadioButton("Manual")
        self.trim_options_group.addButton(self.trim_none)
        self.trim_options_group.addButton(self.trim_auto)
        self.trim_options_group.addButton(self.trim_manual)
        self.trim_none.clicked.connect(lambda: self.trim_mode_change('n'))
        self.trim_auto.clicked.connect(lambda: self.trim_mode_change('a'))
        self.trim_manual.clicked.connect(lambda: self.trim_mode_change('m'))

        self.trim_radio_buttons = [self.trim_none, self.trim_auto, self.trim_manual]

        self.ui_message = QtGui.QLabel()

        self.details_layout = QtGui.QGridLayout()
        self.details_layout.addWidget(self.record_name_label, 0, 0)
        self.details_layout.addWidget(self.record_name_edit, 0, 1)
        self.details_layout.addWidget(self.record_duration_label, 1, 0)
        self.details_layout.addWidget(self.record_duration_spin, 1, 1)
        self.details_layout.addWidget(self.interval_label, 2, 0)
        self.details_layout.addWidget(self.interval_spin, 2, 1)

        self.trim_layout = QtGui.QVBoxLayout()
        self.trim_layout.addWidget(self.trim_none)
        self.trim_layout.addWidget(self.trim_auto)
        self.trim_layout.addWidget(self.trim_manual)

        self.actions_layout = QtGui.QVBoxLayout()
        self.actions_layout.addWidget(self.record_button)
        self.actions_layout.addWidget(self.trim_button)
        self.actions_layout.addWidget(self.cancel_button)

        self.ui_layout = QtGui.QHBoxLayout()
        self.ui_layout.addLayout(self.details_layout, 2) #second argument is a stretch factor
        self.ui_layout.addLayout(self.trim_layout, 1)
        self.ui_layout.addLayout(self.actions_layout, 2)

        self.before_trim_under_layout = QtGui.QHBoxLayout()
        self.before_trim_under_layout.addWidget(self.before.toolbar)
        self.before_trim_under_layout.addWidget(self.play_button_before)

        self.before_trim_layout = QtGui.QVBoxLayout()
        self.before_trim_layout.addWidget(self.before.canvas)
        self.before_trim_layout.addLayout(self.before_trim_under_layout)

        self.befembedding = QtGui.QWidget()
        self.befembedding.setLayout(self.before_trim_layout)

        self.after_trim_under_layout = QtGui.QHBoxLayout()
        self.after_trim_under_layout.addWidget(self.after.toolbar)
        self.after_trim_under_layout.addWidget(self.play_button_after)

        self.after_trim_layout = QtGui.QVBoxLayout()
        self.after_trim_layout.addWidget(self.after.canvas)
        self.after_trim_layout.addLayout(self.after_trim_under_layout)

        self.embedding = QtGui.QWidget()
        self.embedding.setLayout(self.after_trim_layout)

        self.widget_layout = QtGui.QVBoxLayout()
        self.widget_layout.addLayout(self.ui_layout, 0)
        self.widget_layout.addWidget(self.ui_message, 0)
        self.widget_layout.addWidget(self.befembedding, 5)
        self.widget_layout.addWidget(self.embedding, 5)
        self.widget_layout.addWidget(self.apply_button, 0)

        self.setLayout(self.widget_layout)
        self.setWindowTitle('Add new record')
        self.showMaximized()
        self.hide_canvas()

    def hide_canvas(self):
        if self.trim == 'n':
            self.embedding.hide()
        else:
            self.embedding.show()

    def trim_mode_change(self, mode):
        self.trim = mode
        self.hide_canvas()

    def message_user(self, message):
        self.ui_message.setText("<font color=\"red\">* " + message + "</font>")

    def disabling_elements(self, elements, state):
        for x in elements:
            x.setDisabled(state)

    def rec_spin(self):
        self.interval_spin.setRange(1, self.record_duration_spin.value() - 1)

    def int_spin(self):
        pass

    def record(self):
        if self.is_data_valid():
            if self.record_name_edit.text() not in self.model.file_paths:
                self.disabling_elements(self.trim_radio_buttons, True)

                self.message_user("Recording!") #NOT WORKING!
                self.record_duration = int(self.record_duration_spin.value())
                self.record_name = self.record_name_edit.text()

                self.stream = SoundStream(1024, pyaudio.paInt16, 1, f_sampling)
                self.stream.open_stream("in")
                self.stream.record(self.record_duration)
                frames = self.stream.get_frames()
                self.before.frames = frames
                self.stream.close_stream()

                self.before.data = np.fromstring(b''.join(self.before.frames), dtype=np.int16)
                self.message_user('Recording finished!')
                self.before.interval = self.interval_spin.value()
                self.before.replot(self.trim)
                if self.trim == 'a':
                    self.autotrim()
            else:
                self.message_user('Recording ' + self.record_name_edit.text() + ' already exists!')

    def autotrim(self):
        self.after.data = autotrimalgo(np.copy(self.before.data))
        self.after.replot(self.trim)
        self.after.data2frames()

    def cancel_recording(self):
        self.before.clear_data()
        self.after.clear_data()
        self.disabling_elements(self.trim_radio_buttons, False)

    def play(self, which_one):
        self.play_button_before.setEnabled(False)
        self.play_button_after.setEnabled(False)
        QtGui.QApplication.processEvents()

        if which_one == 'b':
            mode = self.before
        else:
            mode = self.after
        if mode.frames is not None:
            stream = SoundStream(1024, pyaudio.paInt16, 1, f_sampling)
            stream.open_stream("out")
            stream.play_recording(list(mode.frames)) #pass a COPY of list
        else:
            self.message_user("Record your voice first!")

        self.play_button_after.setEnabled(True)
        self.play_button_before.setEnabled(True)
        QtGui.QApplication.processEvents()

    def trim_recording(self):
        if self.before.handles is None:
            self.message_user('Not in manual mode or nothing to trim yet')
        else:
            handles = self.before.handles
            xpos = []
            pos1, pos2 = handles.get_last_x_pos()
            xpos.append(pos1[0])
            xpos.append(pos2[0])
            xpos.sort()
            self.after.data = manualtrimalgo(np.copy(self.before.data), np.copy(self.before.timedata), tuple(xpos))
            self.after.data2frames()
            self.after.replot('n')
            self.message_user('Trim successful')

    def save_new_record(self):
        if self.trim == 'n':
            if self.before.data is not None:
                scipy.io.wavfile.write(RECS_DIR + "/" + self.record_name, f_sampling, self.before.data)
            else:
                self.message_user("Record yourself first")
                return
        else:
            if self.after.data is not None:
                scipy.io.wavfile.write(RECS_DIR + "/" + self.record_name, f_sampling, self.after.data)
            else:
                self.message_user("Record yourself or trim the recording")
                return
        self.model.insertRows(self.record_name)
        self.accept()

    def is_data_valid(self):
        if utils.is_valid_path(str(self.record_name_edit.text())):
            if utils.is_number(self.record_duration_spin.value()):
                return True
            else:
                self.message_user("Length must be a valid integer")
                return False
        else:
            self.message_user("Name must be a valid filename")
            return False
