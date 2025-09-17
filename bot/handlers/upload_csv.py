# bot/handlers/upload_csv.py
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from .base import post_file

async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        return

    file = update.message.document
    ticker = update.message.caption.upper() if update.message.caption else None

    if not ticker:
        await update.message.reply_text("Por favor, envie o CSV com a legenda contendo o ticker.")
        return

    file_path = await file.get_file()
    file_bytes = await file_path.download_as_bytearray()

    data = post_file("/upload_csv/", ticker, file.file_name, file_bytes)

    if "error" in data:
        await update.message.reply_text(f"Erro ao processar {file.file_name}: {data['error']}")
    else:
        await update.message.reply_text(f"Arquivo {file.file_name} do ticker {ticker} processado com sucesso.")

def handler():
    return MessageHandler(filters.Document.FileExtension("csv"), handle_csv)
