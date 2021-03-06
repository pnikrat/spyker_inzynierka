from PyQt4 import QtGui


class FileButton(QtGui.QPushButton):
    def __init__(self, text, color, icon=""):
        super(FileButton, self).__init__()
        self.setFixedSize(32, 32)
        self.setStyleSheet("""
            FileButton {
                color:""" + color + """;
                font: 18px;
                border-radius: 2px;
                background-image: url(""" + icon + """);
                }
            FileButton:hover {
                background-color: #c4c4c4;
                }

            FileButton:pressed {
                background-color: #a2a2a2;
                }
            """)
        self.setText(text)