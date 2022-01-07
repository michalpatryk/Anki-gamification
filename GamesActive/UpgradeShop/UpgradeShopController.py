from Core.GameControllerBase import GameControllerBase
import copy
class UpgradeShopController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.gameName = "UpgradeShop"
        self.controllerName = "UpgradeShopController"

    def getAvaliableUpgrades(self) -> list:
        upgrades = self.gameMainframe.getAllUpgrades()
        avaliableUpgrades = list()
        for game in upgrades:
            avaliableUpgrades.append({'gameName': game['gameName'], 'upgrades': list()})
            for upgrade in game['upgrades']:
                if upgrade.isUnlocked:
                    avaliableUpgrades[-1]['upgrades'].append(upgrade)
    
        return avaliableUpgrades

    def canBuyUpgrade(self, upgrade) -> bool:
        return self.gameMainframe.canBuyUpgrade(upgrade.cost)

    def buyUpgrade(self, upgrade):
        if self.gameMainframe.buyUpgrade(upgrade):
            upgrade.onBoughtSuccess()
            return True
        else:
            return False

# add some function here to make note to the mainframe controller that a new element is unlocked
