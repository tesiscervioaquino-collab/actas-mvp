import json
import base64
import google.generativeai as genai
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-001")  # Gemini 3.0

PROMPT = """
Esta imagen es un acta de escrutinio electoral argentina.

Tu tarea es localizar la tabla de resultados manuscrita y extraer su contenido completo.

La tabla tiene exactamente 22 filas y 2 columnas:
- Columna 1 (PARTIDO): nombre de la agrupación política (texto impreso)
- Columna 2 (VOTOS): cantidad de votos obtenidos (número manuscrito)

Reglas estrictas:
1. Devolvé ÚNICAMENTE un JSON válido, sin texto adicional, sin bloques de código, sin explicaciones.
2. El formato debe ser una lista de 22 objetos: [{"partido": "...", "votos": ...}, ...]
3. Si el valor de votos no es legible, usá null.
4. Los votos deben ser números enteros, no strings.
5. Si una celda está en blanco o tiene un guión, usá 0.
6. No inventes valores. Solo transcribí lo que ves.
"""

def extract_table(image_bytes: bytes) -> list[dict]:
    """Send image to Gemini and return extracted table as list of dicts."""
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = model.generate_content([
        {"mime_type": "image/jpeg", "data": image_b64},
        PROMPT
    ])

    raw = response.text.strip()

    # Strip markdown code blocks if model adds them despite instructions
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw)
