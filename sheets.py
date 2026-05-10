import gspread
from config.settings import GOOGLE_SHEETS_ID

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

def _get_sheet():
    # Primera vez abre el navegador para autenticarte con tu cuenta de Google.
    # Guarda el token en ~/.config/gspread/authorized_user.json y no vuelve a pedir login.
    gc = gspread.oauth()
    spreadsheet = gc.open_by_key(GOOGLE_SHEETS_ID)
    return spreadsheet.sheet1

def ensure_headers(sheet):
    if not sheet.row_values(1):
        sheet.append_row(HEADERS)

def write_results(data: dict):
    """
    data = {"codigo_mesa": "0-122-0", "votos": [122, 5, 0, ...]}
    """
    sheet = _get_sheet()
    ensure_headers(sheet)
    row = [data["codigo_mesa"]] + data["votos"]
    sheet.append_row(row)