from Core.GameControllerBase import GameControllerBase

class ScoreController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.gameName = "ScoreDisplay"
        self.controllerName = "ScoreDisplayController"
        self.updateScore = None

    def attachScoreUpdateHandle(self, scoreUpdateHandle):
        self.updateScore = scoreUpdateHandle

    def update(self) -> None:
        if self.updateScore is not None:
            self.updateScore(self.gameMainframe.getScore())
