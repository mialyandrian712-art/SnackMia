from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QMessageBox
)

from app.database.database import get_connection


class StockPage(QWidget):

    def __init__(self):
        super().__init__()

        self.id_selectionne = None

        layout = QVBoxLayout()

        # ==========================
        # Choix du type de stock
        # ==========================

        self.type_stock = QComboBox()

        self.type_stock.addItems([
            "📦 Stock habituel",
            "⭐ Stock du jour"
        ])

        layout.addWidget(
            QLabel("Type de stock")
        )

        layout.addWidget(
            self.type_stock
        )

        titre = QLabel("📦 Gestion du stock")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre)

        # ===== Tableau =====

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Produit",
            "Quantité",
            "Unité",
            "Seuil"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.cellClicked.connect(
            self.selectionner_produit
        )

        layout.addWidget(self.table)

        # ===== Formulaire =====

        # Plat du jour
        self.label_plat_du_jour = QLabel("Plat du jour")
        self.plat_du_jour = QComboBox()

        layout.addWidget(
            self.label_plat_du_jour
        )

        layout.addWidget(
            self.plat_du_jour
        )

        # Produit existant pour le stock du jour
        self.label_produit_du_jour = QLabel("Ingrédient")

        self.produit_du_jour = QComboBox()

        layout.addWidget(
            self.label_produit_du_jour
        )

        layout.addWidget(
            self.produit_du_jour
        )
        
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Nom du produit")

        self.quantite = QLineEdit()
        self.quantite.setPlaceholderText("Quantité")

        self.prix_achat = QLineEdit()
        self.prix_achat.setPlaceholderText(
            "Prix d'achat unitaire (Ar)"
        )

        self.unite = QComboBox()
        self.unite.addItems([
            "Pièce",
            "Kg",
            "Litre",
            "Bouteille",
            "Boîte"
        ])

        self.seuil = QLineEdit()
        self.seuil.setPlaceholderText("Seuil d'alerte")

        layout.addWidget(self.nom)
        layout.addWidget(self.quantite)
        layout.addWidget(self.prix_achat)
        layout.addWidget(self.unite)
        layout.addWidget(self.seuil)

        # ===== Boutons =====

        boutons = QHBoxLayout()

        self.btn_ajouter = QPushButton("➕ Ajouter")
        self.btn_modifier = QPushButton("✏ Modifier")
        self.btn_supprimer = QPushButton("🗑 Supprimer")

        boutons.addWidget(self.btn_ajouter)
        boutons.addWidget(self.btn_modifier)
        boutons.addWidget(self.btn_supprimer)

        layout.addLayout(boutons)

        self.setLayout(layout)

        self.btn_ajouter.clicked.connect(self.ajouter_produit)
        self.btn_modifier.clicked.connect(self.modifier_produit)
        self.btn_supprimer.clicked.connect(self.supprimer_produit)
        self.type_stock.currentIndexChanged.connect(
            self.changer_type_stock
        )

        self.charger_plats_du_jour()

        self.charger_produits_du_jour()

        self.plat_du_jour.currentIndexChanged.connect(
            self.charger_stock
        )
        self.charger_stock()
        self.changer_type_stock()

    def charger_stock(self):

        conn = get_connection()
        cur = conn.cursor()

        self.table.clearSpans()

        # ==========================
        # STOCK HABITUEL
        # ==========================

        if self.type_stock.currentIndex() == 0:

            cur.execute("""
                SELECT
                    id,
                    nom,
                    quantite,
                    unite,
                    seuil,
                    prix_achat
                FROM stock
                ORDER BY nom
            """)

            produits = cur.fetchall()

            self.table.setColumnCount(7)

            self.table.setHorizontalHeaderLabels([
                "ID",
                "Produit",
                "Quantité",
                "Unité",
                "Seuil",
                "Prix d'achat unitaire (Ar)",
                "Valeur du stock (Ar)"
            ])

            self.table.setRowCount(
                len(produits)
            )

            for ligne, produit in enumerate(produits):

                id_produit = produit[0]
                nom = produit[1]
                quantite = float(produit[2])
                unite = produit[3]
                seuil = float(produit[4])
                prix_achat = float(produit[5] or 0)

                # Calcul automatique de la valeur totale du stock
                valeur_stock = quantite * prix_achat

                valeurs = [
                    id_produit,
                    nom,
                    quantite,
                    unite,
                    seuil,
                    prix_achat,
                    valeur_stock
                ]

                for colonne, valeur in enumerate(valeurs):

                    self.table.setItem(
                        ligne,
                        colonne,
                        QTableWidgetItem(
                            str(valeur)
                        )
                    )

        # ==========================
        # STOCK DU JOUR
        # ==========================

        else:

            cur.execute("""
                SELECT
                    stock_plats_du_jour.id,
                    plats_du_jour.nom,
                    stock.nom,
                    stock_plats_du_jour.quantite,
                    stock.unite,
                    stock_plats_du_jour.seuil,
                    stock.prix_achat
                FROM stock_plats_du_jour

                JOIN plats_du_jour
                    ON stock_plats_du_jour.plat_du_jour_id
                    = plats_du_jour.id

                JOIN stock
                    ON stock_plats_du_jour.stock_id
                    = stock.id

                WHERE plats_du_jour.date_jour =
                    date('now', 'localtime')
                AND stock_plats_du_jour.plat_du_jour_id = ?
                ORDER BY stock.nom
            """, (
                self.plat_du_jour.currentData(),
            ))

            produits = cur.fetchall()

            self.table.setColumnCount(7)

            self.table.setHorizontalHeaderLabels([
                "ID",
                "Plat du jour",
                "Produit",
                "Quantité",
                "Unité",
                "Seuil",
                "Prix d'achat (Ar)"
            ])

            self.table.setRowCount(
                len(produits)
            )

            # Affichage des données
            for ligne, produit in enumerate(produits):

                for colonne, valeur in enumerate(produit):

                    self.table.setItem(
                        ligne,
                        colonne,
                        QTableWidgetItem(
                            str(valeur)
                        )
                    )

            # ==========================
            # REGROUPEMENT VISUEL
            # ==========================

            ligne = 0

            while ligne < len(produits):

                plat = produits[ligne][1]

                debut = ligne

                while (
                    ligne + 1 < len(produits)
                    and produits[ligne + 1][1] == plat
                ):
                    ligne += 1

                fin = ligne

                if fin > debut:

                    self.table.setSpan(
                        debut,
                        1,
                        fin - debut + 1,
                        1
                    )

                    cellule = self.table.item(
                        debut,
                        1
                    )

                    if cellule:
                        cellule.setText(
                            "⭐ " + plat
                        )

                else:

                    cellule = self.table.item(
                        debut,
                        1
                    )

                    if cellule:
                        cellule.setText(
                            "⭐ " + plat
                        )

                ligne += 1

        conn.close()
    
    def charger_plats_du_jour(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom
            FROM plats_du_jour
            WHERE disponible = 1
            AND date_jour = date('now', 'localtime')
            ORDER BY nom
        """)

        plats = cur.fetchall()

        self.plat_du_jour.clear()

        for plat_id, nom in plats:
            self.plat_du_jour.addItem(
                nom,
                plat_id
            )

        conn.close()    

    def charger_produits_du_jour(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom
            FROM stock
            ORDER BY nom
        """)

        produits = cur.fetchall()

        self.produit_du_jour.clear()

        for stock_id, nom in produits:

            self.produit_du_jour.addItem(
                nom,
                stock_id
            )

        conn.close()

    def selectionner_produit(self, ligne, colonne):

        # ==========================
        # STOCK HABITUEL
        # ==========================

        if self.type_stock.currentIndex() == 0:

            self.id_selectionne = int(
                self.table.item(ligne, 0).text()
            )

            self.nom.setText(
                self.table.item(ligne, 1).text()
            )

            self.quantite.setText(
                self.table.item(ligne, 2).text()
            )

            self.unite.setCurrentText(
                self.table.item(ligne, 3).text()
            )

            self.seuil.setText(
                self.table.item(ligne, 4).text()
            )

            self.prix_achat.setText(
                self.table.item(ligne, 5).text()
            )

        # ==========================
        # STOCK DU JOUR
        # ==========================

        else:

            self.id_selectionne = int(
                self.table.item(ligne, 0).text()
            )

            # Plat du jour
            plat = self.table.item(
                ligne,
                1
            ).text()

            # Enlever ⭐ devant le nom
            plat = plat.replace("⭐ ", "")

            index_plat = self.plat_du_jour.findText(
                plat
            )

            if index_plat >= 0:

                self.plat_du_jour.setCurrentIndex(
                    index_plat
                )

            # Ingrédient
            produit = self.table.item(
                ligne,
                2
            ).text()

            index_produit = self.produit_du_jour.findText(
                produit
            )

            if index_produit >= 0:

                self.produit_du_jour.setCurrentIndex(
                    index_produit
                )

            # Quantité
            self.quantite.setText(
                self.table.item(
                    ligne,
                    3
                ).text()
            )

            # Unité
            self.unite.setCurrentText(
                self.table.item(
                    ligne,
                    4
                ).text()
            )

            # Seuil
            self.seuil.setText(
                self.table.item(
                    ligne,
                    5
                ).text()
            )    

    def ajouter_produit(self):

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # STOCK DU JOUR
        # ==========================

        if self.type_stock.currentIndex() == 1:

            if self.plat_du_jour.currentData() is None:
                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Sélectionne un plat du jour."
                )
                return

            if self.produit_du_jour.currentData() is None:
                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Sélectionne un ingrédient."
                )
                return

            if (
                self.quantite.text() == ""
                or self.seuil.text() == ""
            ):
                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Remplis la quantité et le seuil."
                )
                return

            try:
                quantite = float(
                    self.quantite.text().replace(",", ".")
                )

                seuil = float(
                    self.seuil.text().replace(",", ".")
                )

            except ValueError:

                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "La quantité et le seuil doivent être des nombres."
                )
                return

            # Vérifier si l'ingrédient existe déjà
            cur.execute("""
                SELECT COUNT(*)
                FROM stock_plats_du_jour
                WHERE plat_du_jour_id = ?
                AND stock_id = ?
            """, (
                self.plat_du_jour.currentData(),
                self.produit_du_jour.currentData()
            ))

            existe = cur.fetchone()[0]

            if existe > 0:

                conn.close()

                QMessageBox.warning(
                    self,
                    "Doublon",
                    "Cet ingrédient est déjà affecté à ce plat du jour."
                )
                return

            # Ajouter dans le stock du jour
            cur.execute("""
                INSERT INTO stock_plats_du_jour(
                    plat_du_jour_id,
                    stock_id,
                    quantite,
                    seuil
                )
                VALUES(?,?,?,?)
            """, (
                self.plat_du_jour.currentData(),
                self.produit_du_jour.currentData(),
                quantite,
                seuil
            ))

            conn.commit()
            conn.close()

            self.quantite.clear()
            self.seuil.clear()

            self.charger_stock()

            QMessageBox.information(
                self,
                "Succès",
                "Ingrédient ajouté au stock du jour."
            )

            return

        # ==========================
        # STOCK HABITUEL
        # ==========================

        if (
            self.nom.text() == ""
            or self.quantite.text() == ""
            or self.seuil.text() == ""
        ):

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "Remplis tous les champs."
            )
            return

        try:
            quantite = float(
                self.quantite.text()
            )

            seuil = float(
                self.seuil.text()
            )
            prix_achat = float(
                self.prix_achat.text().replace(",", ".")
            )

        except ValueError:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "La quantité et le seuil doivent être des nombres."
            )
            return

        cur.execute("""
            INSERT INTO stock(
                nom,
                quantite,
                unite,
                seuil,
                prix_achat
            )
            VALUES(?,?,?,?,?)
        """, (
            self.nom.text(),
            quantite,
            self.unite.currentText(),
            seuil,
            prix_achat
        ))

        conn.commit()
        conn.close()

        self.nom.clear()
        self.quantite.clear()
        self.prix_achat.clear()
        self.seuil.clear()

        self.charger_produits_du_jour()
        self.charger_stock()

        QMessageBox.information(
            self,
            "Succès",
            "Produit ajouté."
        )

    def modifier_produit(self):

        if self.id_selectionne is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un produit."
            )

            return

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # STOCK DU JOUR
        # ==========================

        if self.type_stock.currentIndex() == 1:

            if self.plat_du_jour.currentData() is None:
                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Sélectionne un plat du jour."
                )

                return

            if self.produit_du_jour.currentData() is None:
                conn.close()

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

                seuil = float(
                    self.seuil.text().replace(",", ".")
                )

            except ValueError:

                conn.close()

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "La quantité et le seuil doivent être des nombres."
                )

                return

            cur.execute("""
                UPDATE stock_plats_du_jour
                SET
                    plat_du_jour_id = ?,
                    stock_id = ?,
                    quantite = ?,
                    seuil = ?
                WHERE id = ?
            """, (
                self.plat_du_jour.currentData(),
                self.produit_du_jour.currentData(),
                quantite,
                seuil,
                self.id_selectionne
            ))

            conn.commit()
            conn.close()

            self.charger_stock()

            QMessageBox.information(
                self,
                "Succès",
                "Stock du jour modifié."
            )

            return

        # ==========================
        # STOCK HABITUEL
        # ==========================

        if self.nom.text() == "":

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "Le nom du produit est obligatoire."
            )

            return

        try:

            quantite = float(
                self.quantite.text()
            )

            seuil = float(
                self.seuil.text()
            )

            prix_achat = float(
                self.prix_achat.text().replace(",", ".")
            )

        except ValueError:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "La quantité et le seuil doivent être des nombres."
            )

            return

        cur.execute("""
            UPDATE stock
            SET
                nom = ?,
                quantite = ?,
                unite = ?,
                seuil = ?,
                prix_achat = ?
            WHERE id = ?
        """, (
            self.nom.text(),
            quantite,
            self.unite.currentText(),
            seuil,
            prix_achat,
            self.id_selectionne
        ))

        conn.commit()
        conn.close()

        self.charger_produits_du_jour()
        self.charger_stock()
 
        QMessageBox.information(
            self,
            "Succès",
            "Produit modifié."
        )


    def supprimer_produit(self):

        if self.id_selectionne is None:

            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un produit."
            )

            return

        reponse = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer cet ingrédient ?"
        )

        if reponse != QMessageBox.Yes:
            return

        conn = get_connection()
        cur = conn.cursor()

        # ==========================
        # STOCK DU JOUR
        # ==========================

        if self.type_stock.currentIndex() == 1:

            cur.execute("""
                DELETE FROM stock_plats_du_jour
                WHERE id = ?
            """, (
                self.id_selectionne,
            ))

            conn.commit()
            conn.close()

            self.id_selectionne = None

            self.quantite.clear()
            self.seuil.clear()

            self.charger_stock()

            QMessageBox.information(
                self,
                "Succès",
                "Ingrédient supprimé du stock du jour."
            )

            return

        # ==========================
        # STOCK HABITUEL
        # ==========================

        cur.execute("""
            DELETE FROM stock
            WHERE id = ?
        """, (
            self.id_selectionne,
        ))

        conn.commit()
        conn.close()

        self.id_selectionne = None

        self.nom.clear()
        self.quantite.clear()
        self.seuil.clear()

        self.charger_produits_du_jour()
        self.charger_stock()

        QMessageBox.information(
            self,
            "Succès",
            "Produit supprimé."
        )

    def changer_type_stock(self):

        est_stock_du_jour = (
            self.type_stock.currentIndex() == 1
        )

        # Plat du jour
        self.label_plat_du_jour.setVisible(
            est_stock_du_jour
        )

        self.plat_du_jour.setVisible(
            est_stock_du_jour
        )

        # Ingrédient du stock
        self.label_produit_du_jour.setVisible(
            est_stock_du_jour
        )

        self.produit_du_jour.setVisible(
            est_stock_du_jour
        )

        # Nom du produit classique
        self.nom.setVisible(
            not est_stock_du_jour
        )

        self.charger_stock()