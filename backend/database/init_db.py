from sqlalchemy import create_engine, text
import sys
import os
from backend.database.models import Base
from backend.config import Config

def init_database():
    engine = create_engine(Config.DATABASE_URL)
    
    Base.metadata.create_all(engine)
    
    with engine.connect() as conn:
        conn.execute(text("SELECT create_hypertable('prices', 'time', if_not_exists => TRUE);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_coin_time ON prices (coin_id, time DESC);"))
        
        conn.commit()
    
    print("DB initialized successfully!")

if __name__ == "__main__":
    init_database()
