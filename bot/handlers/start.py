# bot/handlers/start.py
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou o Bot do Desafio Aboda.\nUse /help para ver os comandos disponíveis."
    )

def handler():
    return CommandHandler("start", start)
