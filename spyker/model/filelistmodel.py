from PyQt4 import QtCore


class FileListModel(QtCore.QAbstractListModel):
    def __init__(self, file_paths=[], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__file_paths = file_paths



    def rowCount(self, parent):
        return len(self.__file_paths)

    def data(self, index, role):

        if role == QtCore.Qt.EditRole:
            return self.__file_paths[index.row()]

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.__file_paths[row]
            return value

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.__file_paths[index.row()] = value
            self.dataChanged.emit(index, index)
            return True

    # =====================================================#
    # INSERTING & REMOVING
    # =====================================================#
    def insertRows(self, file_name):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__file_paths), len(self.__file_paths))
        self.__file_paths.insert(len(self.__file_paths), file_name)
        self.endInsertRows()

    def removeRows(self, position, rows):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)

        for i in range(rows):
            value = self.__file_paths[position]
            self.__file_paths.remove(value)

        self.endRemoveRows()
