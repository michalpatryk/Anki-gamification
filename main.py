import sys
from PyQt6.QtWidgets import QApplication
from Core import AnkiGamificationApp


if __name__ == '__main__':
    app = AnkiGamificationApp.AnkiGamificationApp(sys.argv)
    sys.exit(app.exec())
