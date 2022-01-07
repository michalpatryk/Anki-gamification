from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow
from PyQt6 import QtCore, QtWidgets
from numbers import Number
import typing


class ScoreWidget(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional['QtWidgets.QWidget'] = ...) -> None:
        super().__init__(parent=parent)
        self.setObjectName("ScoreWidget")

        self.basicLabelText = "<html><head/><body><p><span style=\" font-size:{size}pt;\">{score}</span></p></body></html>"
        self.labelSize = 18
        self.score = 0

        self.scoreValueLabel = QtWidgets.QLabel(self)
        self.scoreValueLabel.setWordWrap(True)
        self.scoreValueLabel.setObjectName("scoreValueLabel")
        self.scoreValueLabel.setText(self.basicLabelText.format(size=self.labelSize, score=self.score))

        self.scoreInformationLabel = QtWidgets.QLabel(self)
        self.scoreInformationLabel.setText("Current score:")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scoreInformationLabel.sizePolicy().hasHeightForWidth())

        self.scoreInformationLabel.setSizePolicy(sizePolicy)
        self.scoreInformationLabel.setObjectName("scoreInformationLabel")

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.scoreValueLabel, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.scoreInformationLabel, 0, 0, 1, 1)

    def updateScoreValue(self, score: Number):
        self.score = score

        displayedScore = "{:.5}".format(score)
        self.scoreValueLabel.setText(self.basicLabelText.format(size=self.labelSize, score=displayedScore))


class ScoreWindow(DefaultGameMdiSubWindow):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow, controller=None) -> None:
        super().__init__(parent=parent, flags=flags, controller=controller)
        self.resize(250, 125)
        self.menuName = "Score"
        self.isUnlocked = True
        self.shouldStartVisible = False
        self.gameName = "ScoreDisplay"
        self.setWindowTitle(self.menuName)


        self.scoreWidget = ScoreWidget(self)
        self.setWidget(self.scoreWidget)
        self.controller.attachScoreUpdateHandle(self.updateScoreValue)

    def updateScoreValue(self, score):
        self.scoreWidget.updateScoreValue(score)
