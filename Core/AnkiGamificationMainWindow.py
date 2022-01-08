import typing
from PyQt6 import QtCore, QtWidgets, QtGui

import GamesActive
from .GameMainframe import GameMainframe
from .DefaultGameMdiSubWindow import DefaultGameMdiSubWindow

class MdiView(QtWidgets.QMdiArea):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self.setObjectName("MdiView")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(200, 100)



class AnkiGamificationMainWindow(QtWidgets.QMainWindow):
    def __init__(self, gameMainframe: GameMainframe) -> None:
        super(AnkiGamificationMainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setMaximumSize(500, 500)
        self.setWindowTitle("AnkiGamification")
        self.setObjectName("AnkiGamificationMainWindow")

        # Initialize main area
        self.mdiArea = MdiView(self)
        self.setCentralWidget(self.mdiArea)
        # Customize menubar
        self.menuBar = QtWidgets.QMenuBar(self)
        self.gameMenu = QtWidgets.QMenu("&Games", self)

        self.menuActionsDictionary = dict()
        self.gamesDictionary = dict()

        self.gameMainframe = gameMainframe
        self.gameLoopTimer = QtCore.QTimer()
        self.gameLoopTimer.timeout.connect(self.gameMainframe.update)
        self.gameLoopTimer.start(100)

        # Startup game windows
        games = GamesActive.loadFiles()
        for game in games:
            controller = self.gameMainframe.addGame(game.controller)
            if controller is not None:
                self.initGame(game.window, controller)
            else:
                self.initGame(game.window, self.gameMainframe.getGameByControllerType(game.controller))

        self.createWindowControlMenu()

        self.menuBar.addMenu(self.gameMenu)
        self.menuBar.addMenu(self.windowLocationMenu)
        self.setMenuBar(self.menuBar)


    def initGame(self, gameType: DefaultGameMdiSubWindow, controller):
        game = gameType(self, controller=controller) #type: DefaultGameMdiSubWindow
        game.setVisible(game.shouldStartVisible)
        self.mdiArea.addSubWindow(game)
        self.gamesDictionary[game.gameName] = game
        self.menuActionsDictionary[game.menuName] =  QtGui.QAction(game.menuName, self.gameMenu, checkable=True)
        self.menuActionsDictionary[game.menuName].toggled.connect(lambda: self.GameMenuEntry(game))
        self.menuActionsDictionary[game.menuName].setEnabled(game.isUnlocked)
        self.menuActionsDictionary[game.menuName].setChecked(game.shouldStartVisible)
        self.gameMenu.addAction(self.menuActionsDictionary[game.menuName])


    def GameMenuEntry(self, subWindow: DefaultGameMdiSubWindow):
        if(self.menuActionsDictionary[subWindow.menuName].isChecked()):
            self.gamesDictionary[subWindow.gameName].show()
        else:
            self.gamesDictionary[subWindow.gameName].hide()


    def mdiSubwindowOnClose(self, sender: DefaultGameMdiSubWindow):
        self.menuActionsDictionary[sender.menuName].setChecked(False)
        self.gamesDictionary[sender.gameName].hide()

    def createWindowControlMenu(self):
        self.windowLocationMenu = QtWidgets.QMenu("&Window control", self)
        self.cascadeWindowsAction =  QtGui.QAction("Cascade windows", self.windowLocationMenu)
        self.cascadeWindowsAction.triggered.connect(self.mdiArea.cascadeSubWindows)
        self.windowLocationMenu.addAction(self.cascadeWindowsAction)

    def getMenuAction(self, menuName):
        return self.menuActionsDictionary[menuName]   

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.gameMainframe.save()
        print("exiting")
        return super().closeEvent(a0)
