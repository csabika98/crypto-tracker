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
