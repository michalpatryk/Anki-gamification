import json
import pickle
from GamesActive.QuizGame.AnkiQuizGameController import QuizGameController, QuizGameModel


class GameMainframe():
    def __init__(self) -> None:
        self.ankiFile = None
        self.score = 0
        self.multipliers = list()
        self.games = dict()

        # self.load()
        # list of all the game controllers
        # self.games = list()

        # self.games.append(QuizGameController())
        if not any(type(game) is QuizGameController for game in self.games.values()):
            quizGameController = QuizGameController(self.activeAction)
            self.games[quizGameController.controllerName] = quizGameController

    def update(self):  # update all the games here
        # self.score += 1
        for game in self.games.values():
            game.update()

    def activeAction(self):
        self.score += 1
        print(self.score)

    def load(self):
        # leaving this if I ever want to go into full transparency - too much work in this proof of concept
        # try:
        #     with open('save.json', 'r') as f:
        #         saveData = json.load(f)
        #         print(saveData)
        # except EnvironmentError:
        #     print("no saves")
        try:
            with open('save.json', 'rb') as f:
                self.games, self.score = pickle.load(f)
        except EnvironmentError:
            print("no saves")

    def save(self):
        # try:
        #     with open('save.json', 'w') as f:
        #         gamesJson = [game.getModel() for game in self.games]
        #         json.dump(gamesJson, f, sort_keys=True, indent=4)
        # except EnvironmentError:
        #     print(EnvironmentError)

        try:
            with open('save.json', 'wb') as f:
                # gamesJson = [game.getModel() for game in self.games]
                saveData = self.games, self.score
                pickle.dump(saveData, f)
        except EnvironmentError:
            print(EnvironmentError)
