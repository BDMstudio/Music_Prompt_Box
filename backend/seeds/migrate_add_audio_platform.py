#!/usr/bin/env python3
"""
Migration: Add audio_platform and audio_metadata columns to styles table.
Safe to run multiple times — skips if columns already exist.
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "music_prompt_box.db"


def column_exists(cursor: sqlite3.Cursor, table: str, column: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())


def migrate():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run seed_db.py first.")
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    added = 0

    if not column_exists(cursor, "styles", "audio_platform"):
        cursor.execute("ALTER TABLE styles ADD COLUMN audio_platform VARCHAR(20)")
        print("Added column: audio_platform")
        added += 1
    else:
        print("Column already exists: audio_platform (skipped)")

    if not column_exists(cursor, "styles", "audio_metadata"):
        cursor.execute("ALTER TABLE styles ADD COLUMN audio_metadata TEXT")
        print("Added column: audio_metadata")
        added += 1
    else:
        print("Column already exists: audio_metadata (skipped)")

    conn.commit()
    conn.close()

    if added:
        print(f"Migration complete: {added} column(s) added.")
    else:
        print("No migration needed.")


if __name__ == "__main__":
    migrate()
