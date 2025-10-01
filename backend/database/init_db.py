from sqlalchemy import create_engine, text
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables!")

def init_database():
    engine = create_engine(DATABASE_URL)
    
    Base.metadata.create_all(engine)
    
    with engine.connect() as conn:
        conn.execute(text("SELECT create_hypertable('prices', 'time', if_not_exists => TRUE);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_coin_time ON prices (coin_id, time DESC);"))
        
        conn.commit()
    
    print("DB initialized successfully!")

if __name__ == "__main__":
    init_database()
