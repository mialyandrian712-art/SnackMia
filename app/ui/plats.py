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
    QHeaderView
)

from app.database.database import get_connection


class PlatsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.id_selectionne = None

        # ===== Layout principal =====

        layout = QVBoxLayout()

        titre = QLabel("🍔 Gestion des plats")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre)

        # ===== Tableau =====

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Nom",
            "Catégorie",
            "Prix (Ar)"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.cellClicked.connect(
            self.selectionner_plat
        )

        layout.addWidget(self.table)

        # ===== Formulaire =====

        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Nom du plat")

        self.categorie = QComboBox()
        self.categorie.setMaxVisibleItems(14)

        self.categorie.addItems([
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
        ])

        self.prix = QLineEdit()
        self.prix.setPlaceholderText("Prix en Ariary")

        layout.addWidget(self.nom)
        layout.addWidget(self.categorie)
        layout.addWidget(self.prix)

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

        # ===== Connexions =====

        self.btn_ajouter.clicked.connect(
            self.ajouter_plat
        )

        self.btn_modifier.clicked.connect(
            self.modifier_plat
        )

        self.btn_supprimer.clicked.connect(
            self.supprimer_plat
        )

        self.charger_plats()
        
    def charger_plats(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom, categorie, prix
            FROM plats
            ORDER BY nom
        """)

        plats = cur.fetchall()
        print(plats)

        self.table.setRowCount(len(plats))

        for ligne, plat in enumerate(plats):
            for colonne, valeur in enumerate(plat):
                self.table.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(str(valeur))
                )

        conn.close()


    def selectionner_plat(self, ligne, colonne):

        self.id_selectionne = int(
            self.table.item(ligne, 0).text()
        )

        self.nom.setText(
            self.table.item(ligne, 1).text()
        )

        self.categorie.setCurrentText(
            self.table.item(ligne, 2).text()
        )

        self.prix.setText(
            self.table.item(ligne, 3).text()
        )


    def ajouter_plat(self):

        if self.nom.text() == "" or self.prix.text() == "":
            QMessageBox.warning(
                self,
                "Erreur",
                "Remplis tous les champs."
            )
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO plats(nom, categorie, prix)
            VALUES (?, ?, ?)
        """, (
            self.nom.text(),
            self.categorie.currentText(),
            float(self.prix.text())
        ))

        conn.commit()
        conn.close()

        self.nom.clear()
        self.prix.clear()

        self.charger_plats()

        QMessageBox.information(
            self,
            "Succès",
            "Plat ajouté avec succès."
        )


    def modifier_plat(self):

        if self.id_selectionne is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un plat."
            )
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE plats
            SET nom = ?, categorie = ?, prix = ?
            WHERE id = ?
        """, (
            self.nom.text(),
            self.categorie.currentText(),
            float(self.prix.text()),
            self.id_selectionne
        ))

        conn.commit()
        conn.close()

        self.charger_plats()

        QMessageBox.information(
            self,
            "Succès",
            "Plat modifié."
        )


    def supprimer_plat(self):

        if self.id_selectionne is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Sélectionne un plat."
            )
            return

        reponse = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer ce plat ?"
        )

        if reponse != QMessageBox.Yes:
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM plats WHERE id=?",
            (self.id_selectionne,)
        )

        conn.commit()
        conn.close()

        self.id_selectionne = None

        self.nom.clear()
        self.prix.clear()

        self.charger_plats()

        QMessageBox.information(
            self,
            "Succès",
            "Plat supprimé."
        )