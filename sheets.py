from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config.settings import GOOGLE_SHEETS_ID, GOOGLE_CREDENTIALS_PATH

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Header row — must match the order in gemini.py PARTY_NAMES
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

def ensure_headers():
    """Write header row if Sheet1 is empty."""
    service = _get_service()
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=GOOGLE_SHEETS_ID,
        range="Sheet1!A1"
    ).execute()

    if not result.get("values"):
        sheet.values().update(
            spreadsheetId=GOOGLE_SHEETS_ID,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body={"values": [HEADERS]}
        ).execute()

def write_results(data: dict):
    """
    Write one row per acta.
    data = {"codigo_mesa": "0-122-0", "votos": [122, 5, 0, ...]}
    Row: codigo_mesa | voto_partido_1 | voto_partido_2 | ...
    """
    ensure_headers()
    service = _get_service()
    sheet = service.spreadsheets()

    row = [data["codigo_mesa"]] + data["votos"]

    sheet.values().append(
        spreadsheetId=GOOGLE_SHEETS_ID,
        range="Sheet1!A:V",
        valueInputOption="RAW",
        body={"values": [row]}
    ).execute()