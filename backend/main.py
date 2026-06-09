import asyncio

from fastapi import FastAPI

from database import create_tables

from polygon_feed import PolygonFeed

from scanner import scanner

from ai_engine import get_top_candidates

app = FastAPI()

feed = PolygonFeed()


@app.on_event("startup")
async def startup():

    create_tables()

    asyncio.create_task(
        feed.connect()
    )


@app.get("/")
def root():

    return {
        "status": "running"
    }


@app.get("/big-trades")
def big_trades():

    return scanner.big_trades[:100]


@app.get("/top-money-flow")
def top_money_flow():

    return get_top_candidates()


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
