from sqlalchemy import Column, String, Numeric, BigInteger, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Coin(Base):
    __tablename__ = 'coins'
    
    coin_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=False)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class Price(Base):
    __tablename__ = 'prices'
    
    time = Column(DateTime, primary_key=True)
    coin_id = Column(String(50), primary_key=True)
    symbol = Column(String(10), nullable=False)
    price_usd = Column(Numeric(20, 8), nullable=False)
    market_cap = Column(BigInteger)
    volume_24h = Column(BigInteger)
