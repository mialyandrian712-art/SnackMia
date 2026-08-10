from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QFrame,
    QMessageBox
)
from app.database.database import get_connection


class CaissePage(QWidget):

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

        gauche_layout.addWidget(self.liste_produits)

        gauche.setLayout(gauche_layout)

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

        droite_layout.addWidget(titre_ticket)

        self.ticket = QListWidget()

        droite_layout.addWidget(self.ticket)

        self.total = QLabel("Total : 0 Ar")

        self.total.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        droite_layout.addWidget(self.total)

        self.btn_vider = QPushButton("🗑️ Vider le ticket")
        self.btn_vider.setMinimumHeight(50)

        droite_layout.addWidget(self.btn_vider)

        self.btn_encaisser = QPushButton("💵 Encaisser")
        self.btn_encaisser.setMinimumHeight(50)

        droite_layout.addWidget(self.btn_encaisser)

        droite.setLayout(droite_layout)

        principal.addWidget(gauche, 2)
        principal.addWidget(droite, 1)

        self.setLayout(principal)
        self.charger_produits()
        self.btn_vider.clicked.connect(
            self.vider_ticket
        )

        self.btn_encaisser.clicked.connect(
            self.encaisser
        )

    def charger_produits(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT nom, prix
            FROM plats
            ORDER BY categorie, nom
        """)

        produits = cur.fetchall()

        self.liste_produits.clear()

        for nom, prix in produits:
            self.liste_produits.addItem(
                f"{nom} - {int(prix)} Ar"
            )

        conn.close()

    def ajouter_au_ticket(self, item):

        texte = item.text()

        nom, prix = texte.rsplit(" - ", 1)

        prix = int(prix.replace(" Ar", ""))

        if nom in self.panier:

            self.panier[nom]["quantite"] += 1

        else:

            self.panier[nom] = {
                "prix": prix,
                "quantite": 1
            }

        self.actualiser_ticket()

    def actualiser_ticket(self):

        self.ticket.clear()

        total = 0

        for nom, infos in self.panier.items():

            quantite = infos["quantite"]
            prix = infos["prix"]

            sous_total = quantite * prix

            total += sous_total

            self.ticket.addItem(
                f"{nom}   x{quantite}   {sous_total:,} Ar"
            )

        self.total.setText(
            f"Total : {total:,} Ar"
        )

    def vider_ticket(self):

        self.panier.clear()

        self.actualiser_ticket()

    def verifier_stock(self):

        conn = get_connection()
        cur = conn.cursor()

        for nom_plat, infos in self.panier.items():

            cur.execute("""
                SELECT
                    stock.nom,
                    stock.quantite,
                    recettes.quantite
                FROM recettes
                JOIN plats
                    ON recettes.plat_id = plats.id
                JOIN stock
                    ON recettes.stock_id = stock.id
                WHERE plats.nom = ?
            """, (
                nom_plat,
            ))

            ingredients = cur.fetchall()

            for nom_stock, stock_disponible, quantite_recette in ingredients:

                quantite_necessaire = (
                    quantite_recette *
                    infos["quantite"]
                )

                if stock_disponible < quantite_necessaire:

                    conn.close()

                    QMessageBox.warning(
                        self,
                        "Stock insuffisant",
                        f"Il n'y a pas assez de '{nom_stock}' pour préparer {nom_plat}."
                    )

                    return False

        conn.close()

        return True

    def destocker(self, cur):

        for nom_plat, infos in self.panier.items():

            cur.execute("""
                SELECT
                    recettes.stock_id,
                    recettes.quantite
                FROM recettes
                JOIN plats
                    ON recettes.plat_id = plats.id
                WHERE plats.nom = ?
            """, (
                nom_plat,
            ))

            ingredients = cur.fetchall()

            for stock_id, quantite_recette in ingredients:

                quantite_necessaire = (
                    quantite_recette *
                    infos["quantite"]
                )

                cur.execute("""
                    UPDATE stock
                    SET quantite = quantite - ?
                    WHERE id = ?
                """, (
                    quantite_necessaire,
                    stock_id
                ))
    
    def encaisser(self):

        if not self.panier:
            QMessageBox.warning(
                self,
                "Ticket vide",
                "Ajoutez au moins un produit."
            )
            return

        # Vérifier le stock avant toute modification
        if not self.verifier_stock():
            return

        conn = get_connection()
        cur = conn.cursor()

        try:

            # Calcul du total
            total = 0

            for infos in self.panier.values():
                total += infos["prix"] * infos["quantite"]

            # Déstockage
            self.destocker(cur)

            # Enregistrement de la vente
            cur.execute("""
                INSERT INTO ventes(
                    date_vente,
                    total,
                    mode_paiement
                )
                VALUES(
                    datetime('now'),
                    ?,
                    ?
                )
            """, (
                total,
                "Espèces"
            ))

            vente_id = cur.lastrowid

            # Enregistrement des détails
            for nom, infos in self.panier.items():

                cur.execute("""
                    INSERT INTO details_vente(
                        vente_id,
                        plat,
                        quantite,
                        prix
                    )
                    VALUES(?,?,?,?)
                """, (
                    vente_id,
                    nom,
                    infos["quantite"],
                    infos["prix"]
                ))

            # Tout s'est bien passé
            conn.commit()

        except Exception as e:

            # Annuler toutes les modifications
            conn.rollback()

            QMessageBox.critical(
                self,
                "Erreur",
                f"La vente n'a pas pu être enregistrée.\n\n{e}"
            )

            conn.close()
            return

        conn.close()

        QMessageBox.information(
            self,
            "Succès",
            "Vente enregistrée avec succès."
        )

        self.vider_ticket()