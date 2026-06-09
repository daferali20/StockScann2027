import requests

from config import TELEGRAM_TOKEN
from config import TELEGRAM_CHAT_ID


def telegram_alert(message):

    if not TELEGRAM_TOKEN:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
    )


def send_big_trade_alert(symbol, value):

    msg = (
        f"🔥 BIG FLOW\n"
        f"{symbol}\n"
        f"${value:,.0f}"
    )

    telegram_alert(msg)
