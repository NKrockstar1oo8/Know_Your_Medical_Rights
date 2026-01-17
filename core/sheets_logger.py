# core/sheets_logger.py

import os
import json
import gspread
import traceback
from datetime import datetime
from google.oauth2.service_account import Credentials


def log_to_google_sheets(user_input, extracted_facts, verdict):
    """
    Logs interaction to Google Sheets using Render environment variables
    """

    try:
        # -------------------------------------------------
        # 1️⃣ Read secrets from ENV (Render way)
        # -------------------------------------------------
        service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
        sheet_name = os.environ.get("SHEET_NAME")

        if not service_account_json:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT env variable not found")

        if not sheet_name:
            raise RuntimeError("SHEET_NAME env variable not found")

        service_account_info = json.loads(service_account_json)

        # -------------------------------------------------
        # 2️⃣ Build credentials
        # -------------------------------------------------
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes
        )

        # -------------------------------------------------
        # 3️⃣ Authorize & open sheet
        # -------------------------------------------------
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name).sheet1

        # -------------------------------------------------
        # 4️⃣ Prepare row
        # -------------------------------------------------
        row = [
            datetime.utcnow().isoformat(),
            user_input,
            json.dumps(extracted_facts, ensure_ascii=False),
            verdict.get("verdict_type"),
            json.dumps(verdict, ensure_ascii=False),
        ]

        # -------------------------------------------------
        # 5️⃣ Append
        # -------------------------------------------------
        sheet.append_row(row, value_input_option="RAW")

        print("✅ Logged to Google Sheets successfully")

    except Exception:
        print("❌ Google Sheets logging failed")
        traceback.print_exc()
