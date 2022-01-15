from .NotepadController import NotepadController
from .NotepadWindow import NotepadWindow
from collections import namedtuple

def load():
    View = namedtuple("View", ['window', 'controller'])
    return View(NotepadWindow, NotepadController)