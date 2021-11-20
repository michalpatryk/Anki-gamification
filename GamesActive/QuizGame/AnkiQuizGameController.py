import random
from Core.GameControllerBase import GameControllerBase
# from .AnkiQuizWindow import QuizGameWindow


# contains a set of functions that are executed by said game widget
class QuizGameController(GameControllerBase):
    def __init__(self, gameMainframe) -> None:
        super().__init__(gameMainframe)
        self.model = QuizGameModel()
        self.gameName = "AnkiQuizGame"
        self.controllerName = "AnkiQuizGameController"
        self.view = None

    # if needed, you can attach interrupt and modify your view
    # def attachInterrupt(self, widget : QuizGameWindow):
    #     self.view = widget

    def update(self):
        self.model.someValue += 1

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
        self.gameMainframe.activeAction(5)


class QuizGameModel():
    def __init__(self) -> None:
        # might want to change that in the future - it is too dependent on the ordering
        self.questions = list()
        self.answers = list()

        # self.verbs = list()
        # self.nouns = list()
        # self.adjective = list()
        # self.adverb = list()

        self.someValue = 0
