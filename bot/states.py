# bot/states.py
"""
Centraliza os estados usados pelos ConversationHandlers do bot.
Isso evita import cíclico entre telegram_bot.py e os handlers.
"""

# Estados para consultas de volume e fechamento
ASK_TICKER_HV, ASK_TICKER_LC = range(2)

# Estados para métricas consolidadas
ASK_START, ASK_END, ASK_TICKER_METRICS = range(3)
