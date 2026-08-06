from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from app.database.database import get_connection
from app.ui.detail_vente import DetailVente


class VentesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("📋 Historique des ventes")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(titre)

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "N°",
            "Date",
            "Total (Ar)",
            "Paiement"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)
        
        self.table.cellDoubleClicked.connect(
            self.ouvrir_detail
        )

        self.setLayout(layout)

        self.charger_ventes()

    def charger_ventes(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, date_vente, total, mode_paiement
            FROM ventes
            ORDER BY id DESC
        """)

        ventes = cur.fetchall()

        self.table.setRowCount(len(ventes))

        for ligne, vente in enumerate(ventes):
            for colonne, valeur in enumerate(vente):
                self.table.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(str(valeur))
                )

        conn.close()

    def ouvrir_detail(self, ligne, colonne):

        print("Double-clic détecté")

        vente_id = int(
            self.table.item(ligne, 0).text()
        )

        fenetre = DetailVente(vente_id)

        fenetre.exec()