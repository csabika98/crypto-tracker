from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # CoinGecko
    COINGECKO_API_URL = os.getenv("COINGECKO_API_URL")
    
    # Collection
    COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", 50))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    
    @classmethod
    def validate(cls):
        """Validate that required config is present"""
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL is required!")
        return True

# Validate on import
Config.validate()
