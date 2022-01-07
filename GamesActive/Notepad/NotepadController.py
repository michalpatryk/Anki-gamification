from Core.GameControllerBase import GameControllerBase


class NotepadController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.gameName = "Notepad"
        self.controllerName = "NotepadController"
        self.unlockHandle = None
        self.upgrades.append(GameControllerBase.Upgrade(id=0, tier=0, name="UnlockNotepad", description="Unlocks Notepad", 
                                                isBought=False, cost=10.0, type=GameControllerBase.UpgradeType.GLOBAL_UPGRADE, 
                                                function="PASS", isUnlocked=True, 
                                                onBoughtSuccess=self.unlock,
                                                onBoughtFailure=None))

    def attachUnlockHandle(self, unlockHandle):
        self.unlockHandle = unlockHandle

    def unlock(self):
        self.unlockHandle()
