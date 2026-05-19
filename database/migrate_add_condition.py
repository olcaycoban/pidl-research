"""
Tek seferlik migration: participants tablosuna condition sütunu ekler (H4: adaptive vs fixed).
Mevcut veritabanı varsa çalıştırın: python -m database.migrate_add_condition
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "research_data.db")

def migrate():
    if not os.path.exists(DB_PATH):
        print("Veritabanı yok, migration gerekmez.")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(participants)")
    cols = [row[1] for row in cur.fetchall()]
    if "condition" in cols:
        print("participants.condition zaten mevcut.")
    else:
        cur.execute("ALTER TABLE participants ADD COLUMN condition VARCHAR(20) DEFAULT 'adaptive'")
        conn.commit()
        print("participants.condition eklendi.")
    conn.close()

if __name__ == "__main__":
    migrate()
