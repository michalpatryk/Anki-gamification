import random
import operator
from Core.GameControllerBase import GameControllerBase, DefaultModel
# from .AnkiQuizWindow import QuizGameWindow


# contains a set of functions that are executed by said game widget
class QuizGameController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.model = QuizGameModel()
        self.gameName = "AnkiQuizGame"
        self.controllerName = "AnkiQuizGameController"
        self.view = None

        self.upgrades.append(GameControllerBase.Upgrade(id=0, tier=0, name="RewardMultiplier", description="Answer reward multiplier", 
                                                        isBought=False, cost=5.0, type=GameControllerBase.UpgradeType.ACTIVE_UPGRADE, 
                                                        function="MULTIPLY 2", isUnlocked=True, 
                                                        onBoughtSuccess=self.generateNewMultiplierReward,
                                                        onBoughtFailure=None))
        self.upgrades.append(GameControllerBase.Upgrade(id=1, tier=0, name="RewardMultiplier", description="Answer reward bonus", 
                                                        isBought=False, cost=1.0, type=GameControllerBase.UpgradeType.ACTIVE_UPGRADE, 
                                                        function="MULTIPLY 1.2; ADD 1", isUnlocked=True, 
                                                        onBoughtSuccess=None,
                                                        onBoughtFailure=None))


    def appendQuestionAndAnswer(self, question, answer):
        self.model.questions.append(question)
        self.model.answers.append(answer)

    def populateQuestionsAndAnswers(self, questions, answers):
        self.model.questions = questions
        self.model.answers = answers

    def getRandomQuestion(self):
        return random.choice(self.model.questions)

    def getRandomAnswer(self):
        return random.choice(self.model.answers)

    def getQuizSet(self):
        quizSet = dict()
        answers = list()

        pos = random.randrange(0, len(self.model.answers))
        quizSet['question'] = self.model.questions[pos]
        quizSet['correctAnswer'] = self.model.answers[pos]
        for i in range(3):
            answers.append(self.getRandomAnswer())
        quizSet['wrongAnswers'] = answers
        return quizSet

    def goodAnswer(self):
        baseReward = 5
        activeUpgrades = [upgrade for upgrade in self.upgrades if upgrade.type == GameControllerBase.UpgradeType.ACTIVE_UPGRADE]
        baseReward = GameControllerBase.Upgrade.calculateMultiplier(baseReward, activeUpgrades)
        self.gameMainframe.activeAction(baseReward)

    def generateNewMultiplierReward(self):
        lastUpgrade = self.upgrades[-1]
        self.upgrades.append(GameControllerBase.Upgrade(id=0,
                                                        tier=lastUpgrade.tier + 1, 
                                                        name="RewardMultiplier_{}".format(lastUpgrade.tier + 1), 
                                                        description="Answer reward multiplier", 
                                                        isBought=False, 
                                                        cost=lastUpgrade.cost * 2.2, 
                                                        type=GameControllerBase.UpgradeType.ACTIVE_UPGRADE, 
                                                        function="MULTIPLY 2", 
                                                        isUnlocked=True, 
                                                        onBoughtSuccess=self.generateNewMultiplierReward,
                                                        onBoughtFailure=None))


class QuizGameModel(DefaultModel):
    def __init__(self) -> None:
        super().__init__()
        # might want to change that in the future - it is too dependent on the ordering
        self.questions = list()
        self.answers = list()

        # self.verbs = list()
        # self.nouns = list()
        # self.adjective = list()
        # self.adverb = list()

        self.someValue = 0
        