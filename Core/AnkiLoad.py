from ankisync2.anki21 import db
from os import listdir
from os.path import dirname

from collections import defaultdict

class AnkiNotesLoader():
    def __init__(self, file) -> None:
        self.file = file
        db.database.init(file)
        self.decks = list()
        self.selectedDecks = None
        self.selectedCards = list()
        self.selectedNotes = list()
        self.possibleFields = dict()


        self.selectedQuestionFields = list()
        self.selectedAnswerFields = list()
        self.questions = list()
        self.answers = list()

    def loadDecks(self) -> None:
        self.decks = list(db.Decks.select())

    def getDeckNames(self) -> list:
        return list([deck.name for deck in self.decks])



    def setInDict(self, dic: dict, keys, value):
        for key in keys[:-1]:
            if dic[key] == 0:
                dic[key] = dict()
            dic = dic[key]
        dic[keys[-1]] = value
            
            
    def getDeckTree(self) -> dict:
        separator = "\x1f"
        decks = list([deck.name for deck in self.decks])
        if('Default' in decks):
            decks.remove('Default')

        split_deck =  list([deck.split(separator) for deck in decks])
        split_deck.sort(key=lambda e: len(e), reverse=False)
        nested_dict = lambda: defaultdict(nested_dict)

        deckTree = dict()
        for deck in split_deck:
            test = deck[0]
            for mini in deck[1:]:
                test += separator + mini
            
            cards = db.Cards.select().where(db.Cards.did == (db.Decks.select().where(db.Decks.name % test)[0]))
                

            self.setInDict(deckTree, deck, cards.count())
        return deckTree

    def loadDeck(self, deckName) -> None:
        self.selectedDecks = next(deck for deck in self.decks if deck.name == deckName)

    def selectDecks(self, deckNames) -> None:
        self.selectedDecks = [deck for deck in self.decks if deck.name in deckNames]

    def clearSelectedDecks(self) -> None:
        self.selectedDecks = list()

    def getFields(self) -> list:
        self.selectedCards = list(db.Cards.select().where(db.Cards.did.in_(self.selectedDecks)))

        note_ids = set([card.nid for card in self.selectedCards])
        self.selectedNotes = list(db.Notes.select().where(db.Notes.id.in_(note_ids)))

        note_type_ids = set([note.mid for note in self.selectedNotes])

        self.possibleFields = dict()
        for note_type_id in note_type_ids:
            query = list(db.Fields.select(db.Fields.name).where(db.Fields.ntid == note_type_id))
            self.possibleFields[db.Notetypes.select().where(db.Notetypes.id == note_type_id)[0].name] = [field.name for field in query]
        return self.possibleFields


    def selectQuestionFields(self, fieldData):
        self.selectedQuestionFields = dict()
        for data in fieldData:
            noteType = db.Notetypes.get(db.Notetypes.name % data[0])
            field = db.Fields.get((db.Fields.name % data[1]) & (db.Fields.ntid == noteType.id))
            if noteType.id in self.selectedQuestionFields:
                self.selectedQuestionFields[noteType.id].append(field)    
            else:
                self.selectedQuestionFields[noteType.id] = [field]

    def selectAnswerFields(self, fieldData):
        self.selectedAnswerFields = dict()
        for data in fieldData:
            noteType = db.Notetypes.get(db.Notetypes.name % data[0])
            field = db.Fields.get((db.Fields.name % data[1]) & (db.Fields.ntid == noteType.id))
            if noteType.id in self.selectedAnswerFields:
                self.selectedAnswerFields[noteType.id].append(field)    
            else:
                self.selectedAnswerFields[noteType.id] = [field]


    def getAnswersAndQuestions(self) -> tuple[list, list]:
        for noteType in self.selectedQuestionFields.items():
            notes = db.Notes.select(db.Notes.flds).where(db.Notes.mid == noteType[0])
            for note in notes:
                question = list()
                for field in noteType[1]:
                    try:
                        question.append(note.flds[field.ord])
                    except IndexError:
                        print("Detected empty field while importing questions! Adding first field of a card")
                        question.append(note.flds[0])
                self.questions.append('\n'.join([str(elem) for elem in question]))

        for noteType in self.selectedAnswerFields.items():
            notes = db.Notes.select(db.Notes.flds).where(db.Notes.mid == noteType[0])
            for note in notes:
                answer = list()
                for field in noteType[1]:
                    try:
                        answer.append(note.flds[field.ord])
                    except IndexError:
                        print("Detected empty field while importing answers! Adding last field of a card")
                        answer.append(note.flds[-1])
                self.answers.append('\n'.join([str(elem) for elem in answer]))

        return self.questions, self.answers