import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class EntryLayout(QtGui.QGridLayout):
    def __init__(self, label_name):
        QtGui.QVBoxLayout.__init__(self)
        self.setAlignment(Qt.AlignTop)

        label = QtGui.QLabel(label_name)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtGui.QSpinBox()
        self.button = QtGui.QPushButton('plot')

        edit_layout = QtGui.QHBoxLayout()
        edit_layout.addWidget(self.slider)
        edit_layout.addWidget(self.spinbox)

        self.addWidget(label, 0, 0)
        self.addLayout(edit_layout, 1, 0)
        self.addWidget(self.button, 2, 0)

        self.slider.valueChanged.connect(self.slider_value_changed)
        self.spinbox.valueChanged.connect(self.spinbox_value_changed)

    def set_maximum(self, max):
        self.slider.setMaximum(max)
        self.spinbox.setMaximum(max)

    def slider_value_changed(self, value):
        self.spinbox.setValue(value)

    def spinbox_value_changed(self, value):
        self.slider.setValue(value)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    awd = EntryLayout("elo ziomeczku")
    dwa = QtGui.QDialog()
    dwa.setLayout(awd)
    dwa.resize(400, 80)
    dwa.show()
    sys.exit(app.exec_())
