from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)

from PySide6.QtCore import Qt

from app.database.database import get_connection


class RapportsPage(QWidget):

    def __init__(self):
        super().__init__()

        # ==========================
        # Layout principal
        # ==========================

        layout = QVBoxLayout()

        titre = QLabel("📊 Rapports")
        titre.setAlignment(Qt.AlignCenter)

        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:15px;
        """)

        layout.addWidget(titre)

        # ==========================
        # Cartes
        # ==========================

        cartes = QHBoxLayout()

        self.ca = self.creer_carte(
            "💰 Chiffre d'affaires",
            "0 Ar"
        )

        self.depenses = self.creer_carte(
            "💸 Dépenses",
            "0 Ar"
        )

        self.resultat = self.creer_carte(
            "📈 Résultat",
            "0 Ar"
        )

        cartes.addWidget(self.ca)
        cartes.addWidget(self.depenses)
        cartes.addWidget(self.resultat)

        layout.addLayout(cartes)

        # ==========================
        # Bouton actualiser
        # ==========================

        self.btn_actualiser = QPushButton(
            "🔄 Actualiser le rapport"
        )

        self.btn_actualiser.setMinimumHeight(50)

        layout.addWidget(
            self.btn_actualiser
        )

        self.setLayout(layout)

        # ==========================
        # Connexion
        # ==========================

        self.btn_actualiser.clicked.connect(
            self.actualiser
        )

        self.actualiser()

    # ==========================
    # Créer une carte
    # ==========================

    def creer_carte(
        self,
        titre,
        valeur
    ):

        carte = QFrame()

        carte.setStyleSheet("""
            QFrame {
                background:white;
                border:1px solid #dddddd;
                border-radius:15px;
            }
        """)

        carte.setMinimumHeight(130)

        layout = QVBoxLayout()

        label_titre = QLabel(titre)

        label_titre.setAlignment(
            Qt.AlignCenter
        )

        label_titre.setStyleSheet("""
            font-size:16px;
            color:gray;
        """)

        label_valeur = QLabel(valeur)

        label_valeur.setAlignment(
            Qt.AlignCenter
        )

        label_valeur.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        layout.addWidget(label_titre)
        layout.addWidget(label_valeur)

        carte.setLayout(layout)

        # On garde la valeur accessible
        carte.valeur = label_valeur

        return carte

    # ==========================
    # Actualiser le rapport
    # ==========================

    def actualiser(self):

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # Chiffre d'affaires du jour
        # ==========================

        cur.execute("""
            SELECT COALESCE(
                SUM(total),
                0
            )
            FROM ventes
            WHERE date(date_vente)
                  = date('now')
        """)

        chiffre_affaires = cur.fetchone()[0]

        # ==========================
        # Dépenses du jour
        # ==========================

        cur.execute("""
            SELECT COALESCE(
                SUM(montant),
                0
            )
            FROM depenses
            WHERE date(date_depense)
                  = date('now')
        """)

        total_depenses = cur.fetchone()[0]

        conn.close()

        # ==========================
        # Résultat
        # ==========================

        resultat = (
            chiffre_affaires
            - total_depenses
        )

        # ==========================
        # Affichage
        # ==========================

        self.ca.valeur.setText(
            f"{chiffre_affaires:,.0f} Ar"
        )

        self.depenses.valeur.setText(
            f"{total_depenses:,.0f} Ar"
        )

        self.resultat.valeur.setText(
            f"{resultat:,.0f} Ar"
        )