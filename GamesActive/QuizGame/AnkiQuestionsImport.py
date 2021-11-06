

from PyQt6.QtWidgets import QDialog
import typing
from PyQt6 import QtCore, QtWidgets, QtGui

class LoadQuestionsDialog(QtWidgets.QDialog):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType =  QtCore.Qt.WindowType.Dialog) -> None:
        super().__init__(parent=parent, flags=flags)
        print(123)


