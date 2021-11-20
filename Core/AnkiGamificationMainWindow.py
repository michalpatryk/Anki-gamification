import typing
from PyQt6 import QtCore, QtWidgets, QtGui

import GamesActive

from GamesActive.QuizGame.AnkiQuizGameController import QuizGameModel
from .GameMainframe import GameMainframe
from .DefaultGameMdiSubWindow import DefaultGameMdiSubWindow

from GamesActive.QuizGame.AnkiQuizWindow import QuizGameWindow
# we can add an component list file in GamesActive with imports only. 
# I'm probably reinventing packages

class MdiView(QtWidgets.QMdiArea):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        # self.mdiSubWindow = DefaultGameMdiSubWindow(
        #     self)
        # # self.mdiSubWindow2 = QuizGameWindow(self)

        # button = QtWidgets.QPushButton()
        # button.clicked.connect(AnkiGamificationMainWindow.onClick)
        # self.mdiSubWindow.setWidget(button)

        # self.addSubWindow(self.mdiSubWindow)
        # # self.addSubWindow(self.mdiSubWindow2)


class AnkiGamificationMainWindow(QtWidgets.QMainWindow):
    def __init__(self, gameMainframe: GameMainframe) -> None:
        super(AnkiGamificationMainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setMaximumSize(500, 500)
        self.setWindowTitle("AnkiGamification")

        # Initialize main area
        self.mdiArea = MdiView(self)
        self.setCentralWidget(self.mdiArea)

        # customize menubar
        self.menuBar = QtWidgets.QMenuBar(self)
        self.gameMenu = QtWidgets.QMenu("&Games", self)

        self.menuActionsDictionary = dict()
        self.gamesDictionary = dict()

        self.gameMainframe = gameMainframe
        self.gameLoopTimer = QtCore.QTimer()
        self.gameLoopTimer.timeout.connect(self.gameMainframe.update)
        self.gameLoopTimer.start(100)

        games = GamesActive.loadFiles()
        for game in games:
            controller = self.gameMainframe.addGame(game.controller)
            if controller is not None:
                self.initGame(game.window, controller)
            else:
                self.initGame(game.window, self.gameMainframe.getGameByControllerType(game.controller))


        self.menuBar.addMenu(self.gameMenu)
        self.setMenuBar(self.menuBar)


    def initGame(self, gameType: DefaultGameMdiSubWindow, controller):
        game = gameType(self, controller=controller) #type: DefaultGameMdiSubWindow
        game.setVisible(game.shouldStartVisible)
        self.mdiArea.addSubWindow(game)
        self.gamesDictionary[game.gameName] = game
        self.menuActionsDictionary[game.menuName] =  QtGui.QAction(game.menuName, self.gameMenu, checkable=True)
        self.menuActionsDictionary[game.menuName].toggled.connect(lambda: self.GameMenuEntry(game))
        self.menuActionsDictionary[game.menuName].setEnabled(game.isUnlocked)
        self.gameMenu.addAction(self.menuActionsDictionary[game.menuName])


    def GameMenuEntry(self, subWindow: DefaultGameMdiSubWindow):
        if(self.menuActionsDictionary[subWindow.menuName].isChecked()):
            self.gamesDictionary[subWindow.gameName].show()
        else:
            self.gamesDictionary[subWindow.gameName].hide()


    def mdiSubwindowOnClose(self, sender: DefaultGameMdiSubWindow):
        self.menuActionsDictionary[sender.menuName].setChecked(False)
        self.gamesDictionary[sender.gameName].hide()
        

    def onClick(self):
        print("hey")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.gameMainframe.save()
        print("exiting")
        return super().closeEvent(a0)
