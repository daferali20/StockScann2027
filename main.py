import asyncio
import json
from datetime import datetime
from collections import deque

import uvicorn
import websockets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =====================================
# الإعدادات
# =====================================

POLYGON_API_KEY = "PUT_YOUR_KEY_HERE"

MIN_FLOW_VALUE = 500000  # 500 ألف دولار

MAX_STORED_TRADES = 5000

# =====================================
# FastAPI
# =====================================

app = FastAPI(title="Hot Money Flow Scanner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# الذاكرة
# =====================================

big_trades = deque(maxlen=MAX_STORED_TRADES)

symbol_stats = {}

# =====================================
# وظائف الماسح
# =====================================

def update_symbol(symbol, value):

    if symbol not in symbol_stats:
        symbol_stats[symbol] = {
            "money_flow": 0,
            "trades": 0,
            "last_update": None
        }

    symbol_stats[symbol]["money_flow"] += value
    symbol_stats[symbol]["trades"] += 1
    symbol_stats[symbol]["last_update"] = datetime.utcnow()


def process_trade(trade):

    try:

        symbol = trade.get("sym")

        price = float(trade.get("p", 0))
        size = int(trade.get("s", 0))

        trade_value = price * size

        if trade_value < MIN_FLOW_VALUE:
            return

        row = {
            "symbol": symbol,
            "price": price,
            "size": size,
            "value": trade_value,
            "time": datetime.utcnow().isoformat()
        }

        big_trades.appendleft(row)

        update_symbol(symbol, trade_value)

        print(
            f"🔥 {symbol:<6} "
            f"${trade_value:,.0f}"
        )

    except Exception as e:
        print("Trade Error:", e)


# =====================================
# Polygon WebSocket
# =====================================

async def polygon_stream():

    while True:

        try:

            uri = "wss://socket.polygon.io/stocks"

            async with websockets.connect(uri) as ws:

                await ws.send(
                    json.dumps({
                        "action": "auth",
                        "params": POLYGON_API_KEY
                    })
                )

                await ws.send(
                    json.dumps({
                        "action": "subscribe",
                        "params": "T.*"
                    })
                )

                print("Connected To Polygon")

                while True:

                    message = await ws.recv()

                    data = json.loads(message)

                    if not isinstance(data, list):
                        continue

                    for item in data:

                        if item.get("ev") == "T":
                            process_trade(item)

        except Exception as e:

            print("WebSocket Error:", e)

            await asyncio.sleep(5)


# =====================================
# API
# =====================================

@app.get("/")
async def root():

    return {
        "status": "running",
        "scanner": "hot_money_flow"
    }


@app.get("/big-trades")
async def get_big_trades():

    return list(big_trades)


@app.get("/top-flows")
async def get_top_flows():

    rows = []

    for symbol, data in symbol_stats.items():

        rows.append({
            "symbol": symbol,
            "money_flow": data["money_flow"],
            "trades": data["trades"]
        })

    rows.sort(
        key=lambda x: x["money_flow"],
        reverse=True
    )

    return rows[:50]


# =====================================
# Startup
# =====================================

@app.on_event("startup")
async def startup():

    asyncio.create_task(
        polygon_stream()
    )


# =====================================
# Main
# =====================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
