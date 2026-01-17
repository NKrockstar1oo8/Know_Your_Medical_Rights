# core/chat_history.py

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# =====================================================
# Database setup
# =====================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

DB_PATH = LOG_DIR / "chat_history.db"

# Single shared connection (safe for Streamlit)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)

def _init_db():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_input TEXT NOT NULL,
            extracted_facts TEXT NOT NULL,
            verdict TEXT NOT NULL
        )
    """)
    conn.commit()

_init_db()

# =====================================================
# Public logging API (USED BY UI)
# =====================================================

def save_chat(user_input: str, facts: dict, verdict: dict):
    """
    Persist a single user interaction to SQLite.
    """
    conn.execute(
        """
        INSERT INTO chat_history (
            timestamp,
            user_input,
            extracted_facts,
            verdict
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            user_input.strip(),
            json.dumps(facts, ensure_ascii=False),
            json.dumps(verdict, ensure_ascii=False),
        )
    )
    conn.commit()
