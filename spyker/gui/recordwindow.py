from spyker.model.recording import *
from spyker.utils.constants import RECS_DIR
import spyker.utils.utils as utils
from spyker.utils.constants import f_sampling
import scipy.io.wavfile
import numpy as np


class RecordWindow(QtGui.QDialog):
    def __init__(self, model):
        super(RecordWindow, self).__init__()

        self.record_name = None
        self.record_duration = None
        self.stream = None
        self.model = model
        self.trim = 'n'

        self.initUI()

    def initUI(self):
        self.before = TrimCanvas()
        self.after = TrimCanvas()

        self.record_name_label = QtGui.QLabel('Name')
        self.record_name_edit = QtGui.QLineEdit()

        self.record_duration_label = QtGui.QLabel('Length')
        self.record_duration_edit = QtGui.QLineEdit()

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
        self.details_layout.addWidget(self.record_duration_edit, 1, 1)

        self.trim_layout = QtGui.QVBoxLayout()
        self.trim_layout.addWidget(self.trim_none)
        self.trim_layout.addWidget(self.trim_auto)
        self.trim_layout.addWidget(self.trim_manual)

        self.actions_layout = QtGui.QVBoxLayout()
        self.actions_layout.addWidget(self.record_button)
        self.actions_layout.addWidget(self.trim_button)
        self.actions_layout.addWidget(self.cancel_button)

        self.ui_layout = QtGui.QHBoxLayout()
        self.ui_layout.addLayout(self.details_layout)
        self.ui_layout.addLayout(self.trim_layout)
        self.ui_layout.addLayout(self.actions_layout)

        self.before_trim_under_layout = QtGui.QHBoxLayout()
        self.before_trim_under_layout.addWidget(self.before.toolbar)
        self.before_trim_under_layout.addWidget(self.play_button_before)

        self.before_trim_layout = QtGui.QVBoxLayout()
        self.before_trim_layout.addWidget(self.before.canvas)
        self.before_trim_layout.addLayout(self.before_trim_under_layout)

        self.after_trim_under_layout = QtGui.QHBoxLayout()
        self.after_trim_under_layout.addWidget(self.after.toolbar)
        self.after_trim_under_layout.addWidget(self.play_button_after)

        self.after_trim_layout = QtGui.QVBoxLayout()
        self.after_trim_layout.addWidget(self.after.canvas)
        self.after_trim_layout.addLayout(self.after_trim_under_layout)

        self.widget_layout = QtGui.QVBoxLayout()
        self.widget_layout.addLayout(self.ui_layout)
        self.widget_layout.addWidget(self.ui_message)
        self.widget_layout.addLayout(self.before_trim_layout)
        self.widget_layout.addLayout(self.after_trim_layout)
        self.widget_layout.addWidget(self.apply_button)

        self.setLayout(self.widget_layout)
        self.setGeometry(200, 200, 700, 500)
        self.setWindowTitle('Add new record')

        self.hide_canvas()

    def hide_canvas(self):
        if self.trim == 'n':
            self.after.hidecanvas(True)
            self.play_button_after.hide()
        else:
            self.after.hidecanvas(False)
            self.play_button_after.show()

    def trim_mode_change(self, mode):
        self.trim = mode
        self.hide_canvas()

    def message_user(self, message):
        self.ui_message.setText("<font color=\"red\">* " + message + "</font>")

    def disabling_elements(self, elements, state):
        for x in elements:
            x.setDisabled(state)

    def record(self):
        if self.is_data_valid():
            self.disabling_elements(self.trim_radio_buttons, True)

            self.message_user("Recording!") #NOT WORKING!
            self.record_duration = int(self.record_duration_edit.text())
            self.record_name = self.record_name_edit.text()

            self.stream = SoundStream(1024, pyaudio.paInt16, 1, f_sampling)
            self.stream.open_stream("in")
            self.stream.record(self.record_duration)
            frames = self.stream.get_frames()
            self.before.frames = frames
            self.stream.close_stream()

            self.before.data = np.fromstring(b''.join(self.before.frames), dtype=np.int16)
            self.message_user('Recording finished!')
            self.before.replot(self.trim, self.record_duration)
            if self.trim == 'a':
                self.autotrim()

    def autotrim(self):
        self.after.data = autotrimalgo(np.copy(self.before.data))
        self.after.replot(self.trim, self.record_duration)
        self.after.data2frames()

    def cancel_recording(self):
        self.before.clear_data()
        self.after.clear_data()
        self.disabling_elements(self.trim_radio_buttons, False)

    def play(self, which_one):
        if which_one == 'b':
            mode = self.before
        else:
            mode = self.after
        if mode.frames is not None:
            self.stream = SoundStream(1024, pyaudio.paInt16, 1, f_sampling)
            self.stream.open_stream("out")
            print len(mode.frames)
            self.stream.play_recording(list(mode.frames)) #pass a COPY of list
        else:
            self.message_user("Record your voice first!")

    def save_new_record(self):
        if self.record_name is not None:
            if self.trim == 'n':
                #self.stream.save_to_file(self.record_name)
                scipy.io.wavfile.write(RECS_DIR + "/" + self.record_name, f_sampling, self.before.data)
            else:
                scipy.io.wavfile.write(RECS_DIR + "/" + self.record_name, f_sampling, self.after.data)
            self.model.insertRows(self.record_name)
            self.accept()
        else:
            self.message_user("No recording to save")

    def is_data_valid(self):
        if utils.is_valid_path(str(self.record_name_edit.text())):
            if utils.is_number(self.record_duration_edit.text()):
                return True
            else:
                self.message_user("Length must be a valid integer")
                return False
        else:
            self.message_user("Name must be a valid filename")
            return False
