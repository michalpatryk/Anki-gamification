from collections import namedtuple
from enum import Enum, auto
import typing
class GameControllerBase():
    class UpgradeType(str, Enum):
        ACTIVEUPGRADE = "ACTIVEUPGRADE",
        GLOBALUPGRADE = "GLOBALUPGRADE",
        WINDOWUPGRADE = "WINDOWUPGRADE"

    class Upgrade(typing.NamedTuple):
        id: int
        name: str                   # upgrade name
        description: str            # upgrade description
        isBought: bool              # flag to check if upgrade is bought
        cost: int                   # upgrade cost in shop
        type: Enum                  # upgrade type
        function: typing.Callable   # function with an action that the upgrade does
        isUnlocked: bool = False     # flag to set whether an upgrade should show in shop or not


    def __init__(self, gameMainframe) -> None:
        self.gameMainframe = gameMainframe

        self.model = DefaultModel()
        self.gameName = "Default"
        self.controllerName = "DefaultController"
        self.enabled = True
        self.upgrades = list()

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
            self.model.upgrades = list()
            for upgrade in self.upgrades:
                self.model.upgrades.append(DefaultModel.Upgrade(upgrade.name, upgrade.isBought)._asdict())
            return self.model.__dict__
        else:
            return None

    def getUpgrades(self):
        return {'gameName': self.gameName, 'upgrades': self.upgrades}

    # activates upgrade bought in shop
    def activateUpgrade(self):
        pass

class DefaultModel():
    class Upgrade(typing.NamedTuple):
        name: str                   # unique upgrade id
        isBought: bool              # flag to check if upgrade is bought

    def __init__(self) -> None:
        self.upgrades = list()