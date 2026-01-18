# core/sheets_logger.py

import os
import json
import base64
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback


def log_to_google_sheets(user_input, extracted_facts, verdict):
    try:
        # 1. Read base64 credential
        b64 = os.environ.get("GOOGLE_SERVICE_ACCOUNT_B64")
        if not b64:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_B64 missing")

        service_account_info = json.loads(
            base64.b64decode(b64).decode("utf-8")
        )

        # 2. Auth
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes,
        )

        client = gspread.authorize(credentials)

        # 3. Open sheet
        sheet_name = os.environ.get("SHEET_NAME")
        if not sheet_name:
            raise RuntimeError("SHEET_NAME missing")

        sheet = client.open(sheet_name).sheet1

        # 4. Append row
        row = [
            datetime.utcnow().isoformat(),
            user_input,
            json.dumps(extracted_facts, ensure_ascii=False),
            verdict.get("verdict_type"),
            json.dumps(verdict.get("primary_violations", []), ensure_ascii=False),
            json.dumps(verdict.get("imc_duties", []), ensure_ascii=False),
            json.dumps(verdict.get("procedural_remedies", []), ensure_ascii=False),
            json.dumps(verdict.get("sources", []), ensure_ascii=False),
            os.environ.get("SYSTEM_VERSION", "unknown"),
        ]


        sheet.append_row(row, value_input_option="RAW")

    except Exception:
        print("❌ Google Sheets logging failed")
        traceback.print_exc()
