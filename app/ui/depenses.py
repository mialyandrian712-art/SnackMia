from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from app.database.database import get_connection


class DepensesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.id_selectionne = None

        # ==========================
        # Titre
        # ==========================

        layout = QVBoxLayout()

        titre = QLabel("💰 Gestion des dépenses")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre)

        # ==========================
        # Tableau
        # ==========================

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Date",
            "Libellé",
            "Catégorie",
            "Montant (Ar)"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.cellClicked.connect(
            self.selectionner_depense
        )

        layout.addWidget(self.table)

        # ==========================
        # Formulaire
        # ==========================

        self.libelle = QLineEdit()
        self.libelle.setPlaceholderText(
            "Libellé de la dépense"
        )

        self.categorie = QComboBox()

        self.categorie.addItems([
            "Matières premières",
            "Transport",
            "Électricité",
            "Eau",
            "Loyer",
            "Salaires",
            "Entretien",
            "Autre"
        ])

        self.montant = QLineEdit()
        self.montant.setPlaceholderText(
            "Montant en Ariary"
        )

        layout.addWidget(self.libelle)
        layout.addWidget(self.categorie)
        layout.addWidget(self.montant)

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

        boutons.addWidget(self.btn_ajouter)
        boutons.addWidget(self.btn_modifier)
        boutons.addWidget(self.btn_supprimer)

        layout.addLayout(boutons)

        self.setLayout(layout)

        # ==========================
        # Connexions
        # ==========================

        self.btn_ajouter.clicked.connect(
            self.ajouter_depense
        )

        self.btn_modifier.clicked.connect(
            self.modifier_depense
        )

        self.btn_supprimer.clicked.connect(
            self.supprimer_depense
        )

        self.charger_depenses()

    # ==========================
    # Charger les dépenses
    # ==========================

    def charger_depenses(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                date_depense,
                libelle,
                categorie,
                montant
            FROM depenses
            ORDER BY date_depense DESC
        """)

        depenses = cur.fetchall()

        self.table.setRowCount(
            len(depenses)
        )

        for ligne, depense in enumerate(depenses):

            for colonne, valeur in enumerate(depense):

                self.table.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

        conn.close()

    # ==========================
    # Sélectionner une dépense
    # ==========================

    def selectionner_depense(
        self,
        ligne,
        colonne
    ):

        self.id_selectionne = int(
            self.table.item(
                ligne,
                0
            ).text()
        )

        self.libelle.setText(
            self.table.item(
                ligne,
                2
            ).text()
        )

        self.categorie.setCurrentText(
            self.table.item(
                ligne,
                3
            ).text()
        )

        self.montant.setText(
            self.table.item(
                ligne,
                4
            ).text()
        )

    # ==========================
    # Ajouter
    # ==========================

    def ajouter_depense(self):

        if (
            self.libelle.text().strip() == ""
            or self.montant.text().strip() == ""
        ):

            QMessageBox.warning(
                self,
                "Erreur",
                "Remplis tous les champs."
            )

            return

        try:

            montant = float(
                self.montant.text()
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Erreur",
                "Le montant doit être un nombre."
            )

            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO depenses(
                date_depense,
                libelle,
                categorie,
                montant
            )
            VALUES(
                datetime('now'),
                ?,
                ?,
                ?
            )
        """, (
            self.libelle.text().strip(),
            self.categorie.currentText(),
            montant
        ))

        conn.commit()
        conn.close()

        self.libelle.clear()
        self.montant.clear()

        self.charger_depenses()

        QMessageBox.information(
            self,
            "Succès",
            "Dépense ajoutée avec succès."
        )

    # ==========================
    # Modifier
    # ==========================

    def modifier_depense(self):

        if self.id_selectionne is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne une dépense."
            )

            return

        try:

            montant = float(
                self.montant.text()
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Erreur",
                "Le montant doit être un nombre."
            )

            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE depenses
            SET
                libelle = ?,
                categorie = ?,
                montant = ?
            WHERE id = ?
        """, (
            self.libelle.text().strip(),
            self.categorie.currentText(),
            montant,
            self.id_selectionne
        ))

        conn.commit()
        conn.close()

        self.id_selectionne = None

        self.libelle.clear()
        self.montant.clear()

        self.charger_depenses()

        QMessageBox.information(
            self,
            "Succès",
            "Dépense modifiée."
        )

    # ==========================
    # Supprimer
    # ==========================

    def supprimer_depense(self):

        if self.id_selectionne is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne une dépense."
            )

            return

        reponse = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer cette dépense ?"
        )

        if reponse != QMessageBox.Yes:
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM depenses WHERE id = ?",
            (self.id_selectionne,)
        )

        conn.commit()
        conn.close()

        self.id_selectionne = None

        self.libelle.clear()
        self.montant.clear()

        self.charger_depenses()

        QMessageBox.information(
            self,
            "Succès",
            "Dépense supprimée."
        )