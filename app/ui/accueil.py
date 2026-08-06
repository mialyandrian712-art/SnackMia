from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton
)
from PySide6.QtCore import Qt


class Carte(QFrame):
    def __init__(self, titre, valeur):
        super().__init__()

        self.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #dddddd;
                border-radius:15px;
            }
        """)

        self.setFixedSize(280,120)

        layout = QVBoxLayout()

        titre_label = QLabel(titre)
        titre_label.setStyleSheet("""
            font-size:16px;
            color:gray;
        """)

        self.valeur = QLabel(valeur)
        self.valeur.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        layout.addWidget(titre_label)
        layout.addWidget(self.valeur)

        self.setLayout(layout)


class AccueilPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            background:#F5F6FA;
        """)

        layout = QVBoxLayout()

        titre = QLabel("Tableau de bord")
        titre.setAlignment(Qt.AlignLeft)

        titre.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
            padding:20px;
        """)

        layout.addWidget(titre)

        grille = QGridLayout()

        self.ca = Carte("💰 Chiffre d'affaires", "0 Ar")
        self.plats = Carte("🍔 Plats", "0")
        self.stock = Carte("📦 Stock", "0")
        self.alertes = Carte("⚠ Alertes", "0")

        grille.addWidget(self.ca,0,0)
        grille.addWidget(self.plats,0,1)
        grille.addWidget(self.stock,1,0)
        grille.addWidget(self.alertes,1,1)

        layout.addLayout(grille)

        bouton = QPushButton("🧾 Nouvelle vente")
        bouton.setFixedHeight(55)

        bouton.setStyleSheet("""
            QPushButton{
                background:#2E86DE;
                color:white;
                font-size:18px;
                border:none;
                border-radius:10px;
            }

            QPushButton:hover{
                background:#1B4F72;
            }
        """)

        layout.addWidget(bouton)

        layout.addStretch()

        self.setLayout(layout)