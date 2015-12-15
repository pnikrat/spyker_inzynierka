import sys
from collections import OrderedDict

import matplotlib
from PyQt4 import QtGui

import spyker.model.charts as plots
from spyker.gui.mainwindow import MainWindow
from spyker.model.chartlistmodel import ChartListModel
from spyker.model.filelistmodel import FileListModel
from spyker.utils.constants import ChartType

if __name__ == '__main__':
    chart_dict = OrderedDict({ChartType.RAW: plots.raw,
                              ChartType.ENVELOPE: plots.envelope,
                              ChartType.FFT: plots.fft,
                              ChartType.MFCC: plots.mfccoefs,
                              ChartType.STFT: plots.stft,
                              ChartType.FORMANTS: plots.formant_freqs_on_fft,
                              ChartType.STFT3D: plots.stft3d})

    chart_list_model = ChartListModel(chart_dict)
    file_list_model = FileListModel()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow(file_list_model, chart_list_model)
    main_window.show()
    sys.exit(app.exec_())


