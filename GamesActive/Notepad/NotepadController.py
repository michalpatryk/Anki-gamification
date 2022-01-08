import operator
from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow
from Core.GameControllerBase import GameControllerBase


class NotepadController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.gameName = "Notepad"
        self.controllerName = "NotepadController"
        self.unlockHandle = None
        # self.increaseMaxSizeHandle = None

        self.delayedUpgrades = list()
        self.shouldBeUnlocked = False
        self.upgrades.append(GameControllerBase.Upgrade(id=0, tier=0, name="UnlockNotepad", description="Unlocks Notepad", 
                                                isBought=False, cost=10.0, type=GameControllerBase.UpgradeType.GLOBAL_UPGRADE, 
                                                function="PASS", isUnlocked=True, 
                                                onBoughtSuccess=self.unlock,
                                                onBoughtFailure=None))

        sizeUpgrade_1 = GameControllerBase.Upgrade(id=1, tier=0, name="1_0", description="Increase max width", 
                                                isBought=False, cost=100.0, type=GameControllerBase.UpgradeType.GLOBAL_UPGRADE, 
                                                function="PASS", isUnlocked=False, 
                                                onBoughtSuccess=lambda: self.increaseSizeUpgrade(50, 0, operator.add, sizeUpgrade_1),
                                                onBoughtFailure=None)
        self.upgrades.append(sizeUpgrade_1)
        sizeUpgrade_2 = GameControllerBase.Upgrade(id=2, tier=0, name="2_0", description="Increase max height", 
                                                isBought=False, cost=100.0, type=GameControllerBase.UpgradeType.GLOBAL_UPGRADE, 
                                                function="PASS", isUnlocked=False, 
                                                onBoughtSuccess=lambda: self.increaseSizeUpgrade(0, 50, operator.add, sizeUpgrade_2),
                                                onBoughtFailure=None)
        self.upgrades.append(sizeUpgrade_2)
        sizeUpgrade_3 = GameControllerBase.Upgrade(id=3, tier=0, name="3_0", description="Increase width and height", 
                                                isBought=False, cost=500.0, type=GameControllerBase.UpgradeType.GLOBAL_UPGRADE, 
                                                function="PASS", isUnlocked=False, 
                                                onBoughtSuccess=lambda: self.increaseSizeUpgrade(50, 50, operator.add, sizeUpgrade_3),
                                                onBoughtFailure=None)
        self.upgrades.append(sizeUpgrade_3)


    def attachUnlockHandle(self, unlockHandle):
        self.unlockHandle = unlockHandle
        if self.shouldBeUnlocked:
            self.unlock()
    
    def attachIncreaseMaxSizeHandle(self, increaseMaxSizeHandle):
        self.increaseMaxSizeHandle = increaseMaxSizeHandle

    def unlock(self):
        if self.unlockHandle is not None:
            self.unlockHandle()
        else:
            self.shouldBeUnlocked = True
        upgradeIdsToUnlock = (1, 2, 3)
        for upgrade in self.upgrades:
            if upgrade.id in upgradeIdsToUnlock and upgrade.tier == 0:
                upgrade.isUnlocked = True

