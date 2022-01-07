from collections import namedtuple
from enum import Enum, auto
import typing
class GameControllerBase():
    class UpgradeType(str, Enum):
        ACTIVE_UPGRADE = "ACTIVE_UPGRADE",
        GLOBAL_UPGRADE = "GLOBAL_UPGRADE",
        WINDOW_UPGRADE = "WINDOW_UPGRADE"

    class Upgrade():

        def __init__(self, id: int, tier: int, name: str, description: str, cost: int, type: Enum, function: str, isUnlocked: bool, isBought: bool = False, onBoughtSuccess: typing.Callable = None, onBoughtFailure: typing.Callable = None) -> None:
            self.id = id
            self.tier = tier
            self.name = name                  # upgrade name
            self.description = description    # upgrade description
            self.isBought = isBought          # flag to check if upgrade is bought
            self.cost = cost                  # upgrade cost in shop
            self.type = type                  # upgrade type
            self.function = function          # function with an action that the upgrade does
            self.isUnlocked = isUnlocked      # flag to set whether an upgrade should show in shop or not
            self.onBoughtSuccessHandle = onBoughtSuccess
            self.onBoughtFailureHandle = onBoughtFailure

        def onBoughtSuccess(self):
            if self.onBoughtSuccessHandle is not None:
                self.onBoughtSuccessHandle()
        
        def onBoughtFailure(self):
            if self.onBoughtFailureHandle is not None:
                self.onBoughtFailureHandle()

        def calculateMultiplier(baseValue, upgrades):
            #ex "ADD 1" "ADD 2" "ADD 3"
            # "MULTIPLY 2" "MULTIPLY 2"
            # "POWER 1.15" "POWER 1.1"
            # "ADD 1; MULTIPLY 1"
            #in essence: a string with pairs

            upgradePairs = [upgrade.function.split(";") for upgrade in upgrades if upgrade.isBought == True]
            additions = list()
            multipliers = list()
            powers = list()
            for upgradeStack in upgradePairs:
                for upgrade in upgradeStack:
                    upgradeData = upgrade.split(" ")
                    upgradeData[0] = upgradeData[0].upper()
                    if upgradeData[0] == "ADD":
                        additions.append(float(upgradeData[1]))
                    elif upgradeData[0] == "MULTIPLY":
                        multipliers.append(float(upgradeData[1]))
                    elif upgradeData[0] == "POWER":
                        powers.append(float(upgradeData[1]))
            value = baseValue + sum(additions)
            for multiplier in multipliers:
                value *= multiplier
            for power in powers:
                value ** power
            return value


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