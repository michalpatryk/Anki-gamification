from ankisync2.anki21 import db
from os import listdir
from os.path import dirname



class AnkiNotesLoader():
    def __init__(self, file) -> None:
        self.testing(file)
        self.deck = None
        self.cards = None
        self.notes = None
        self.fields = None

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
    

dir = dirname(__file__) + '/../Anki_data' + '/collection.anki2'
AnkiNotesLoader(dir)