import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/service_account.json")

# Fail fast on missing keys instead of breaking later with a cryptic error.
_required = {
    "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "GOOGLE_SHEETS_ID": GOOGLE_SHEETS_ID,
}
_missing = [name for name, value in _required.items() if not value]
if _missing:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(_missing)}. Set them in .env."
    )