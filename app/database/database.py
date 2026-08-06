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

    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_database()
    update_database()
    print("Base de données prête.")