
from PyQt6 import QtCore, QtWidgets, QtGui
import operator
import typing

class DefaultGameMdiSubWindow(QtWidgets.QMdiSubWindow):

    def __init__(self, parent: QtWidgets.QWidget, flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow, controller = None) -> None:
        super().__init__(parent=parent, flags=flags)
        self.setGeometry(40, 50, 250, 250)
        self.setMaximumSize(250, 250)
        self.setWindowFlags(self.windowFlags() &~ QtCore.Qt.WindowType.WindowMaximizeButtonHint)
        self.menuName = "Default"
        self.isUnlocked = False
        self.shouldStartVisible = False
        self.gameName = "DefaultGameName"
        self.controller = controller


    def onClick(self):
        self.hide()

    def closeEvent(self, closeEvent: QtGui.QCloseEvent) -> None:
        self.mdiArea().parent().mdiSubwindowOnClose(self)

    def unlock(self):
        self.isUnlocked = True
        if self.mdiArea() is not None:
            action = self.mdiArea().parent().getMenuAction(self.menuName)
            action.setEnabled(True)

    def increaseMaxSize(self, width, height, operator: operator):
        size = self.maximumSize()
        size.setWidth(operator(size.width(), width))
        size.setHeight(operator(size.height(), height))
        self.setMaximumSize(size)