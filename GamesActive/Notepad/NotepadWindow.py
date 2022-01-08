from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow
from PyQt6 import QtCore, QtWidgets
import typing


class NotepadWidget(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional['QWidget'] = ..., flags: QtCore.Qt.WindowType = ...) -> None:
        super().__init__(parent=parent, flags=flags)
        self.setObjectName("NotepadWidget")
        self.resize(400, 300)
        self.mainWidgetLayout = QtWidgets.QGridLayout(self)
        self.mainWidgetLayout.setObjectName("mainWidgetLayout")
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.tabLayout1 = QtWidgets.QGridLayout(self.tab)
        self.tabLayout1.setObjectName("tabLayout1")
        self.textEdit1 = QtWidgets.QTextEdit(self.tab)
        self.textEdit1.setObjectName("textEdit1")
        self.tabLayout1.addWidget(self.textEdit1, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "Tab 1")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabLayout2 = QtWidgets.QGridLayout(self.tab_2)
        self.tabLayout2.setObjectName("tabLayout2")
        self.textEdit2 = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit2.setObjectName("textEdit2")
        self.tabLayout2.addWidget(self.textEdit2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "Tab 2")
        self.mainWidgetLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

class NotepadWindow(DefaultGameMdiSubWindow):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow, controller=None) -> None:
        super().__init__(parent=parent, flags=flags, controller=controller)
        self.setMaximumSize(250, 400)
        self.resize(150, 400)
        self.menuName = "Notepad"
        self.isUnlocked = False
        self.shouldStartVisible = False
        self.gameName = "NotepadDisplay"
        self.setWindowTitle(self.menuName)

        self.notepadWidget = NotepadWidget(self, flags)
        self.setWidget(self.notepadWidget)
        self.controller.attachUnlockHandle(self.unlock)
        self.controller.attachIncreaseMaxSizeHandle(self.increaseMaxSize)
