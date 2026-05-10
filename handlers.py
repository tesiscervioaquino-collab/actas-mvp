from telegram import Update
from telegram.ext import ContextTypes
from processing.image import preprocess
from processing.gemini import extract_table
from storage.sheets import write_results

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming photo messages."""
    await update.message.reply_text("📸 Acta recibida. Procesando...")

    # Download the highest-resolution version of the photo
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    try:
        # Preprocess and extract
        processed = preprocess(bytes(image_bytes))
        rows = extract_table(processed)

        # Save to Sheets
        user = update.effective_user
        write_results(rows, user.id, user.username)

        # Confirm to fiscal
        summary = "\n".join(
            f"{r['partido']}: {r['votos']}" for r in rows
        )
        await update.message.reply_text(
            f"✅ Datos guardados en Sheets ({len(rows)} partidos):\n\n{summary}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error al procesar el acta: {str(e)}\n\nReintentá con una foto más clara."
        )

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bot de carga de actas activo.\n\nEnviá una foto del acta y los resultados se guardarán automáticamente."
    )
