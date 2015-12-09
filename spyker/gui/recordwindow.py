from PyQt4 import QtGui
import pyaudio
import tempfile

from spyker.model.recording import SoundStream, autotrimalgo
from spyker.utils.constants import RECS_DIR
from spyker.gui.chartwindow import ChartWindow
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
import spyker.model.charts as plots
import spyker.utils.utils as utils
from spyker.utils.pltutils import plot_function
from spyker.utils.constants import f_sampling
import matplotlib.pyplot as plt
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
        self.file_handle = tempfile.NamedTemporaryFile()
        self.frames = None
        self.data = None

        self.initUI()

    def initUI(self):
        self.figB = plt.figure()
        self.figA = plt.figure()
        self.canvasB = FigureCanvas(self.figB)
        self.toolbarB = NavigationToolbar2QT(self.canvasB, self)
        self.before_label = QtGui.QLabel('Signal before trim')
        self.canvasA = FigureCanvas(self.figA)
        self.toolbarA = NavigationToolbar2QT(self.canvasA, self)
        self.after_label = QtGui.QLabel('Signal after trim')

        self.record_name_label = QtGui.QLabel('Name')
        self.record_name_edit = QtGui.QLineEdit()

        self.record_duration_label = QtGui.QLabel('Length')
        self.record_duration_edit = QtGui.QLineEdit()

        self.record_button = QtGui.QPushButton('Record')
        self.record_button.clicked.connect(lambda: self.record())

        self.play_button_before = QtGui.QPushButton('Play signal before trimming')
        self.play_button_before.clicked.connect(lambda: self.play())

        self.play_button_after = QtGui.QPushButton('Play signal after trimming')
        self.play_button_after.clicked.connect(lambda: self.play())

        self.trim_button = QtGui.QPushButton('Trim')
        self.trim_button.clicked.connect(lambda: self.trim_recording())

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

        self.ui_layout = QtGui.QHBoxLayout()
        self.ui_layout.addLayout(self.details_layout)
        self.ui_layout.addLayout(self.trim_layout)
        self.ui_layout.addLayout(self.actions_layout)

        self.before_trim_under_layout = QtGui.QHBoxLayout()
        self.before_trim_under_layout.addWidget(self.toolbarB)
        self.before_trim_under_layout.addWidget(self.play_button_before)

        self.before_trim_layout = QtGui.QVBoxLayout()
        self.before_trim_layout.addWidget(self.canvasB)
        self.before_trim_layout.addLayout(self.before_trim_under_layout)

        self.after_trim_under_layout = QtGui.QHBoxLayout()
        self.after_trim_under_layout.addWidget(self.toolbarA)
        self.after_trim_under_layout.addWidget(self.play_button_after)

        self.after_trim_layout = QtGui.QVBoxLayout()
        self.after_trim_layout.addWidget(self.canvasA)
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
            self.canvasA.hide()
            self.play_button_after.hide()
            self.toolbarA.hide()
        else:
            self.canvasA.show()
            self.play_button_after.show()
            self.toolbarA.show()

    def trim_mode_change(self, mode):
        self.trim = mode
        self.hide_canvas()

    def message_user(self, message):
        self.ui_message.setText("<font color=\"red\">* " + message + "</font>")

    def record(self):
        if self.is_data_valid():
            #self.clean_temp_data()
            self.message_user("Recording!") #NOT WORKING!
            self.record_duration = int(self.record_duration_edit.text())
            self.record_name = self.record_name_edit.text()

            self.stream = SoundStream(1024, pyaudio.paInt16, 1, f_sampling)
            self.stream.open_stream("in")
            self.stream.record(self.record_duration)
            self.frames = self.stream.get_frames()

            #self.file_handle.write()
            #self.file_handle.seek(0) #return to front of file
            self.stream.close_stream()

            self.data = np.fromstring(b''.join(self.frames), dtype=np.int16)
            self.message_user('Recording finished!')
            self.replot_before()
            if self.trim == 'a':
                self.data = autotrimalgo(np.copy(self.data))
                self.replot_after()

    def replot_before(self):
        data = plots.raw(f_sampling, self.data)
        plot_function(self.figB, data)
        self.canvasB.draw()

    def replot_after(self):
        data = plots.raw(f_sampling, self.data)
        plot_function(self.figA, data)
        self.canvasA.draw()

    def clean_temp_data(self):
        self.file_handle.write(b''.join([]))
        self.file_handle.seek(0)

    def play(self):
        if self.data is not None:
            self.stream = SoundStream(1024, pyaudio.paInt16, 1, f_sampling)
            self.stream.open_stream("out")
            self.stream.play_recording(list(self.frames)) #pass a COPY of list
        else:
            self.message_user("Record your voice first!")

    def save_new_record(self):
        if self.record_name is not None:
            #self.stream.save_to_file(self.record_name)
            scipy.io.wavfile.write(RECS_DIR + "/" + self.record_name, f_sampling, self.data)
            self.model.insertRows(self.record_name)
            self.accept()

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
