- [Cryptocurrency Analytics Platform](#cryptocurrency-analytics-platform)
  * [Use-Case](#use-case)
  * [Core Functionality](#core-functionality)
  * [Why This Project?](#why-this-project)
  * [Architecture Overview](#architecture-overview)
  * [Services](#services)
  * [Tech Stack](#tech-stack)
  * [Example Queries](#example-queries)
  * [How to run?](#how-to-run)
  * [API endpoints](#available-api-endpoints)

# Cryptocurrency Analytics Platform

## Use-Case:
To **track and analyze cryptocurrency prices in real-time**, helping you understand market trends and make informed decisions. 
Think of it as your personal crypto market observatory.

## Core Functionality
* Automatic Data Collection
* Smart Analytics
* Dashboard

## Why This Project?

- **CoinGecko API** - Free, no API key required, reliable data source about Cryptocurrency
- **Time-series optimized** - PostgreSQL + TimescaleDB ideal for price data (initially i had an idea of using NoSQL -> MongoDB)
- **Business relevance** - Price trend analysis, volatility tracking, ROI calculations
- **Engaging visualizations** - Price charts, comparisons, and insights


**Key Differences from MongoDB version:**
- SQL-based schema with proper relationships
- TimescaleDB hypertables for automatic time-series optimization
- Example SQL queries showing analytics capabilities
- SQLAlchemy ORM integration
- More structured data modeling approach


## Architecture Overview

Mermaid Chart:
<img width="3343" height="3840" alt="Untitled diagram _ Mermaid Chart-2025-10-01-192558" src="https://github.com/user-attachments/assets/883dc174-ecbf-4f8d-8e2f-96e1e65b4697" />


```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Data Collector │ ───> │  PostgreSQL +   │ <─── │  Analytics      │
│  Service        │      │  TimescaleDB    │      │  Service        │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────────┐
                                                   │  API Service    │
                                                   └─────────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────────┐
                                                   │  Frontend       │
                                                   │  Dashboard      │
                                                   └─────────────────┘
```

## Services

1. **Collector** - Periodic data collection (Python + APScheduler) (https://pypi.org/project/APScheduler/)
2. **Analytics** - Trend calculation, volatility analysis, price change percentages
3. **API** - FastAPI REST endpoints with SQLAlchemy ORM
4. **Frontend** - React dashboard with Chart.js visualizations
5. **PostgreSQL + TimescaleDB** - Optimized time-series data storage

## Tech Stack

- **Backend**: Python, FastAPI(https://fastapi.tiangolo.com/), SQLAlchemy (https://www.sqlalchemy.org/)
- **Database**: PostgreSQL + TimescaleDB 
- **Frontend**: Basic React, Chart.js
- **Data Source**: CoinGecko API
- **Scheduler**: APScheduler
- **Containerization**: Docker & Docker Compose

## Example Queries

```
~/Desktop/Projects/crypto-tracker% docker exec -it crypto_timescaledb psql -U csabasallai -d crypto_db
psql (16.10)
Type "help" for help.

crypto_db=# SELECT coin_id, name, symbol FROM coins ORDER BY name LIMIT 10;
               coin_id                |                  name                  | symbol  
--------------------------------------+----------------------------------------+---------
 aave                                 | Aave                                   | aave
 aptos                                | Aptos                                  | apt
 avalanche-2                          | Avalanche                              | avax
 binancecoin                          | BNB                                    | bnb
 binance-bridged-usdt-bnb-smart-chain | Binance Bridged USDT (BNB Smart Chain) | bsc-usd
 bitcoin                              | Bitcoin                                | btc
 bitcoin-cash                         | Bitcoin Cash                           | bch
 bitget-token                         | Bitget Token                           | bgb
 cardano                              | Cardano                                | ada
 chainlink                            | Chainlink                              | link
(10 rows)

crypto_db=# 
```
## How to run?

1. Clone the repository 

2. Simply run the following:

```
docker compose up --build
```

## Available API endpoints

### API Reference

Base URL: `http://localhost:8000`

### Base Endpoints

### GET /
Returns API information and version.

**Response:**
```json
{
  "message": "Crypto Analytics API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### GET /health
Health check endpoint with database connectivity test.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

###  Coins Endpoints

### GET /api/coins
Returns all tracked cryptocurrencies.

**Response:**
```json
{
  "count": 50,
  "coins": [
    {
      "coin_id": "bitcoin",
      "name": "Bitcoin",
      "symbol": "BTC",
      "image_url": "https://..."
    }
  ]
}
```

### GET /api/coins/{coin_id}/price
Returns current price data for a specific coin.

**Parameters:**
- `coin_id` (path) - Coin identifier (e.g., "bitcoin", "ethereum")

**Response:**
```json
{
  "coin_id": "bitcoin",
  "symbol": "BTC",
  "price_usd": 117747.00,
  "market_cap": 2346478676373,
  "volume_24h": 67635483758,
  "timestamp": "2025-10-01T21:54:01Z"
}
```

### GET /api/coins/{coin_id}/history
Returns historical price data for a specific coin.

**Parameters:**
- `coin_id` (path) - Coin identifier
- `hours` (query) - Number of hours of history (1-720, default: 24)

**Response:**
```json
{
  "coin_id": "bitcoin",
  "symbol": "BTC",
  "period_hours": 24,
  "data_points": 24,
  "prices": [
    {
      "time": "2025-10-01T20:54:01Z",
      "price": 117500.00,
      "market_cap": 2345000000000,
      "volume": 67000000000
    }
  ]
}
```

---

###  Analytics Endpoints

### GET /api/analytics/trending
Returns top price movers in the last 24 hours.

**Parameters:**
- `limit` (query) - Number of results (1-50, default: 10)

**Response:**
```json
{
  "period": "24h",
  "count": 10,
  "trending": [
    {
      "coin_id": "bitcoin",
      "symbol": "BTC",
      "current_price": 117747.00,
      "price_24h_ago": 115000.00,
      "change_percent": 2.39,
      "last_update": "2025-10-01T21:54:01Z",
      "direction": "up"
    }
  ]
}
```

### GET /api/analytics/summary
Returns overall market statistics.

**Response:**
```json
{
  "total_coins_tracked": 50,
  "total_market_cap": 2500000000000,
  "total_volume_24h": 100000000000
}
```

---

###  Interactive Documentation

### GET /docs
Access the auto-generated Swagger UI documentation with interactive API testing.

---
