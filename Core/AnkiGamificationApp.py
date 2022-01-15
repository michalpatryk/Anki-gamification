
import typing
import json
from PyQt6 import QtWidgets
from .AnkiGamificationMainWindow import AnkiGamificationMainWindow
from .GameMainframe import GameMainframe


class AnkiGamificationApp(QtWidgets.QApplication):
    def __init__(self, argv: typing.List[str]) -> None:
        super().__init__(argv)
        self.config = None
        self.saveData = None
        self.loadConfig()

        self.gameMainframe = GameMainframe()
        self.gameMainframe.load()
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
                json.dumps(self.config, f)  
        except EnvironmentError:
            print("no config")
