import pandas as pd
import numpy as np
from typing import List, Dict

class PerformanceTracker:
    def __init__(self):
        self.trades: List[Dict] = []
        self.current_balance: float = 0
        self.initial_balance: float = 0
        self.total_profit_loss: float = 0
        self.win_count: int = 0
        self.loss_count: int = 0

    def record_trade(self, action: str, price: float, amount: float):
        trade = {
            'action': action,
            'price': price,
            'amount': amount,
            'value': price * amount
        }
        self.trades.append(trade)

    def calculate_performance(self):
        df = pd.DataFrame(self.trades)
        df['cumulative_value'] = df['value'].cumsum()
        
        self.total_profit_loss = df['cumulative_value'].iloc[-1] - self.initial_balance
        self.current_balance = self.initial_balance + self.total_profit_loss
        
        win_trades = df[df['value'] > 0]
        loss_trades = df[df['value'] < 0]
        
        self.win_count = len(win_trades)
        self.loss_count = len(loss_trades)
        
        win_rate = self.win_count / len(df) if len(df) > 0 else 0
        
        # Yeni performans metrikleri
        total_return = (self.current_balance - self.initial_balance) / self.initial_balance * 100
        sharpe_ratio = self.calculate_sharpe_ratio(df)
        max_drawdown = self.calculate_max_drawdown(df)
        profit_factor = self.calculate_profit_factor(df)
        
        return {
            'total_profit_loss': self.total_profit_loss,
            'current_balance': self.current_balance,
            'win_count': self.win_count,
            'loss_count': self.loss_count,
            'win_rate': win_rate,
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'profit_factor': profit_factor
        }

    def calculate_sharpe_ratio(self, df):
        returns = df['value'].pct_change().dropna()
        return np.sqrt(252) * returns.mean() / returns.std()

    def calculate_max_drawdown(self, df):
        cumulative_returns = (1 + df['value'].pct_change()).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns / peak) - 1
        return drawdown.min()

    def calculate_profit_factor(self, df):
        profits = df[df['value'] > 0]['value'].sum()
        losses = abs(df[df['value'] < 0]['value'].sum())
        return profits / losses if losses != 0 else float('inf')

    def reset(self, initial_balance: float):
        self.trades = []
        self.current_balance = initial_balance
        self.initial_balance = initial_balance
        self.total_profit_loss = 0
        self.win_count = 0
        self.loss_count = 0

    def get_trade_history(self) -> pd.DataFrame:
        return pd.DataFrame(self.trades)
