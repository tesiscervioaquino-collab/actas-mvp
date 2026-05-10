from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers import handle_photo, handle_start

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot corriendo. Presioná Ctrl+C para detener.")
    app.run_polling()

if __name__ == "__main__":
    main()
