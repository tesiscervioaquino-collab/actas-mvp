from telegram import Update
from telegram.ext import ContextTypes
from processing.image import preprocess
from processing.gemini import extract_table, PARTY_NAMES
from storage.sheets import write_results

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming photo messages."""
    await update.message.reply_text("📸 Acta recibida. Procesando...")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    try:
        processed = preprocess(bytes(image_bytes))
        data = extract_table(processed)
        write_results(data)

        # Build summary message
        lines = [f"✅ Mesa *{data['codigo_mesa']}* guardada en Sheets\n"]
        for name, votes in zip(PARTY_NAMES, data["votos"]):
            if votes:
                lines.append(f"{name}: {votes}")

        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error al procesar el acta: {str(e)}\n\nReintentá con una foto más clara."
        )

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bot de carga de actas activo.\n\nEnviá una foto del acta y los resultados se guardarán automáticamente en Sheets."
    )