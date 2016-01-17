import os
import sys
from collections import OrderedDict
from dircache import listdir
from os.path import isfile
from os.path import join

from PyQt4 import QtGui, QtCore

import spyker.model.charts as plots
from spyker.gui.mainwindow import MainWindow
from spyker.model.chartlistmodel import ChartListModel
from spyker.model.filelistmodel import FileListModel
from spyker.utils.constants import ChartType, RECS_DIR

if __name__ == '__main__':

    chart_dict = OrderedDict({ChartType.RAW: plots.raw,
                              ChartType.PSD: plots.psd,
                              ChartType.MFCC: plots.mfccoefs,
                              ChartType.STFT: plots.stft,
                              ChartType.FORMANTS: plots.formant_freqs,
                              ChartType.STFT3D: plots.stft3d})

    chart_list_model = ChartListModel(chart_dict)

    file_list_model = FileListModel()

    if os.path.exists(RECS_DIR):
        for f in listdir(RECS_DIR):
            if isfile(join(RECS_DIR, f)):
                file_list_model.insertRows(f)

    app = QtGui.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile('icons/16.png', QtCore.QSize(16, 16))
    app_icon.addFile('icons/24.png', QtCore.QSize(24, 24))
    app_icon.addFile('icons/32.png', QtCore.QSize(32, 32))
    app_icon.addFile('icons/64.png', QtCore.QSize(64, 64))
    app_icon.addFile('icons/128.png', QtCore.QSize(128, 128))
    app_icon.addFile('icons/256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    main_window = MainWindow(file_list_model, chart_list_model)
    main_window.show()
    sys.exit(app.exec_())
