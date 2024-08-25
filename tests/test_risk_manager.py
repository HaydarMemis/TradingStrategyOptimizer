import unittest
from unittest.mock import Mock
from main.utils.risk_manager import RiskManager

class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.risk_manager = RiskManager()
        self.mock_balance = 10000
        self.mock_price = 100

    def test_calculate_position_size(self):
        risk_percentage = 0.02
        stop_loss_percentage = 0.05
        
        expected_position_size = (self.mock_balance * risk_percentage) / (self.mock_price * stop_loss_percentage)
        actual_position_size = self.risk_manager.calculate_position_size(self.mock_balance, self.mock_price, risk_percentage, stop_loss_percentage)
        
        self.assertAlmostEqual(actual_position_size, expected_position_size, places=2)

    def test_calculate_stop_loss(self):
        entry_price = 100
        stop_loss_percentage = 0.05
        
        expected_stop_loss = entry_price * (1 - stop_loss_percentage)
        actual_stop_loss = self.risk_manager.calculate_stop_loss(entry_price, stop_loss_percentage)
        
        self.assertAlmostEqual(actual_stop_loss, expected_stop_loss, places=2)

    def test_calculate_take_profit(self):
        entry_price = 100
        risk_reward_ratio = 2
        stop_loss_percentage = 0.05
        
        expected_take_profit = entry_price * (1 + (stop_loss_percentage * risk_reward_ratio))
        actual_take_profit = self.risk_manager.calculate_take_profit(entry_price, risk_reward_ratio, stop_loss_percentage)
        
        self.assertAlmostEqual(actual_take_profit, expected_take_profit, places=2)

if __name__ == '__main__':
    unittest.main()
