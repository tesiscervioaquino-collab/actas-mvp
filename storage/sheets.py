import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config.settings import GOOGLE_SHEETS_ID, GOOGLE_CREDENTIALS_PATH

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADERS = [
    "CODIGO_MESA",
    "ALIANZA LA LIBERTAD AVANZA",
    "PARTIDO NUEVO BUENOS AIRES",
    "LIBER.AR",
    "FRENTE DE IZQUIERDA -UNIDAD-",
    "FRENTE PATRIOTA FEDERAL",
    "UNION LIBERAL",
    "ALIANZA FUERZA PATRIA",
    "COALICION CIVICA A.R.I",
    "MOV. POL. SOC. Y CULTURAL PROYECTO SUR",
    "PROPUESTA FEDERAL PARA EL CAMBIO",
    "ALIANZA PROVINCIAS UNIDAS",
    "ALIANZA POTENCIA",
    "ALIANZA UNION FEDERAL",
    "ALIANZA NUEVOS AIRES",
    "MOVIMIENTO AVANZADA SOCIALISTA",
    "TOTAL VOTOS AGRUPACIONES POLITICAS",
    "VOTOS NULOS",
    "VOTOS RECURRIDOS",
    "VOTOS DE IDENTIDAD IMPUGNADA",
    "VOTOS EN BLANCO",
    "TOTAL DE VOTOS",
]

def _get_service():
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)

def _get_first_sheet_name(service):
    """Get the actual name of the first sheet, regardless of language."""
    meta = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEETS_ID).execute()
    name = meta["sheets"][0]["properties"]["title"]
    logger.info(f"Nombre de hoja detectado: '{name}'")
    return name

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