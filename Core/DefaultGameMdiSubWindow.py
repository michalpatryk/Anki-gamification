
from PyQt6 import QtCore, QtWidgets, QtGui
import typing

class DefaultGameMdiSubWindow(QtWidgets.QMdiSubWindow):

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow) -> None:
        super().__init__(parent=parent, flags=flags)
        self.setGeometry(40, 50, 250, 250)
        self.setMaximumSize(250, 250)
        self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowType.WindowMaximizeButtonHint)


    def onClick(self):
        self.hide()

    def closeEvent(self, closeEvent: QtGui.QCloseEvent) -> None:
        self.mdiArea().parent().mdiSubwindowOnClose(self)
        return super().closeEvent(closeEvent)