from telegram import Update, InputFile
from telegram.ext import MessageHandler, ContextTypes, filters
from io import BytesIO
from .base import call_api
from app.services.nlp_service import parse_with_groq


async def handle_nlp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parsed = parse_with_groq(text)

    intent = parsed.get("intent")
    ticker = parsed.get("ticker")
    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")

    # 🔹 Highest Volume
    if intent == "highest_volume" and ticker:
        params = {"start_date": start_date, "end_date": end_date}
        # remove None para não poluir a query
        params = {k: v for k, v in params.items() if v}

        r = call_api(f"/highest_volume/{ticker}", params=params)
        data = r.json()

        if "error" in data:
            await update.message.reply_text(data["error"])
        else:
            await update.message.reply_text(
                f"{ticker} - Maior volume {data['highest_volume']} em {data['date']}"
            )

    # 🔹 Lowest Closing Price
    elif intent == "lowest_closing_price" and ticker:
        params = {"start_date": start_date, "end_date": end_date}
        params = {k: v for k, v in params.items() if v}

        r = call_api(f"/lowest_closing_price/{ticker}", params=params)
        data = r.json()

        if "error" in data:
            await update.message.reply_text(data["error"])
        else:
            await update.message.reply_text(
                f"{ticker} - Menor fechamento {data['lowest_closing_price']} em {data['date']}"
            )

    # 🔹 Consolidated Metrics (gera Excel)
    elif intent == "consolidated_metrics":
        params = {}
        if ticker:
            params["ticker"] = ticker
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        r = call_api("/consolidated_metrics", params=params)
        if r.status_code != 200 or "application/json" in r.headers.get("content-type", "").lower():
            try:
                msg = r.json().get("error", "Erro ao gerar métricas.")
            except Exception:
                msg = "Erro ao gerar métricas."
            await update.message.reply_text(msg)
        else:
            file_bytes = BytesIO(r.content)
            file_bytes.seek(0)
            filename = f"{ticker or 'ALL'}_metrics.xlsx"
            await update.message.reply_document(
                document=InputFile(file_bytes, filename=filename),
                caption=f"Métricas consolidadas ({ticker or 'TODOS'})"
            )

    else:
        await update.message.reply_text(
            "Não consegui entender sua pergunta. "
            "Tente algo como: 'Qual o maior volume da BBVA em 2020?'"
        )


def handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, handle_nlp)
