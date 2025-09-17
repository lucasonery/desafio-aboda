# bot/handlers/consolidated.py
from telegram import Update, InputFile
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from io import BytesIO
from .base import call_api
from bot.states import ASK_START, ASK_END, ASK_TICKER_METRICS   # ✅ agora importa do states

# Início da conversa
async def consolidated_metrics_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Informe a data inicial (YYYY-MM-DD):")
    return ASK_START

# Pergunta data final
async def ask_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["start_date"] = update.message.text.strip()
    await update.message.reply_text("Agora informe a data final (YYYY-MM-DD):")
    return ASK_END

# Pergunta ticker
async def ask_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["end_date"] = update.message.text.strip()
    await update.message.reply_text("Digite o ticker desejado ou 'TODOS':")
    return ASK_TICKER_METRICS

# Processa e envia Excel
async def send_consolidated_metrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticker = update.message.text.strip().upper()
    start_date = context.user_data["start_date"]
    end_date = context.user_data["end_date"]

    params = {"start_date": start_date, "end_date": end_date}
    if ticker != "TODOS":
        params["ticker"] = ticker

    r = call_api("/consolidated_metrics", params=params)

    # verifica se é erro (JSON com error)
    if r.status_code != 200 or "application/json" in r.headers.get("content-type", "").lower():
        try:
            msg = r.json().get("error", "Erro ao gerar métricas.")
        except Exception:
            msg = "Erro ao gerar métricas."
        await update.message.reply_text(msg)
        return ConversationHandler.END

    # envia excel
    file_bytes = BytesIO(r.content)
    file_bytes.seek(0)
    filename = f"{ticker if ticker!='TODOS' else 'ALL'}_metrics.xlsx"

    await update.message.reply_document(
        document=InputFile(file_bytes, filename=filename),
        caption=f"Métricas consolidadas de {ticker} ({start_date} a {end_date})"
    )
    return ConversationHandler.END

def handler():
    return ConversationHandler(
        entry_points=[CommandHandler("consolidated_metrics", consolidated_metrics_start)],
        states={
            ASK_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_end_date)],
            ASK_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_ticker)],
            ASK_TICKER_METRICS: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_consolidated_metrics)],
        },
        fallbacks=[],
    )
