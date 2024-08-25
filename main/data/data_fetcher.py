import ccxt

class DataFetcher:
    def __init__(self, exchange_name):
        self.exchange = getattr(ccxt, exchange_name)()

    def fetch_ohlcv(self, symbol, timeframe, limit):
        return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)