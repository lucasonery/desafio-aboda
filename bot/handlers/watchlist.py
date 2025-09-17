# bot/handlers/watchlist.py
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from .base import call_api

async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = call_api("/watchlist")
    data = r.json()
    await update.message.reply_text(f"Tickers disponíveis: {', '.join(data['tickers'])}")

def handler():
    return CommandHandler("watchlist", watchlist)
