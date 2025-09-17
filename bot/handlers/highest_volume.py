# bot/handlers/highest_volume.py
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from .base import call_api
from bot.states import ASK_TICKER_HV   # ✅ agora importa do states

async def highest_volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = update.message.text.strip().split(maxsplit=1)
    if len(parts) == 1:
        await update.message.reply_text("Qual ticker você quer consultar para maior volume?")
        return ASK_TICKER_HV

    ticker = parts[1].strip().upper()
    return await process_highest_volume(update, ticker)

async def ask_ticker_highest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticker = update.message.text.strip().upper()
    return await process_highest_volume(update, ticker)

async def process_highest_volume(update: Update, ticker: str):
    r = call_api(f"/highest_volume/{ticker}")
    data = r.json()
    if "error" in data:
        await update.message.reply_text(data["error"])
    else:
        await update.message.reply_text(f"{ticker} - Maior volume {data['highest_volume']} em {data['date']}")
    return ConversationHandler.END

def handler():
    return ConversationHandler(
        entry_points=[CommandHandler("highest_volume", highest_volume)],
        states={ASK_TICKER_HV: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_ticker_highest)]},
        fallbacks=[],
    )
