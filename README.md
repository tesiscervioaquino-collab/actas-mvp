# Actas MVP

Bot de Telegram para digitalización automática de actas de escrutinio electoral usando Gemini.

## Flujo

1. El fiscal envía una foto del acta por Telegram
2. El bot rescala la imagen y llama a la API de Gemini 3
3. Gemini extrae la tabla de 22 partidos y sus votos
4. Los resultados se guardan en Google Sheets

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
| `GOOGLE_CREDENTIALS_PATH` | Ruta al JSON de la service account |

## Estructura de Google Sheets

La hoja debe llamarse `Sheet1` con columnas en este orden:
`timestamp | user_id | username | partido | votos`
