from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Trade(Base):

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)

    symbol = Column(String(20))

    price = Column(Float)

    size = Column(Integer)

    value = Column(Float)

    side = Column(String(10))

    timestamp = Column(DateTime)


def create_tables():
    Base.metadata.create_all(bind=engine)


def save_trade(data):

    db = SessionLocal()

    trade = Trade(
        symbol=data["symbol"],
        price=data["price"],
        size=data["size"],
        value=data["value"],
        side=data["side"],
        timestamp=data["timestamp"]
    )

    db.add(trade)
    db.commit()
    db.close()
