from pathlib import Path
import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from Core.AnkiLoad import AnkiNotesLoader


class ImportWizard(QtWidgets.QWizard):
    def __init__(self, parent, finishHandle: QtWidgets.QWidget, flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.Dialog) -> None:
        super().__init__(parent=parent, flags=flags)
        self.finishHandle = finishHandle
        self.setFixedSize(640, 480)
        self.addPage(LoadCollectionPage(self))
        self.addPage(LoadDeckPage(self))
        self.addPage(SelectFieldsPage(self))

        self.resize(640, 480)
        self.setWindowTitle("Anki collection importer")
        self.ankiNotesLoader = None  # type: AnkiNotesLoader
        self.button(QtWidgets.QWizard.WizardButton.FinishButton).clicked.connect(
            self.onFinish)
        self.show()

    def onFinish(self):
        self.finishHandle(self.ankiNotesLoader.getAnswersAndQuestions())
        # finisher = self.parent()
        # while finisher.objectName != "QuizGameWindow":
        #     finisher = finisher.parent()
        # finisher.loadWizardResults(self.ankiNotesLoader.getAnswersAndQuestions())


class ImportWizardPage(QtWidgets.QWizardPage):
    def wizard(self) -> ImportWizard:
        return super().wizard()


class LoadCollectionPage(ImportWizardPage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.loadCollectionLayout = QtWidgets.QGridLayout(self)
        self.loadCollectionLayout.setObjectName("loadCollectionLayout")
        self.selectCollectionInfoLabel = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.selectCollectionInfoLabel.sizePolicy().hasHeightForWidth())
        self.selectCollectionInfoLabel.setSizePolicy(sizePolicy)
        self.selectCollectionInfoLabel.setObjectName(
            "selectCollectionInfoLabel")
        self.loadCollectionLayout.addWidget(
            self.selectCollectionInfoLabel, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.loadCollectionLayout.addWidget(self.lineEdit, 4, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.loadCollectionLayout.addWidget(self.pushButton, 4, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setObjectName("checkBox")
        self.loadCollectionLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading |
                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.label.setText("<html><head/><body><p>There are no Anki flashcards loaded. Please select a collection.anki2 file. Selected file will be read only, but it is nonetheless advised to use a copy instead of your main file. File locaiton is explained at <a href=\"https://docs.ankiweb.net/files.html\"><span style=\" text-decoration: underline; color:#0000ff;\">https://docs.ankiweb.net/files.html</span></a></p></body></html>")
        self.selectCollectionInfoLabel.setText("Select collection file:")
        self.pushButton.setText("...")
        self.checkBox.setText("I understand the risks")

        self.loadCollectionLayout.addWidget(self.label, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.loadCollectionLayout.addItem(spacerItem, 2, 0, 1, 1)

        self.pushButton.clicked.connect(self.onSelectFile)
        self.lineEdit.textChanged.connect(self.onLineEditEdited)
        self.checkBox.clicked.connect(self.completeChanged)

        self.fname = '.\\Anki_data'
        self.lineEdit.setText(self.fname)
        self.registerField("collectionFile", self.lineEdit)

        self.checkBox.setChecked(True)

    def onSelectFile(self):
        fname, extension = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                                                 self.fname, "Collection files (*.anki2);; All files (*.*)")
        if fname:
            self.fname = fname
            self.lineEdit.setText(self.fname)
            self.completeChanged.emit()

    def onLineEditEdited(self, text):
        self.fname = text
        self.completeChanged.emit()

    def isComplete(self) -> bool:
        return Path(self.fname).is_file() and self.checkBox.isChecked()


class LoadDeckPage(ImportWizardPage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self.loadDeckLayout = QtWidgets.QGridLayout(self)
        self.loadDeckLayout.setObjectName("loadDeckLayout")
        self.decksView = QtWidgets.QTreeWidget(self)
        self.decksView.setObjectName("decksView")
        self.loadDeckLayout.addWidget(self.decksView, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.loadDeckLayout.addWidget(self.label, 0, 0, 1, 1)

        self.decksView.setHeaderItem(QtWidgets.QTreeWidgetItem(
            ["Deck names", "Cards count", "Selected"]))
        self.decksView.header().setStretchLastSection(False)
        self.decksView.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.decksView.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.decksView.header().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.label.setText("Select deck:")
        self.decksView.itemClicked.connect(self.updateSelectedDecks)
        self.decksView.itemDoubleClicked.connect(self.deckClicked)
        self.decksView.checkLocation = 2

    def initializePage(self) -> None:
        def recursiveAdd(parent: QtWidgets.QTreeWidgetItem, value):
            if type(value) == int:
                parent.setCheckState(
                    self.decksView.checkLocation, QtCore.Qt.CheckState.Unchecked)
                parent.setData(1, QtCore.Qt.ItemDataRole.DisplayRole, value)
            else:
                for subdeck in value.items():
                    child = QtWidgets.QTreeWidgetItem([subdeck[0]])
                    parent.addChild(child)
                    parent.setExpanded(True)
                    # parent.setFlags(parent.flags() & ~QtCore.Qt.ItemFlag.ItemIsCl)
                    recursiveAdd(child, subdeck[1])

        self.wizard().ankiNotesLoader = AnkiNotesLoader(self.field("collectionFile"))
        self.wizard().ankiNotesLoader.loadDecks()
        self.decksView.clear()

        treeDeck = self.wizard().ankiNotesLoader.getDeckTree()

        for deck in treeDeck.items():
            item = QtWidgets.QTreeWidgetItem(self.decksView, [deck[0]])
            recursiveAdd(item, deck[1])

        return super().initializePage()

    def deckClicked(self, item: QtWidgets.QTreeWidgetItem):
        checkState = item.checkState(self.decksView.checkLocation)
        if item.childCount() == 0:
            if checkState == QtCore.Qt.CheckState.Unchecked:
                item.setCheckState(self.decksView.checkLocation,
                                   QtCore.Qt.CheckState.Checked)
            else:
                item.setCheckState(self.decksView.checkLocation,
                                   QtCore.Qt.CheckState.Unchecked)
        self.updateSelectedDecks()

    def updateSelectedDecks(self):
        # self.decksView.findItems(
        #     "", QtCore.Qt.MatchFlag.MatchContains | QtCore.Qt.MatchFlag.MatchRecursive)

        selectedDecks = list()
        for deck in self.decksView.findItems("", QtCore.Qt.MatchFlag.MatchContains | QtCore.Qt.MatchFlag.MatchRecursive):
            if deck.checkState(self.decksView.checkLocation) == QtCore.Qt.CheckState.Checked:
                deckFullName = ''
                separator = "\x1f"
                while deck is not None:
                    deckFullName = deck.text(0) + separator + deckFullName
                    deck = deck.parent()
                deckFullName = deckFullName[:-len(separator)]
                selectedDecks.append(deckFullName)

        self.wizard().ankiNotesLoader.clearSelectedDecks()
        if len(selectedDecks) > 0:
            self.wizard().ankiNotesLoader.selectDecks(selectedDecks)
        self.completeChanged.emit()

    def isComplete(self) -> bool:
        if self.wizard().ankiNotesLoader.selectedDecks:
            return True
        else:
            return False


class SelectFieldsPage(ImportWizardPage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.questionLabel = QtWidgets.QLabel(self)
        self.questionLabel.setObjectName("questionLabel")
        self.gridLayout.addWidget(self.questionLabel, 1, 0, 1, 1)
        self.answerLabel = QtWidgets.QLabel(self)
        self.answerLabel.setObjectName("answerLabel")
        self.gridLayout.addWidget(self.answerLabel, 3, 0, 1, 1)
        self.informationLabel = QtWidgets.QLabel(self)
        self.informationLabel.setObjectName("informationLabel")
        self.gridLayout.addWidget(self.informationLabel, 0, 0, 1, 1)
        self.questionTreeWidget = QtWidgets.QTreeWidget(self)
        self.questionTreeWidget.setObjectName("questionTreeWidget")
        self.gridLayout.addWidget(self.questionTreeWidget, 2, 0, 1, 1)
        self.answerTreeWidget = QtWidgets.QTreeWidget(self)
        self.answerTreeWidget.setObjectName("answerTreeWidget")
        self.gridLayout.addWidget(self.answerTreeWidget, 4, 0, 1, 1)

        self.questionLabel.setText("Questions field:")
        self.answerLabel.setText("Answers field:")
        self.informationLabel.setText(
            "<html><head/><body><p>Please select fields that will be used as questions and answers for the quiz.</p></body></html>")

        self.fieldSelectLocation = 1

        self.questionTreeWidget.setHeaderHidden(True)
        self.questionTreeWidget.setHeaderItem(
            QtWidgets.QTreeWidgetItem(["Field names", "Selected"]))
        self.questionTreeWidget.header().setStretchLastSection(False)
        self.questionTreeWidget.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.questionTreeWidget.header().setSectionResizeMode(
            self.fieldSelectLocation, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.questionTreeWidget.fieldType = "Question"

        self.answerTreeWidget.setHeaderHidden(True)
        self.answerTreeWidget.setHeaderItem(
            QtWidgets.QTreeWidgetItem(["Field names", "Selected"]))
        self.answerTreeWidget.header().setStretchLastSection(False)
        self.answerTreeWidget.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.answerTreeWidget.header().setSectionResizeMode(
            self.fieldSelectLocation, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.answerTreeWidget.fieldType = "Answer"

        self.questionTreeWidget.itemDoubleClicked.connect(self.fieldClicked)
        self.answerTreeWidget.itemDoubleClicked.connect(self.fieldClicked)

    def initializePage(self) -> None:
        self.questionTreeWidget.clear()
        self.answerTreeWidget.clear()
        decks = self.wizard().ankiNotesLoader.getFields()
        for deck in decks.items():
            questionItemTree = QtWidgets.QTreeWidgetItem(
                self.questionTreeWidget, [deck[0]])
            answerItemTree = QtWidgets.QTreeWidgetItem(
                self.answerTreeWidget, [deck[0]])
            for field in deck[1]:
                questionItem = QtWidgets.QTreeWidgetItem([field])
                questionItem.setCheckState(1, QtCore.Qt.CheckState.Unchecked)
                questionItemTree.addChild(questionItem)

                answerItem = QtWidgets.QTreeWidgetItem([field])
                answerItem.setCheckState(1, QtCore.Qt.CheckState.Unchecked)
                answerItemTree.addChild(answerItem)
            questionItemTree.setExpanded(True)
            answerItemTree.setExpanded(True)
        return super().initializePage()

    def fieldClicked(self, item: QtWidgets.QTreeWidgetItem):
        checkState = item.checkState(self.fieldSelectLocation)
        if item.childCount() == 0:
            if checkState == QtCore.Qt.CheckState.Unchecked:
                item.setCheckState(self.fieldSelectLocation,
                                   QtCore.Qt.CheckState.Checked)
            else:
                item.setCheckState(self.fieldSelectLocation,
                                   QtCore.Qt.CheckState.Unchecked)
        self.updateSelectedFields(item)

    def updateSelectedFields(self, item: QtWidgets.QTreeWidgetItem):
        # item.treeWidget().findItems(
        #     "", QtCore.Qt.MatchFlag.MatchContains | QtCore.Qt.MatchFlag.MatchRecursive)

        selectedFields = list()
        for deck in item.treeWidget().findItems("", QtCore.Qt.MatchFlag.MatchContains | QtCore.Qt.MatchFlag.MatchRecursive):
            if deck.checkState(self.fieldSelectLocation) == QtCore.Qt.CheckState.Checked:
                noteTypeAndFieldName = list()
                while deck is not None:
                    noteTypeAndFieldName.append(deck.text(0))
                    deck = deck.parent()
                selectedFields.append(noteTypeAndFieldName[::-1])

        if item.treeWidget().fieldType == 'Question':
            self.wizard().ankiNotesLoader.selectQuestionFields(selectedFields)
        elif item.treeWidget().fieldType == 'Answer':
            self.wizard().ankiNotesLoader.selectAnswerFields(selectedFields)
        self.completeChanged.emit()

    def isComplete(self) -> bool:
        if self.wizard().ankiNotesLoader.selectedQuestionFields and self.wizard().ankiNotesLoader.selectedAnswerFields:
            return True
        else:
            return False
