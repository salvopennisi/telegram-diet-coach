import asyncio
import nest_asyncio
import sys
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes, 
    MessageHandler, 
    filters
)
from dotenv import load_dotenv
import os
from datetime import datetime
from Utilities.input_messages_parserer import (
    parse_message_for_plan
)
from src.Planner import (
    get_daily_plan
)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
nest_asyncio.apply()
load_dotenv()


TOKEN = os.getenv("TOKEN")
GAS_BASE_URL = os.getenv("GAS_BASE_URL")
# -------------------------------------
# 🧾 Logging configurato (compatibile Render + locale)
# -------------------------------------
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("diet-coach-bot")

# -------------------------------
# 🔹 Comandi Telegram
# -------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! 👋 Sono il tuo *Diet Coach Bot*.\n",
        parse_mode="Markdown"
    )

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        logger.info(f"Argomenti ricevuti: {args}")

        week_day_number = None
        meal = None

        # 🔹 Analizza gli argomenti senza ordine obbligato
        for arg in args:
            if arg.isdigit():
                week_day_number = int(arg)
            else:
                meal = arg.capitalize()

        # 🔹 Se non specifica il giorno → usa quello corrente
        if week_day_number is None:
            week_day_number = datetime.now().isoweekday()

        logger.info(f"Richiesta piano: giorno={week_day_number}, pasto={meal}")

        await update.message.reply_text("⏳ Recupero il piano alimentare...")
        result = get_daily_plan(url=GAS_BASE_URL,week_day_number=week_day_number, meal=meal, logger=logger)
        await update.message.reply_text(result, parse_mode="Markdown")

    except Exception as e:
        logger.exception("Errore nella gestione del comando /plan")
        await update.message.reply_text(f"❌ Errore nel comando /plan:\n{e}")



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        logger.info(f"Messaggio ricevuto: {text}")

        week_day_number, meal = parse_message_for_plan(text, logger=logger)
        logger.info(f"Richiesta interpretata: giorno={week_day_number}, pasto={meal}")

        await update.message.reply_text("⏳ Recupero il piano alimentare...")
        result = get_daily_plan(url=GAS_BASE_URL,week_day_number=week_day_number, meal=meal, logger=logger)
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logger.exception("Errore nella gestione del comando /plan")
        await update.message.reply_text(f"❌ Errore nel comando /plan:\n{e}")

# -------------------------------------
# 🚀 Main
# -------------------------------------

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot avviato 🚀")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
