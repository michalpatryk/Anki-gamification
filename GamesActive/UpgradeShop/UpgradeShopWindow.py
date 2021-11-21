from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow
from PyQt6 import QtCore, QtWidgets
import typing


class UpgradeShopWindow(DefaultGameMdiSubWindow):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow, controller=None) -> None:
        super().__init__(parent=parent, flags=flags, controller=controller)
        self.resize(250, 125)
        self.menuName = "Upgrades"
        self.isUnlocked = True
        self.shouldStartVisible = False
        self.gameName = "UpgradeShop"
        self.setWindowTitle(self.menuName)

