import json
import time
import pickle
from GamesActive.QuizGame.AnkiQuizGameController import QuizGameController


class GameMainframe():
    def __init__(self) -> None:
        self.ankiFile = None
        self.score = 0
        self.multipliers = list()
        self.games = dict()
        self.lastAutosave = time.time()

        # QuizGame should always be active
        if not any(type(game) is QuizGameController for game in self.games.values()):
            quizGameController = QuizGameController(self)
            self.games[quizGameController.controllerName] = quizGameController

    def update(self):  # update all the games here
        self.score += 1
        for game in self.games.values():
            game.update()
        if time.time() - self.lastAutosave > 60 * 10:
            self.lastAutosave = time.time()
            self.save()


    def activeAction(self, weight):
        self.score += weight
        print(self.score)

    def load(self):
        try:
            with open('save.json', 'r') as f:
                gameSaveData = json.load(f)
                self.games = gameSaveData["models"]
                self.score = gameSaveData["score"]    
        except EnvironmentError:
            print("no saves")

    def save(self):
        try:
            with open('save.json', 'w') as f:
                gameSaveData = dict()
                gameSaveData["models"] = dict()
                for game in self.games.items():
                    gameSaveData["models"][game[0]] = game[1].getModel()
                gameSaveData["score"] = self.score
                
                json.dump(gameSaveData, f, indent=4)
        except EnvironmentError:
            print(EnvironmentError)
                        

    def addGame(self, controller: type):
        if not any(controller is type(game) for game in self.games.values()):
            initializedController = controller(self)
            if initializedController.controllerName in self.games:
                initializedController.load(self.games[initializedController.controllerName])      
            self.games[initializedController.controllerName] = initializedController
            return initializedController
        else:
            return None

    def getGameByControllerType(self, controller: type):
        return [game for game in self.games.values() if type(game) == controller][0]

    def getScore(self):
        return self.score

    def increaseScore(self, value):
        self.score += value

    def decreaseScore(self, value):
        self.score -= value

    # Multiplier as a pair of value and operator? Or a lambda?
    def addGlobalMultiplier(self, multiplier):
        pass

    def getAllUpgrades(self):
        upgrades = list()
        for game in self.games.values():
            upgrades.append(game.getUpgrades())
        return upgrades