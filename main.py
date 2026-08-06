import sys
from PySide6.QtWidgets import QApplication

from app.app import SnackMia

app = QApplication(sys.argv)

fenetre = SnackMia()
fenetre.show()

sys.exit(app.exec())