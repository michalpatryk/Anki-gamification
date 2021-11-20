from .ScoreController import ScoreController
from .ScoreWindow import ScoreWindow
from collections import namedtuple

def load():
    View = namedtuple('View', ['window', 'controller'])
    return View(ScoreWindow, ScoreController)
