from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDateEdit
)

from PySide6.QtCore import QDate

from app.database.database import get_connection
from app.ui.detail_vente import DetailVente


class VentesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # ==========================
        # Filtres
        # ==========================

        filtres = QHBoxLayout()

        self.periode = QComboBox()

        self.periode.addItems([
            "Toutes",
            "Aujourd'hui",
            "Hier",
            "Cette semaine",
            "La semaine dernière",
            "Ce mois",
            "Le mois dernier",
            "Cette année"
        ])

        filtres.addWidget(
            QLabel("Période :")
        )

        filtres.addWidget(
            self.periode
        ) 

        self.date_precise = QDateEdit()
        self.date_precise.setCalendarPopup(True)
        self.date_precise.setDate(
            QDate.currentDate()
        )

        filtres.addWidget(
            QLabel("Date précise :")
        )

        filtres.addWidget(
            self.date_precise
        )

        self.btn_date = QPushButton(
            "🔎 Date précise"
        )

        filtres.addWidget(
            self.btn_date
        )

        self.recherche = QLineEdit()

        self.recherche.setPlaceholderText(
            "🔎 N° de vente..."
        )

        filtres.addWidget(
            self.recherche
        )

        self.paiement = QComboBox()

        self.paiement.addItems([
            "Tous",
            "Espèces"
        ])

        filtres.addWidget(
            QLabel("Paiement :")
        )

        filtres.addWidget(
            self.paiement
        )

        layout.addLayout(filtres)

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

        # ==========================
        # Connexions des filtres
        # ==========================

        self.periode.currentTextChanged.connect(
            self.charger_ventes
        )

        self.paiement.currentTextChanged.connect(
            self.charger_ventes
        )

        self.recherche.textChanged.connect(
            self.charger_ventes
        )

        self.btn_date.clicked.connect(
            self.rechercher_par_date
        )

        self.setLayout(layout)

        self.charger_ventes()

    def charger_ventes(self):

        conn = get_connection()
        cur = conn.cursor()

        conditions = []
        parametres = []

        # ==========================
        # Filtre de période
        # ==========================

        periode = self.periode.currentText()

        if periode == "Aujourd'hui":
            conditions.append(
                "date(date_vente) = date('now', 'localtime')"
            )

        elif periode == "Hier":
            conditions.append(
                "date(date_vente) = date('now', 'localtime', '-1 day')"
            )

        elif periode == "Cette semaine":
            conditions.append("""
                date(date_vente) >= date(
                    'now',
                    '-' || ((strftime('%w', 'now') + 6) % 7)
                    || ' days',
                    'localtime'
                )
            """)

        elif periode == "La semaine dernière":
            conditions.append("""
                date(date_vente) >= date(
                    'now',
                    '-' || ((strftime('%w', 'now') + 6) % 7 + 7)
                    || ' days',
                    'localtime'
                )
                AND date(date_vente) < date(
                    'now',
                    '-' || ((strftime('%w', 'now') + 6) % 7)
                    || ' days',
                    'localtime'
                )
            """)

        elif periode == "Ce mois":
            conditions.append("""
                strftime('%Y-%m', date_vente)
                = strftime('%Y-%m', 'now', 'localtime')
            """)

        elif periode == "Le mois dernier":
            conditions.append("""
                strftime('%Y-%m', date_vente)
                = strftime('%Y-%m', 'now', 'localtime', '-1 month')
            """)

        elif periode == "Cette année":
            conditions.append("""
                strftime('%Y', date_vente)
                = strftime('%Y', 'now', 'localtime')
            """)

        # ==========================
        # Filtre paiement
        # ==========================

        paiement = self.paiement.currentText()

        if paiement != "Tous":
            conditions.append(
                "mode_paiement = ?"
            )
            parametres.append(paiement)

        # ==========================
        # Recherche
        # ==========================

        recherche = self.recherche.text().strip()

        if recherche:
            conditions.append(
                "CAST(id AS TEXT) LIKE ?"
            )
            parametres.append(
                f"%{recherche}%"
            )

        # ==========================
        # Requête
        # ==========================

        requete = """
            SELECT
                id,
                date_vente,
                total,
                mode_paiement
            FROM ventes
        """

        if conditions:
            requete += " WHERE " + " AND ".join(conditions)

        requete += """
            ORDER BY id DESC
        """

        cur.execute(
            requete,
            parametres
        )

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

    def rechercher_par_date(self):

        date_precise = self.date_precise.date().toString(
            "yyyy-MM-dd"
        )

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                date_vente,
                total,
                mode_paiement
            FROM ventes
            WHERE date(date_vente) = ?
            ORDER BY id DESC
        """, (
            date_precise,
        ))

        ventes = cur.fetchall()

        self.table.setRowCount(
            len(ventes)
        )

        for ligne, vente in enumerate(ventes):

            for colonne, valeur in enumerate(vente):

                self.table.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(str(valeur))
                )

        conn.close()    