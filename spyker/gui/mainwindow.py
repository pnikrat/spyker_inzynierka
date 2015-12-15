import os

import pyaudio
from PyQt4 import QtGui, QtCore

from spyker.gui.chartlistview import ChartListView
from spyker.gui.chartwindow import ChartWindow
from spyker.gui.dialogwindow import DialogWindow
from spyker.gui.filebutton import FileButton
from spyker.gui.filelistview import FileListView
from spyker.gui.recordwindow import RecordWindow
from spyker.model.recording import SoundStream
from spyker.utils.constants import RECS_DIR


class FileGrid(QtGui.QGridLayout):
    def __init__(self, model):
        super(FileGrid, self).__init__()

        self.model = model

        self.list_view = FileListView(self.model)

        add_button = FileButton("+", "#35ae56")
        add_button.clicked.connect(self.start_add_new_window)

        remove_button = FileButton("-", "#d05d4f")
        remove_button.clicked.connect(self.confirm_deletion)

        play_button = FileButton("", "#35ae56", "icons/play.png")
        play_button.clicked.connect(lambda: self.play_recording())

        self.addWidget(self.list_view, 0, 0, 6, 1)
        self.addWidget(add_button, 0, 1)
        self.addWidget(remove_button, 1, 1)
        self.addWidget(play_button, 2, 1)

    def start_add_new_window(self):
        self.new_record_window = RecordWindow(self.model)
        self.new_record_window.exec_()

    def confirm_deletion(self):
        dialog_window = DialogWindow(self.model, 'Are you sure you want to delete this recording?')
        if dialog_window.exec_():
            if dialog_window.result:
                file_name = self.list_view.currentIndex().data().toString()
                self.model.removeRows(self.list_view.currentIndex().row(), 1)
                os.remove(RECS_DIR + "/" + str(file_name))

    def play_recording(self):
        current_recording = self.model.data(self.list_view.currentIndex(), QtCore.Qt.DisplayRole)
        stream = SoundStream(1024, pyaudio.paInt16, 1, 44100)
        stream.open_stream("out")
        stream.play_wav_recording(current_recording)


class ChartGrid(QtGui.QGridLayout):
    def __init__(self, model):
        super(ChartGrid, self).__init__()

        self.model = model

        self.list_view = ChartListView(self.model)
        self.addWidget(self.list_view, 0, 0, 6, 1)


class PlotGrid(QtGui.QGridLayout):
    def __init__(self, Fmodel, Cmodel, Fview, Cview):
        super(PlotGrid, self).__init__()

        self.Fmodel = Fmodel
        self.Cmodel = Cmodel
        self.Fview = Fview
        self.Cview = Cview
        self.current_chart_key = None
        self.current_chart_value = None
        self.current_recording = None
        self.setColumnMinimumWidth(1, 200)

        self.file_label = QtGui.QLabel('Current file is: None')

        self.chart_label = QtGui.QLabel('Current chart is: None')

        self.plot_button = QtGui.QPushButton('Plot')
        self.plot_button.clicked.connect(self.button_clicked)

        self.addWidget(self.file_label, 0, 0, 1, 2)

        self.addWidget(self.chart_label, 1, 0, 1, 2)

        self.addWidget(self.plot_button, 2, 0, 1, 2)

    def button_clicked(self):
        # try:
            chart_window = ChartWindow(self.current_chart_value, self.current_recording, self.current_chart_key)
            chart_window.show()
        # except TypeError:
        #     self.chart_label.setText("Choose chart type and file first!")

    def labels_change(self):
        self.current_recording = self.Fmodel.data(self.Fview.currentIndex(), QtCore.Qt.DisplayRole)
        self.file_label.setText('Current file is: %s' % self.current_recording)

        self.current_chart_key, self.current_chart_value = self.Cmodel.data(self.Cview.currentIndex(),
                                                                            QtCore.Qt.UserRole)
        self.chart_label.setText('Current chart is: %s' % self.current_chart_key)


class MainWindow(QtGui.QWidget):
    def __init__(self, file_list_model, chart_list_model):
        super(MainWindow, self).__init__()

        self.file_list_model = file_list_model
        self.chart_list_model = chart_list_model

        hbox = QtGui.QHBoxLayout(self)

        file_grid = FileGrid(self.file_list_model)
        file_frame = QtGui.QFrame()
        file_frame.setLayout(file_grid)

        chart_grid = ChartGrid(self.chart_list_model)
        chart_frame = QtGui.QFrame()
        chart_frame.setLayout(chart_grid)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(file_frame)
        splitter1.addWidget(chart_frame)

        plot_grid = PlotGrid(self.file_list_model, self.chart_list_model, file_grid.list_view, chart_grid.list_view)
        plot_frame = QtGui.QFrame()
        plot_frame.setLayout(plot_grid)
        chart_grid.list_view.clicked.connect(plot_grid.labels_change)
        file_grid.list_view.clicked.connect(plot_grid.labels_change)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(plot_frame)

        splitter2.setStretchFactor(0, 2)
        splitter2.setStretchFactor(1, 1)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        self.setGeometry(200, 200, 700, 200)
        self.setWindowTitle('Main window')
