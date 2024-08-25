import ccxt
import config  # API anahtarlarınızı saklayacağınız bir config dosyası
import pandas as pd
import numpy as np
import time
from data.data_fetcher import DataFetcher
from strategies.indicator_strategy import LorentzianClassification
from utils.risk_manager import RiskManager
from utils.performance_tracker import PerformanceTracker

def connect_to_exchange():
    # Borsa nesnesini oluştur
    exchange = ccxt.binance({
        'apiKey': config.API_KEY,
        'secret': config.SECRET_KEY,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future'  # Vadeli işlemler için. Spot piyasa için bu satırı kaldırın.
        }
    })
    
    return exchange

def main():
    # Borsaya bağlan
    exchange = connect_to_exchange()
    
    # Bağlantıyı test et
    try:
        balance = exchange.fetch_balance()
        print("Bağlantı başarılı. Bakiye:", balance['total'])
    except Exception as e:
        print("Bağlantı hatası:", str(e))
        return

    # Veri çekme
    fetcher = DataFetcher(exchange)
    symbol = 'BTC/USDT'
    timeframe = '1h'
    limit = 2000
    
    # Strateji, risk yönetimi ve performans izleme nesnelerini oluştur
    strategy = LorentzianClassification()
    risk_manager = RiskManager(initial_balance=10000, risk_per_trade=0.02)
    performance_tracker = PerformanceTracker()
    
    # Gerçek zamanlı test döngüsü
    while True:
        try:
            # Güncel veriyi çek
            ohlcv_data = fetcher.fetch_ohlcv(symbol, timeframe, limit)
            
            # Veriyi DataFrame'e dönüştür
            df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Stratejiyi uygula
            features = strategy.calculate_features(df)
            
            # Lorentzian mesafelerini hesapla
            distances = np.zeros((len(features), len(features)))
            for i in range(len(features)):
                for j in range(i+1, len(features)):
                    distances[i, j] = strategy.lorentzian_distance(features[i], features[j])
                    distances[j, i] = distances[i, j]
            
            # Modeli eğit ve tahmin yap
            strategy.model.fit(distances, np.zeros(len(features)))
            predictions = strategy.model.predict(distances)
            
            # Son veri noktası için sinyal oluştur
            current_signal = 1 if predictions[-1] == 1 else -1
            current_price = df['close'].iloc[-1]
            
            # Risk yönetimi
            position_size = risk_manager.calculate_position_size(current_price)
            
            # Alım-satım kararı
            if current_signal == 1:
                print(f"Alım sinyali: {current_price} fiyatından {position_size} adet al")
                performance_tracker.record_trade('buy', current_price, position_size)
            elif current_signal == -1:
                print(f"Satım sinyali: {current_price} fiyatından {position_size} adet sat")
                performance_tracker.record_trade('sell', current_price, position_size)
            
            # Performans metrikleri hesapla ve göster
            metrics = performance_tracker.calculate_performance()
            print(f"Güncel performans: Toplam K/Z: {metrics['total_profit_loss']:.2f}, Kazanma Oranı: {metrics['win_rate']:.2f}")
            
            # Bir sonraki veri noktasını bekle
            time.sleep(3600)  # 1 saat bekle (timeframe'e göre ayarlanabilir)
        
        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            time.sleep(60)  # Hata durumunda 1 dakika bekle ve tekrar dene

if __name__ == "__main__":
    main()
