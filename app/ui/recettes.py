from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)

from app.database.database import get_connection


class RecettesPage(QWidget):

    def __init__(self):
        super().__init__()
        self.recette_selectionnee = None

        layout = QVBoxLayout()

        titre = QLabel("🍔 Gestion des recettes")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre)

        # Choix du type de recette

        self.type_recette = QComboBox()

        self.type_recette.addItems([
            "🍔 Plat habituel",
            "⭐ Plat du jour",
            "🛍️ Vitrine",
            "🥐 Petit déjeuner"
        ])

        layout.addWidget(
            QLabel("Type de recette")
        )

        layout.addWidget(
            self.type_recette
        )

        # Choix du plat

        self.plat = QComboBox()

        layout.addWidget(QLabel("Plat"))

        layout.addWidget(self.plat)

        # Choix de l'ingrédient

        self.stock = QComboBox()

        layout.addWidget(QLabel("Ingrédient"))

        layout.addWidget(self.stock)

        # Quantité

        self.quantite = QLineEdit()

        self.quantite.setPlaceholderText(
            "Quantité utilisée"
        )

        layout.addWidget(self.quantite)

        # Bouton

        self.btn_ajouter = QPushButton(
            "➕ Ajouter à la recette"
        )

        layout.addWidget(self.btn_ajouter)

        # Tableau

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "Plat",
            "Ingrédient",
            "Quantité"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table.cellClicked.connect(
            self.selectionner_recette
        )

        self.label_cout_total = QLabel(
            "💰 Coût total des ingrédients : 0.00 Ar"
        )

        self.label_cout_total.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(
            self.label_cout_total
        )

        # ==========================
        # PRIX DE VENTE
        # ==========================

        self.label_prix_vente = QLabel(
            "💵 Prix de vente : 0.00 Ar"
        )

        self.label_prix_vente.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            padding:5px;
        """)

        layout.addWidget(
            self.label_prix_vente
        )

        # ==========================
        # MARGE BRUTE
        # ==========================

        self.label_marge = QLabel(
            "📈 Marge brute : 0.00 Ar"
        )

        self.label_marge.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            padding:5px;
        """)

        layout.addWidget(
            self.label_marge
        )

        layout.addWidget(self.table)
        boutons = QHBoxLayout()

        self.btn_modifier = QPushButton("✏ Modifier")
        self.btn_supprimer = QPushButton("🗑 Supprimer")

        boutons.addWidget(self.btn_modifier)
        boutons.addWidget(self.btn_supprimer)

        layout.addLayout(boutons)

        self.btn_modifier.clicked.connect(
            self.modifier_recette
        )

        self.btn_supprimer.clicked.connect(
            self.supprimer_recette
        )

        self.setLayout(layout)

        self.charger_plats()
        self.charger_stock()
        self.charger_recettes()

        self.btn_ajouter.clicked.connect(
            self.ajouter_recette
        )
        self.plat.currentIndexChanged.connect(
            self.charger_recettes
        )
        self.type_recette.currentIndexChanged.connect(
            self.changer_type_recette
        )

    def changer_type_recette(self):

        self.recette_selectionnee = None

        self.charger_plats()
        self.charger_recettes()    

    def charger_plats(self):

        conn = get_connection()
        cur = conn.cursor()

        self.plat.clear()

        if self.type_recette.currentIndex() == 0:

            # 🍔 Plat habituel
            cur.execute("""
                SELECT id, nom
                FROM plats
                WHERE categorie NOT IN (
                    'Vitrine',
                    'Petit déjeuner',
                    'Boisson',
                    'Biscuits'
                )
                ORDER BY nom
            """)

        elif self.type_recette.currentIndex() == 1:

            # ⭐ Plat du jour
            cur.execute("""
                SELECT id, nom
                FROM plats_du_jour
                WHERE disponible = 1
                AND date_jour = date('now', 'localtime')
                ORDER BY nom
            """)

        elif self.type_recette.currentIndex() == 2:

            # 🛍️ Vitrine
            cur.execute("""
                SELECT id, nom
                FROM plats
                WHERE categorie = 'Vitrine'
                ORDER BY nom
            """)

        elif self.type_recette.currentIndex() == 3:

            # 🥐 Petit déjeuner
            cur.execute("""
                SELECT id, nom
                FROM plats
                WHERE categorie = 'Petit déjeuner'
                ORDER BY nom
            """)

        for plat_id, nom in cur.fetchall():

            self.plat.addItem(
                nom,
                plat_id
            )

        conn.close()


    def charger_stock(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom
            FROM stock
            ORDER BY nom
        """)

        produits = cur.fetchall()

        print("Produits trouvés :", produits)   # <-- ajoute cette ligne

        self.stock.clear()

        for stock_id, nom in produits:
            self.stock.addItem(
                nom,
                stock_id
            )

        print("Nombre d'éléments :", self.stock.count())  # <-- ajoute cette ligne

        conn.close()

    def ajouter_recette(self):

        if self.quantite.text() == "":
            QMessageBox.warning(
                self,
                "Erreur",
                "Entre une quantité."
            )
            return

        if self.plat.currentData() is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un plat."
            )
            return

        if self.stock.currentData() is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un ingrédient."
            )
            return

        try:
            quantite = float(
                self.quantite.text().replace(",", ".")
            )
        except ValueError:
            QMessageBox.warning(
                self,
                "Erreur",
                "La quantité doit être un nombre."
            )
            return

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # RECETTES
        # ==========================

        # 🍔 Plat habituel
        # 🛍️ Vitrine
        # 🥐 Petit déjeuner
        if self.type_recette.currentIndex() in (0, 2, 3):

            cur.execute("""
                SELECT COUNT(*)
                FROM recettes
                WHERE plat_id = ?
                AND stock_id = ?
            """, (
                self.plat.currentData(),
                self.stock.currentData()
            ))

            existe = cur.fetchone()[0]

            if existe > 0:

                conn.close()

                QMessageBox.warning(
                    self,
                    "Doublon",
                    "Cet ingrédient est déjà présent dans cette recette."
                )

                return

            cur.execute("""
                INSERT INTO recettes(
                    plat_id,
                    stock_id,
                    quantite
                )
                VALUES(?,?,?)
            """, (
                self.plat.currentData(),
                self.stock.currentData(),
                quantite
            ))

        # ==========================
        # PLAT DU JOUR
        # ==========================

        elif self.type_recette.currentIndex() == 1:

            cur.execute("""
                SELECT COUNT(*)
                FROM recettes_plats_du_jour
                WHERE plat_du_jour_id = ?
                AND stock_id = ?
            """, (
                self.plat.currentData(),
                self.stock.currentData()
            ))

            existe = cur.fetchone()[0]

            if existe > 0:

                conn.close()

                QMessageBox.warning(
                    self,
                    "Doublon",
                    "Cet ingrédient est déjà présent dans cette recette."
                )

                return

            cur.execute("""
                INSERT INTO recettes_plats_du_jour(
                    plat_du_jour_id,
                    stock_id,
                    quantite
                )
                VALUES(?,?,?)
            """, (
                self.plat.currentData(),
                self.stock.currentData(),
                quantite
            ))

        conn.commit()
        conn.close()

        self.quantite.clear()

        self.charger_recettes()

        QMessageBox.information(
            self,
            "Succès",
            "Ingrédient ajouté à la recette."
        )

    def charger_recettes(self):

        conn = get_connection()
        cur = conn.cursor()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "Ingrédient",
            "Quantité utilisée",
            "Prix unitaire (Ar)",
            "Coût (Ar)"
        ])

        # ==========================
        # PLAT HABITUEL
        # ==========================

        if self.type_recette.currentIndex() == 0:

            cur.execute("""
                SELECT
                    recettes.id,
                    recettes.stock_id,
                    stock.nom,
                    recettes.quantite,
                    stock.prix_achat
                FROM recettes
                JOIN stock
                    ON recettes.stock_id = stock.id
                WHERE recettes.plat_id = ?
                ORDER BY stock.nom
            """, (
                self.plat.currentData(),
            ))

        # ==========================
        # PLAT DU JOUR
        # ==========================

        elif self.type_recette.currentIndex() == 1:

            cur.execute("""
                SELECT
                    recettes_plats_du_jour.id,
                    recettes_plats_du_jour.stock_id,
                    stock.nom,
                    recettes_plats_du_jour.quantite,
                    stock.prix_achat
                FROM recettes_plats_du_jour
                JOIN stock
                    ON recettes_plats_du_jour.stock_id = stock.id
                WHERE recettes_plats_du_jour.plat_du_jour_id = ?
                ORDER BY stock.nom
            """, (
                self.plat.currentData(),
            ))

        # ==========================
        # VITRINE / PETIT DÉJEUNER
        # ==========================

        elif self.type_recette.currentIndex() in (2, 3):

            cur.execute("""
                SELECT
                    recettes.id,
                    recettes.stock_id,
                    stock.nom,
                    recettes.quantite,
                    stock.prix_achat
                FROM recettes
                JOIN stock
                    ON recettes.stock_id = stock.id
                WHERE recettes.plat_id = ?
                ORDER BY stock.nom
            """, (
                self.plat.currentData(),
            ))    

        recettes = cur.fetchall()

        self.table.setRowCount(
            len(recettes)
        )

        for ligne, recette in enumerate(recettes):

            # Données de la recette
            nom_ingredient = recette[2]
            quantite = float(recette[3])
            prix_unitaire = float(recette[4] or 0)

            # Calcul du coût de l'ingrédient
            cout = quantite * prix_unitaire

            # Nom de l'ingrédient
            self.table.setItem(
                ligne,
                0,
                QTableWidgetItem(nom_ingredient)
            )

            # Quantité utilisée
            self.table.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    str(quantite)
                )
            )

            # Prix unitaire
            self.table.setItem(
                ligne,
                2,
                QTableWidgetItem(
                    f"{prix_unitaire:.2f}"
                )
            )

            # Coût
            self.table.setItem(
                ligne,
                3,
                QTableWidgetItem(
                    f"{cout:.2f}"
                )
            )

            # ID de la recette
            self.table.item(
                ligne,
                0
            ).setData(
                1000,
                recette[0]
            )

            # ID du produit dans le stock
            self.table.item(
                ligne,
                0
            ).setData(
                1001,
                recette[1]
            )

        # ==========================
        # COÛT TOTAL DE LA RECETTE
        # ==========================

        cout_total = 0

        for recette in recettes:
            quantite = float(recette[3])
            prix_unitaire = float(recette[4] or 0)

            cout_total += quantite * prix_unitaire

        # Affichage du coût total
        self.label_cout_total.setText(
            f"💰 Coût total des ingrédients : {cout_total:.2f} Ar"       
        )

        # ==========================
        # PRIX DE VENTE DU PLAT
        # ==========================

        prix_vente = 0

        if self.type_recette.currentIndex() == 1:
            # ⭐ Plat du jour
            cur.execute("""
                SELECT prix
                FROM plats_du_jour
                WHERE id = ?
            """, (
                self.plat.currentData(),
            ))
        else:
            # 🍔 Plat habituel / 🛍️ Vitrine / 🥐 Petit déjeuner
            cur.execute("""
                SELECT prix
                FROM plats
                WHERE id = ?
            """, (
                self.plat.currentData(),
            ))

        resultat_prix = cur.fetchone()

        if resultat_prix:
            prix_vente = float(resultat_prix[0] or 0)

        self.label_prix_vente.setText(
            f"💵 Prix de vente : {prix_vente:,.0f} Ar"
        )

        # ==========================
        # MARGE BRUTE
        # ==========================

        marge = prix_vente - cout_total

        self.label_marge.setText(
            f"📈 Marge brute : {marge:,.0f} Ar"
        )

        conn.close()

    def actualiser(self):

        self.charger_plats()
        self.charger_stock()
        self.charger_recettes()

    def selectionner_recette(self, ligne, colonne):

        # ID de la recette
        self.recette_selectionnee = self.table.item(
            ligne,
            0
        ).data(1000)

        # ID exact de l'ingrédient
        stock_id = self.table.item(
            ligne,
            0
        ).data(1001)

        # Sélectionner l'ingrédient avec son ID
        index = self.stock.findData(
            stock_id
        )

        if index >= 0:
            self.stock.setCurrentIndex(
                index
            )

        # Quantité
        self.quantite.setText(
            self.table.item(
                ligne,
                1
            ).text()
        )

    def modifier_recette(self):

        if self.recette_selectionnee is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne une recette."
            )

            return

        if self.stock.currentData() is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un ingrédient."
            )

            return

        try:

            quantite = float(
                self.quantite.text().replace(",", ".")
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Erreur",
                "La quantité doit être un nombre."
            )

            return

        if quantite <= 0:

            QMessageBox.warning(
                self,
                "Erreur",
                "La quantité doit être supérieure à 0."
            )

            return

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # PLAT HABITUEL
        # VITRINE
        # PETIT DÉJEUNER
        # ==========================

        if self.type_recette.currentIndex() in (0, 2, 3):

            cur.execute("""
                UPDATE recettes
                SET stock_id = ?,
                    quantite = ?
                WHERE id = ?
            """, (
                self.stock.currentData(),
                quantite,
                self.recette_selectionnee
            ))

        # ==========================
        # PLAT DU JOUR
        # ==========================

        elif self.type_recette.currentIndex() == 1:

            cur.execute("""
                UPDATE recettes_plats_du_jour
                SET stock_id = ?,
                    quantite = ?
                WHERE id = ?
            """, (
                self.stock.currentData(),
                quantite,
                self.recette_selectionnee
            ))

        conn.commit()
        conn.close()

        self.recette_selectionnee = None

        self.quantite.clear()

        self.charger_recettes()

        QMessageBox.information(
            self,
            "Succès",
            "Recette modifiée."
        )

    # ==========================
    # Supprimer
    # ==========================

    def supprimer_recette(self):

        if self.recette_selectionnee is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne une recette."
            )

            return

        reponse = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer cet ingrédient de la recette ?"
        )

        if reponse != QMessageBox.Yes:
            return

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # PLAT HABITUEL
        # VITRINE
        # PETIT DÉJEUNER
        # ==========================

        if self.type_recette.currentIndex() in (0, 2, 3):

            cur.execute("""
                DELETE FROM recettes
                WHERE id = ?
            """, (
                self.recette_selectionnee,
            ))

        # ==========================
        # PLAT DU JOUR
        # ==========================

        elif self.type_recette.currentIndex() == 1:

            cur.execute("""
                DELETE FROM recettes_plats_du_jour
                WHERE id = ?
            """, (
                self.recette_selectionnee,
            ))

        conn.commit()
        conn.close()

        self.recette_selectionnee = None

        self.quantite.clear()

        self.charger_recettes()

        QMessageBox.information(
            self,
            "Succès",
            "Ingrédient supprimé."
        )