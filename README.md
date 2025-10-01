# TOC
- [Cryptocurrency Analytics Platform](#cryptocurrency-analytics-platform)
  * [Use-Case](#use-case)
  * [Core Functionality](#core-functionality)
  * [Why This Project?](#why-this-project)
  * [Architecture Overview](#architecture-overview)
  * [Services](#services)
  * [Tech Stack](#tech-stack)
  * [Example Queries](#example-queries)
  * [Installation-Docker](#installation-docker)
  * [Local Installation](#local-installation)
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
## Installation [Docker]

1. Clone the repository 

2. Simply run the following:

```
docker compose up --build
```

The app is set to capture data in every 50 seconds, you can change this by modifying COLLECTION_INTERVAL in the docker-compose file

```

crypto_backend      | DB initialized successfully!
crypto_backend      | 
crypto_backend      | Collector running in background
crypto_backend      | 
crypto_backend      | ==================================================
crypto_backend      | ALL SERVICES RUNNING
crypto_backend      | ==================================================
crypto_backend      | 
crypto_backend      | API: http://localhost:8000
crypto_backend      | Docs: http://localhost:8000/docs
crypto_backend      | 
crypto_backend      | Press Ctrl+C to stop
crypto_backend      | 
crypto_frontend     |    ▲ Next.js 15.5.4
crypto_frontend     |    - Local:        http://localhost:3000
crypto_frontend     |    - Network:      http://172.18.0.4:3000
crypto_frontend     | 
crypto_frontend     |  ✓ Starting...
crypto_backend      | START: Starting Crypto Data Collector
crypto_backend      | CONFIG: Collection interval: 50 seconds
crypto_backend      | START: Starting data collection at 2025-10-01 22:46:56
crypto_backend      | INFO:     Started server process [1]
crypto_backend      | INFO:     Waiting for application startup.
crypto_backend      | INFO:     Application startup complete.
crypto_backend      | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
crypto_frontend     |  ✓ Ready in 769ms
crypto_backend      | Added 50 new coins, 50 price records
crypto_backend      | Scheduled to run every 50 seconds
crypto_backend      | Press Ctrl+C to stop
crypto_backend      | 
crypto_backend      | INFO:     172.18.0.1:49596 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49596 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49622 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49626 - "GET /api/coins/bitcoin/history?hours=24 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49612 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49626 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49704 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49734 - "GET /api/coins/bitcoin/history?hours=24 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49704 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49720 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49726 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:49726 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/coins/ethereum/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35568 - "GET /api/coins/ethereum/history?hours=24 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35568 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/coins/bitcoin/history?hours=24 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35568 - "GET /api/coins/bitcoin/history?hours=168 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35568 - "GET /api/coins/bitcoin/history?hours=720 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35568 - "GET /api/coins/bitcoin/history?hours=24 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35568 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:34988 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35002 - "GET /api/coins/bitcoin/history?hours=24 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35574 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
crypto_backend      | START: Starting data collection at 2025-10-01 22:47:47
crypto_backend      | Added 0 new coins, 50 price records
crypto_backend      | INFO:     172.18.0.1:35508 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35508 - "GET /api/coins HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35546 - "GET /api/coins/bitcoin/history?hours=24 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35516 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35530 - "GET /api/coins/bitcoin/price HTTP/1.1" 200 OK
crypto_backend      | INFO:     172.18.0.1:35516 - "GET /api/analytics/trending?limit=10 HTTP/1.1" 200 OK
```

<img width="1848" height="926" alt="image" src="https://github.com/user-attachments/assets/9ed50507-e1ec-4fef-a556-790a814c9250" />

If there is a new pull, simply refresh the page to see.
Also you can click to the coins.. to see the market change
<img width="683" height="463" alt="image" src="https://github.com/user-attachments/assets/67e407bc-6bef-472c-823b-db72eb54cfff" />
<img width="1847" height="919" alt="image" src="https://github.com/user-attachments/assets/34b2f68c-6208-4f7d-85b6-3772ed00fcba" />

## Local Installation

If you want to run it outside docker.

Make sure you have installed PostgreSQL with TimescaleDB, or just pull it from docker (docker pull timescale/timescaledb:latest-pg16)

Create your .env and place it inside the /backend directory or set these environment variables.

Example (make sure to create the db, and user/password correct)
```
# DB Configuration
DATABASE_URL=postgresql://csabasallai:passwordtest@localhost:5432/crypto_db

# CoinGecko Configuration
COINGECKO_API_URL=https://api.coingecko.com/api/v3
COLLECTION_INTERVAL=3600

# Application LOG Settings
LOG_LEVEL=INFO
```

1. Clone the repository
2. CD to the backend directory
3. Create a python virtual env. in this directory 
```
python -m venv venv
```
4. Based on your op.system activate venv
```
source venv/bin/activate or .\venv\bin\Activate.ps1
```
5. Install the dependencies
```
pip install -r requirements.txt
```
6. CD to the root dir
7. Build frontend, CD to the frontend directory
```
npm ci
npm run build
```
8. Start backend from the root dir.
```
python run.py
```
9. Start frontend from the frontend dir.
```
npm run start
```

If you wish to see the data from the API:

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
