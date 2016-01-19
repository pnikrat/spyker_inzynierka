#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class EntryLayout(QtGui.QGridLayout):
    def __init__(self, label_name):
        QtGui.QVBoxLayout.__init__(self)
        self.setAlignment(Qt.AlignTop)

        label = QtGui.QLabel(label_name)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtGui.QDoubleSpinBox()
        self.button = QtGui.QPushButton(u'Wykreśl przekrój w osi ' + str(label_name))

        edit_layout = QtGui.QGridLayout()
        edit_layout.addWidget(self.slider, 0, 0, 1, 2)
        edit_layout.addWidget(self.spinbox, 0, 2, 1, 1)

        self.addWidget(label, 0, 0)
        self.addLayout(edit_layout, 1, 0)
        self.addWidget(self.button, 2, 0)

        self.slider.valueChanged.connect(self.slider_value_changed)
        self.spinbox.valueChanged.connect(self.spinbox_value_changed)
        self.should_update = True

    def set_maximum(self, slider_max, spinbox_max):
        self.slider_max = slider_max
        self.spinbox_max = spinbox_max

        self.slider.setMaximum(slider_max)
        self.spinbox.setMaximum(spinbox_max)

        self.step = float(spinbox_max) / slider_max
        self.spinbox.setSingleStep(self.step)

    def reset(self):
        self.slider.setValue(0)
        self.spinbox.setValue(0)

    def slider_value_changed(self, value):
        if self.should_update:
            self.should_update = False
            self.spinbox.setValue(value * self.step)
            return
        self.should_update = True

    def spinbox_value_changed(self, value):
        if self.should_update:
            self.should_update = False
            slider_value = self.slider_max * float(value) / self.spinbox_max
            self.slider.setValue(slider_value)
            return
        self.should_update = True
