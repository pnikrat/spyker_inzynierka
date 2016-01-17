#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class DialogWindow(QtGui.QDialog):
    def __init__(self, model, message):
        super(DialogWindow,self).__init__()

        self.model = model

        self.result = None

        self.message_label = QtGui.QLabel(message)

        self.yes_button = QtGui.QPushButton('Tak')
        self.no_button = QtGui.QPushButton('Nie')
        self.no_button.clicked.connect(lambda: self.no_decision())
        self.yes_button.clicked.connect(lambda: self.yes_decision())

        grid = QtGui.QGridLayout()
        grid.addWidget(self.message_label, 0, 0, 1, 2)
        grid.addWidget(self.yes_button, 1, 0)
        grid.addWidget(self.no_button, 1, 1)

        self.setLayout(grid)
        self.setGeometry(200, 200, 100, 100)
        self.setWindowTitle(u'Potwierdzenie')

    def no_decision(self):
        self.result = False
        self.accept()

    def yes_decision(self):
        self.result = True
        self.accept()