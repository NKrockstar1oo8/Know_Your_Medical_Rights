# core/sheets_logger.py

import json
from datetime import datetime

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


def log_to_google_sheets(user_input, extracted_facts, verdict):
    try:
        creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials = Credentials.from_service_account_info(
            creds_dict, scopes=scopes
        )

        client = gspread.authorize(credentials)

        sheet = client.open(st.secrets["SHEET_NAME"]).sheet1

        row = [
            datetime.utcnow().isoformat(),
            user_input,
            json.dumps(extracted_facts, ensure_ascii=False),
            verdict.get("verdict_type", "UNKNOWN"),
            json.dumps(verdict.get("primary_violations", []), ensure_ascii=False),
            json.dumps(verdict.get("procedural_remedies", []), ensure_ascii=False),
            verdict.get("source", ""),
            st.secrets.get("SYSTEM_VERSION", "v1"),
        ]

        sheet.append_row(row, value_input_option="RAW")

    except Exception as e:
        print("❌ Google Sheets logging failed:", e)
