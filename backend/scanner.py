from datetime import datetime

from config import MIN_FLOW_VALUE

from database import save_trade

from alerts import send_big_trade_alert

from ai_engine import update_flow


class Scanner:

    def __init__(self):

        self.big_trades = []

    def process_trade(self, trade):

        symbol = trade["symbol"]
        price = trade["price"]
        size = trade["size"]

        value = price * size

        if value < MIN_FLOW_VALUE:
            return

        side = trade.get("side", "UNKNOWN")

        row = {
            "symbol": symbol,
            "price": price,
            "size": size,
            "value": value,
            "side": side,
            "timestamp": datetime.utcnow()
        }

        self.big_trades.insert(0, row)

        save_trade(row)

        update_flow(symbol, value)

        send_big_trade_alert(symbol, value)

        print(
            f"🔥 {symbol} "
            f"${value:,.0f}"
        )


scanner = Scanner()
