import logging
from telegram import Update
from telegram.ext import ContextTypes
from processing.image import preprocess
from processing.gemini import extract_table, PARTY_NAMES
from storage.sheets import write_results
from config.settings import GOOGLE_SHEETS_ID

logger = logging.getLogger(__name__)

SHEETS_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEETS_ID}"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Foto recibida de user_id={user.id} username={user.username}")
    await update.message.reply_text("📸 Acta recibida. Procesando...")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()
    logger.info(f"Imagen descargada: {len(image_bytes)} bytes")

    try:
        processed = preprocess(bytes(image_bytes))
        logger.info("Imagen preprocesada OK")

        data = extract_table(processed)
        logger.info(f"Tabla extraída OK — code={data['code']}")

        write_results(data)
        logger.info("Datos escritos en Sheets OK")

        lines = [f"✅ Mesa *{data['code']}* guardada en Sheets\n"]
        for name, votes in zip(PARTY_NAMES, data["rows"]):
            if votes:
                lines.append(f"{name}: {votes}")

        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error procesando acta: {e}", exc_info=True)
        await update.message.reply_text(
            f"❌ Error al procesar el acta: {str(e)}\n\nReintentá con una foto más clara."
        )

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/start recibido de user_id={update.effective_user.id}")
    await update.message.reply_text(
        f"👋 Bot de carga de actas activo.\n\n"
        f"Enviá una foto del acta y los resultados se guardarán automáticamente en el Sheets:\n"
        f"{SHEETS_URL}\n\n"
        f"📸 Para mejores resultados, asegurate de que la foto cumpla con estas condiciones:\n\n"
        f"• El acta debe estar completamente visible, sin cortes en los bordes\n"
        f"• Buena iluminación y sin sombras sobre el texto\n"
        f"• Imagen enfocada y sin movimiento\n\n"
        f"Cuando estés listo, enviá la foto. ✅"
    )
