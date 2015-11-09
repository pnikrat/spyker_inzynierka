import os
from PyQt4 import QtGui, QtCore
from spyker.gui.recordwindow import RecordWindow
from spyker.model.filelistmodel import FileListModel
from os import listdir
from os.path import isfile, join
from spyker.utils.constants import RECS_DIR


class FileListView(QtGui.QListView):
    def __init__(self, model):
        super(FileListView, self).__init__()

        self.setModel(model)

        if os.path.exists(RECS_DIR):
            for f in listdir(RECS_DIR):
                if isfile(join(RECS_DIR, f)):
                    self.model().insertRows(f)


class FileButton(QtGui.QPushButton):
    def __init__(self, text, color):
        super(FileButton, self).__init__()
        self.setFixedSize(25, 25)
        self.setStyleSheet("""
            FileButton {
                color:""" + color + """;
                font: 18px;
                border-radius: 2px;
                }

            FileButton:hover {
                background-color: #c4c4c4;
                }

            FileButton:pressed {
                background-color: #a2a2a2;
                }
            """)
        self.setText(text)


class FileGrid(QtGui.QGridLayout):
    def __init__(self, model):
        super(FileGrid, self).__init__()

        self.model = model

        self.list_view = FileListView(self.model)

        add_button = FileButton("+", "#35ae56")
        add_button.clicked.connect(self.start_add_new_window)

        remove_button = FileButton("-", "#d05d4f")
        remove_button.clicked.connect(self.start_add_new_window)

        self.addWidget(self.list_view, 0, 0, 6, 1)
        self.addWidget(add_button, 0, 1)
        self.addWidget(remove_button, 1, 1)

    def start_add_new_window(self):
        self.new_record_window = RecordWindow(self.model)
        self.new_record_window.show()


class ChartGrid(QtGui.QGridLayout):
    def __init__(self):
        super(ChartGrid, self).__init__()

        self.list_view = QtGui.QListView()
        self.addWidget(self.list_view, 0, 0, 6, 1)


class PlotGrid(QtGui.QGridLayout):
    def __init__(self, model):
        super(PlotGrid, self).__init__()

        self.model = model

        self.file_label = QtGui.QLabel('Current file is: ')
        self.file_combo_box = QtGui.QComboBox()
        self.file_combo_box.setModel(self.model)

        self.chart_label = QtGui.QLabel('Current chart is: ')
        self.chart_combo_box = QtGui.QComboBox()
        self.chart_combo_box.setModel(self.model)

        self.plot_button = QtGui.QPushButton('Plot')

        self.addWidget(self.file_label, 0, 0)
        self.addWidget(self.file_combo_box, 0, 1)

        self.addWidget(self.chart_label, 1, 0)
        self.addWidget(self.chart_combo_box, 1, 1)

        self.addWidget(self.plot_button, 2, 1)


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.file_list_model = FileListModel()

        hbox = QtGui.QHBoxLayout(self)

        file_grid = FileGrid(self.file_list_model)
        file_frame = QtGui.QFrame()
        file_frame.setLayout(file_grid)

        chart_grid = ChartGrid()
        chart_frame = QtGui.QFrame()
        chart_frame.setLayout(chart_grid)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(file_frame)
        splitter1.addWidget(chart_frame)

        plot_grid = PlotGrid(self.file_list_model)
        plot_frame = QtGui.QFrame()
        plot_frame.setLayout(plot_grid)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(plot_frame)

        splitter2.setStretchFactor(0, 2)
        splitter2.setStretchFactor(1, 1)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Speaker features')
