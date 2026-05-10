import json
import base64
import google.generativeai as genai
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-001")

PROMPT = """
Esta imagen es un acta de escrutinio electoral argentina (Certificado de Escrutinio).

Tu tarea tiene dos partes:

PARTE 1 - Extraé el código de mesa:
Buscá en el encabezado del acta los campos CIRCUITO, SECCIÓN ELECTORAL y MESA.
Formá el código como: {circuito}-{seccion}-{mesa}
Ejemplo: si Circuito=5, Sección=122, Mesa=312 → el código es "5-122-312"

PARTE 2 - Extraé los votos de la tabla manuscrita:
La tabla tiene una columna de agrupaciones políticas (impresa) y una columna de votos (manuscrita).
Extraé los votos en este orden exacto de filas:

1. ALIANZA LA LIBERTAD AVANZA
2. PARTIDO NUEVO BUENOS AIRES
3. LIBER.AR
4. FRENTE DE IZQUIERDA -UNIDAD-
5. FRENTE PATRIOTA FEDERAL
6. UNION LIBERAL
7. ALIANZA FUERZA PATRIA
8. COALICION CIVICA A.R.I
9. MOV. POL. SOC. Y CULTURAL PROYECTO SUR
10. PROPUESTA FEDERAL PARA EL CAMBIO
11. ALIANZA PROVINCIAS UNIDAS
12. ALIANZA POTENCIA
13. ALIANZA UNION FEDERAL
14. ALIANZA NUEVOS AIRES
15. MOVIMIENTO AVANZADA SOCIALISTA
16. TOTAL VOTOS AGRUPACIONES POLITICAS
17. VOTOS NULOS
18. VOTOS RECURRIDOS
19. VOTOS DE IDENTIDAD IMPUGNADA
20. VOTOS EN BLANCO
21. TOTAL DE VOTOS

Reglas estrictas:
1. Devolvé ÚNICAMENTE un JSON válido, sin texto adicional, sin bloques de código, sin explicaciones.
2. El formato debe ser exactamente este:
{
  "codigo_mesa": "circuito-seccion-mesa",
  "votos": [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21]
}
3. Los votos deben ser números enteros.
4. Si un valor no es legible, usá null.
5. Si una celda está en blanco o tiene un guión, usá 0.
6. No inventes valores. Solo transcribí lo que ves.
"""

PARTY_NAMES = [
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

def extract_table(image_bytes: bytes) -> dict:
    """
    Returns:
        {
            "codigo_mesa": "5-122-312",
            "votos": [122, 5, 0, 14, ...]   # 21 values in party order
        }
    """
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = model.generate_content([
        {"mime_type": "image/jpeg", "data": image_b64},
        PROMPT
    ])

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw)