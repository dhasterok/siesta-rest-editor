import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from siesta.reSTNotes import NotesMainWindow, SIESTA_ICON_PATH

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Dock icon when run from source; the built .app also carries it as its .icns
    app.setWindowIcon(QIcon(str(SIESTA_ICON_PATH / "siesta2.svg")))
    win = NotesMainWindow()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())
