class GameControllerBase():
    def __init__(self, gameMainframe) -> None:
        self.gameMainframe = gameMainframe

        self.model = DefaultModel()
        self.gameName = "Default"
        self.controllerName = "DefaultController"
        self.enabled = True

    def update(self) -> None:
        pass

    def load(self, savedData) -> None:
        if self.model.__dict__.keys() == savedData.keys():
            self.model.__dict__ = savedData
        else:
            raise ValueError(f"Detected corrupted save data in {self.controllerName}! \n" +
                            f"Please remove {self.controllerName} key from 'models:' in save.json")
            
    
    def getModel(self):
        if self.model is not None:
            return self.model.__dict__
        else:
            return None

class DefaultModel():
    pass