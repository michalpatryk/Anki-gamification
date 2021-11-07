from os.path import exists
from pathlib import Path
import re
import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from Core.AnkiLoad import AnkiNotesLoader

class ImportWizard(QtWidgets.QWizard):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.Dialog) -> None:
        super().__init__(parent=parent, flags=flags)
        
        self.setFixedSize(640, 480)
        self.addPage(LoadCollectionPage(self))
        self.addPage(LoadDeckPage(self))
        self.addPage(SelectFieldsPage(self))

        self.resize(640, 480)
        self.setWindowTitle("Anki collection importer")
        self.ankiNotesLoader = None #type: AnkiNotesLoader

class ImportWizardPage(QtWidgets.QWizardPage):
    def wizard(self) -> ImportWizard:
        return super().wizard()


class LoadCollectionPage(ImportWizardPage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.loadCollectionLayout = QtWidgets.QGridLayout(self)
        self.loadCollectionLayout.setObjectName("loadCollectionLayout")
        self.selectCollectionInfoLabel = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectCollectionInfoLabel.sizePolicy().hasHeightForWidth())
        self.selectCollectionInfoLabel.setSizePolicy(sizePolicy)
        self.selectCollectionInfoLabel.setObjectName("selectCollectionInfoLabel")
        self.loadCollectionLayout.addWidget(self.selectCollectionInfoLabel, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.loadCollectionLayout.addWidget(self.lineEdit, 4, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.loadCollectionLayout.addWidget(self.pushButton, 4, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setObjectName("checkBox")
        self.loadCollectionLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.label.setText("<html><head/><body><p>There are no Anki flashcards loaded. Please select a collection.anki2 file. Selected file will be read only, but it is nonetheless advised to use a copy instead of your main file. File locaiton is explained at <a href=\"https://docs.ankiweb.net/files.html\"><span style=\" text-decoration: underline; color:#0000ff;\">https://docs.ankiweb.net/files.html</span></a></p></body></html>")
        self.selectCollectionInfoLabel.setText("Select collection file:")
        self.pushButton.setText("...")
        self.checkBox.setText("I understand the risks")

        self.loadCollectionLayout.addWidget(self.label, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.loadCollectionLayout.addItem(spacerItem, 2, 0, 1, 1)

        self.pushButton.clicked.connect(self.onSelectFile)
        self.lineEdit.textChanged.connect(self.onLineEditEdited)
        self.checkBox.clicked.connect(self.completeChanged)

        self.fname = '.\\Anki_data'
        self.lineEdit.setText(self.fname)
        self.registerField("collectionFile", self.lineEdit)

        self.lineEdit.setText("C:/Own/Programming/Python/Anki-gamification/Anki_data/collection.anki2")
        self.checkBox.setChecked(True)


    def onSelectFile(self):
        fname, extension = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            self.fname,"Collection files (*.anki2);; All files (*.*)")
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
        self.decksView = QtWidgets.QListWidget(self)
        self.decksView.setObjectName("decksView")
        self.loadDeckLayout.addWidget(self.decksView, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.loadDeckLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label.setText("Select deck:")
        self.decksView.itemSelectionChanged.connect(self.deckSelected)

    def initializePage(self) -> None:
        self.wizard().ankiNotesLoader = AnkiNotesLoader(self.field("collectionFile"))
        self.wizard().ankiNotesLoader.loadDecks()
        decks = self.wizard().ankiNotesLoader.getDeckNames()

        # TODO: try to change this to tree, for now lets just make a working prototype
        # treeDeck = self.wizard().ankiNotesLoader.getDeckTree()
        

        # for deck in treeDeck:
        #     child = QtWidgets.QTreeWidgetItem(self.decksView)
        #     child.setText(deck.name)
        #     if type(deck) is dict:

        self.decksView.addItems(decks)
        return super().initializePage()

    def deckSelected(self) -> None:
        self.wizard().ankiNotesLoader.loadDeck(self.decksView.selectedItems()[0].text())
        self.completeChanged.emit()

    def isComplete(self) -> bool:
        if self.decksView.selectedItems():
            return True
        else: 
            return False


class SelectFieldsPage(QtWidgets.QWizardPage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)