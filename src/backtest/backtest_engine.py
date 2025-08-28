"""
回测引擎 - 核心回测框架
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from abc import ABC, abstractmethod

from .portfolio import Portfolio
from .performance import PerformanceAnalyzer
from .risk_manager import RiskManager

class Strategy(ABC):
    """策略基类"""
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        生成交易信号
        
        Args:
            data: 输入数据
            
        Returns:
            包含信号的数据框
        """
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict:
        """获取策略参数"""
        pass

class BacktestEngine:
    """回测引擎类"""
    
    def __init__(self, config: Dict = None):
        """
        初始化回测引擎
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 初始化组件
        self.portfolio = Portfolio(
            initial_capital=self.config.get('initial_capital', 1000000)
        )
        self.performance_analyzer = PerformanceAnalyzer()
        self.risk_manager = RiskManager(self.config.get('risk_config', {}))
        
        # 回测数据
        self.data = None
        self.strategy = None
        self.results = None
        
    def set_data(self, data: pd.DataFrame):
        """设置回测数据"""
        self.data = data.copy()
        self.logger.info(f"设置回测数据: {len(data)} 条记录")
    
    def set_strategy(self, strategy: Strategy):
        """设置策略"""
        self.strategy = strategy
        self.logger.info(f"设置策略: {strategy.__class__.__name__}")
    
    def run_backtest(self) -> Dict:
        """运行回测"""
        if self.data is None:
            raise ValueError("请先设置回测数据")
        if self.strategy is None:
            raise ValueError("请先设置策略")
        
        self.logger.info("开始回测...")
        
        # 生成交易信号
        signals = self.strategy.generate_signals(self.data)
        
        # 执行回测
        results = self._execute_backtest(signals)
        
        # 分析结果
        self.results = self.performance_analyzer.analyze(results)
        
        self.logger.info("回测完成")
        return self.results
    
    def _execute_backtest(self, signals: pd.DataFrame) -> pd.DataFrame:
        """执行回测逻辑"""
        results = []
        
        # 按日期遍历
        for date, daily_data in signals.groupby(level=0):
            # 处理当日交易
            daily_result = self._process_daily_trading(date, daily_data)
            results.append(daily_result)
        
        return pd.DataFrame(results)
    
    def _process_daily_trading(self, date: datetime, daily_signals: pd.DataFrame) -> Dict:
        """处理每日交易"""
        # 检查风险限制
        if not self.risk_manager.check_limits(self.portfolio, daily_signals):
            return {
                'date': date,
                'portfolio_value': self.portfolio.get_total_value(),
                'cash': self.portfolio.cash,
                'positions': self.portfolio.get_positions(),
                'trades': []
            }
        
        # 执行交易
        trades = self._execute_trades(daily_signals)
        
        # 更新持仓
        for trade in trades:
            self.portfolio.execute_trade(trade)
        
        # 更新组合价值
        portfolio_value = self.portfolio.get_total_value()
        
        return {
            'date': date,
            'portfolio_value': portfolio_value,
            'cash': self.portfolio.cash,
            'positions': self.portfolio.get_positions(),
            'trades': trades
        }
    
    def _execute_trades(self, signals: pd.DataFrame) -> List[Dict]:
        """执行交易"""
        trades = []
        
        for idx, signal in signals.iterrows():
            if signal['signal'] == 1:  # 买入信号
                trade = {
                    'type': 'buy',
                    'stock': idx[1] if isinstance(idx, tuple) else idx,
                    'price': signal['price'],
                    'quantity': self._calculate_position_size(signal),
                    'date': signal.name if hasattr(signal, 'name') else idx[0]
                }
                trades.append(trade)
            elif signal['signal'] == -1:  # 卖出信号
                trade = {
                    'type': 'sell',
                    'stock': idx[1] if isinstance(idx, tuple) else idx,
                    'price': signal['price'],
                    'quantity': self._calculate_position_size(signal),
                    'date': signal.name if hasattr(signal, 'name') else idx[0]
                }
                trades.append(trade)
        
        return trades
    
    def _calculate_position_size(self, signal: pd.Series) -> int:
        """计算仓位大小"""
        # 简单的仓位计算方法：可用资金的10%
        available_cash = self.portfolio.cash
        position_size = available_cash * 0.1 / signal['price']
        return int(position_size)
    
    def get_results(self) -> Dict:
        """获取回测结果"""
        if self.results is None:
            raise ValueError("请先运行回测")
        return self.results
    
    def save_results(self, filepath: str):
        """保存回测结果"""
        if self.results is None:
            raise ValueError("请先运行回测")
        
        import json
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        self.logger.info(f"回测结果已保存: {filepath}")

class SimpleMovingAverageStrategy(Strategy):
    """简单移动平均策略"""
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        signals = data.copy()
        
        # 计算移动平均线
        signals['sma_short'] = signals['close'].rolling(window=self.short_window).mean()
        signals['sma_long'] = signals['close'].rolling(window=self.long_window).mean()
        
        # 生成信号
        signals['signal'] = 0
        signals.loc[signals['sma_short'] > signals['sma_long'], 'signal'] = 1
        signals.loc[signals['sma_short'] < signals['sma_long'], 'signal'] = -1
        
        return signals
    
    def get_parameters(self) -> Dict:
        """获取策略参数"""
        return {
            'short_window': self.short_window,
            'long_window': self.long_window
        }

class RSIStrategy(Strategy):
    """RSI策略"""
    
    def __init__(self, window: int = 14, oversold: int = 30, overbought: int = 70):
        self.window = window
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        signals = data.copy()
        
        # 计算RSI
        delta = signals['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()
        rs = gain / loss
        signals['rsi'] = 100 - (100 / (1 + rs))
        
        # 生成信号
        signals['signal'] = 0
        signals.loc[signals['rsi'] < self.oversold, 'signal'] = 1
        signals.loc[signals['rsi'] > self.overbought, 'signal'] = -1
        
        return signals
    
    def get_parameters(self) -> Dict:
        """获取策略参数"""
        return {
            'window': self.window,
            'oversold': self.oversold,
            'overbought': self.overbought
        }