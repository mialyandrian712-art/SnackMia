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

        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Nom du produit")

        self.quantite = QLineEdit()
        self.quantite.setPlaceholderText("Quantité")

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

        self.charger_stock()

    def charger_stock(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom, quantite, unite, seuil
            FROM stock
            ORDER BY nom
        """)

        produits = cur.fetchall()

        self.table.setRowCount(len(produits))

        for ligne, produit in enumerate(produits):
            for colonne, valeur in enumerate(produit):
                self.table.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(str(valeur))
                )

        conn.close()


    def selectionner_produit(self, ligne, colonne):

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


    def ajouter_produit(self):

        if (
            self.nom.text() == ""
            or self.quantite.text() == ""
            or self.seuil.text() == ""
        ):
            QMessageBox.warning(
                self,
                "Erreur",
                "Remplis tous les champs."
            )
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO stock(
                nom,
                quantite,
                unite,
                seuil
            )
            VALUES(?,?,?,?)
        """, (
            self.nom.text(),
            float(self.quantite.text()),
            self.unite.currentText(),
            float(self.seuil.text())
        ))

        conn.commit()
        conn.close()

        self.nom.clear()
        self.quantite.clear()
        self.seuil.clear()

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

        cur.execute("""
            UPDATE stock
            SET nom=?, quantite=?, unite=?, seuil=?
            WHERE id=?
        """, (
            self.nom.text(),
            float(self.quantite.text()),
            self.unite.currentText(),
            float(self.seuil.text()),
            self.id_selectionne
        ))

        conn.commit()
        conn.close()

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
            "Supprimer ce produit ?"
        )

        if reponse != QMessageBox.Yes:
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM stock WHERE id=?",
            (self.id_selectionne,)
        )

        conn.commit()
        conn.close()

        self.id_selectionne = None

        self.nom.clear()
        self.quantite.clear()
        self.seuil.clear()

        self.charger_stock()

        QMessageBox.information(
            self,
            "Succès",
            "Produit supprimé."
        )