
import typing
import json
from PyQt6 import QtCore, QtWidgets, QtGui
from . import GameController as gc
from . import DefaultGameMdiSubWindow

from GamesActive.QuizGame.AnkiQuizWidget import QuizGameWindow

# this is a useless proxy and should be removed? At the very least it shouldnt be the one to add subwindows
class MdiView(QtWidgets.QMdiArea):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self.mdiSubWindow = DefaultGameMdiSubWindow.DefaultGameMdiSubWindow(self)
        self.mdiSubWindow2 = QuizGameWindow(self)
        
        button = QtWidgets.QPushButton()
        button.clicked.connect(AnkiGamificationMainWindow.onClick)
        self.mdiSubWindow.setWidget(button)

        self.addSubWindow(self.mdiSubWindow)
        self.addSubWindow(self.mdiSubWindow2)


class AnkiGamificationMainWindow(QtWidgets.QMainWindow):
    def __init__(self, gameMainframe : gc.GameMainframe) -> None:
        super(AnkiGamificationMainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("AnkiGamification")
        
        # Initialize main area
        self.mdiArea = MdiView(self)
        self.setCentralWidget(self.mdiArea)

        # customize menubar
        self.menuBar = QtWidgets.QMenuBar(self)
        self.fileMenu = QtWidgets.QMenu("&File", self)

        self.QuizGameMenuAction = QtGui.QAction('QuizGame', self.fileMenu, checkable=True)
        self.QuizGameMenuAction.toggled.connect(self.QuizGameMenuEntry)
        self.fileMenu.addAction(self.QuizGameMenuAction)
        
        self.menuBar.addMenu(self.fileMenu)
        self.setMenuBar(self.menuBar)

        self.gameMainframe = gameMainframe
        self.gameLoopTimer = QtCore.QTimer()
        self.gameLoopTimer.timeout.connect(self.gameMainframe.update)
        self.gameLoopTimer.start(100)
    
    def QuizGameMenuEntry(self):
        if(self.QuizGameMenuAction.isChecked()):
            subWindow = QuizGameWindow(self.mdiArea)
            subWindow.setObjectName('tester')
            subWindow.show()
            self.QuizGameMenuAction.setEnabled(False)
            print("checked")
        else: 
            print("not checked")
        
    def mdiSubwindowOnClose(self, sender):
        self.QuizGameMenuAction.setChecked(False)
        self.QuizGameMenuAction.setEnabled(True)
        

    def onClick(self):
        print("hey")
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.gameMainframe.save()
        print("exiting")
        return super().closeEvent(a0)


class AnkiGamificationApp(QtWidgets.QApplication):
    def __init__(self, argv: typing.List[str]) -> None:
        super().__init__(argv)
        self.config = None
        self.saveData = None
        self.loadConfig()

        self.gameMainframe = gc.GameMainframe()
        self.GUI = AnkiGamificationMainWindow(self.gameMainframe)
        self.GUI.show()

    def loadConfig(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except EnvironmentError:
            print("no config")

    def saveConfig(self):
        try:
            with open('config.json', 'r') as f:
                json.dumps(self.config, f) #untested
        except EnvironmentError:
            print("no config")



