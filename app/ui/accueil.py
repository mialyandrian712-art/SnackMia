from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from app.database.database import get_connection

from PySide6.QtCore import Qt, QDate


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

        date_label = QLabel(
            "📅 " + QDate.currentDate().toString("dd/MM/yyyy") + " — Données du jour"
        )

        date_label.setStyleSheet("""
            font-size:16px;
            color:gray;
            padding-left:20px;
        """)

        layout.addWidget(date_label)

        grille = QGridLayout()

        self.ca = Carte(
            "💰 Chiffre d'affaires",
            "0 Ar"
        )

        self.resultat = Carte(
            "📈 Résultat du jour",
            "0 Ar"
        )

        self.ventes = Carte(
            "🧾 Ventes aujourd'hui",
            "0"
        )

        self.plats = Carte(
            "🍔 Plats",
            "0"
        )

        self.stock = Carte(
            "📦 Stock",
            "0"
        )

        self.alertes = Carte(
            "⚠️ Alertes",
            "0"
        )

        grille.addWidget(self.ca, 0, 0)
        grille.addWidget(self.resultat, 0, 1)

        grille.addWidget(self.ventes, 1, 0)
        grille.addWidget(self.plats, 1, 1)

        grille.addWidget(self.stock, 2, 0)
        grille.addWidget(self.alertes, 2, 1)

        layout.addLayout(grille)

        # ==========================
        # Stock à surveiller
        # ==========================

        titre_stock = QLabel(
            "⚠️ Stock à surveiller"
        )

        titre_stock.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre_stock)

        self.table_alertes = QTableWidget()

        self.table_alertes.setColumnCount(3)

        self.table_alertes.setHorizontalHeaderLabels([
            "Produit",
            "Quantité",
            "Seuil"
        ])

        self.table_alertes.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_alertes.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(
            self.table_alertes
        )

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

        self.actualiser()

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
            WHERE date(date_vente) = date('now')
        """)

        chiffre_affaires = cur.fetchone()[0]

        # ==========================
        # Résultat du jour
        # ==========================

        cur.execute("""
            SELECT COALESCE(
                SUM(montant),
                0
            )
            FROM depenses
            WHERE date(date_depense) = date('now')
        """)

        total_depenses = cur.fetchone()[0]

        resultat = (
            chiffre_affaires
            - total_depenses
        )

        # ==========================
        # Nombre de ventes aujourd'hui
        # ==========================

        cur.execute("""
            SELECT COUNT(*)
            FROM ventes
            WHERE date(date_vente) = date('now')
        """)

        nombre_ventes = cur.fetchone()[0]

        # ==========================
        # Nombre de plats
        # ==========================

        cur.execute("""
            SELECT COUNT(*)
            FROM plats
        """)

        nombre_plats = cur.fetchone()[0]

        # ==========================
        # Nombre de produits en stock
        # ==========================

        cur.execute("""
            SELECT COUNT(*)
            FROM stock
        """)

        nombre_stock = cur.fetchone()[0]

        # ==========================
        # Alertes stock
        # ==========================

        cur.execute("""
            SELECT COUNT(*)
            FROM stock
            WHERE seuil > 0
            AND quantite <= seuil
        """)

        nombre_alertes = cur.fetchone()[0]

        # ==========================
        # Produits en stock faible
        # ==========================

        cur.execute("""
            SELECT
                nom,
                quantite,
                seuil
            FROM stock
            WHERE seuil > 0
            AND quantite <= seuil
            ORDER BY quantite ASC
        """)

        alertes_stock = cur.fetchall()

        conn.close()

        # ==========================
        # Affichage
        # ==========================

        self.ca.valeur.setText(
            f"{chiffre_affaires:,.0f} Ar"
        )

        self.resultat.valeur.setText(
            f"{resultat:,.0f} Ar"
        )

        self.ventes.valeur.setText(
            str(nombre_ventes)
        )

        self.plats.valeur.setText(
            str(nombre_plats)
        )

        self.stock.valeur.setText(
            str(nombre_stock)
        )

        self.alertes.valeur.setText(
            str(nombre_alertes)
        )    

        # ==========================
        # Affichage des alertes stock
        # ==========================

        self.table_alertes.setRowCount(
            len(alertes_stock)
        )

        for ligne, produit in enumerate(
            alertes_stock
        ):

            for colonne, valeur in enumerate(
                produit
            ):

                item = QTableWidgetItem(
                    str(valeur)
                )

                self.table_alertes.setItem(
                    ligne,
                    colonne,
                    item
                )