import json
import pickle
class GameMainframe():
    def __init__(self) -> None:
        self.ankiFile = None
        self.score = 0
        self.multipliers = list()
        self.games = list() 

        self.load()
        # list of all the game controller
        # self.games = list() 
        # self.games.append(QuizGameController())
        # self.games.append(QuizGameController())


    def update(self): # update all the games here
        # self.score += 1 
        for game in self.games:
            game.update()

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


class GameControllerBase():
    def __init__(self) -> None:
        self.model = None

    def update(self) -> None:
        pass

    def load(self):
        pass
    
    def getModel(self):
        return self.model.__dict__

     

class QuizGameController(GameControllerBase): # contains a set of functions that are executed by said game widget
    def __init__(self) -> None:
        self.model = QuizGameModel()

    def update(self):
        self.model.someValue += 1

    

class QuizGameModel():
    def __init__(self) -> None:
        self.componentName = 'QuizGame'
        self.someValue = 0



