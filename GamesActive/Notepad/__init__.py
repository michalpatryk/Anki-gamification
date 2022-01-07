# from .AnkiQuizGameController import QuizGameController
# from .AnkiQuizWindow import QuizGameWindow
# from collections import namedtuple

# def load():
#     View = namedtuple('View', ['window', 'controller'])
#     return View(QuizGameWindow, QuizGameController)

from .NotepadController import NotepadController
from .NotepadWindow import NotepadWindow
from collections import namedtuple

def load():
    View = namedtuple("View", ['window', 'controller'])
    return View(NotepadWindow, NotepadController)