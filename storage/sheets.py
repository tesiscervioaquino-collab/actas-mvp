import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config.settings import GOOGLE_SHEETS_ID, GOOGLE_CREDENTIALS_PATH
from processing.constants import PARTY_NAMES

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADERS = ["CODIGO_MESA"] + PARTY_NAMES

# Resolved once and reused for the whole run.
_service = None
_sheet_name = None
_headers_ready = False

def _get_service():
    global _service
    if _service is None:
        creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
        _service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    return _service

def _get_first_sheet_name(service):
    """Name of the first sheet, regardless of language. Cached after first call."""
    global _sheet_name
    if _sheet_name is None:
        meta = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEETS_ID).execute()
        _sheet_name = meta["sheets"][0]["properties"]["title"]
        logger.info(f"Nombre de hoja detectado: '{_sheet_name}'")
    return _sheet_name

def _format_header(service, sheet_name):
    """Bold the header row."""
    service.spreadsheets().batchUpdate(
        spreadsheetId=GOOGLE_SHEETS_ID,
        body={"requests": [{
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        }]}
    ).execute()

def ensure_headers(service, sheet_name):
    global _headers_ready
    if _headers_ready:
        return
    result = service.spreadsheets().values().get(
        spreadsheetId=GOOGLE_SHEETS_ID,
        range=f"'{sheet_name}'!A1"
    ).execute()
    if not result.get("values"):
        service.spreadsheets().values().update(
            spreadsheetId=GOOGLE_SHEETS_ID,
            range=f"'{sheet_name}'!A1",
            valueInputOption="RAW",
            body={"values": [HEADERS]}
        ).execute()
        _format_header(service, sheet_name)
        logger.info("Encabezados escritos y formateados")
    _headers_ready = True

def write_results(data: dict):
    service = _get_service()
    sheet_name = _get_first_sheet_name(service)
    ensure_headers(service, sheet_name)

    row = [data["code"]] + data["rows"]
    service.spreadsheets().values().append(
        spreadsheetId=GOOGLE_SHEETS_ID,
        range=f"'{sheet_name}'!A:V",
        valueInputOption="RAW",
        body={"values": [row]}
    ).execute()
    logger.info(f"Fila escrita en Sheets: {row[0]}")