from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    
    # CoinGecko
    COINGECKO_API_URL = os.getenv(
        "COINGECKO_API_URL", 
        "https://api.coingecko.com/api/v3"
    )
    
    # Collection
    COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", 3600))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Validate that required config is present"""
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is required!")
        return True

# Validate on import
Config.validate()
