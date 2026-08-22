from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QDateEdit,
    QMessageBox,
    QHeaderView
)

from PySide6.QtCore import QDate

from app.database.database import get_connection


class PlatsDuJourPage(QWidget):

    def __init__(self):
        super().__init__()

        self.plat_selectionne = None

        layout = QVBoxLayout()

        # ==========================
        # Titre
        # ==========================

        titre = QLabel("⭐ Plats du jour")

        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre)

        # ==========================
        # Date
        # ==========================

        layout.addWidget(
            QLabel("📅 Date")
        )

        self.date = QDateEdit()

        self.date.setCalendarPopup(True)

        self.date.setDate(
            QDate.currentDate()
        )

        layout.addWidget(self.date)

        # ==========================
        # Nom
        # ==========================

        layout.addWidget(
            QLabel("Nom du plat")
        )

        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex : Sandwich kebab"
        )

        layout.addWidget(self.nom)

        # ==========================
        # Prix
        # ==========================

        layout.addWidget(
            QLabel("Prix")
        )

        self.prix = QLineEdit()

        self.prix.setPlaceholderText(
            "Ex : 8000"
        )

        layout.addWidget(self.prix)

        # ==========================
        # Boutons
        # ==========================

        boutons = QHBoxLayout()

        self.btn_ajouter = QPushButton(
            "➕ Ajouter"
        )

        self.btn_modifier = QPushButton(
            "✏ Modifier"
        )

        self.btn_supprimer = QPushButton(
            "🗑 Supprimer"
        )

        boutons.addWidget(
            self.btn_ajouter
        )

        boutons.addWidget(
            self.btn_modifier
        )

        boutons.addWidget(
            self.btn_supprimer
        )

        layout.addLayout(boutons)

        # ==========================
        # Tableau
        # ==========================

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Plat",
            "Prix"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.cellClicked.connect(
            self.selectionner_plat
        )

        layout.addWidget(
            self.table
        )

        self.setLayout(layout)

        # ==========================
        # Connexions
        # ==========================

        self.btn_ajouter.clicked.connect(
            self.ajouter_plat
        )

        self.btn_modifier.clicked.connect(
            self.modifier_plat
        )

        self.btn_supprimer.clicked.connect(
            self.supprimer_plat
        )

        self.date.dateChanged.connect(
            self.charger_plats
        )

        self.charger_plats()

    # ==============================
    # Charger les plats
    # ==============================

    def charger_plats(self):

        conn = get_connection()
        cur = conn.cursor()

        date_jour = self.date.date().toString(
            "yyyy-MM-dd"
        )

        cur.execute("""
            SELECT
                id,
                date_jour,
                nom,
                prix
            FROM plats_du_jour
            WHERE date_jour = ?
            ORDER BY nom
        """, (
            date_jour,
        ))

        plats = cur.fetchall()

        conn.close()

        self.table.setRowCount(
            len(plats)
        )

        for ligne, plat in enumerate(plats):

            plat_id = plat[0]
            date_jour = plat[1]
            nom = plat[2]
            prix = plat[3]

            item_date = QTableWidgetItem(
                date_jour
            )

            item_nom = QTableWidgetItem(
                nom
            )

            item_prix = QTableWidgetItem(
                f"{prix:,.0f} Ar"
            )

            item_nom.setData(
                1000,
                plat_id
            )

            self.table.setItem(
                ligne,
                0,
                item_date
            )

            self.table.setItem(
                ligne,
                1,
                item_nom
            )

            self.table.setItem(
                ligne,
                2,
                item_prix
            )

    # ==============================
    # Ajouter
    # ==============================

    def ajouter_plat(self):

        nom = self.nom.text().strip()
        prix_texte = self.prix.text().strip()

        if not nom:
            QMessageBox.warning(
                self,
                "Erreur",
                "Entre le nom du plat."
            )
            return

        if not prix_texte:
            QMessageBox.warning(
                self,
                "Erreur",
                "Entre le prix."
            )
            return

        try:
            prix = float(prix_texte)
        except ValueError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Le prix doit être un nombre."
            )
            return

        date_jour = self.date.date().toString(
            "yyyy-MM-dd"
        )

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO plats_du_jour(
                date_jour,
                nom,
                prix,
                disponible
            )
            VALUES(?,?,?)
        """, (
            date_jour,
            nom,
            prix
        ))

        conn.commit()
        conn.close()

        self.nom.clear()
        self.prix.clear()

        self.charger_plats()

        QMessageBox.information(
            self,
            "Succès",
            "Plat du jour ajouté."
        )

    # ==============================
    # Sélectionner
    # ==============================

    def selectionner_plat(
        self,
        ligne,
        colonne
    ):

        item = self.table.item(
            ligne,
            1
        )

        if item is None:
            return

        self.plat_selectionne = item.data(
            1000
        )

        self.nom.setText(
            item.text()
        )

        prix = self.table.item(
            ligne,
            2
        ).text()

        prix = prix.replace(
            " Ar",
            ""
        ).replace(
            ",",
            ""
        )

        self.prix.setText(
            prix
        )

    # ==============================
    # Modifier
    # ==============================

    def modifier_plat(self):

        if self.plat_selectionne is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un plat."
            )
            return

        nom = self.nom.text().strip()
        prix_texte = self.prix.text().strip()

        if not nom or not prix_texte:
            QMessageBox.warning(
                self,
                "Erreur",
                "Remplis tous les champs."
            )
            return

        try:
            prix = float(prix_texte)
        except ValueError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Le prix doit être un nombre."
            )
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE plats_du_jour
            SET nom = ?,
                prix = ?
            WHERE id = ?
        """, (
            nom,
            prix,
            self.plat_selectionne
        ))

        conn.commit()
        conn.close()

        self.plat_selectionne = None

        self.nom.clear()
        self.prix.clear()

        self.charger_plats()

        QMessageBox.information(
            self,
            "Succès",
            "Plat du jour modifié."
        )

    # ==============================
    # Supprimer
    # ==============================

    def supprimer_plat(self):

        if self.plat_selectionne is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un plat."
            )
            return

        reponse = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer ce plat du jour ?"
        )

        if reponse != QMessageBox.Yes:
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM plats_du_jour
            WHERE id = ?
        """, (
            self.plat_selectionne,
        ))

        conn.commit()
        conn.close()

        self.plat_selectionne = None

        self.nom.clear()
        self.prix.clear()

        self.charger_plats()

        QMessageBox.information(
            self,
            "Succès",
            "Plat du jour supprimé."
        )