from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from backend.database.models import Coin, Price
from backend.config import Config

app = FastAPI(
    title="Crypto Analytics API",
    description="Real-time cryptocurrency price tracking and analytics",
    version="1.0.0"
)

# CORS - to allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Db configs
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/")
def root():
    return {
        "message": "Crypto Analytics API", 
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

@app.get("/api/coins")
def get_coins(db: Session = Depends(get_db)):
    """Get all tracked coins"""
    coins = db.query(Coin).all()
    return {
        "count": len(coins),
        "coins": [
            {
                "coin_id": c.coin_id,
                "name": c.name,
                "symbol": c.symbol.upper(),
                "image_url": c.image_url
            } for c in coins
        ]
    }

@app.get("/api/coins/{coin_id}/price")
def get_current_price(coin_id: str, db: Session = Depends(get_db)):
    """Get latest price for a coin"""
    price = db.query(Price).filter(
        Price.coin_id == coin_id
    ).order_by(Price.time.desc()).first()
    
    if not price:
        raise HTTPException(status_code=404, detail="Coin not found")
    
    return {
        "coin_id": price.coin_id,
        "symbol": price.symbol.upper(),
        "price_usd": float(price.price_usd),
        "market_cap": price.market_cap,
        "volume_24h": price.volume_24h,
        "timestamp": price.time
    }

@app.get("/api/coins/{coin_id}/history")
def get_price_history(
    coin_id: str,
    hours: int = Query(24, ge=1, le=720, description="Hours of history (1-720)"),
    db: Session = Depends(get_db)
):
    """Get historical prices"""
    start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    prices = db.query(Price).filter(
        Price.coin_id == coin_id,
        Price.time >= start_time
    ).order_by(Price.time).all()
    
    if not prices:
        raise HTTPException(status_code=404, detail="No data found for this coin")
    
    return {
        "coin_id": coin_id,
        "symbol": prices[0].symbol.upper(),
        "period_hours": hours,
        "data_points": len(prices),
        "prices": [
            {
                "time": p.time,
                "price": float(p.price_usd),
                "market_cap": p.market_cap,
                "volume": p.volume_24h
            } for p in prices
        ]
    }

@app.get("/api/analytics/trending")
def get_trending(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """Get top movers in last 24h"""
    query = text("""
        WITH price_changes AS (
            SELECT 
                coin_id,
                symbol,
                FIRST(price_usd, time) as price_24h_ago,
                LAST(price_usd, time) as current_price,
                LAST(time, time) as last_update
            FROM prices
            WHERE time > NOW() - INTERVAL '24 hours'
            GROUP BY coin_id, symbol
        )
        SELECT 
            coin_id,
            symbol,
            current_price,
            price_24h_ago,
            ((current_price - price_24h_ago) / price_24h_ago * 100) as change_pct,
            last_update
        FROM price_changes
        WHERE price_24h_ago IS NOT NULL 
          AND current_price IS NOT NULL
          AND price_24h_ago != current_price  -- Filter out 0% changes
        ORDER BY ABS((current_price - price_24h_ago) / price_24h_ago) DESC
        LIMIT :limit
    """)
    
    result = db.execute(query, {"limit": limit})
    rows = result.fetchall()
    
    return {
        "period": "24h",
        "count": len(rows),
        "trending": [
            {
                "coin_id": row[0],
                "symbol": row[1].upper(),
                "current_price": float(row[2]),
                "price_24h_ago": float(row[3]),
                "change_percent": round(float(row[4]), 2),
                "last_update": row[5],
                "direction": "up" if float(row[4]) > 0 else "down"
            } for row in rows
        ]
    }
   

@app.get("/api/analytics/summary")
def get_market_summary(db: Session = Depends(get_db)):
    """Get overall market summary"""
    query = text("""
        SELECT 
            COUNT(DISTINCT coin_id) as total_coins,
            SUM(market_cap) as total_market_cap,
            SUM(volume_24h) as total_volume_24h
        FROM (
            SELECT DISTINCT ON (coin_id) 
                coin_id, market_cap, volume_24h
            FROM prices
            ORDER BY coin_id, time DESC
        ) latest_prices
    """)
    
    result = db.execute(query).fetchone()
    
    return {
        "total_coins_tracked": result[0],
        "total_market_cap": result[1],
        "total_volume_24h": result[2]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
