from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow
from PyQt6 import QtCore, QtWidgets
import typing

class UpgradeShopWidget(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional['QtWidgets.QWidget'], getAvaliableUpgradesHandle) -> None:
        super().__init__(parent=parent)
        self.getUpgrades = getAvaliableUpgradesHandle

        self.showUnlockedCheckbox = QtWidgets.QCheckBox(self)
        self.showUnlockedCheckbox.setObjectName("showUnlockedCheckbox")
        
        self.buyAllButton = QtWidgets.QPushButton(self)
        self.buyAllButton.setObjectName("buyAllButton")
        
        self.upgradesTree = QtWidgets.QTreeWidget(self)
        self.upgradesTree.setObjectName("upgradesTree")
        self.upgradesTree.setColumnCount(3)
        self.upgradesTree.setHeaderItem(QtWidgets.QTreeWidgetItem(
            ["Description", "Type", "Cost"]))
        self.upgradesTree.header().setStretchLastSection(False)
        self.upgradesTree.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.upgradesTree.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.upgradesTree.header().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.buyAllButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.showUnlockedCheckbox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.upgradesTree, 0, 0, 1, 2)

        self.showUnlockedCheckbox.setText("Show unlocked")
        self.buyAllButton.setText("Buy all available")
        self.loadUpgrades()

    def loadUpgrades(self):
        games = self.getUpgrades()
        for game in games:
            if len(game['upgrades']) > 0:
                gameUpgradesTree = QtWidgets.QTreeWidgetItem(
                    self.upgradesTree, [game['gameName']])

                for upgrade in game['upgrades']:
                    upgradeItem = QtWidgets.QTreeWidgetItem([upgrade.description, upgrade.type, str(upgrade.cost)])
                    gameUpgradesTree.addChild(upgradeItem)

                gameUpgradesTree.setExpanded(True)


class UpgradeShopWindow(DefaultGameMdiSubWindow):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ..., flags: QtCore.Qt.WindowType = QtCore.Qt.WindowType.SubWindow, controller=None) -> None:
        super().__init__(parent=parent, flags=flags, controller=controller)
        self.setMaximumSize(400, 200)
        self.resize(400, 200)
        self.menuName = "Upgrades"
        self.isUnlocked = True
        self.shouldStartVisible = False
        self.gameName = "UpgradeShop"
        self.setWindowTitle(self.menuName)
        self.setObjectName("UpgradeWidget")

        self.shopWidget = UpgradeShopWidget(self, self.controller.getAvaliableUpgrades)
        self.setWidget(self.shopWidget)
