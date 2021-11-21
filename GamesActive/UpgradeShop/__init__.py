from .UpgradeShopController import UpgradeShopController
from .UpgradeShopWindow import UpgradeShopWindow
from collections import namedtuple

def load():
    View = namedtuple('View', ['window', 'controller'])
    return View(UpgradeShopWindow, UpgradeShopController)
