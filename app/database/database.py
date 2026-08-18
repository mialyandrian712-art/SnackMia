import sqlite3
from pathlib import Path

# Chemin vers le dossier data
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "snackmia.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        categorie TEXT NOT NULL,
        prix REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_vente TEXT NOT NULL,
        total REAL NOT NULL,
        mode_paiement TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS details_vente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vente_id INTEGER NOT NULL,
        plat TEXT NOT NULL,
        quantite INTEGER NOT NULL,
        prix REAL NOT NULL,
        FOREIGN KEY (vente_id) REFERENCES ventes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        quantite REAL NOT NULL,
        unite TEXT NOT NULL,
        seuil REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recettes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plat_id INTEGER NOT NULL,
        stock_id INTEGER NOT NULL,
        quantite REAL NOT NULL,
        FOREIGN KEY (plat_id) REFERENCES plats(id),
        FOREIGN KEY (stock_id) REFERENCES stock(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS depenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_depense TEXT NOT NULL,
        libelle TEXT NOT NULL,
        categorie TEXT NOT NULL,
        montant REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plats_du_jour (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_jour TEXT NOT NULL,
        nom TEXT NOT NULL,
        prix REAL NOT NULL,
        disponible INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recettes_plats_du_jour (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plat_du_jour_id INTEGER NOT NULL,
        stock_id INTEGER NOT NULL,
        quantite REAL NOT NULL,
        FOREIGN KEY (plat_du_jour_id)
            REFERENCES plats_du_jour(id),
        FOREIGN KEY (stock_id)
            REFERENCES stock(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_plats_du_jour (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plat_du_jour_id INTEGER NOT NULL,
        stock_id INTEGER NOT NULL,
        quantite REAL NOT NULL,
        seuil REAL NOT NULL DEFAULT 0,
        FOREIGN KEY (plat_du_jour_id)
            REFERENCES plats_du_jour(id),
        FOREIGN KEY (stock_id)
            REFERENCES stock(id)
    )
    """)

    conn.commit()
    conn.close()

def update_database():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            ALTER TABLE plats
            ADD COLUMN disponible INTEGER DEFAULT 1
        """)
    except sqlite3.OperationalError:
        # La colonne existe déjà
        pass

    try:
        cursor.execute("""
            ALTER TABLE stock
            ADD COLUMN prix_achat REAL DEFAULT 0
        """)
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_database()
    update_database()
    print("Base de données prête.")