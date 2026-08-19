from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QComboBox,
    QLineEdit,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView 
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
        # Sélection de la période
        # ==========================

        periode_layout = QHBoxLayout()

        periode_label = QLabel("Période :")

        self.periode = QComboBox()

        self.periode.addItems([
            "Aujourd'hui",
            "Hier",
            "Cette semaine",
            "Ce mois",
            "Cette année"
        ])

        periode_layout.addWidget(periode_label)
        periode_layout.addWidget(self.periode)
        periode_layout.addStretch()

        layout.addLayout(periode_layout)

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

        self.cout_ingredients = self.creer_carte(
            "🍳 Coût des ingrédients",
            "0 Ar"
        )

        self.resultat = self.creer_carte(
            "📈 Résultat",
            "0 Ar"
        )

        self.nombre_ventes = self.creer_carte(
            "🧾 Nombre de ventes",
            "0"
        )

        self.panier_moyen = self.creer_carte(
            "🛒 Panier moyen",
            "0 Ar"
        )

        cartes.addWidget(self.ca)
        cartes.addWidget(self.depenses)
        cartes.addWidget(self.cout_ingredients)
        cartes.addWidget(self.resultat)
        cartes.addWidget(self.nombre_ventes)
        cartes.addWidget(self.panier_moyen)

        layout.addLayout(cartes)

        # ==========================
        # Plats les plus vendus
        # ==========================

        titre_plats = QLabel(
            "🍔 Plats les plus vendus"
        )

        titre_plats.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre_plats)

        self.table_plats = QTableWidget()

        self.table_plats.setColumnCount(2)

        self.table_plats.setHorizontalHeaderLabels([
            "Plat",
            "Quantité vendue"
        ])

        self.table_plats.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_plats.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(self.table_plats)

        # ==========================
        # Alertes stock
        # ==========================

        titre_stock = QLabel(
            "📦 État du stock habituel"
        )

        titre_stock.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre_stock)

        self.table_stock = QTableWidget()

        self.table_stock.setColumnCount(4)

        self.table_stock.setHorizontalHeaderLabels([
            "Produit",
            "Quantité",
            "Unité",
            "Seuil"
        ])

        self.table_stock.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_stock.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(self.table_stock)

        # ==========================
        # Stock du jour
        # ==========================

        titre_stock_jour = QLabel(
            "⭐ État du stock du jour"
        )

        titre_stock_jour.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding:10px;
        """)

        self.table_stock_jour = QTableWidget()

        self.table_stock_jour.setColumnCount(5)

        self.table_stock_jour.setHorizontalHeaderLabels([
            "Plat du jour",
            "Produit",
            "Quantité",
            "Unité",
            "Seuil"
        ])

        self.table_stock_jour.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_stock_jour.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        # ==========================
        # Historique des ventes
        # ==========================

        titre_historique = QLabel(
            "📜 Historique des ventes"
        )

        titre_historique.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre_historique)

        # ==========================
        # Recherche dans l'historique
        # ==========================

        self.recherche = QLineEdit()

        self.recherche.setPlaceholderText(
            "🔎 Rechercher un plat..."
        )

        layout.addWidget(
            self.recherche
        )

        self.table_historique = QTableWidget()

        self.table_historique.setColumnCount(5)

        self.table_historique.setHorizontalHeaderLabels([
            "Date",
            "Plat",
            "Quantité",
            "Prix",
            "Total"
        ])

        self.table_historique.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_historique.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(self.table_historique)

        # ==========================
        # Historique des dépenses
        # ==========================

        titre_depenses = QLabel(
            "💸 Historique des dépenses"
        )

        titre_depenses.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre_depenses)

        self.table_depenses = QTableWidget()

        self.table_depenses.setColumnCount(4)

        self.table_depenses.setHorizontalHeaderLabels([
            "Date",
            "Libellé",
            "Catégorie",
            "Montant"
        ])

        self.table_depenses.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_depenses.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(self.table_depenses)

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

        layout.removeWidget(titre_plats)
        layout.removeWidget(self.table_plats)

        layout.removeWidget(titre_stock)
        layout.removeWidget(self.table_stock)

        layout.removeWidget(titre_historique)
        layout.removeWidget(self.recherche)
        layout.removeWidget(self.table_historique)

        layout.removeWidget(titre_depenses)
        layout.removeWidget(self.table_depenses)

        # ==========================
        # Organisation en onglets
        # ==========================

        onglets = QTabWidget()

        # ==========================
        # Style des onglets
        # ==========================

        onglets.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dddddd;
                background: white;
                border-radius: 8px;
            }

            QTabBar::tab {
                background: #eeeeee;
                padding: 10px 20px;
                margin-right: 3px;
                border-radius: 6px;
                font-size: 14px;
            }

            QTabBar::tab:selected {
                background: #2D313A;
                color: white;
                font-weight: bold;
            }

            QTabBar::tab:hover {
                background: #404652;
                color: white;
            }
        """)

        # --------------------------
        # Onglet Produits
        # --------------------------

        page_produits = QWidget()
        layout_produits = QVBoxLayout()

        layout_produits.addWidget(titre_plats)
        layout_produits.addWidget(self.table_plats)

        page_produits.setLayout(
            layout_produits
        )

        onglets.addTab(
            page_produits,
            "🍔 Produits"
        )

        # --------------------------
        # Onglet Stock
        # --------------------------

        page_stock = QWidget()
        layout_stock = QVBoxLayout()

        layout_stock.addWidget(titre_stock)
        layout_stock.addWidget(self.table_stock)

        layout_stock.addWidget(titre_stock_jour)
        layout_stock.addWidget(self.table_stock_jour)

        page_stock.setLayout(
            layout_stock
        )

        onglets.addTab(
            page_stock,
            "📦 Stock"
        )

        # --------------------------
        # Onglet Historique
        # --------------------------

        page_historique = QWidget()
        layout_historique = QVBoxLayout()

        layout_historique.addWidget(
            titre_historique
        )

        layout_historique.addWidget(
            self.recherche
        )

        layout_historique.addWidget(
            self.table_historique
        )

        layout_historique.addWidget(
            titre_depenses
        )

        layout_historique.addWidget(
            self.table_depenses
        )

        page_historique.setLayout(
            layout_historique
        )

        onglets.addTab(
            page_historique,
            "📜 Historique"
        )

        # --------------------------
        # Ajouter les onglets
        # --------------------------

        layout.addWidget(onglets)

        onglets.setMinimumHeight(400)

        self.setLayout(layout)

        # ==========================
        # Connexion
        # ==========================

        self.btn_actualiser.clicked.connect(
            self.actualiser
        )

        self.periode.currentIndexChanged.connect(
            self.actualiser
        )

        self.recherche.textChanged.connect(
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
        # Déterminer la période
        # ==========================

        periode = self.periode.currentText()

        if periode == "Aujourd'hui":

            condition = """
                date(date_vente) = date('now')
            """

            condition_depenses = """
                date(date_depense) = date('now')
            """

        elif periode == "Hier":

            condition = """
                date(date_vente) = date('now', '-1 day')
            """

            condition_depenses = """
                date(date_depense) = date('now', '-1 day')
            """

        elif periode == "Cette semaine":

            condition = """
                date(date_vente)
                >= date('now', 'weekday 0', '-6 days')
            """

            condition_depenses = """
                date(date_depense)
                >= date('now', 'weekday 0', '-6 days')
            """

        elif periode == "Ce mois":

            condition = """
                strftime('%Y-%m', date_vente)
                = strftime('%Y-%m', 'now')
            """

            condition_depenses = """
                strftime('%Y-%m', date_depense)
                = strftime('%Y-%m', 'now')
            """

        elif periode == "Cette année":

            condition = """
                strftime('%Y', date_vente)
                = strftime('%Y', 'now')
            """

            condition_depenses = """
                strftime('%Y', date_depense)
                = strftime('%Y', 'now')
            """

        else:

            condition = """
                date(date_vente) = date('now')
            """

            condition_depenses = """
                date(date_depense) = date('now')
            """

        # ==========================
        # Chiffre d'affaires
        # ==========================

        cur.execute(f"""
            SELECT COALESCE(
                SUM(total),
                0
            )
            FROM ventes
            WHERE {condition}
        """)

        chiffre_affaires = cur.fetchone()[0]

        # ==========================
        # Dépenses
        # ==========================

        cur.execute(f"""
            SELECT COALESCE(
                SUM(montant),
                0
            )
            FROM depenses
            WHERE {condition_depenses}
        """)

        total_depenses = cur.fetchone()[0]

        # ==========================
        # Nombre de ventes
        # ==========================

        cur.execute(f"""
            SELECT COUNT(*)
            FROM ventes
            WHERE {condition}
        """)

        nombre_ventes = cur.fetchone()[0]

        # ==========================
        # Coût des ingrédients
        # ==========================

        cur.execute(f"""
            SELECT
                COALESCE(
                    SUM(
                        details_vente.quantite
                        * recettes.quantite
                        * stock.prix_achat
                    ),
                    0
                )
            FROM details_vente
            JOIN ventes
                ON details_vente.vente_id = ventes.id
            JOIN recettes
                ON details_vente.plat_id = recettes.plat_id
            JOIN stock
                ON recettes.stock_id = stock.id
            WHERE details_vente.type_plat = 'habituel'
            AND {condition}
        """)

        cout_ingredients_habituels = cur.fetchone()[0]

        cur.execute(f"""
            SELECT
                COALESCE(
                    SUM(
                        details_vente.quantite
                        * recettes_plats_du_jour.quantite
                        * stock.prix_achat
                    ),
                    0
                )
            FROM details_vente
            JOIN ventes
                ON details_vente.vente_id = ventes.id
            JOIN recettes_plats_du_jour
                ON details_vente.plat_id =
                   recettes_plats_du_jour.plat_du_jour_id
            JOIN stock
                ON recettes_plats_du_jour.stock_id = stock.id
            WHERE details_vente.type_plat = 'jour'
            AND {condition}
        """)

        cout_ingredients_jour = cur.fetchone()[0]

        cout_ingredients = (
            cout_ingredients_habituels
            + cout_ingredients_jour
        )

        # ==========================
        # Résultat
        # ==========================

        resultat = (
            chiffre_affaires
            - total_depenses
        )

        # ==========================
        # Panier moyen
        # ==========================

        if nombre_ventes > 0:

            panier_moyen = (
                chiffre_affaires
                / nombre_ventes
            )

        else:

            panier_moyen = 0

        # ==========================
        # Plats les plus vendus
        # ==========================

        cur.execute(f"""
            SELECT
                details_vente.plat,
                SUM(details_vente.quantite) AS quantite_totale
            FROM details_vente
            JOIN ventes
                ON details_vente.vente_id = ventes.id
            WHERE {condition}
            GROUP BY details_vente.plat
            ORDER BY quantite_totale DESC
        """)

        plats_vendus = cur.fetchall()

        # ==========================
        # Historique des ventes
        # ==========================

        recherche = self.recherche.text().strip()

        if recherche:

            cur.execute(f"""
                SELECT
                    ventes.date_vente,
                    details_vente.plat,
                    details_vente.quantite,
                    details_vente.prix,
                    details_vente.quantite * details_vente.prix
                FROM details_vente
                JOIN ventes
                    ON details_vente.vente_id = ventes.id
                WHERE {condition}
                AND details_vente.plat LIKE ?
                ORDER BY ventes.date_vente DESC
            """, (
                f"%{recherche}%",
            ))

        else:

            cur.execute(f"""
                SELECT
                    ventes.date_vente,
                    details_vente.plat,
                    details_vente.quantite,
                    details_vente.prix,
                    details_vente.quantite * details_vente.prix
                FROM details_vente
                JOIN ventes
                    ON details_vente.vente_id = ventes.id
                WHERE {condition}
                ORDER BY ventes.date_vente DESC
            """)

        historique = cur.fetchall()

        # ==========================
        # Historique des dépenses
        # ==========================

        if periode == "Aujourd'hui":

            condition_depenses = """
                date(date_depense) = date('now')
            """

        elif periode == "Hier":

            condition_depenses = """
                date(date_depense) = date('now', '-1 day')
            """

        elif periode == "Cette semaine":

            condition_depenses = """
                date(date_depense)
                >= date('now', 'weekday 0', '-6 days')
            """

        elif periode == "Ce mois":

            condition_depenses = """
                strftime('%Y-%m', date_depense)
                = strftime('%Y-%m', 'now')
            """

        elif periode == "Cette année":

            condition_depenses = """
                strftime('%Y', date_depense)
                = strftime('%Y', 'now')
            """

        else:

            condition_depenses = """
                date(date_depense) = date('now')
            """

        cur.execute(f"""
            SELECT
                date_depense,
                libelle,
                categorie,
                montant
            FROM depenses
            WHERE {condition_depenses}
            ORDER BY date_depense DESC
        """)

        historique_depenses = cur.fetchall()

        # ==========================
        # État du stock
        # ==========================

        cur.execute("""
            SELECT
                nom,
                quantite,
                unite,
                seuil
            FROM stock
            ORDER BY quantite ASC
        """)

        stock = cur.fetchall()   

        # ==========================
        # État du stock du jour
        # ==========================

        cur.execute("""
            SELECT
                plats_du_jour.nom,
                stock.nom,
                stock_plats_du_jour.quantite,
                stock.unite,
                stock_plats_du_jour.seuil
            FROM stock_plats_du_jour
            JOIN plats_du_jour
                ON stock_plats_du_jour.plat_du_jour_id
                = plats_du_jour.id
            JOIN stock
                ON stock_plats_du_jour.stock_id
                = stock.id
            WHERE plats_du_jour.date_jour =
                date('now', 'localtime')
            ORDER BY plats_du_jour.nom, stock.nom
        """)

        stock_jour = cur.fetchall()

        # ==========================
        # Affichage
        # ==========================

        self.ca.valeur.setText(
            f"{chiffre_affaires:,.0f} Ar"
        )

        self.depenses.valeur.setText(
            f"{total_depenses:,.0f} Ar"
        )

        self.cout_ingredients.valeur.setText(
            f"{cout_ingredients:,.0f} Ar"
        )

        self.resultat.valeur.setText(
            f"{resultat:,.0f} Ar"
        )

        self.nombre_ventes.valeur.setText(
            str(nombre_ventes)
        )

        self.panier_moyen.valeur.setText(
            f"{panier_moyen:,.0f} Ar"
        )

        # ==========================
        # Affichage des plats vendus
        # ==========================

        self.table_plats.setRowCount(
            len(plats_vendus)
        )

        for ligne, plat in enumerate(plats_vendus):

            self.table_plats.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    str(plat[0])
                )
            )

            self.table_plats.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    str(plat[1])
                )
            )

        # ==========================
        # Affichage du stock
        # ==========================

        self.table_stock.setRowCount(
            len(stock)
        )

        for ligne, produit in enumerate(stock):

            nom, quantite, unite, seuil = produit

            valeurs = [
                nom,
                quantite,
                unite,
                seuil
            ]

            for colonne, valeur in enumerate(valeurs):

                item = QTableWidgetItem(
                    str(valeur)
                )

                self.table_stock.setItem(
                    ligne,
                    colonne,
                    item
                )

            # ==========================
            # Alerte stock faible
            # ==========================

            if quantite <= seuil:

                for colonne in range(4):

                    item = self.table_stock.item(
                        ligne,
                        colonne
                    )

                    if item:

                        item.setText(
                            "⚠️ " + item.text()
                        )

                        font = item.font()
                        font.setBold(True)

                        item.setFont(font)

        # ==========================
        # Affichage du stock du jour
        # ==========================

        self.table_stock_jour.setRowCount(
            len(stock_jour)
        )

        for ligne, produit in enumerate(stock_jour):

            plat, nom, quantite, unite, seuil = produit

            valeurs = [
                plat,
                nom,
                quantite,
                unite,
                seuil
            ]

            for colonne, valeur in enumerate(valeurs):

                item = QTableWidgetItem(
                    str(valeur)
                )

                self.table_stock_jour.setItem(
                    ligne,
                    colonne,
                    item
                )

            # Alerte stock faible
            if quantite <= seuil:

                for colonne in range(5):

                    item = self.table_stock_jour.item(
                        ligne,
                        colonne
                    )

                    if item:

                        item.setText(
                            "⚠️ " + item.text()
                        )

                        font = item.font()
                        font.setBold(True)

                        item.setFont(font)

        # ==========================
        # Affichage de l'historique
        # ==========================

        self.table_historique.setRowCount(
            len(historique)
        )

        for ligne, vente in enumerate(historique):

            for colonne, valeur in enumerate(vente):

                self.table_historique.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

        # ==========================
        # Affichage des dépenses
        # ==========================

        self.table_depenses.setRowCount(
            len(historique_depenses)
        )

        for ligne, depense in enumerate(
            historique_depenses
        ):

            for colonne, valeur in enumerate(
                depense
            ):

                self.table_depenses.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )        
    
        conn.close()