from Core.DefaultGameMdiSubWindow import DefaultGameMdiSubWindow
from PyQt6 import QtCore, QtWidgets, QtGui
import typing

class UpgradeItem(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None:
        super().__init__(parent=parent)

class UpgradesContainer(QtWidgets.QTreeWidget):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

class UpgradeShopWidget(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional['QtWidgets.QWidget'], getAvaliableUpgradesHandle, canBuyUpgradeHandle, buyUpgradeHandle) -> None:
        super().__init__(parent=parent)
        self.getAvaliableUpgradesHandle = getAvaliableUpgradesHandle
        self.canBuyUpgradeHandle = canBuyUpgradeHandle
        self.buyUpgradeHandle = buyUpgradeHandle

        self.showBoughtCheckbox = QtWidgets.QCheckBox(self)
        self.showBoughtCheckbox.setObjectName("showUnlockedCheckbox")
        
        self.buyAllButton = QtWidgets.QPushButton(self)
        self.buyAllButton.setObjectName("buyAllButton")
        
        self.upgradesTree = UpgradesContainer(self)
        self.upgradesTree.setObjectName("upgradesTree")
        self.upgradesTree.setColumnCount(4)
        self.upgradesTree.setHeaderItem(QtWidgets.QTreeWidgetItem(
            ["Description", "Type", "Cost/Buy"]))
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
        self.gridLayout.addWidget(self.showBoughtCheckbox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.upgradesTree, 0, 0, 1, 2)

        self.showBoughtCheckbox.setText("Show bought")
        self.buyAllButton.setText("Buy all available")
        self.loadUpgrades()

        self.buyAllButton.clicked.connect(self.buyAllUpgrades)
        self.showBoughtCheckbox.clicked.connect(self.loadUpgrades)

    def loadUpgrades(self):
        self.upgradesTree.clear()
        self.gamesUpgrades = self.getAvaliableUpgradesHandle()
        for gameUpgrades in self.gamesUpgrades:
            if len(gameUpgrades['upgrades']) > 0:
                gameUpgradesTree = QtWidgets.QTreeWidgetItem(self.upgradesTree, [gameUpgrades['gameName']])
                for upgrade in gameUpgrades['upgrades']:
                    if upgrade.isBought == False: 
                        upgradeItem = QtWidgets.QTreeWidgetItem([upgrade.description, upgrade.type])
                        gameUpgradesTree.addChild(upgradeItem)
                        button = QtWidgets.QPushButton(self.upgradesTree)
                        button.clicked.connect(lambda checked=False, upgrade=upgrade: self.buyUpgrade(upgrade))
                        button.setText(str(int(upgrade.cost)))
                        button.setProperty("upgrade", upgrade)
                        self.upgradesTree.setItemWidget(upgradeItem, 2, button)
                    elif self.showBoughtCheckbox.isChecked() == True:
                        upgradeItem = QtWidgets.QTreeWidgetItem([upgrade.description, upgrade.type, "{:.3}".format(upgrade.cost)])
                        gameUpgradesTree.addChild(upgradeItem)
                gameUpgradesTree.setExpanded(True)

    def buyUpgrade(self, upgrade):
        if self.buyUpgradeHandle(upgrade):
            self.loadUpgrades()

    def buyAllUpgrades(self):
        for game in self.gamesUpgrades:
            for upgrade in game["upgrades"]:
                if upgrade.isBought == False and upgrade.isUnlocked == True:
                    self.buyUpgrade(upgrade=upgrade) 

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

        self.shopWidget = UpgradeShopWidget(self, self.controller.getAvaliableUpgrades, 
                                                  self.controller.canBuyUpgrade, 
                                                  self.controller.buyUpgrade)
        self.setWidget(self.shopWidget)
        self.controller.popAllDelayedUpgrades()
        self.controller.attachReloadShopHandle(self.shopWidget.loadUpgrades)
