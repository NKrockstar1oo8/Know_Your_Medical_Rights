import json
import time
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "audit.log")

def log_event(event_type: str, payload: dict):
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": int(time.time()),
        "event_type": event_type,
        "payload": payload
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
