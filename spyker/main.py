from collections import OrderedDict
import sys
from PyQt4 import QtGui
from spyker.gui.mainwindow import MainWindow
from spyker.model.chartlistmodel import ChartListModel
from spyker.model.filelistmodel import FileListModel
import spyker.model.charts as plots
from spyker.utils.constants import ChartType

if __name__ == '__main__':
    chart_dict = OrderedDict({ChartType.RAW: plots.raw,
                              ChartType.ENVELOPE: plots.envelope,
                              ChartType.FFT: plots.fft,
                              ChartType.MFCC: plots.mfccoefs,
                              ChartType.STFT: plots.stft})

    chart_list_model = ChartListModel(chart_dict)
    file_list_model = FileListModel()

    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow(file_list_model, chart_list_model)
    main_window.show()
    sys.exit(app.exec_())
