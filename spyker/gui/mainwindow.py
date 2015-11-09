import os
from PyQt4 import QtGui, QtCore
from spyker.gui.recordwindow import RecordWindow
from spyker.model.filelistmodel import FileListModel
from os import listdir
from os.path import isfile, join

RECS_DIR = "records"


class FileListView(QtGui.QListView):
    def __init__(self, model):
        super(FileListView, self).__init__()

        self.setModel(model)

        if os.path.exists(RECS_DIR):
            for f in listdir(RECS_DIR):
                if isfile(join(RECS_DIR, f)):
                    self.model().insertRows(f)


class FileGrid(QtGui.QGridLayout):
    def __init__(self):
        super(FileGrid, self).__init__()

        self.model = FileListModel()

        self.list_view = FileListView(self.model)

        add_button = QtGui.QPushButton('+')
        add_button.clicked.connect(self.start_add_new_window)

        remove_button = QtGui.QPushButton('-')
        remove_button.clicked.connect(self.start_add_new_window)

        edit_button = QtGui.QPushButton('e')
        edit_button.clicked.connect(self.start_add_new_window)

        self.addWidget(self.list_view, 0, 0, 6, 1)
        self.addWidget(add_button, 0, 1)
        self.addWidget(remove_button, 1, 1)
        self.addWidget(edit_button, 2, 1)

    def start_add_new_window(self):
        self.new_record_window = RecordWindow(self.model)
        self.new_record_window.show()


class ChartGrid(QtGui.QGridLayout):
    def __init__(self):
        super(ChartGrid, self).__init__()

        self.model = FileListModel()

        self.table_view = QtGui.QListView()
        self.table_view.setModel(self.model)

        add_button = QtGui.QPushButton('+')
        add_button.clicked.connect(self.start_add_new_window)

        remove_button = QtGui.QPushButton('-')
        remove_button.clicked.connect(self.start_add_new_window)

        edit_button = QtGui.QPushButton('e')
        edit_button.clicked.connect(self.start_add_new_window)

        self.addWidget(self.table_view, 0, 0, 6, 1)
        self.addWidget(add_button, 0, 1)
        self.addWidget(remove_button, 1, 1)
        self.addWidget(edit_button, 2, 1)

    def start_add_new_window(self):
        self.new_record_window = (self.model)
        self.new_record_window.show()


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        hbox = QtGui.QHBoxLayout(self)

        file_grid = FileGrid()
        file_frame = QtGui.QFrame()
        file_frame.setLayout(file_grid)

        chart_grid = ChartGrid()
        chart_frame = QtGui.QFrame()
        chart_frame.setLayout(chart_grid)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(file_frame)
        splitter1.addWidget(chart_frame)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)

        empty_frame = QtGui.QFrame()
        splitter2.addWidget(empty_frame)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Speaker features')
