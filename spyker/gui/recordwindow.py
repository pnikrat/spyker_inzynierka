from PyQt4 import QtGui


class NewRecordWindow(QtGui.QWidget):
    def __init__(self, model):
        super(NewRecordWindow, self).__init__()

        self.model = model

        self.name_label = QtGui.QLabel('name')
        self.name_edit = QtGui.QLineEdit()

        self.ok_button = QtGui.QPushButton('Ok')
        self.ok_button.clicked.connect(lambda: self.add_new_file())
        self.cancel_button = QtGui.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.name_edit, 0, 1)
        grid.addWidget(self.ok_button, 1, 0)
        grid.addWidget(self.cancel_button, 1, 1)
        self.setLayout(grid)
        self.setGeometry(200, 200, 200, 200)
        self.setWindowTitle('Add new record')

    def add_new_file(self):
        self.model.insertRows(self.name_edit.text())
        self.close()
