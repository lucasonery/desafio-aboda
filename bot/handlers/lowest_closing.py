# bot/handlers/lowest_closing.py
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from .base import call_api
from bot.states import ASK_TICKER_LC   # ✅ agora importa do states

async def lowest_closing_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = update.message.text.strip().split(maxsplit=1)
    if len(parts) == 1:
        await update.message.reply_text("Qual ticker você quer consultar para menor fechamento?")
        return ASK_TICKER_LC

    ticker = parts[1].strip().upper()
    return await process_lowest_closing(update, ticker)

async def ask_ticker_lowest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticker = update.message.text.strip().upper()
    return await process_lowest_closing(update, ticker)

async def process_lowest_closing(update: Update, ticker: str):
    r = call_api(f"/lowest_closing_price/{ticker}")
    data = r.json()
    if "error" in data:
        await update.message.reply_text(data["error"])
    else:
        await update.message.reply_text(f"{ticker} - Menor fechamento {data['lowest_closing_price']} em {data['date']}")
    return ConversationHandler.END

def handler():
    return ConversationHandler(
        entry_points=[CommandHandler("lowest_closing_price", lowest_closing_price)],
        states={ASK_TICKER_LC: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_ticker_lowest)]},
        fallbacks=[],
    )
