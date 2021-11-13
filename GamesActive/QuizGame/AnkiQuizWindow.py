import typing
from PyQt6 import QtCore, QtWidgets, QtGui
from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow

from .AnkiQuizGameController import QuizGameController
from .AnkiQuestionsImportWizard import ImportWizard


class QuizGameQuestionWidget(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional['QtWidgets.QWidget'] = ...) -> None:
        super().__init__(parent=parent)
        self.mainLayout = QtWidgets.QGridLayout()
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
        self.buttonA.setText("Answer A")
        
        self.buttonB = QtWidgets.QPushButton(self)
        self.buttonB.setObjectName("buttonB")
        self.buttonB.setText("AnswerB")
        
        self.buttonC = QtWidgets.QPushButton(self)
        self.buttonC.setObjectName("buttonC")
        self.buttonC.setText("AnswerC")
        
        self.buttonD = QtWidgets.QPushButton(self)
        self.buttonD.setObjectName("buttonD")
        self.buttonD.setText("AnswerD")
        
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

class QuizGameWrongAnswerWidget(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional['QtWidgets.QWidget'] = ...) -> None:
        super().__init__(parent=parent)
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
        self.labelAnswerTypeInfo.setText("Good Answer")
        self.labelAnswerTypeInfo.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")

        self.mistakeLayout.addWidget(self.labelCorrectAnswer, 1, 0, 1, 1)
        self.mistakeLayout.addWidget(self.labelUserAnwer, 0, 0, 1, 1)

        self.widgetLayout.addWidget(self.labelAnswerTypeInfo, 0, 0, 1, 1)
        self.widgetLayout.addLayout(self.mistakeLayout, 1, 0, 1, 1)
        self.widgetLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.setLayout(self.widgetLayout)

class QuizGameGoodAnswerWidget(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional['QtWidgets.QWidget'] = ...) -> None:
        super().__init__(parent=parent)
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
        self.labelAnswerTypeInfo.setText("Wrong Answer")
        self.labelAnswerTypeInfo.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")

        self.mistakeLayout.addWidget(self.labelCorrectAnswer, 1, 0, 1, 1)
        self.mistakeLayout.addWidget(self.labelUserAnwer, 0, 0, 1, 1)

        self.widgetLayout.addWidget(self.labelAnswerTypeInfo, 0, 0, 1, 1)
        self.widgetLayout.addLayout(self.mistakeLayout, 1, 0, 1, 1)
        self.widgetLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.setLayout(self.widgetLayout)


class QuizGameWindow(DefaultGameMdiSubWindow):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow, controller = None) -> None:
        super().__init__(parent=parent, flags=flags, controller=controller)
        self.menuName = "Quiz"
        self.gameName = "AnkiQuizGame"

        self.mainWidget = QuizGameQuestionWidget(self)

        self.mainWidget.setObjectName("mainWidgetLayout")

        self.wrongAnswerWidget = QuizGameWrongAnswerWidget(self)
        self.wrongAnswerWidget.hide()
        self.goodAnswerWidget = QuizGameGoodAnswerWidget(self)
        self.goodAnswerWidget.hide()


        self.setWidget(self.mainWidget)
        self.mainWidget.buttonA.clicked.connect(self.onClick)


        if len(self.controller.model.questions) == 0:
            loadQuestionsWizard = ImportWizard(self)
            # loadQuestionsWizard.done(1).connect(self.loadWizardResults)
            # print(loadQuestionsWizard.getResults)
            # self.loadQuestionsWizard.show()


        # self.controller.attachInterrupt(self)

    def onClick(self):
        self.mainWidget.hide()
        self.setWidget(self.wrongAnswerWidget)
        self.wrongAnswerWidget.show()
        print("widget2")

    def loadWizardResults(self, questionsAndAnswers):
        self.controller.model.questions = questionsAndAnswers[0]
        self.controller.model.answers = questionsAndAnswers[1]
        print(5)
        

