from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config.settings import GOOGLE_SHEETS_ID, GOOGLE_CREDENTIALS_PATH

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def _get_service():
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)

def write_results(rows: list[dict], user_id: int, username: str):
    """
    Write extracted table to Google Sheets.
    Each row: timestamp | user_id | username | partido | votos
    """
    service = _get_service()
    sheet = service.spreadsheets()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    values = [
        [timestamp, str(user_id), username or "", row["partido"], row["votos"]]
        for row in rows
    ]

    sheet.values().append(
        spreadsheetId=GOOGLE_SHEETS_ID,
        range="Sheet1!A:E",
        valueInputOption="RAW",
        body={"values": values}
    ).execute()
