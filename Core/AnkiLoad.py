from ankisync2.anki21 import db
from os import listdir
from os.path import dirname



class AnkiNotesLoader():
    def __init__(self, file) -> None:
        # self.testing(file)
        self.file = file
        db.database.init(file)
        self.decks = list()
        self.selectedDeck = None
        self.cards = list()
        self.notes = list()
        self.fields = list()

    def loadDecks(self) -> None:
        self.decks = list(db.Decks.select())

    def getDeckNames(self) -> list:
        return list([deck.name for deck in self.decks])

    # Rethink this
    def getDeckTree(self) -> dict:

        def recursiveList(self):
            pass
        stem = dict()
        for deck in self.decks:
            print(deck.name.find('\x1f') )
        stem = dict([(deck.name, '1') for deck in self.decks if deck.name.find('\x1f') == -1])
        testDict = dict()
        testDict['1'] = dict()
        testDict['1']['1'] = 1
        testDict['2'] = 2
        return testDict

    def loadDeck(self, deckName) -> None:
        self.deck = next(deck for deck in self.decks if deck.name == deckName)
        # self.cards = list(db.Cards.select().where(db.Cards.did == self.deck.id))

        # note_ids = set([card.nid for card in self.cards])
        # self.notes = list(db.Notes.select().where(db.Notes.id.in_(note_ids)))

        # note_type_ids = set([note.mid for note in self.notes])
        # self.fields = list(db.Fields.select().where(db.Fields.ntid.in_(note_type_ids)))

        # print([field.name for field in self.fields])

    def getFields(self) -> list:
        self.cards = list(db.Cards.select().where(db.Cards.did == self.deck.id))

        note_ids = set([card.nid for card in self.cards])
        self.notes = list(db.Notes.select().where(db.Notes.id.in_(note_ids)))

        note_type_ids = set([note.mid for note in self.notes])
        self.fields = list(db.Fields.select().where(db.Fields.ntid.in_(note_type_ids)))

        print([field.name for field in self.fields])

    def testing(self, file):
        db.database.init(file)

        # we dont need NoteTypes, it only contains note name and some useless formatting
        # first, we need decks - to show user deck names so he can select a good one - this gives us its id to get all the cards
        # second - we fetch all the cards from the deck, as they contain sheduling
        # third - we fetch all the notes and check if we have different notes 
        # fourth - we fetch all the required noteTypes(by using the ids we have gotten from the notes).    --- we dont even need to use noteTypes
        # - just fetch field names
        # We force the user to accept/ignore said note type (and select fields if he accepts). This gives us noteType ids to use in fields table
        # fifth - we fetch all the fields for a given note type and 

        # first:
        decks = list(db.Decks.select())
        # for now - only one deck supported
        deck = decks[3]
        # deck_names = ([deck_name.name for deck_name in decks if deck_name.name.find('\x1f') == -1])

        # second:
        cards = list(db.Cards.select().where(db.Cards.did == deck.id))


        # third:
        note_ids = set([card.nid for card in cards])
        notes = list(db.Notes.select().where(db.Notes.id.in_(note_ids)))

        # fourth - skipping noteTypes
        note_type_ids = set([note.mid for note in notes])
        fields = list(db.Fields.select().where(db.Fields.ntid.in_(note_type_ids)))
        print("loaded")
    

# dir = dirname(__file__) + '/../Anki_data' + '/collection.anki2'
# AnkiNotesLoader(dir)