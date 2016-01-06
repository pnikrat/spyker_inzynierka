from PyQt4 import QtGui, QtCore


class FilePicker(QtGui.QDialog):
    def __init__(self, model, file_picker_listener):
        super(FilePicker, self).__init__()
        self.model = model
        self.file_picker_listener = file_picker_listener
        self.init_ui()

    def init_ui(self):
        self.vBoxLayout = QtGui.QVBoxLayout()
        self.init_list_view()
        self.init_buttons_layout()
        self.setLayout(self.vBoxLayout)

    def init_list_view(self):
        self.file_list_view = QtGui.QListView()
        self.file_list_view.setModel(self.model)
        self.vBoxLayout.addWidget(self.file_list_view)

    def init_buttons_layout(self):
        buttons_layout = QtGui.QHBoxLayout()
        ok_button = QtGui.QPushButton("Ok")
        ok_button.clicked.connect(self.on_ok_button)

        cancel_button = QtGui.QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        self.vBoxLayout.addLayout(buttons_layout)

    def on_ok_button(self):
        picked_file = self.model.data(self.file_list_view.currentIndex(), QtCore.Qt.DisplayRole)
        self.file_picker_listener.file_picked(picked_file)
        self.close()
