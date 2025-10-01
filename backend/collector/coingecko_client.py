import requests
from typing import List, Dict
import time
import os
import sys
from backend.config import Config

class CoinGeckoClient:
    BASE_URL = Config.COINGECKO_API_URL
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_top_coins(self, limit: int = 50) -> List[Dict]:
        """Get top N cryptocurrencies by market cap"""
        url = f"{self.BASE_URL}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: fetching coins: {e}")
            return []
    
    def get_coin_data(self, coin_ids: List[str]) -> List[Dict]:
        """Get detailed data for specific coins"""
        # CoinGecko free tier: max 10-50 calls/minute
        # So then lets batch by getting markets endpoint
        return self.get_top_coins(limit=100)

# For Quick Test
if __name__ == "__main__":
    client = CoinGeckoClient()
    coins = client.get_top_coins(10)
    for coin in coins:
        print(f"{coin['symbol'].upper()}: ${coin['current_price']}")
