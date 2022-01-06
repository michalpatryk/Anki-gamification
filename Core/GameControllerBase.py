from collections import namedtuple
from enum import Enum, auto
import typing
class GameControllerBase():
    class UpgradeType(str, Enum):
        ACTIVE_UPGRADE = "ACTIVE_UPGRADE",
        GLOBAL_UPGRADE = "GLOBAL_UPGRADE",
        WINDOW_UPGRADE = "WINDOW_UPGRADE"

    class Upgrade():

        def __init__(self, id: int, tier: int, name: str, description: str, cost: int, type: Enum, function: typing.Callable, isUnlocked: bool, isBought: bool = False, onBoughtSuccess: typing.Callable = None, onBoughtFailure: typing.Callable = None) -> None:
            self.id = id
            self.tier = tier
            self.name = name                  # upgrade name
            self.description = description    # upgrade description
            self.isBought = isBought          # flag to check if upgrade is bought
            self.cost = cost                  # upgrade cost in shop
            self.type = type                  # upgrade type
            self.function = function          # function with an action that the upgrade does
            self.isUnlocked = isUnlocked      # flag to set whether an upgrade should show in shop or not
            self.onBoughtSuccess = onBoughtSuccess
            self.onBoughtFailure = onBoughtFailure


        def onBoughtSuccess(self):
            if self.onBoughtSuccess is not None:
                self.onBoughtSuccess()
        
        def onBoughtFailure(self):
            if self.onBoughtFailure is not None:
                self.onBoughtFailure()


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
            self.loadUpgrades()

        else:
            raise ValueError(f"Detected corrupted save data in {self.controllerName}! \n" +
                            f"Please remove {self.controllerName} key from 'models:' in save.json")
    
    def loadUpgrades(self):
        self.model.upgrades.sort(key=lambda upgrade: upgrade["tier"])
        for savedUpgrade in self.model.upgrades:
            upgradesWithCorrectId = [upgrade for upgrade in self.upgrades if upgrade.id == savedUpgrade["id"]]
            if savedUpgrade["isBought"] == True:
                upgradesWithCorrectId[-1].isBought = True
                upgradesWithCorrectId[-1].onBoughtSuccess()


    def getModel(self):
        if self.model is not None:
            self.model.upgrades = list()
            for upgrade in self.upgrades:
                self.model.upgrades.append(DefaultModel.Upgrade(upgrade.id, upgrade.tier, upgrade.name, upgrade.isBought)._asdict())
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
        id: int                     # id unique for each upgrade type in given controler
        tier: int                   # tier of the upgrade of given type
        name: str                   # upgrade name
        isBought: bool              # flag to check if upgrade is bought

    def __init__(self) -> None:
        self.upgrades = list()