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

    def charger_plats(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom
            FROM plats
            ORDER BY nom
        """)

        self.plat.clear()

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

        conn = get_connection()
        cur = conn.cursor()

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
            float(self.quantite.text())
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

        cur.execute("""
            SELECT
                recettes.id,
                stock.nom,
                recettes.quantite
            FROM recettes
            JOIN stock
                ON recettes.stock_id = stock.id
            WHERE recettes.plat_id = ?
            ORDER BY stock.nom
        """, (
            self.plat.currentData(),
        ))

        recettes = cur.fetchall()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels([
            "Ingrédient",
            "Quantité"
        ])

        self.table.setRowCount(len(recettes))

        for ligne, recette in enumerate(recettes):

            # recette = (id, nom, quantité)

            self.table.setItem(
                ligne,
                0,
                QTableWidgetItem(recette[1])
            )

            self.table.setItem(
                ligne,
                1,
                QTableWidgetItem(str(recette[2]))
            )

            # On cache l'id dans la première cellule
            self.table.item(ligne, 0).setData(
                1000,
                recette[0]
            )

        conn.close()

    def actualiser(self):

        self.charger_plats()
        self.charger_stock()
        self.charger_recettes()

    def selectionner_recette(self, ligne, colonne):

        self.recette_selectionnee = self.table.item(
            ligne,
            0
        ).data(1000)

        self.stock.setCurrentText(
            self.table.item(ligne, 0).text()
        )

        self.quantite.setText(
            self.table.item(ligne, 1).text()
        )

    def modifier_recette(self):

        if self.recette_selectionnee is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne une recette."
            )
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE recettes
            SET stock_id = ?, quantite = ?
            WHERE id = ?
        """, (
            self.stock.currentData(),
            float(self.quantite.text()),
            self.recette_selectionnee
        ))

        conn.commit()
        conn.close()

        self.charger_recettes()

        QMessageBox.information(
            self,
            "Succès",
            "Recette modifiée."
        )

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

        cur.execute(
            "DELETE FROM recettes WHERE id=?",
            (self.recette_selectionnee,)
        )

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