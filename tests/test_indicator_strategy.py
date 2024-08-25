import unittest
import pandas as pd
from main.strategies.indicator_strategy import IndicatorStrategy

class TestIndicatorStrategy(unittest.TestCase):
    def setUp(self):
        # Test için örnek veri oluştur
        self.test_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [102, 103, 104, 105, 106],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105]
        }, index=pd.date_range(start='2023-01-01', periods=5))
        
        self.strategy = IndicatorStrategy()

    def test_generate_signals(self):
        signals = self.strategy.generate_signals(self.test_data)
        self.assertIsInstance(signals, pd.Series)
        self.assertEqual(len(signals), len(self.test_data))
        self.assertTrue(all(signal in [-1, 0, 1] for signal in signals))

    def test_calculate_indicators(self):
        indicators = self.strategy.calculate_indicators(self.test_data)
        self.assertIsInstance(indicators, pd.DataFrame)
        self.assertEqual(len(indicators), len(self.test_data))
        # Burada, stratejinizde kullandığınız indikatörlerin varlığını kontrol edin
        # Örnek: self.assertIn('SMA', indicators.columns)

    def test_strategy_logic(self):
        indicators = self.strategy.calculate_indicators(self.test_data)
        signal = self.strategy.strategy_logic(indicators.iloc[-1])
        self.assertIn(signal, [-1, 0, 1])

if __name__ == '__main__':
    unittest.main()
