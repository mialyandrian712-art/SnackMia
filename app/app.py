from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)

from PySide6.QtCore import Qt
import sys

from app.ui.accueil import AccueilPage
from app.ui.plats import PlatsPage
from app.ui.caisse import CaissePage
from app.ui.ventes import VentesPage
from app.ui.stock import StockPage
from app.ui.recettes import RecettesPage
from app.ui.depenses import DepensesPage

class SnackMia(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snack Mia")
        self.resize(1400, 800)

        # Widget principal
        central = QWidget()
        self.setCentralWidget(central)

        # Layout principal
        principal = QHBoxLayout()
        principal.setContentsMargins(0, 0, 0, 0)
        principal.setSpacing(0)

        central.setLayout(principal)
                # ===== MENU LATÉRAL =====

        menu = QWidget()
        menu.setFixedWidth(230)

        menu.setStyleSheet("""
            background:#20232A;
        """)

        menu_layout = QVBoxLayout(menu)

        logo = QLabel("🍽️\nSnack Mia")
        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet("""
            color:white;
            font-size:26px;
            font-weight:bold;
            padding:20px;
        """)

        menu_layout.addWidget(logo)
                # ===== BOUTONS DU MENU =====

        self.btn_accueil = QPushButton("🏠 Accueil")
        self.btn_plats = QPushButton("🍔 Plats")
        self.btn_caisse = QPushButton("🧾 Caisse")
        self.btn_ventes = QPushButton("📋 Ventes")
        self.btn_recettes = QPushButton("🍳 Recettes")
        self.btn_stock = QPushButton("📦 Stock")
        self.btn_depenses = QPushButton("💰 Dépenses")
        self.btn_rapports = QPushButton("📊 Rapports")
        self.btn_parametres = QPushButton("⚙️ Paramètres")

        boutons = [
            self.btn_accueil,
            self.btn_plats,
            self.btn_caisse,
            self.btn_ventes,
            self.btn_recettes,
            self.btn_stock,
            self.btn_depenses,
            self.btn_rapports,
            self.btn_parametres,
        ]

        for bouton in boutons:
            bouton.setMinimumHeight(45)

            bouton.setStyleSheet("""
                QPushButton{
                    color:white;
                    background:#2D313A;
                    border:none;
                    text-align:left;
                    padding-left:15px;
                    font-size:15px;
                }

                QPushButton:hover{
                    background:#404652;
                }
            """)

            menu_layout.addWidget(bouton)

        menu_layout.addStretch()

        principal.addWidget(menu)
                # ===== PAGES =====

        self.pages = QStackedWidget()

        self.accueil = AccueilPage()
        self.plats = PlatsPage()
        self.caisse = CaissePage()
        self.ventes = VentesPage()
        self.stock = StockPage()
        self.recettes = RecettesPage()
        self.depenses = DepensesPage()

        self.caisse.vente_enregistree.connect(
            self.actualiser_apres_vente
        )

        self.pages.addWidget(self.accueil)
        self.pages.addWidget(self.plats)
        self.pages.addWidget(self.caisse)
        self.pages.addWidget(self.ventes)
        self.pages.addWidget(self.stock)
        self.pages.addWidget(self.recettes)
        self.pages.addWidget(self.depenses)

        principal.addWidget(self.pages)

        self.btn_accueil.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.accueil)
        )
        self.btn_plats.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.plats)
        )
        self.btn_caisse.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.caisse)
        )
        self.btn_ventes.clicked.connect(
            self.ouvrir_ventes
        )
        self.btn_stock.clicked.connect(
            self.ouvrir_stock
        )
        self.btn_recettes.clicked.connect(
            self.ouvrir_recettes
        )
        self.btn_depenses.clicked.connect(
            self.ouvrir_depenses
        )

    def actualiser_apres_vente(self):

        self.stock.charger_stock()
        self.ventes.charger_ventes()
        self.recettes.actualiser()

    def ouvrir_depenses(self):

        self.depenses.charger_depenses()

        self.pages.setCurrentWidget(
            self.depenses
        )    
    
    def ouvrir_recettes(self):

        self.recettes.actualiser()

        self.pages.setCurrentWidget(
            self.recettes
        )

    def ouvrir_stock(self):

        self.stock.charger_stock()

        self.pages.setCurrentWidget(
            self.stock
        )    

    def ouvrir_ventes(self):

        self.ventes.charger_ventes()

        self.pages.setCurrentWidget(
            self.ventes
        )    