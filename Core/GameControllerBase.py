from collections import namedtuple
from enum import Enum, auto
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

    def getUpgrades(self):
        pass

    # activates upgrade bought in shop
    def activateUpgrade(self):
        pass

class DefaultModel():
    class UpgradeType(Enum):
        ACTIVEUPGRADE = auto(),
        GLOBALUPGRADE = auto(),
        WINDOWUPGRADE = auto()
    # name - unique upgrade id, upgrade description, asName, cost to unlock, upgrade type, lambda with common function
    Upgrade = namedtuple("Upgrade", ['name', 'description', 'isUnlocked', 'cost', 'type', 'function'])
    def __init__(self) -> None:
        self.upgrades = list()