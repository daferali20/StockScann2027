import asyncio
import json
import websockets

from scanner import scanner

from config import POLYGON_API_KEY


class PolygonFeed:

    async def connect(self):

        while True:

            try:

                async with websockets.connect(
                    "wss://socket.polygon.io/stocks"
                ) as ws:

                    await ws.send(
                        json.dumps(
                            {
                                "action": "auth",
                                "params": POLYGON_API_KEY
                            }
                        )
                    )

                    await ws.send(
                        json.dumps(
                            {
                                "action": "subscribe",
                                "params": "T.*"
                            }
                        )
                    )

                    print("Connected")

                    while True:

                        msg = await ws.recv()

                        data = json.loads(msg)

                        if not isinstance(data, list):
                            continue

                        for item in data:

                            if item.get("ev") != "T":
                                continue

                            scanner.process_trade(
                                {
                                    "symbol": item.get("sym"),
                                    "price": item.get("p"),
                                    "size": item.get("s"),
                                    "side": "BUY"
                                }
                            )

            except Exception as e:

                print(e)

                await asyncio.sleep(5)
