# core/sheets_logger.py

import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback


def log_to_google_sheets(user_input, extracted_facts, verdict):
    try:
        # Load service account JSON correctly
        service_account_info = json.loads(
            st.secrets["GOOGLE_SERVICE_ACCOUNT"]
        )

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes
        )

        client = gspread.authorize(credentials)

        sheet_name = st.secrets["SHEET_NAME"]
        sheet = client.open(sheet_name).sheet1

        row = [
            datetime.utcnow().isoformat(),
            user_input,
            json.dumps(extracted_facts, ensure_ascii=False),
            verdict.get("verdict_type"),
            verdict.get("primary_violation"),
            json.dumps(verdict, ensure_ascii=False),
        ]

        sheet.append_row(row)

    except Exception:
        print("❌ Google Sheets logging failed")
        traceback.print_exc()
