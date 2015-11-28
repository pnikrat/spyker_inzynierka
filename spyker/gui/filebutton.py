from PyQt4 import QtGui


class FileButton(QtGui.QPushButton):
    def __init__(self, text, color):
        super(FileButton, self).__init__()
        self.setFixedSize(25, 25)
        self.setStyleSheet("""
            FileButton {
                color:""" + color + """;
                font: 18px;
                border-radius: 2px;
                }

            FileButton:hover {
                background-color: #c4c4c4;
                }

            FileButton:pressed {
                background-color: #a2a2a2;
                }
            """)
        self.setText(text)
