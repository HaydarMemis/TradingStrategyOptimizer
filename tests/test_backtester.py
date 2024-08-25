import unittest
import pandas as pd
from main.utils.backtester import Backtester, run_backtest

class TestBacktester(unittest.TestCase):
    def setUp(self):
        # Test için örnek veri oluştur
        self.test_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [102, 103, 104, 105, 106],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105]
        }, index=pd.date_range(start='2023-01-01', periods=5))

        # Basit bir test stratejisi
        def test_strategy(row):
            return 1 if row['close'] > row['open'] else -1

        self.strategy = test_strategy
        self.initial_balance = 10000

    def test_backtester_initialization(self):
        backtester = Backtester(self.test_data, self.strategy, self.initial_balance)
        self.assertEqual(backtester.initial_balance, self.initial_balance)
        self.assertEqual(backtester.current_balance, self.initial_balance)
        self.assertEqual(len(backtester.positions), 0)
        self.assertEqual(len(backtester.trades), 0)

    def test_run_backtest(self):
        result = run_backtest(self.test_data, self.strategy, self.initial_balance)
        self.assertIn('total_return', result)
        self.assertIn('total_profit_loss', result)
        self.assertIn('win_rate', result)
        self.assertIn('total_trades', result)
        self.assertIn('win_trades', result)
        self.assertIn('loss_trades', result)

    def test_open_close_position(self):
        backtester = Backtester(self.test_data, self.strategy, self.initial_balance)
        backtester._open_position(pd.Timestamp('2023-01-01'), 100)
        self.assertEqual(len(backtester.positions), 1)
        backtester._close_position(pd.Timestamp('2023-01-02'), 102)
        self.assertEqual(len(backtester.positions), 0)
        self.assertEqual(len(backtester.trades), 1)

if __name__ == '__main__':
    unittest.main()
