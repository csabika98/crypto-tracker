import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Coin {
  coin_id: string;
  name: string;
  symbol: string;
  image_url?: string;
}

export interface PriceData {
  coin_id: string;
  symbol: string;
  price_usd: number;
  market_cap: number;
  volume_24h: number;
  timestamp: string;
}

export interface PricePoint {
  time: string;
  price: number;
  market_cap?: number;
  volume?: number;
}

export interface PriceHistory {
  coin_id: string;
  symbol: string;
  period_hours: number;
  data_points: number;
  prices: PricePoint[];
}

export interface TrendingCoin {
  coin_id: string;
  symbol: string;
  current_price: number;
  price_24h_ago: number;
  change_percent: number;
  last_update: string;
  direction: 'up' | 'down';
}

export interface MarketSummary {
  total_coins_tracked: number;
  total_market_cap: number;
  total_volume_24h: number;
}

const api = {
  async getCoins(): Promise<{ count: number; coins: Coin[] }> {
    const response = await axios.get(`${API_BASE_URL}/api/coins`);
    return response.data;
  },

  async getCurrentPrice(coinId: string): Promise<PriceData> {
    const response = await axios.get(`${API_BASE_URL}/api/coins/${coinId}/price`);
    return response.data;
  },

  async getPriceHistory(coinId: string, hours: number = 24): Promise<PriceHistory> {
    const response = await axios.get(
      `${API_BASE_URL}/api/coins/${coinId}/history?hours=${hours}`
    );
    return response.data;
  },

  async getTrending(limit: number = 10): Promise<{ period: string; count: number; trending: TrendingCoin[] }> {
    const response = await axios.get(`${API_BASE_URL}/api/analytics/trending?limit=${limit}`);
    return response.data;
  },

  async getMarketSummary(): Promise<MarketSummary> {
    const response = await axios.get(`${API_BASE_URL}/api/analytics/summary`);
    return response.data;
  },

  async healthCheck(): Promise<{ status: string; database: string }> {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  },
};

export default api;
