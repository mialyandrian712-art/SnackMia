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

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Date",
            "Libellé",
            "Catégorie",
            "Type de stock",
            "Produit",
            "Quantité",
            "Prix unitaire (Ar)",
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
            "🛒 Achat stock",
            "Transport",
            "Électricité",
            "Eau",
            "Loyer",
            "Salaires",
            "Entretien",
            "Autre"
        ])

        # ==========================
        # Informations achat stock
        # ==========================

        self.type_stock_achat = QComboBox()

        self.type_stock_achat.addItems([
            "🧂 Ingrédient",
            "🥤 Boisson",
            "🍪 Biscuit"
        ])

        self.label_type_stock_achat = QLabel("Type de stock")

        self.produit_achat = QComboBox()

        self.label_produit_achat = QLabel("Produit")

        self.quantite_achat = QLineEdit()
        self.quantite_achat.setPlaceholderText(
            "Quantité achetée"
        )

        self.prix_unitaire_achat = QLineEdit()
        self.prix_unitaire_achat.setPlaceholderText(
            "Prix d'achat unitaire (Ar)"
        )

        self.total_achat = QLineEdit()
        self.total_achat.setPlaceholderText(
            "Total (Ar)"
        )

        self.total_achat.setReadOnly(True)

        layout.addWidget(self.label_type_stock_achat)
        layout.addWidget(self.type_stock_achat)

        layout.addWidget(self.label_produit_achat)
        layout.addWidget(self.produit_achat)

        layout.addWidget(self.quantite_achat)
        layout.addWidget(self.prix_unitaire_achat)
        layout.addWidget(self.total_achat)

        # Montant de la dépense normale
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

        self.categorie.currentTextChanged.connect(
            self.changer_formulaire_depense
        )

        self.type_stock_achat.currentIndexChanged.connect(
            self.charger_produits_achat
        )

        self.quantite_achat.textChanged.connect(
            self.calculer_total_achat
        )

        self.prix_unitaire_achat.textChanged.connect(
            self.calculer_total_achat
        )

        self.btn_ajouter.clicked.connect(
            self.ajouter_depense
        )

        self.changer_formulaire_depense()

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
                depenses.id,
                depenses.date_depense,
                depenses.libelle,
                depenses.categorie,
                depenses.type_stock,
                stock.nom,
                depenses.quantite,
                depenses.prix_unitaire,
                depenses.montant
            FROM depenses
            LEFT JOIN stock
                ON depenses.produit_id = stock.id
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

                if valeur is None:
                    valeur = ""

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

        # Libellé
        self.libelle.setText(
            self.table.item(
                ligne,
                2
            ).text()
        )

        # Catégorie
        self.categorie.setCurrentText(
            self.table.item(
                ligne,
                3
            ).text()
        )

        # ==========================
        # Achat de stock
        # ==========================

        type_stock = self.table.item(
            ligne,
            4
        ).text()

        produit = self.table.item(
            ligne,
            5
        ).text()

        quantite = self.table.item(
            ligne,
            6
        ).text()

        prix_unitaire = self.table.item(
            ligne,
            7
        ).text()

        montant = self.table.item(
            ligne,
            8
        ).text()

        if type_stock:

            # Type de stock
            if type_stock == "ingredient":
                self.type_stock_achat.setCurrentIndex(0)

            elif type_stock == "boisson":
                self.type_stock_achat.setCurrentIndex(1)

            elif type_stock == "biscuit":
                self.type_stock_achat.setCurrentIndex(2)

            # Recharger les produits du type choisi
            self.charger_produits_achat()

            # Sélectionner le produit
            index = self.produit_achat.findText(
                produit
            )

            if index >= 0:
                self.produit_achat.setCurrentIndex(
                    index
                )

            # Quantité
            self.quantite_achat.setText(
                quantite
            )

            # Prix unitaire
            self.prix_unitaire_achat.setText(
                prix_unitaire
            )

            # Total
            self.total_achat.setText(
                montant
            )

        else:

            # ==========================
            # Dépense normale
            # ==========================

            self.montant.setText(
                montant
            )

    # ==========================
    # Ajouter
    # ==========================

    def ajouter_depense(self):

        achat_stock = (
            self.categorie.currentText()
            == "🛒 Achat stock"
        )

        # ==========================
        # ACHAT DE STOCK
        # ==========================

        if achat_stock:

            if (
                self.produit_achat.currentData() is None
                or self.quantite_achat.text().strip() == ""
                or self.prix_unitaire_achat.text().strip() == ""
            ):

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Sélectionne un produit et remplis la quantité ainsi que le prix d'achat."
                )

                return

            try:

                quantite = float(
                    self.quantite_achat.text()
                )

                prix_unitaire = float(
                    self.prix_unitaire_achat.text()
                )

            except ValueError:

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "La quantité et le prix d'achat doivent être des nombres."
                )

                return

            if quantite <= 0 or prix_unitaire < 0:

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "La quantité doit être supérieure à 0 et le prix ne peut pas être négatif."
                )

                return

            produit_id = (
                self.produit_achat.currentData()
            )

            nom_produit = (
                self.produit_achat.currentText()
            )

            total = (
                quantite
                * prix_unitaire
            )

            conn = get_connection()
            cur = conn.cursor()

            # ==========================
            # Ajouter la dépense
            # ==========================

            # Déterminer le type de stock
            if self.type_stock_achat.currentIndex() == 0:
                type_stock = "ingredient"
            elif self.type_stock_achat.currentIndex() == 1:
                type_stock = "boisson"
            else:
                type_stock = "biscuit"    

            cur.execute("""
                INSERT INTO depenses(
                    date_depense,
                    libelle,
                    categorie,
                    montant,
                    type_stock,
                    produit_id,
                    quantite,
                    prix_unitaire
                )
                VALUES(
                    datetime('now'),
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
            """, (
                f"Achat stock - {nom_produit}",
                "🛒 Achat stock",
                total,
                type_stock,
                produit_id,
                quantite,
                prix_unitaire
            ))

            # ==========================
            # Mettre à jour le stock
            # ==========================

            cur.execute("""
                UPDATE stock
                SET
                    quantite = quantite + ?,
                    prix_achat = ?
                WHERE id = ?
            """, (
                quantite,
                prix_unitaire,
                produit_id
            ))

            conn.commit()
            conn.close()

            # Nettoyer le formulaire

            self.quantite_achat.clear()
            self.prix_unitaire_achat.clear()
            self.total_achat.clear()

            self.charger_depenses()

            QMessageBox.information(
                self,
                "Succès",
                f"Achat enregistré avec succès.\n\n"
                f"Produit : {nom_produit}\n"
                f"Quantité : {quantite:g}\n"
                f"Total : {total:,.0f} Ar\n\n"
                f"Le stock a été mis à jour."
            )

            return

        # ==========================
        # DEPENSE NORMALE
        # ==========================

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

        conn = get_connection()
        cur = conn.cursor()

        # Récupérer l'ancienne dépense
        cur.execute("""
            SELECT
                type_stock,
                produit_id,
                quantite,
                prix_unitaire,
                montant
            FROM depenses
            WHERE id = ?
        """, (
            self.id_selectionne,
        ))

        ancienne = cur.fetchone()

        if ancienne is None:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "Dépense introuvable."
            )

            return

        ancien_type = ancienne[0]
        ancien_produit_id = ancienne[1]
        ancienne_quantite = ancienne[2] or 0

        achat_stock = (
            self.categorie.currentText()
            == "🛒 Achat stock"
        )

        # ==========================
        # MODIFICATION ACHAT STOCK
        # ==========================

        if achat_stock:

            if (
                self.produit_achat.currentData() is None
                or self.quantite_achat.text().strip() == ""
                or self.prix_unitaire_achat.text().strip() == ""
            ):

                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Sélectionne un produit et remplis la quantité ainsi que le prix d'achat."
                )

                return

            try:

                nouvelle_quantite = float(
                    self.quantite_achat.text()
                )

                nouveau_prix = float(
                    self.prix_unitaire_achat.text()
                )

            except ValueError:

                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "La quantité et le prix d'achat doivent être des nombres."
                )

                return

            if nouvelle_quantite <= 0 or nouveau_prix < 0:

                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "La quantité doit être supérieure à 0 et le prix ne peut pas être négatif."
                )

                return

            nouveau_produit_id = (
                self.produit_achat.currentData()
            )

            nouveau_nom_produit = (
                self.produit_achat.currentText()
            )

            nouveau_total = (
                nouvelle_quantite
                * nouveau_prix
            )

            # ==========================
            # Restaurer l'ancien stock
            # ==========================

            if (
                ancien_type is not None
                and ancien_produit_id is not None
                and ancienne_quantite
            ):

                cur.execute("""
                    UPDATE stock
                    SET quantite = quantite - ?
                    WHERE id = ?
                """, (
                    ancienne_quantite,
                    ancien_produit_id
                ))

            # ==========================
            # Ajouter le nouveau stock
            # ==========================

            cur.execute("""
                UPDATE stock
                SET
                    quantite = quantite + ?,
                    prix_achat = ?
                WHERE id = ?
            """, (
                nouvelle_quantite,
                nouveau_prix,
                nouveau_produit_id
            ))

            # ==========================
            # Modifier la dépense
            # ==========================

            cur.execute("""
                UPDATE depenses
                SET
                    libelle = ?,
                    categorie = ?,
                    montant = ?,
                    type_stock = ?,
                    produit_id = ?,
                    quantite = ?,
                    prix_unitaire = ?
                WHERE id = ?
            """, (
                f"Achat stock - {nouveau_nom_produit}",
                "🛒 Achat stock",
                nouveau_total,
                self.type_stock_achat.currentText(),
                nouveau_produit_id,
                nouvelle_quantite,
                nouveau_prix,
                self.id_selectionne
            ))

            conn.commit()
            conn.close()

            self.id_selectionne = None

            self.quantite_achat.clear()
            self.prix_unitaire_achat.clear()
            self.total_achat.clear()

            self.charger_depenses()

            QMessageBox.information(
                self,
                "Succès",
                "Achat de stock modifié.\n\n"
                "Le stock a été recalculé."
            )

            return

        # ==========================
        # MODIFICATION DEPENSE NORMALE
        # ==========================

        try:

            montant = float(
                self.montant.text()
            )

        except ValueError:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "Le montant doit être un nombre."
            )

            return

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

        # ==========================
        # Confirmation
        # ==========================

        reponse = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer cette dépense ?"
        )

        if reponse != QMessageBox.Yes:
            return

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # Récupérer les informations
        # de la dépense
        # ==========================

        cur.execute("""
            SELECT
                type_stock,
                produit_id,
                quantite
            FROM depenses
            WHERE id = ?
        """, (
            self.id_selectionne,
        ))

        depense = cur.fetchone()

        if depense is None:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "Dépense introuvable."
            )

            return

        type_stock = depense[0]
        produit_id = depense[1]
        quantite = depense[2] or 0

        # ==========================
        # Si c'est un achat de stock
        # ==========================

        if (
            type_stock is not None
            and produit_id is not None
            and quantite > 0
        ):

            # Retirer la quantité du stock
            cur.execute("""
                UPDATE stock
                SET quantite = quantite - ?
                WHERE id = ?
            """, (
                quantite,
                produit_id
            ))

        # ==========================
        # Supprimer la dépense
        # ==========================

        cur.execute(
            """
            DELETE FROM depenses
            WHERE id = ?
            """,
            (
                self.id_selectionne,
            )
        )

        conn.commit()
        conn.close()

        # ==========================
        # Nettoyer le formulaire
        # ==========================

        self.id_selectionne = None

        self.libelle.clear()
        self.montant.clear()
        self.quantite_achat.clear()
        self.prix_unitaire_achat.clear()
        self.total_achat.clear()

        self.charger_depenses()

        QMessageBox.information(
            self,
            "Succès",
            "Dépense supprimée.\n\n"
            "Si c'était un achat de stock, "
            "la quantité correspondante a été retirée du stock."
        )

    def rechercher_par_date(self):

        date_precise = self.date_precise.date().toString(
            "yyyy-MM-dd"
        )

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                depenses.id,
                depenses.date_depense,
                depenses.libelle,
                depenses.categorie,
                depenses.type_stock,
                stock.nom,
                depenses.quantite,
                depenses.prix_unitaire,
                depenses.montant
            FROM depenses
            LEFT JOIN stock
                ON depenses.produit_id = stock.id
            WHERE date(depenses.date_depense) = ?
            ORDER BY depenses.date_depense DESC
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

                if valeur is None:
                    valeur = ""
                    
                self.table.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )    

    # ==========================
    # Adapter le formulaire
    # ==========================

    def changer_formulaire_depense(self):

        achat_stock = (
            self.categorie.currentText()
            == "🛒 Achat stock"
        )

        # ==========================
        # Formulaire achat de stock
        # ==========================

        self.label_type_stock_achat.setVisible(
            achat_stock
        )

        self.type_stock_achat.setVisible(
            achat_stock
        )

        self.label_produit_achat.setVisible(
            achat_stock
        )

        self.produit_achat.setVisible(
            achat_stock
        )

        self.quantite_achat.setVisible(
            achat_stock
        )

        self.prix_unitaire_achat.setVisible(
            achat_stock
        )

        self.total_achat.setVisible(
            achat_stock
        )

        # ==========================
        # Ancien formulaire
        # ==========================

        self.libelle.setVisible(
            not achat_stock
        )

        self.montant.setVisible(
            not achat_stock
        )

        # La catégorie reste visible
        # pour pouvoir changer de type
        self.categorie.setVisible(True)

        # ==========================
        # Charger les produits
        # ==========================

        if achat_stock:
            self.charger_produits_achat()


    # ==========================
    # Charger les produits du stock
    # ==========================

    def charger_produits_achat(self):

        self.produit_achat.clear()

        type_stock_index = (
            self.type_stock_achat.currentIndex()
        )

        if type_stock_index == 0:
            type_stock = "ingredient"

        elif type_stock_index == 1:
            type_stock = "boisson"

        else:
            type_stock = "biscuit"

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom
            FROM stock
            WHERE type_stock = ?
            ORDER BY nom
        """, (
            type_stock,
        ))

        produits = cur.fetchall()

        conn.close()

        for produit_id, nom in produits:

            self.produit_achat.addItem(
                nom,
                produit_id
            )


    # ==========================
    # Calculer le total de l'achat
    # ==========================

    def calculer_total_achat(self):

        try:

            quantite = float(
                self.quantite_achat.text()
            )

            prix_unitaire = float(
                self.prix_unitaire_achat.text()
            )

            total = (
                quantite
                * prix_unitaire
            )

            self.total_achat.setText(
                f"{total:.0f}"
            )

        except ValueError:

            self.total_achat.clear()