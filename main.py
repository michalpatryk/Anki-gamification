import sys
from PyQt6.QtWidgets import QApplication
from Core import AnkiGamificationApp, GameController


if __name__ == '__main__':
    app = AnkiGamificationApp.AnkiGamificationApp(sys.argv)
    sys.exit(app.exec())
