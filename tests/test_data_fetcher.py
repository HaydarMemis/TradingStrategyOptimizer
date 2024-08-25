import unittest
from unittest.mock import Mock, patch
from main.data.data_fetcher import DataFetcher

class TestDataFetcher(unittest.TestCase):
    def setUp(self):
        self.exchange_name = 'binance'
        self.data_fetcher = DataFetcher(self.exchange_name)

    @patch('ccxt.binance')
    def test_fetch_ohlcv(self, mock_exchange):
        # Sahte veri oluştur
        mock_ohlcv_data = [
            [1625097600000, 35000, 35100, 34900, 35050, 100],
            [1625184000000, 35050, 35200, 34950, 35150, 120]
        ]
        
        # Mock exchange'in fetch_ohlcv metodunu yapılandır
        mock_exchange.return_value.fetch_ohlcv.return_value = mock_ohlcv_data
        
        # DataFetcher'ın fetch_ohlcv metodunu çağır
        symbol = 'BTC/USDT'
        timeframe = '1d'
        limit = 2
        result = self.data_fetcher.fetch_ohlcv(symbol, timeframe, limit)
        
        # Sonuçları doğrula
        self.assertEqual(result, mock_ohlcv_data)
        mock_exchange.return_value.fetch_ohlcv.assert_called_once_with(symbol, timeframe, limit=limit)

if __name__ == '__main__':
    unittest.main()
