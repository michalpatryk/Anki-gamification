from Core.GameControllerBase import GameControllerBase
# from .AnkiQuizWindow import QuizGameWindow

class QuizGameController(GameControllerBase): # contains a set of functions that are executed by said game widget
    def __init__(self) -> None:
        super().__init__()
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

class QuizGameModel():
    def __init__(self) -> None:
        self.questions = list()
        self.answers = list()

        # self.verbs = list()
        # self.nouns = list()
        # self.adjective = list()
        # self.adverb = list()

        self.someValue = 0



