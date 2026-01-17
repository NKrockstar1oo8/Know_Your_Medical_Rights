# core/chat_history.py
"""
Persistent chat history storage.
Append-only.
Auditable.
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "logs/chat_history.json"


def save_chat(user_input: str, facts: dict, verdict: dict):
    os.makedirs("logs", exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_input.strip(),
        "extracted_facts": facts,      # store AS-IS (no schema assumptions)
        "system_verdict": verdict
    }

    # Load existing history safely
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)
