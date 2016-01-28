#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pyaudio
from PyQt4 import QtGui, QtCore

from spyker.gui.chartlistview import ChartListView
from spyker.gui.chartwindow import ChartWindow
from spyker.gui.dialogwindow import DialogWindow, OkWindow
from spyker.gui.filebutton import FileButton
from spyker.gui.filelistview import FileListView
from spyker.gui.recordwindow import RecordWindow
from spyker.model.recording import SoundStream
from spyker.utils.constants import RECS_DIR, f_sampling


class FileGrid(QtGui.QGridLayout):
    def __init__(self, model):
        super(FileGrid, self).__init__()

        self.model = model

        self.list_view = FileListView(self.model)

        file_grid_label = QtGui.QLabel('Nagrania')

        add_button = FileButton("+", "#35ae56")
        add_button.clicked.connect(self.start_new_record_window)
        add_button.setToolTip("Dodaj nowe nagranie")

        remove_button = FileButton("-", "#d05d4f")
        remove_button.clicked.connect(self.confirm_deletion)
        remove_button.setToolTip(u"Usuń wybrane nagranie")

        play_button = FileButton("", "#35ae56", "icons/play.png")
        play_button.clicked.connect(lambda: self.play_recording())
        play_button.setToolTip(u"Odtwórz wybrane nagranie")

        self.addWidget(file_grid_label, 0, 0, 1, 2)
        self.addWidget(self.list_view, 1, 0, 30, 1)
        self.addWidget(add_button, 1, 1)
        self.addWidget(remove_button, 2, 1)
        self.addWidget(play_button, 3, 1)
        self.setRowStretch(0, 0)
        self.setRowStretch(1, 10)

    def start_new_record_window(self):
        new_record_window = RecordWindow(self.model)
        new_record_window.exec_()

    def confirm_deletion(self):
        if len(self.model.file_paths) == 0:
            ok_window = OkWindow(u'W katalogu nie ma plików do usunięcia')
            ok_window.exec_()
            return
        dialog_window = DialogWindow(self.model, u'Czy jesteś pewien?')
        if dialog_window.exec_():
            if dialog_window.result:
                file_name = self.list_view.currentIndex().data().toString()
                self.model.removeRows(self.list_view.currentIndex().row(), 1)
                os.remove(RECS_DIR + "/" + str(file_name))

    def play_recording(self):
        if len(self.model.file_paths) == 0:
            ok_window = OkWindow(u'W katalogu nie ma plików do odtworzenia')
            ok_window.exec_()
            return
        current_recording = self.model.data(self.list_view.currentIndex(), QtCore.Qt.DisplayRole)
        stream = SoundStream(1024, pyaudio.paInt16, 1, f_sampling)
        stream.open_stream("out")
        stream.play_wav_recording(current_recording)


class ChartGrid(QtGui.QGridLayout):
    def __init__(self, model):
        super(ChartGrid, self).__init__()

        self.model = model
        chart_grid_label = QtGui.QLabel(u'Przekształcenia')

        self.list_view = ChartListView(self.model)
        self.addWidget(chart_grid_label, 0, 0, 1, 1)
        self.addWidget(self.list_view, 1, 0, 6, 1)
        self.setRowStretch(0, 0)
        self.setRowStretch(1, 10)


class PlotGrid(QtGui.QGridLayout):
    def __init__(self, Fmodel, Cmodel, Fview, Cview):
        super(PlotGrid, self).__init__()

        self.file_model = Fmodel
        self.chart_model = Cmodel
        self.file_view = Fview
        self.chart_view = Cview
        self.current_chart_key = None
        self.current_chart_value = None
        self.current_recording = None
        self.setColumnMinimumWidth(1, 200)

        self.file_label = QtGui.QLabel(u'Nagranie: ')

        self.chart_label = QtGui.QLabel(u'Przekształcenie: ')

        self.plot_button = QtGui.QPushButton(u'Wykreśl')
        self.plot_button.clicked.connect(self.button_clicked)

        self.addWidget(self.file_label, 0, 0, 1, 2)

        self.addWidget(self.chart_label, 1, 0, 1, 2)

        self.addWidget(self.plot_button, 2, 0, 1, 2)

    def button_clicked(self):
        if self.current_chart_value is None or self.current_recording is None:
            self.chart_label.setText(u"Wybierz plik\noraz rodzaj przekształcenia!")
        else:
            try:
                chart_window = ChartWindow(self.current_chart_value, self.current_recording, self.current_chart_key,
                                           self.file_model)
                chart_window.show()
            except IOError:
                self.chart_label.setText(u"Wybierz plik\noraz rodzaj przekształcenia!")
        # except TypeError:
        #     self.chart_label.setText(u"Wybierz plik\noraz rodzaj przekształcenia!")

    def labels_change(self):
        try:
            self.current_recording = self.file_model.data(self.file_view.currentIndex(), QtCore.Qt.DisplayRole)
            self.file_label.setText(u'Nagranie:  %s' % unicode(self.current_recording))

            self.current_chart_key, self.current_chart_value = self.chart_model.data(self.chart_view.currentIndex(),
                                                                                     QtCore.Qt.UserRole)
            self.chart_label.setText(u'Przekształcenie: %s' % unicode(self.current_chart_key))
        except IndexError:
            self.file_label.setText(u'Brak nagrań!')


class MainWindow(QtGui.QWidget):
    def __init__(self, file_list_model, chart_list_model):
        super(MainWindow, self).__init__()

        self.file_list_model = file_list_model
        self.chart_list_model = chart_list_model

        hbox = QtGui.QVBoxLayout(self)

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
        file_grid.list_view.doubleClicked.connect(file_grid.play_recording)
        chart_grid.list_view.doubleClicked.connect(plot_grid.button_clicked)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(plot_frame)

        splitter2.setStretchFactor(0, 2)
        splitter2.setStretchFactor(1, 1)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        self.setGeometry(200, 200, 700, 250)
        self.setWindowTitle('Feature Extraction & Visualisation')
