# core/sheets_logger.py

import json
import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback


def log_to_google_sheets(user_input, extracted_facts, verdict):
    try:
        # -------------------------------------------------
        # 1. Load service account from ENV (Render-safe)
        # -------------------------------------------------
        service_account_raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
        if not service_account_raw:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT env var not found")

        service_account_info = json.loads(service_account_raw)

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes,
        )

        client = gspread.authorize(credentials)

        # -------------------------------------------------
        # 2. Open sheet
        # -------------------------------------------------
        sheet_name = os.environ.get("SHEET_NAME")
        if not sheet_name:
            raise RuntimeError("SHEET_NAME env var not found")

        sheet = client.open(sheet_name).sheet1

        # -------------------------------------------------
        # 3. Prepare row (MATCHES YOUR HEADER)
        # -------------------------------------------------
        row = [
            datetime.utcnow().isoformat(),                              # timestamp
            user_input,                                                  # user_input
            json.dumps(extracted_facts, ensure_ascii=False),             # extracted_facts
            verdict.get("verdict_type"),                                 # verdict_type
            json.dumps(verdict.get("primary_violations", []), ensure_ascii=False),
            json.dumps(verdict.get("procedural_remedies", []), ensure_ascii=False),
            json.dumps(verdict.get("sources", []), ensure_ascii=False),
            os.environ.get("SYSTEM_VERSION", "v1.0"),                    # system_version
        ]

        # -------------------------------------------------
        # 4. Append
        # -------------------------------------------------
        sheet.append_row(row, value_input_option="RAW")

        print("✅ Logged to Google Sheets successfully")

    except Exception:
        print("❌ Google Sheets logging failed")
        traceback.print_exc()
