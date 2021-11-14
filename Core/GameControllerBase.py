class GameControllerBase():
    def __init__(self, gameMainframe) -> None:
        self.gameMainframe = gameMainframe

        self.model = None
        self.gameName = "Default"
        self.controllerName = "DefaultController"
        self.enabled = True

    def update(self) -> None:
        pass

    def load(self):
        pass
    
    def getModel(self):
        return self.model.__dict__
