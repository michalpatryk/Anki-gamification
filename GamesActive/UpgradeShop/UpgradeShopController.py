from Core.GameControllerBase import GameControllerBase
import copy
class UpgradeShopController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.gameName = "UpgradeShop"
        self.controllerName = "UpgradeShopController"

    def getAvaliableUpgrades(self):
        upgrades = self.gameMainframe.getAllUpgrades()
        avaliableUpgrades = list()
        for game in upgrades:
            avaliableUpgrades.append({'gameName': game['gameName'], 'upgrades': list()})
            for upgrade in game['upgrades']:
                if upgrade.isUnlocked:
                    avaliableUpgrades[-1]['upgrades'].append(copy.copy(upgrade))
    
        return avaliableUpgrades
