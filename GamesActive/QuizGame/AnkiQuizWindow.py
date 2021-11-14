import typing
import random
from PyQt6 import QtCore, QtWidgets, QtGui
from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow

from .AnkiQuizGameController import QuizGameController
from .AnkiQuestionsImportWizard import ImportWizard


class NoQuestionsLoadedWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, startWizardHandle) -> None:
        super().__init__(parent=parent)
        self.startWizardHandle = startWizardHandle
        self.setObjectName("AnkiQuizGameViewNoQuestionsLoaded")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.loadQuestionsLabel = QtWidgets.QLabel(self)
        self.loadQuestionsLabel.setWordWrap(True)
        self.loadQuestionsLabel.setObjectName("loadQuestionsLabel")
        self.gridLayout.addWidget(self.loadQuestionsLabel, 0, 0, 1, 1)
        self.startWizardButton = QtWidgets.QPushButton(self)
        self.startWizardButton.setObjectName("startWizardButton")
        self.gridLayout.addWidget(self.startWizardButton, 1, 0, 1, 1)
        # self.setLayout(self.gridLayout)

        self.loadQuestionsLabel.setText(
            "<html><head/><body><p>There are no anki cards loaded! Please click &quot;Load questions&quot; to load your Anki cards in order to use this game. <span style=\" font-weight:600;\">Your cards and ordering will not be changed in any way.</span> Nonetheless, it is advisable to backup your data.</p></body></html>")
        self.startWizardButton.setText("Load questions")

        self.startWizardButton.clicked.connect(self.loadQuestionsOnClick)

    def loadQuestionsOnClick(self):
        self.startWizardHandle()
        # ImportWizard(self.parent().parent(), self.parent().parent().loadWizardResults)


class QuizGameQuestionWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, correctAnswerHandle, wrongAnswerHandle) -> None:
        super().__init__(parent=parent)
        self.correctAnswerHandle = correctAnswerHandle
        self.wrongAnswerHandle = wrongAnswerHandle
        self.setObjectName("AnkiQuizGameViewQuesiton")
        self.mainLayout = QtWidgets.QGridLayout(self)
        self.mainLayout.setObjectName("mainLayout")

        self.labelA = QtWidgets.QLabel(self)
        self.labelA.setObjectName("labelA")
        self.labelA.setText("labelA")

        self.labelB = QtWidgets.QLabel(self)
        self.labelB.setObjectName("labelB")
        self.labelB.setText("labelB")

        self.labelC = QtWidgets.QLabel(self)
        self.labelC.setObjectName("labelC")
        self.labelC.setText("labelC")

        self.labelD = QtWidgets.QLabel(self)
        self.labelD.setObjectName("labelD")
        self.labelD.setText("labelD")

        self.labelQuestion = QtWidgets.QLabel(self)
        self.labelQuestion.setObjectName("labelQuestion")
        self.labelQuestion.setText("Question")

        self.buttonA = QtWidgets.QPushButton(self)
        self.buttonA.setObjectName("buttonA")
        self.buttonA.setText("A")

        self.buttonB = QtWidgets.QPushButton(self)
        self.buttonB.setObjectName("buttonB")
        self.buttonB.setText("B")

        self.buttonC = QtWidgets.QPushButton(self)
        self.buttonC.setObjectName("buttonC")
        self.buttonC.setText("C")

        self.buttonD = QtWidgets.QPushButton(self)
        self.buttonD.setObjectName("buttonD")
        self.buttonD.setText("D")

        self.mainLayout.addWidget(self.labelA, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.labelB, 2, 0, 1, 1)
        self.mainLayout.addWidget(self.labelC, 3, 0, 1, 1)
        self.mainLayout.addWidget(self.labelD, 4, 0, 1, 1)
        self.mainLayout.addWidget(self.labelQuestion, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.buttonA, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.buttonB, 2, 1, 1, 1)
        self.mainLayout.addWidget(self.buttonC, 3, 1, 1, 1)
        self.mainLayout.addWidget(self.buttonD, 4, 1, 1, 1)
        self.mainLayout.setColumnStretch(0, 2)
        self.setLayout(self.mainLayout)

    def setNewLabels(self, quizSet: dict) -> None:
        labelMap = {0: (self.labelA, self.buttonA),
                    1: (self.labelB, self.buttonB),
                    2: (self.labelC, self.buttonC),
                    3: (self.labelD, self.buttonD)}

        self.labelQuestion.setText("Question: \n" + quizSet['question'])
        selector = list(range(4))
        selectedPosition = random.choice(selector)
        selector.remove(selectedPosition)
        label, button = labelMap[selectedPosition]
        label.setText(quizSet['correctAnswer'])
        button.clicked.connect(self.correctAnswerHandle)

        for i in selector:
            label, button = labelMap[i]
            label.setText(quizSet['wrongAnswers'].pop())
            button.clicked.connect(self.wrongAnswerHandle)


class QuizGameWrongAnswerWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, nextQuestionHandle) -> None:
        super().__init__(parent=parent)
        self.setObjectName("AnkiQuizGameViewWrongAnswer")
        self.widgetLayout = QtWidgets.QGridLayout(self)
        self.widgetLayout.setObjectName("widgetLayout")

        self.mistakeLayout = QtWidgets.QGridLayout()
        self.mistakeLayout.setObjectName("mistakeLayout")

        self.labelCorrectAnswer = QtWidgets.QLabel(self)
        self.labelCorrectAnswer.setObjectName("labelCorrectAnswer")
        self.labelCorrectAnswer.setText("CorrectAnswer")

        self.labelUserAnwer = QtWidgets.QLabel(self)
        self.labelUserAnwer.setObjectName("labelUserAnwer")
        self.labelUserAnwer.setText("UserAnswer")

        self.labelAnswerTypeInfo = QtWidgets.QLabel(self)
        self.labelAnswerTypeInfo.setObjectName('labelAnswerTypeInfo')
        self.labelAnswerTypeInfo.setText("Wrong Answer!")
        self.labelAnswerTypeInfo.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Continue")

        self.mistakeLayout.addWidget(self.labelCorrectAnswer, 1, 0, 1, 1)
        self.mistakeLayout.addWidget(self.labelUserAnwer, 0, 0, 1, 1)

        self.widgetLayout.addWidget(self.labelAnswerTypeInfo, 0, 0, 1, 1)
        self.widgetLayout.addLayout(self.mistakeLayout, 1, 0, 1, 1)
        self.widgetLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.setLayout(self.widgetLayout)

        self.pushButton.clicked.connect(nextQuestionHandle)


class QuizGameGoodAnswerWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, nextQuestionHandle) -> None:
        super().__init__(parent=parent)
        self.setObjectName("AnkiQuizGameViewGoodAnswer")
        self.widgetLayout = QtWidgets.QGridLayout(self)
        self.widgetLayout.setObjectName("widgetLayout")

        self.mistakeLayout = QtWidgets.QGridLayout()
        self.mistakeLayout.setObjectName("mistakeLayout")

        self.labelCorrectAnswer = QtWidgets.QLabel(self)
        self.labelCorrectAnswer.setObjectName("labelCorrectAnswer")
        self.labelCorrectAnswer.setText("CorrectAnswer")

        self.labelUserAnwer = QtWidgets.QLabel(self)
        self.labelUserAnwer.setObjectName("labelUserAnwer")
        self.labelUserAnwer.setText("UserAnswer")

        self.labelAnswerTypeInfo = QtWidgets.QLabel(self)
        self.labelAnswerTypeInfo.setObjectName('labelAnswerTypeInfo')
        self.labelAnswerTypeInfo.setText("Good Answer!")
        self.labelAnswerTypeInfo.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Continue")

        self.mistakeLayout.addWidget(self.labelCorrectAnswer, 1, 0, 1, 1)
        self.mistakeLayout.addWidget(self.labelUserAnwer, 0, 0, 1, 1)

        self.widgetLayout.addWidget(self.labelAnswerTypeInfo, 0, 0, 1, 1)
        self.widgetLayout.addLayout(self.mistakeLayout, 1, 0, 1, 1)
        self.widgetLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.setLayout(self.widgetLayout)

        self.pushButton.clicked.connect(nextQuestionHandle)


class QuizGameWindow(DefaultGameMdiSubWindow):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow, controller=None) -> None:
        super().__init__(parent=parent, flags=flags, controller=controller)
        self.menuName = "Quiz"
        self.gameName = "AnkiQuizGame"
        self.setObjectName = "QuizGameWindow"
        # self.views = list()

        self.questionsWidget = QuizGameQuestionWidget(
            self, self.correctAnswer, self.wrongAnswer)
        # self.mainWidget.show()
        # self.mainWidget.hide()
        self.wrongAnswerWidget = QuizGameWrongAnswerWidget(
            self, self.nextQuestion)
        # self.wrongAnswerWidget.hide()
        self.goodAnswerWidget = QuizGameGoodAnswerWidget(
            self, self.nextQuestion)
        # self.goodAnswerWidget.hide()
        self.noQuestionsLoadedWidget = NoQuestionsLoadedWidget(
            self, self.startWizard)
        # self.noQuestionsLoadedWidget.hide()
        self.views = QtWidgets.QStackedWidget(self)
        self.views.addWidget(self.questionsWidget)
        self.views.addWidget(self.wrongAnswerWidget)
        self.views.addWidget(self.goodAnswerWidget)
        self.views.addWidget(self.noQuestionsLoadedWidget)

        self.setWidget(self.views)
        # self.setWidget(self.mainWidget)
        # self.mainWidget.buttonA.clicked.connect(self.onClick)

        # self.goodAnswerWidget.show()
        if len(self.controller.model.questions) == 0:
            self.views.setCurrentWidget(self.noQuestionsLoadedWidget)
            # self.startWizard()
            # self.setWidget(self.noQuestionsLoadedWidget)
            # loadQuestionsWizard = ImportWizard(self)
        else:
            self.loadNewQuizSet()
        # self.controller.attachInterrupt(self)

    def onClick(self):
        # self.mainWidget.hide()
        # self.setWidget(self.wrongAnswerWidget)
        # self.wrongAnswerWidget.show()
        print("widget2")

    def startWizard(self):
        ImportWizard(self, self.loadWizardResults)

    def loadWizardResults(self, questionsAndAnswers):
        self.controller.populateQuestionsAndAnswers(
            questionsAndAnswers[0], questionsAndAnswers[1])
        if len(self.controller.model.questions) == 0:
            self.views.setCurrentWidget(self.noQuestionsLoadedWidget)
        else:
            self.loadNewQuizSet()
            self.views.setCurrentWidget(self.questionsWidget)

    def loadNewQuizSet(self):
        self.questionsWidget.setNewLabels(self.controller.getQuizSet())

    def correctAnswer(self):
        self.views.setCurrentWidget(self.goodAnswerWidget)
        print('correct')

    def wrongAnswer(self):
        self.views.setCurrentWidget(self.wrongAnswerWidget)
        print("wrong")

    def nextQuestion(self):
        self.loadNewQuizSet()
        self.views.setCurrentWidget(self.questionsWidget)
        print('next question')
