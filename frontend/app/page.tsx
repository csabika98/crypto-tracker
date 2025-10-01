'use client';

import { useState, useEffect } from 'react';
import api, { Coin, PriceHistory, TrendingCoin, PriceData } from '@/lib/api';
import PriceChart from '@/components/PriceChart';

export default function Home() {
  const [coins, setCoins] = useState<Coin[]>([]);
  const [selectedCoin, setSelectedCoin] = useState<string>('bitcoin');
  const [currentPrice, setCurrentPrice] = useState<PriceData | null>(null);
  const [priceHistory, setPriceHistory] = useState<PriceHistory | null>(null);
  const [trending, setTrending] = useState<TrendingCoin[]>([]);
  const [period, setPeriod] = useState<number>(24);
  const [loading, setLoading] = useState<boolean>(true);
  const [initializing, setInitializing] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCoins();
    const interval = setInterval(() => {
      if (coins.length === 0) {
        loadCoins(); 
      }
    }, 5000);
    
    return () => clearInterval(interval);
  }, [coins.length]);

  useEffect(() => {
    if (coins.length > 0) {
      loadTrending();
    }
  }, [coins]);

  useEffect(() => {
    if (selectedCoin && coins.length > 0) {
      loadCurrentPrice(selectedCoin);
      loadPriceHistory(selectedCoin, period);
    }
  }, [selectedCoin, period, coins.length]);

  const loadCoins = async () => {
    try {
      const data = await api.getCoins();
      setCoins(data.coins);
      if (data.coins.length > 0) {
        setInitializing(false);
      }
    } catch (err) {
      console.error('Failed to load coins:', err);
    }
  };

  const loadCurrentPrice = async (coinId: string) => {
    try {
      const data = await api.getCurrentPrice(coinId);
      setCurrentPrice(data);
    } catch (err) {
      console.error('Failed to load current price:', err);
    }
  };

  const loadPriceHistory = async (coinId: string, hours: number) => {
    setLoading(true);
    try {
      const data = await api.getPriceHistory(coinId, hours);
      setPriceHistory(data);
      setError(null);
    } catch (err) {
      setError('Failed to load price history');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadTrending = async () => {
    try {
      const data = await api.getTrending(10);
      setTrending(data.trending);
    } catch (err) {
      console.error('Failed to load trending:', err);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(price);
  };

  const formatPercentage = (percent: number) => {
    const sign = percent >= 0 ? '+' : '';
    return `${sign}${percent.toFixed(2)}%`;
  };


  if (initializing && coins.length === 0) {
    return (
      <main className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mb-4"></div>
          <h2 className="text-2xl font-semibold mb-2">Initializing Data Collection</h2>
          <p className="text-gray-600">Fetching cryptocurrency data from CoinGecko...</p>
          <p className="text-sm text-gray-500 mt-2">This may take 10-15 seconds on first startup</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-600 to-purple-800 text-white py-8 px-4 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-bold mb-2">Crypto Analytics Dashboard</h1>
          <p className="text-purple-100">Real-time cryptocurrency price tracking and analysis</p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <aside className="lg:col-span-1 space-y-6">
            {/* Coins List */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Coins</h2>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {coins.slice(0, 20).map((coin) => (
                  <div
                    key={coin.coin_id}
                    onClick={() => setSelectedCoin(coin.coin_id)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedCoin === coin.coin_id
                        ? 'bg-purple-600 text-white'
                        : 'hover:bg-gray-100'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">{coin.symbol.toUpperCase()}</span>
                      <span className={`text-sm ${selectedCoin === coin.coin_id ? 'text-purple-100' : 'text-gray-600'}`}>
                        {coin.name}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Movers */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Top Movers (24h)</h2>
              {trending.length === 0 ? (
                <p className="text-sm text-gray-500">Calculating trends...</p>
              ) : (
                <div className="space-y-3">
                  {trending.slice(0, 5).map((coin) => (
                    <div key={coin.coin_id} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex justify-between items-start mb-1">
                        <span className="font-semibold">{coin.symbol.toUpperCase()}</span>
                        <span className={`text-sm font-semibold px-2 py-1 rounded ${
                          coin.direction === 'up' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-red-100 text-red-700'
                        }`}>
                          {formatPercentage(coin.change_percent)}
                        </span>
                      </div>
                      <span className="text-sm text-gray-600">{formatPrice(coin.current_price)}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </aside>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {/* Price Header */}
            {currentPrice && (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                  <div>
                    <h2 className="text-2xl font-bold mb-2">{currentPrice.symbol.toUpperCase()}</h2>
                    <div className="text-4xl font-bold text-purple-600 mb-2">
                      {formatPrice(currentPrice.price_usd)}
                    </div>
                    <div className="flex gap-4 text-sm text-gray-600">
                      <span>Market Cap: {currentPrice.market_cap ? formatPrice(currentPrice.market_cap) : 'N/A'}</span>
                      <span>24h Volume: {currentPrice.volume_24h ? formatPrice(currentPrice.volume_24h) : 'N/A'}</span>
                    </div>
                  </div>

                  {/* Period Selector */}
                  <div className="flex gap-2">
                    <button
                      onClick={() => setPeriod(24)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        period === 24
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-200 hover:bg-gray-300'
                      }`}
                    >
                      24H
                    </button>
                    <button
                      onClick={() => setPeriod(168)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        period === 168
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-200 hover:bg-gray-300'
                      }`}
                    >
                      7D
                    </button>
                    <button
                      onClick={() => setPeriod(720)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        period === 720
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-200 hover:bg-gray-300'
                      }`}
                    >
                      30D
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Chart */}
            <div className="bg-white rounded-lg shadow p-6">
              {loading ? (
                <div className="flex justify-center items-center h-96">
                  <p className="text-gray-600">Loading chart data...</p>
                </div>
              ) : priceHistory && priceHistory.prices.length > 0 ? (
                <PriceChart
                  data={priceHistory.prices}
                  coinSymbol={priceHistory.symbol}
                  periodHours={period}
                />
              ) : (
                <div className="flex flex-col justify-center items-center h-96">
                  <p className="text-gray-600 mb-2">Collecting price data...</p>
                  <p className="text-sm text-gray-500">Charts will appear as data accumulates</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
