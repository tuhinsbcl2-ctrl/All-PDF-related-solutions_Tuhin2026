"""
Application entry point – creates QApplication and shows MainWindow.
"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.styles import get_theme


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Solutions")
    app.setOrganizationName("Tuhin")
    app.setStyleSheet(get_theme("dark"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
