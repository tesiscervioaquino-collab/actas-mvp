# Actas MVP

Bot de Telegram para la digitalización automática de actas de escrutinio electoral mediante inteligencia artificial.

## Contexto y objetivo

Este trabajo explora la viabilidad de automatizar la digitalización de actas de escrutinio electoral en Argentina mediante modelos de reconocimiento de imágenes. El foco está puesto exclusivamente en la extracción de información a partir de fotos de actas, sin abarcar el análisis de resultados, la selección de mesas testigo ni la validación frente a datos oficiales.

Para abordar el problema se compararon tres familias de modelos — OCR open source, OCR comerciales y modelos multimodales — evaluados sobre actas reales de procesos electorales recientes. A partir de esa comparación se seleccionó el modelo con mejor equilibrio entre precisión, tasa de error, velocidad y costo, y se lo integró en este prototipo funcional orientado a condiciones de uso real.

## Ejemplo de acta procesada

![Ejemplo de acta de escrutinio](acta_ejemplo.jpg)

## Flujo del sistema

1. El fiscal toma una foto del acta y la envía por Telegram
2. El bot rescala la imagen y la envía a la API de Gemini
3. Gemini localiza la tabla manuscrita y extrae el código de mesa y los votos
4. Los resultados se guardan como una fila en Google Sheets

## Estructura de Google Sheets

Una fila por acta con las siguientes columnas:

| CODIGO_MESA | ALIANZA LA LIBERTAD AVANZA | PARTIDO NUEVO BUENOS AIRES | ... | TOTAL DE VOTOS |
|---|---|---|---|---|
| 0-122-312 | 122 | 5 | ... | 246 |

El código de mesa se forma como `circuito-sección-mesa` y es extraído automáticamente del encabezado del acta.

## Setup

### 1. Clonar e instalar dependencias
```bash
git clone <repo-url>
cd actas-mvp
pip install -r requirements.txt
```

### 2. Configurar credenciales
```bash
cp .env.example .env
# Completar .env con tus credenciales
```

Colocar el JSON de la service account de Google en `credentials/service_account.json`.

### 3. Correr
```bash
python main.py
```

## Variables de entorno
 
| Variable | Descripción |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token del bot obtenido desde @BotFather |
| `GEMINI_API_KEY` | API Key de Google AI Studio |
| `GOOGLE_SHEETS_ID` | ID de la planilla (en la URL de Sheets) |