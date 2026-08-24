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
    QHeaderView,
    QDateEdit
)

from PySide6.QtCore import QDate

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
        # Filtres
        # ==========================

        filtres = QHBoxLayout()

        self.periode = QComboBox()

        self.periode.addItems([
            "Toutes",
            "Aujourd'hui",
            "Hier",
            "Cette semaine",
            "La semaine dernière",
            "Ce mois",
            "Le mois dernier",
            "Cette année"
        ])

        filtres.addWidget(
            QLabel("Période :")
        )

        filtres.addWidget(
            self.periode
        )

        self.date_precise = QDateEdit()
        self.date_precise.setCalendarPopup(True)
        self.date_precise.setDate(
            QDate.currentDate()
        )
        self.btn_date = QPushButton("🔎 Date précise")

        filtres.addWidget(
            QLabel("Date précise :")
        )

        filtres.addWidget(
            self.date_precise
        )

        filtres.addWidget(
            self.btn_date
        )

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText(
            "🔎 Rechercher une dépense..."
        )

        filtres.addWidget(
            self.recherche
        )

        layout.addLayout(filtres)

        filtres_categorie = QHBoxLayout()

        self.filtre_categorie = QComboBox()

        self.filtre_categorie.addItems([
            "Toutes",
            "Matières premières",
            "Transport",
            "Électricité",
            "Eau",
            "Loyer",
            "Salaires",
            "Entretien",
            "Autre"
        ])

        filtres_categorie.addWidget(
            QLabel("Catégorie :")
        )

        filtres_categorie.addWidget(
            self.filtre_categorie
        )

        layout.addLayout(
            filtres_categorie
        )

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
        
        self.btn_date.clicked.connect(
            self.rechercher_par_date
        )

        self.periode.currentTextChanged.connect(
            self.charger_depenses
        )

        self.filtre_categorie.currentTextChanged.connect(
            self.charger_depenses
        )

        self.recherche.textChanged.connect(
            self.charger_depenses
        )

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

        conditions = []
        parametres = []

        # ==========================
        # Filtre de période
        # ==========================

        periode = self.periode.currentText()

        if periode == "Aujourd'hui":
            conditions.append(
                "date(date_depense) = date('now', 'localtime')"
            )

        elif periode == "Hier":
            conditions.append(
                "date(date_depense) = date('now', 'localtime', '-1 day')"
            )

        elif periode == "Cette semaine":
            conditions.append("""
                date(date_depense) >= date(
                    'now',
                    '-' || ((strftime('%w', 'now') + 6) % 7)
                    || ' days',
                    'localtime'
                )
            """)

        elif periode == "La semaine dernière":
            conditions.append("""
                date(date_depense) >= date(
                    'now',
                    '-' || ((strftime('%w', 'now') + 6) % 7 + 7)
                    || ' days',
                    'localtime'
                )
                AND date(date_depense) < date(
                    'now',
                    '-' || ((strftime('%w', 'now') + 6) % 7)
                    || ' days',
                    'localtime'
                )
            """)

        elif periode == "Ce mois":
            conditions.append("""
                strftime('%Y-%m', date_depense)
                = strftime('%Y-%m', 'now', 'localtime')
            """)

        elif periode == "Le mois dernier":
            conditions.append("""
                strftime('%Y-%m', date_depense)
                = strftime('%Y-%m', 'now', 'localtime', '-1 month')
            """)

        elif periode == "Cette année":
            conditions.append("""
                strftime('%Y', date_depense)
                = strftime('%Y', 'now', 'localtime')
            """)

        # ==========================
        # Catégorie
        # ==========================

        categorie = self.filtre_categorie.currentText()

        if categorie != "Toutes":
            conditions.append(
                "categorie = ?"
            )
            parametres.append(categorie)

        # ==========================
        # Recherche
        # ==========================

        recherche = self.recherche.text().strip()

        if recherche:
            conditions.append(
                "libelle LIKE ?"
            )
            parametres.append(
                f"%{recherche}%"
            )

        # ==========================
        # Requête
        # ==========================

        requete = """
            SELECT
                id,
                date_depense,
                libelle,
                categorie,
                montant
            FROM depenses
        """

        if conditions:
            requete += " WHERE " + " AND ".join(conditions)

        requete += """
            ORDER BY date_depense DESC
        """

        cur.execute(
            requete,
            parametres
        )

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

    def rechercher_par_date(self):

        date_precise = self.date_precise.date().toString(
            "yyyy-MM-dd"
        )

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
            WHERE date(date_depense) = ?
            ORDER BY date_depense DESC
        """, (
            date_precise,
        ))

        depenses = cur.fetchall()

        conn.close()

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