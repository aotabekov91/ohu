from PyQt5 import QtCore, QtWidgets

class Viewport(QtWidgets.QWidget):

    updated=QtCore.pyqtSignal()

    def update(self, *args, **kwargs):

        super().update(*args, **kwargs)
        self.updated.emit()
