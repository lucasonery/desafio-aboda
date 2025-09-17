# bot/telegram_bot.py
import os
from dotenv import load_dotenv
from telegram.ext import Application

# Estados dos diálogos
ASK_TICKER_HV, ASK_TICKER_LC = range(2)
ASK_START, ASK_END, ASK_TICKER_METRICS = range(3)

from bot.handlers import (
    start,
    help,
    watchlist,
    highest_volume,
    lowest_closing,
    consolidated,
    nlp,
    upload_csv,
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # registra handlers
    app.add_handler(start())
    app.add_handler(help())
    app.add_handler(watchlist())
    app.add_handler(highest_volume())
    app.add_handler(lowest_closing())
    app.add_handler(consolidated())
    app.add_handler(nlp())
    app.add_handler(upload_csv())

    print("Bot rodando no Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()
