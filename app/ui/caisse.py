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

    def charger_produits(self):

        conn = get_connection()
        cur = conn.cursor()

        self.liste_produits.clear()

        # ==========================
        # PLATS HABITUELS
        # ==========================

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

        produits = cur.fetchall()

        for plat_id, nom, prix in produits:

            item = QListWidgetItem(
                f"{nom} - {int(prix)} Ar"
            )

            item.setData(
                Qt.UserRole,
                {
                    "type": "habituel",
                    "id": plat_id,
                    "nom": nom,
                    "prix": prix
                }
            )

            self.liste_produits.addItem(
                item
            )

        # ==========================
        # PLATS DU JOUR
        # ==========================

        cur.execute("""
            SELECT
                id,
                nom,
                prix
            FROM plats_du_jour
            WHERE disponible = 1
            AND date_jour =
                date('now', 'localtime')
            ORDER BY nom
        """)

        plats_du_jour = cur.fetchall()

        if plats_du_jour:

            item_titre = QListWidgetItem(
                "⭐ PLATS DU JOUR"
            )

            item_titre.setFlags(
                Qt.NoItemFlags
            )

            self.liste_produits.addItem(
                item_titre
            )

            for plat_id, nom, prix in plats_du_jour:

                item = QListWidgetItem(
                    f"{nom} - {int(prix)} Ar"
                )

                item.setData(
                    Qt.UserRole,
                    {
                        "type": "jour",
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
                        quantite,
                        prix
                    )
                    VALUES(
                        ?,
                        ?,
                        ?,
                        ?
                    )
                """, (
                    vente_id,
                    infos["nom"],
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