from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from backend.collector.coingecko_client import CoinGeckoClient
from backend.database.models import Coin, Price
from backend.config import Config

engine = create_engine(Config.DATABASE_URL)
Session = sessionmaker(bind=engine)

def collect_data():
    """Collect cryptocurrency data from CoinGecko"""
    print(f"START: Starting data collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    client = CoinGeckoClient()
    session = Session()
    
    try:
        # FETCH top 50 coins
        coins_data = client.get_top_coins(limit=50)
        
        if not coins_data:
            print("NO DATA received")
            return
        
        current_time = datetime.now(timezone.utc)
        coins_added = 0
        prices_added = 0
        
        for coin_data in coins_data:
            coin = session.query(Coin).filter_by(
                coin_id=coin_data['id']
            ).first()
            
            if not coin:
                coin = Coin(
                    coin_id=coin_data['id'],
                    name=coin_data['name'],
                    symbol=coin_data['symbol'],
                    image_url=coin_data.get('image')
                )
                session.add(coin)
                coins_added += 1
            
            # INSERT price record
            price = Price(
                time=current_time,
                coin_id=coin_data['id'],
                symbol=coin_data['symbol'],
                price_usd=coin_data['current_price'],
                market_cap=coin_data.get('market_cap'),
                volume_24h=coin_data.get('total_volume')
            )
            session.add(price)
            prices_added += 1
        
        session.commit()
        print(f"Added {coins_added} new coins, {prices_added} price records")
        
    except Exception as e:
        print(f"Error during collection: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    """Run the collector service"""
    print("START: Starting Crypto Data Collector")
    print(f"CONFIG: Collection interval: {Config.COLLECTION_INTERVAL} seconds")
    
    # We will run it immediately on start
    collect_data()
    
    # Schedule to run every X seconds (we can control this from config)
    scheduler = BlockingScheduler()
    scheduler.add_job(
        collect_data, 
        'interval', 
        seconds=Config.COLLECTION_INTERVAL
    )
    
    print(f"Scheduled to run every {Config.COLLECTION_INTERVAL} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nSHUTDOWN: Shutting down collector gracefully")

if __name__ == "__main__":
    main()
