"""
Migration: participants.condition + task_sessions.block_type sütunları ekler.
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

    # participants.condition
    cur.execute("PRAGMA table_info(participants)")
    cols = [row[1] for row in cur.fetchall()]
    if "condition" in cols:
        print("participants.condition zaten mevcut.")
    else:
        cur.execute("ALTER TABLE participants ADD COLUMN condition VARCHAR(20) DEFAULT 'adaptive'")
        conn.commit()
        print("participants.condition eklendi.")

    # task_sessions.block_type (A2: adaptif vs sabit blok)
    cur.execute("PRAGMA table_info(task_sessions)")
    ts_cols = [row[1] for row in cur.fetchall()]
    if "block_type" in ts_cols:
        print("task_sessions.block_type zaten mevcut.")
    else:
        cur.execute("ALTER TABLE task_sessions ADD COLUMN block_type VARCHAR(20) DEFAULT 'adaptive'")
        conn.commit()
        print("task_sessions.block_type eklendi.")

    conn.close()


if __name__ == "__main__":
    migrate()
