# bot/handlers/help.py
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
Comandos disponíveis:
/watchlist - Lista de tickers disponíveis
/highest_volume - Consulta maior volume negociado
/lowest_closing_price - Consulta menor preço de fechamento
/consolidated_metrics - Pergunta datas + ticker e retorna tabela consolidada (Excel)

Você também pode enviar um arquivo CSV com o nome do ticker como legenda.
    """
    await update.message.reply_text(msg)

def handler():
    return CommandHandler("help", help_command)
