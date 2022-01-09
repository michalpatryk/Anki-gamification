import operator
from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow
from Core.GameControllerBase import GameControllerBase


class NotepadController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.gameName = "Notepad"
        self.controllerName = "NotepadController"
        self.unlockHandle = None

        self.delayedUpgrades = list()
        self.shouldBeUnlocked = False
        self.upgrades.append(GameControllerBase.Upgrade(id=0, tier=0, name="UnlockNotepad", description="Unlocks Notepad", 
                                                isBought=False, cost=10.0, type=GameControllerBase.UpgradeType.GLOBAL_UPGRADE, 
                                                function="PASS", isUnlocked=True, 
                                                onBoughtSuccess=self.unlock,
                                                onBoughtFailure=None))

        self.addSizeUpgrades()




    def attachUnlockHandle(self, unlockHandle):
        self.unlockHandle = unlockHandle
        if self.shouldBeUnlocked:
            self.unlock()
    
    def unlock(self):
        if self.unlockHandle is not None:
            self.unlockHandle()
        else:
            self.shouldBeUnlocked = True
        upgradeIdsToUnlock = (1001, 1002, 1003)
        for upgrade in self.upgrades:
            if upgrade.id in upgradeIdsToUnlock and upgrade.tier == 0:
                upgrade.isUnlocked = True
