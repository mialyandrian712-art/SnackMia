from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QFrame,
    QMessageBox
)

from PySide6.QtCore import Signal, Qt

from app.database.database import get_connection


class CaissePage(QWidget):

    vente_enregistree = Signal()

    def __init__(self):
        super().__init__()

        principal = QHBoxLayout()

        # ==========================
        # Partie gauche : Produits
        # ==========================

        gauche = QWidget()
        gauche_layout = QVBoxLayout()

        titre = QLabel("🧾 Caisse")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        gauche_layout.addWidget(titre)

        # ==========================
        # CATÉGORIES
        # ==========================

        self.categories = QHBoxLayout()
        self.sous_categories = QHBoxLayout()

        self.btn_tous = QPushButton("Tous")
        self.btn_viandes = QPushButton("🥩 Viandes")
        self.btn_riz = QPushButton("🍚 Riz")
        self.btn_minesao = QPushButton("🍜 Mine-sao")
        self.btn_soupe = QPushButton("🍲 Soupe")
        self.btn_gratin = QPushButton("🧀 Gratin")
        self.btn_poutines = QPushButton("🍟 Poutines")
        self.btn_burger = QPushButton("🍔 Burger")
        self.btn_sandwich = QPushButton("🥪 Sandwich")
        self.btn_pizza = QPushButton("🍕 Pizza")
        self.btn_snack = QPushButton("🍿 Snack")
        
        self.btn_boissons = QPushButton("🥤 Boissons")
        self.btn_plats_du_jour = QPushButton("⭐ Plats du jour")
        self.btn_petit_dejeuner = QPushButton("🥐 Petit déjeuner")
        self.btn_vitrine = QPushButton("🛍️ Vitrine")
        self.btn_biscuits = QPushButton("🍪 Biscuits")

        self.btn_tous.clicked.connect(
            lambda: self.charger_produits()
        )

        self.btn_viandes.clicked.connect(
            lambda: self.charger_produits("Viandes")
        )

        self.btn_riz.clicked.connect(
            lambda: self.charger_produits("Riz")
        )

        self.btn_minesao.clicked.connect(
            lambda: self.charger_produits("Mine-sao")
        )

        self.btn_soupe.clicked.connect(
            lambda: self.charger_produits("Soupe")
        )

        self.btn_gratin.clicked.connect(
            lambda: self.charger_produits("Gratin")
        )

        self.btn_poutines.clicked.connect(
            lambda: self.charger_produits("Poutines")
        )

        self.btn_burger.clicked.connect(
            lambda: self.charger_produits("Burger")
        )

        self.btn_sandwich.clicked.connect(
            lambda: self.charger_produits("Sandwich")
        )

        self.btn_pizza.clicked.connect(
            lambda: self.charger_produits("Pizza")
        )

        self.btn_snack.clicked.connect(
            lambda: self.charger_produits("Snack")
        )

        self.btn_boissons.clicked.connect(
            lambda: self.charger_produits("Boisson")
        )

        self.btn_petit_dejeuner.clicked.connect(
            lambda: self.charger_produits("Petit déjeuner")
        )

        self.btn_vitrine.clicked.connect(
            lambda: self.charger_produits("Vitrine")
        )

        self.btn_biscuits.clicked.connect(
            lambda: self.charger_produits("Biscuits")
        )

        self.btn_plats_du_jour.clicked.connect(
            lambda: self.charger_produits("Plat du jour")
        )

        # ==========================
        # GRANDES SECTIONS
        # ==========================

        self.categories.addWidget(self.btn_tous)
        self.categories.addWidget(self.btn_boissons)
        self.categories.addWidget(self.btn_plats_du_jour)
        self.categories.addWidget(self.btn_petit_dejeuner)
        self.categories.addWidget(self.btn_vitrine)
        self.categories.addWidget(self.btn_biscuits)

        # ==========================
        # SOUS-CATÉGORIES DES PLATS
        # ==========================

        self.sous_categories.addWidget(self.btn_viandes)
        self.sous_categories.addWidget(self.btn_riz)
        self.sous_categories.addWidget(self.btn_minesao)
        self.sous_categories.addWidget(self.btn_soupe)
        self.sous_categories.addWidget(self.btn_gratin)
        self.sous_categories.addWidget(self.btn_poutines)
        self.sous_categories.addWidget(self.btn_burger)
        self.sous_categories.addWidget(self.btn_sandwich)
        self.sous_categories.addWidget(self.btn_pizza)
        self.sous_categories.addWidget(self.btn_snack)

        gauche_layout.addLayout(self.categories)
        gauche_layout.addLayout(self.sous_categories)

        self.liste_produits = QListWidget()

        self.panier = {}

        self.liste_produits.itemClicked.connect(
            self.ajouter_au_ticket
        )

        gauche_layout.addWidget(
            self.liste_produits
        )

        gauche.setLayout(
            gauche_layout
        )

        # ==========================
        # Partie droite : Ticket
        # ==========================

        droite = QFrame()

        droite.setStyleSheet("""
            QFrame{
                background:#F5F5F5;
                border-radius:10px;
            }
        """)

        droite_layout = QVBoxLayout()

        titre_ticket = QLabel("Ticket")

        titre_ticket.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        droite_layout.addWidget(
            titre_ticket
        )

        self.ticket = QListWidget()

        droite_layout.addWidget(
            self.ticket
        )

        self.total = QLabel(
            "Total : 0 Ar"
        )

        self.total.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        droite_layout.addWidget(
            self.total
        )

        self.btn_vider = QPushButton(
            "🗑️ Vider le ticket"
        )

        self.btn_vider.setMinimumHeight(50)

        droite_layout.addWidget(
            self.btn_vider
        )

        self.btn_encaisser = QPushButton(
            "💵 Encaisser"
        )

        self.btn_encaisser.setMinimumHeight(50)

        droite_layout.addWidget(
            self.btn_encaisser
        )

        droite.setLayout(
            droite_layout
        )

        principal.addWidget(
            gauche,
            2
        )

        principal.addWidget(
            droite,
            1
        )

        self.setLayout(
            principal
        )

        self.charger_produits()

        self.btn_vider.clicked.connect(
            self.vider_ticket
        )

        self.btn_encaisser.clicked.connect(
            self.encaisser
        )

    # =========================================================
    # CHARGER LES PLATS HABITUELS + PLATS DU JOUR
    # =========================================================

    def charger_produits(self, categorie=None):

        conn = get_connection()
        cur = conn.cursor()

        self.liste_produits.clear()

        # =========================================================
        # PLATS HABITUELS
        # =========================================================

        if categorie is None:

            item_titre = QListWidgetItem(
                "🍔 PLATS HABITUELS"
            )

            item_titre.setFlags(
                Qt.NoItemFlags
            )

            self.liste_produits.addItem(
                item_titre
            )

            cur.execute("""
                SELECT
                    id,
                    nom,
                    prix
                FROM plats
                WHERE disponible = 1
                ORDER BY categorie, nom
            """)

        elif categorie in [
            "Viandes",
            "Riz",
            "Mine-sao",
            "Soupe",
            "Gratin",
            "Poutines",
            "Burger",
            "Sandwich",
            "Pizza",
            "Snack",
            "Boisson",
            "Petit déjeuner",
            "Vitrine",
            "Biscuits"
        ]:

            titre = "🥤 BOISSONS" if categorie == "Boisson" else "🍔 PLATS HABITUELS"

            item_titre = QListWidgetItem(
                titre
            )

            item_titre.setFlags(
                Qt.NoItemFlags
            )

            self.liste_produits.addItem(
                item_titre
            )

            cur.execute("""
                SELECT
                    id,
                    nom,
                    prix
                FROM plats
                WHERE disponible = 1
                AND categorie = ?
                ORDER BY nom
            """, (
                categorie,
            ))

        # =========================================================
        # PLATS DU JOUR
        # =========================================================

        elif categorie == "Plat du jour":

            item_titre = QListWidgetItem(
                "⭐ PLATS DU JOUR"
            )

            item_titre.setFlags(
                Qt.NoItemFlags
            )

            self.liste_produits.addItem(
                item_titre
            )

            cur.execute("""
                SELECT
                    id,
                    nom,
                    prix
                FROM plats_du_jour
                WHERE disponible = 1
                AND date_jour = date('now', 'localtime')
                ORDER BY nom
            """)

        else:
            conn.close()
            return

        produits = cur.fetchall()

        # =========================================================
        # AFFICHAGE
        # =========================================================

        for plat_id, nom, prix in produits:

            item = QListWidgetItem(
                f"{nom} - {int(prix)} Ar"
            )

            item.setData(
                Qt.UserRole,
                {
                    "type": (
                        "jour"
                        if categorie == "Plat du jour"
                        else "habituel"
                    ),
                    "id": plat_id,
                    "nom": nom,
                    "prix": prix
                }
            )

            self.liste_produits.addItem(
                item
            )

        conn.close()

    # =========================================================
    # AJOUTER AU TICKET
    # =========================================================

    def ajouter_au_ticket(self, item):

        infos = item.data(
            Qt.UserRole
        )

        # Ligne titre ou ligne non cliquable
        if not infos:
            return

        cle = (
            infos["type"],
            infos["id"]
        )

        if cle in self.panier:

            self.panier[cle]["quantite"] += 1

        else:

            self.panier[cle] = {
                "type": infos["type"],
                "id": infos["id"],
                "nom": infos["nom"],
                "prix": infos["prix"],
                "quantite": 1
            }

        self.actualiser_ticket()

    # =========================================================
    # ACTUALISER LE TICKET
    # =========================================================

    def actualiser_ticket(self):

        self.ticket.clear()

        total = 0

        for infos in self.panier.values():

            quantite = infos["quantite"]
            prix = infos["prix"]

            sous_total = (
                quantite * prix
            )

            total += sous_total

            self.ticket.addItem(
                f"{infos['nom']}   "
                f"x{quantite}   "
                f"{sous_total:,.0f} Ar"
            )

        self.total.setText(
            f"Total : {total:,.0f} Ar"
        )

    # =========================================================
    # VIDER LE TICKET
    # =========================================================

    def vider_ticket(self):

        self.panier.clear()

        self.actualiser_ticket()

    # =========================================================
    # ENCAISSER
    # =========================================================

    def encaisser(self):

        if not self.panier:

            QMessageBox.warning(
                self,
                "Ticket vide",
                "Ajoutez au moins un produit."
            )

            return

        conn = get_connection()
        cur = conn.cursor()

        try:

            # =================================================
            # 1. VÉRIFIER TOUS LES STOCKS
            # =================================================

            for infos in self.panier.values():

                quantite_plat = infos[
                    "quantite"
                ]

                plat_id = infos["id"]

                # =============================================
                # PLAT HABITUEL
                # =============================================

                if infos["type"] == "habituel":

                    cur.execute("""
                        SELECT
                            stock.id,
                            stock.nom,
                            stock.quantite,
                            recettes.quantite
                        FROM recettes
                        JOIN stock
                            ON recettes.stock_id =
                               stock.id
                        WHERE recettes.plat_id = ?
                    """, (
                        plat_id,
                    ))

                    ingredients = cur.fetchall()

                    if not ingredients:

                        raise Exception(
                            f"Le plat « {infos['nom']} » "
                            "n'a pas encore de recette."
                        )

                    for (
                        stock_id,
                        nom_stock,
                        stock_disponible,
                        quantite_recette
                    ) in ingredients:

                        besoin = (
                            quantite_recette
                            * quantite_plat
                        )

                        if (
                            stock_disponible
                            < besoin
                        ):

                            raise Exception(
                                f"Stock insuffisant pour "
                                f"« {nom_stock} ».\n\n"
                                f"Plat : {infos['nom']}\n"
                                f"Nécessaire : {besoin:g}\n"
                                f"Disponible : "
                                f"{stock_disponible:g}"
                            )

                # =============================================
                # PLAT DU JOUR
                # =============================================

                else:

                    cur.execute("""
                        SELECT
                            stock_plats_du_jour.id,
                            stock.nom,
                            stock_plats_du_jour.quantite,
                            recettes_plats_du_jour.quantite
                        FROM recettes_plats_du_jour
                        JOIN stock
                            ON recettes_plats_du_jour.stock_id =
                               stock.id
                        JOIN stock_plats_du_jour
                            ON stock_plats_du_jour.stock_id =
                               recettes_plats_du_jour.stock_id
                            AND stock_plats_du_jour.plat_du_jour_id =
                               recettes_plats_du_jour.plat_du_jour_id
                        WHERE recettes_plats_du_jour.plat_du_jour_id = ?
                    """, (
                        plat_id,
                    ))

                    ingredients = cur.fetchall()

                    if not ingredients:

                        raise Exception(
                            f"Le plat du jour "
                            f"« {infos['nom']} » "
                            "n'a pas encore de recette."
                        )

                    for (
                        stock_jour_id,
                        nom_stock,
                        stock_disponible,
                        quantite_recette
                    ) in ingredients:

                        besoin = (
                            quantite_recette
                            * quantite_plat
                        )

                        if (
                            stock_disponible
                            < besoin
                        ):

                            raise Exception(
                                f"Stock du jour insuffisant "
                                f"pour « {nom_stock} ».\n\n"
                                f"Plat : {infos['nom']}\n"
                                f"Nécessaire : {besoin:g}\n"
                                f"Disponible : "
                                f"{stock_disponible:g}"
                            )

            # =================================================
            # 2. CALCULER LE TOTAL
            # =================================================

            total = 0

            for infos in self.panier.values():

                total += (
                    infos["prix"]
                    * infos["quantite"]
                )

            # =================================================
            # 3. ENREGISTRER LA VENTE
            # =================================================

            cur.execute("""
                INSERT INTO ventes(
                    date_vente,
                    total,
                    mode_paiement
                )
                VALUES(
                    datetime('now', 'localtime'),
                    ?,
                    ?
                )
            """, (
                total,
                "Espèces"
            ))

            vente_id = cur.lastrowid

            # =================================================
            # 4. ENREGISTRER LES DÉTAILS
            # =================================================

            for infos in self.panier.values():

                cur.execute("""
                    INSERT INTO details_vente(
                        vente_id,
                        plat,
                        plat_id,
                        type_plat,
                        quantite,
                        prix
                    )
                    VALUES(
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?
                    )
                """, (
                    vente_id,
                    infos["nom"],
                    infos["id"],
                    infos["type"],
                    infos["quantite"],
                    infos["prix"]
                ))

            # =================================================
            # 5. DÉDUIRE LE STOCK
            # =================================================

            for infos in self.panier.values():

                quantite_plat = infos[
                    "quantite"
                ]

                plat_id = infos["id"]

                # =============================================
                # STOCK HABITUEL
                # =============================================

                if infos["type"] == "habituel":

                    cur.execute("""
                        SELECT
                            stock_id,
                            quantite
                        FROM recettes
                        WHERE plat_id = ?
                    """, (
                        plat_id,
                    ))

                    ingredients = cur.fetchall()

                    for (
                        stock_id,
                        quantite_recette
                    ) in ingredients:

                        a_retirer = (
                            quantite_recette
                            * quantite_plat
                        )

                        cur.execute("""
                            UPDATE stock
                            SET quantite =
                                quantite - ?
                            WHERE id = ?
                        """, (
                            a_retirer,
                            stock_id
                        ))

                # =============================================
                # STOCK DU JOUR
                # =============================================

                else:

                    cur.execute("""
                        SELECT
                            stock_id,
                            quantite
                        FROM recettes_plats_du_jour
                        WHERE plat_du_jour_id = ?
                    """, (
                        plat_id,
                    ))

                    ingredients = cur.fetchall()

                    for (
                        stock_id,
                        quantite_recette
                    ) in ingredients:

                        a_retirer = (
                            quantite_recette
                            * quantite_plat
                        )

                        cur.execute("""
                            UPDATE stock_plats_du_jour
                            SET quantite =
                                quantite - ?
                            WHERE plat_du_jour_id = ?
                            AND stock_id = ?
                        """, (
                            a_retirer,
                            plat_id,
                            stock_id
                        ))

            # =================================================
            # 6. VALIDER
            # =================================================

            conn.commit()

            conn.close()

            # Actualiser les autres pages
            self.vente_enregistree.emit()

            QMessageBox.information(
                self,
                "Succès",
                "Vente enregistrée avec succès."
            )

            self.vider_ticket()

        except Exception as e:

            conn.rollback()
            conn.close()

            QMessageBox.critical(
                self,
                "Erreur",
                f"La vente n'a pas pu être enregistrée.\n\n{e}"
            )