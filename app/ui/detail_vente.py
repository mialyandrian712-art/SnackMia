from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from app.database.database import get_connection


class DetailVente(QDialog):

    def __init__(self, vente_id):
        super().__init__()

        self.vente_id = vente_id

        self.setWindowTitle(f"Vente n°{vente_id}")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.titre = QLabel(f"🧾 Détail de la vente n°{vente_id}")
        self.titre.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(self.titre)

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "Plat",
            "Quantité",
            "Prix"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table) 

        self.setLayout(layout)

        self.charger_details()


    def charger_details(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT plat, quantite, prix
            FROM details_vente
            WHERE vente_id=?
        """, (self.vente_id,))

        details = cur.fetchall()

        self.table.setRowCount(len(details))

        for ligne, detail in enumerate(details):
            for colonne, valeur in enumerate(detail):
                self.table.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(str(valeur))
                )

        conn.close()