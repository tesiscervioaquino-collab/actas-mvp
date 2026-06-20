import json
import base64
import logging
from google import genai
from google.genai import types
from config.settings import GEMINI_API_KEY

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

# Matches the configuration used in the model evaluation. The low thinking level
# is deliberate: the default is noticeably slower for this task.
GEN_CONFIG = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_level="low"),
    temperature=0.1,
    response_mime_type="application/json",
)

PROMPT = """
Foto de un "Telegrama de Mesa" (acta electoral argentina) con layout fijo.

Tarea 1 — CÓDIGO:
- Leer los campos impresos en la parte superior: "Sección", "Circuito" y "Mesa".
- Devolver un string con formato: SECCION-CIRCUITO-MESA (por ejemplo: 122-0-312).
- No inventar dígitos. Si alguno es ilegible, devolver null en su lugar.

Tarea 2 — TABLA DE VOTOS:
- Encontrar y extraer únicamente la columna numérica manuscrita de DIPUTADOS NACIONALES.
- Devolver exactamente 21 filas, desde la primera agrupación política hasta la fila de TOTAL DE VOTOS.
- Cada fila debe ser un entero o null.
- Ignorar texto de partidos, bordes, sellos y manuscritos fuera de la tabla.
- Si una celda está en blanco o tiene un guión, devolver 0.
- No inventar valores. Solo transcribir lo que se ve.

Devolver únicamente JSON válido con esta estructura, sin explicaciones ni texto adicional:
{
  "code": "SECCION-CIRCUITO-MESA",
  "rows": [int|null, int|null, ... 21 elementos en total]
}
"""

def extract_table(image_bytes: bytes) -> dict:
    logger.info("Enviando imagen a Gemini 3...")
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            {"role": "user", "parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": image_b64}},
                {"text": PROMPT}
            ]}
        ],
        config=GEN_CONFIG
    )

    raw = response.text.strip()
    logger.info(f"Respuesta cruda de Gemini: {raw[:200]}")

    result = json.loads(raw)
    logger.info(f"Extracción exitosa — Mesa: {result.get('code')} | Filas: {len(result.get('rows', []))}")
    return result