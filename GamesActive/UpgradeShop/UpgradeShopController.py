from Core.GameControllerBase import GameControllerBase

class UpgradeShopController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.gameName = "UpgradeShop"
        self.controllerName = "UpgradeShopController"

