import numpy as np

class RiskManager:
    def __init__(self, initial_balance, risk_per_trade, max_drawdown=0.2):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.max_drawdown = max_drawdown
        self.trades = []

    def calculate_position_size(self, entry_price, stop_loss):
        risk_amount = self.current_balance * self.risk_per_trade
        price_difference = abs(entry_price - stop_loss)
        position_size = risk_amount / price_difference
        return position_size

    def update_balance(self, profit_loss):
        self.current_balance += profit_loss
        self.trades.append(profit_loss)

    def calculate_drawdown(self):
        peak = self.initial_balance
        drawdown = 0
        for trade in self.trades:
            peak = max(peak, self.initial_balance + trade)
            drawdown = max(drawdown, (peak - (self.initial_balance + trade)) / peak)
        return drawdown

    def check_max_drawdown(self):
        current_drawdown = self.calculate_drawdown()
        return current_drawdown <= self.max_drawdown

    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        returns = np.array(self.trades) / self.initial_balance
        excess_returns = returns - risk_free_rate / 252  # Günlük risk-free oran
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
        return sharpe_ratio

    def calculate_total_return(self):
        total_return = (self.current_balance - self.initial_balance) / self.initial_balance
        return total_return * 100  # Yüzde olarak döndür

    def get_risk_metrics(self):
        return {
            "current_balance": self.current_balance,
            "total_return": self.calculate_total_return(),
            "drawdown": self.calculate_drawdown(),
            "sharpe_ratio": self.calculate_sharpe_ratio()
        }
