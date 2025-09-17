# bot/handlers/base.py
import requests
from io import BytesIO
from telegram import InputFile
import os

# 🔹 Mantém compatibilidade local e Docker
# - Se tiver API_URL no .env → usa
# - Se não tiver → assume 127.0.0.1:8000
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def call_api(endpoint: str, params=None):
    """Chama a API e retorna o Response"""
    r = requests.get(f"{API_URL}{endpoint}", params=params)
    return r

def post_file(endpoint: str, ticker: str, file_name: str, file_bytes: bytes):
    """Upload de CSV para a API"""
    files = {"file": (file_name, file_bytes)}
    r = requests.post(f"{API_URL}{endpoint}", params={"ticker": ticker}, files=files)
    return r.json()

def send_excel(update, r, filename, caption):
    """Envia um arquivo Excel como resposta do bot"""
    file_bytes = BytesIO(r.content)
    file_bytes.seek(0)
    return update.message.reply_document(
        document=InputFile(file_bytes, filename=filename),
        caption=caption
    )
