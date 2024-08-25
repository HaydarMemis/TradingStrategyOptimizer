import pandas as pd
import numpy as np
from typing import List, Dict, Callable

class Backtester:
    def __init__(self, data: pd.DataFrame, strategy: Callable, initial_balance: float):
        self.data = data
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.positions: List[Dict] = []
        self.trades: List[Dict] = []

    def run(self) -> Dict:
        for index, row in self.data.iterrows():
            signal = self.strategy(row)
            if signal == 1 and not self.positions:
                self._open_position(index, row['close'])
            elif signal == -1 and self.positions:
                self._close_position(index, row['close'])

        return self._calculate_performance()

    def _open_position(self, date: pd.Timestamp, price: float):
        position_size = self.current_balance * 0.02 / price  # %2 risk
        cost = position_size * price
        self.current_balance -= cost
        self.positions.append({
            'entry_date': date,
            'entry_price': price,
            'size': position_size
        })

    def _close_position(self, date: pd.Timestamp, price: float):
        position = self.positions.pop()
        profit_loss = (price - position['entry_price']) * position['size']
        self.current_balance += (position['size'] * price)
        self.trades.append({
            'entry_date': position['entry_date'],
            'exit_date': date,
            'entry_price': position['entry_price'],
            'exit_price': price,
            'profit_loss': profit_loss
        })

    def _calculate_performance(self) -> Dict:
        total_profit_loss = sum(trade['profit_loss'] for trade in self.trades)
        win_trades = [trade for trade in self.trades if trade['profit_loss'] > 0]
        loss_trades = [trade for trade in self.trades if trade['profit_loss'] <= 0]

        return {
            'total_return': (self.current_balance - self.initial_balance) / self.initial_balance * 100,
            'total_profit_loss': total_profit_loss,
            'win_rate': len(win_trades) / len(self.trades) if self.trades else 0,
            'total_trades': len(self.trades),
            'win_trades': len(win_trades),
            'loss_trades': len(loss_trades)
        }

def run_backtest(data: pd.DataFrame, strategy: Callable, initial_balance: float) -> Dict:
    backtester = Backtester(data, strategy, initial_balance)
    return backtester.run()
