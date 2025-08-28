"""
回测引擎测试
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.backtest.backtest_engine import BacktestEngine, SimpleMovingAverageStrategy

class TestBacktestEngine:
    """回测引擎测试类"""
    
    def setup_method(self):
        """每个测试方法前运行"""
        self.config = {
            'initial_capital': 1000000,
            'commission_rate': 0.001
        }
        self.engine = BacktestEngine(self.config)
    
    def test_initialization(self):
        """测试初始化"""
        assert self.engine.config == self.config
        assert hasattr(self.engine, 'portfolio')
        assert hasattr(self.engine, 'performance_analyzer')
        assert hasattr(self.engine, 'risk_manager')
    
    def test_set_data(self):
        """测试设置数据"""
        test_data = pd.DataFrame({
            'close': [100, 101, 102, 103, 104],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        self.engine.set_data(test_data)
        assert self.engine.data is not None
        assert len(self.engine.data) == 5
    
    def test_set_strategy(self):
        """测试设置策略"""
        strategy = SimpleMovingAverageStrategy(short_window=2, long_window=4)
        self.engine.set_strategy(strategy)
        assert self.engine.strategy is not None
    
    def test_strategy_parameters(self):
        """测试策略参数"""
        strategy = SimpleMovingAverageStrategy()
        params = strategy.get_parameters()
        assert isinstance(params, dict)
        assert 'short_window' in params
        assert 'long_window' in params
    
    def test_simple_moving_average_strategy(self):
        """测试简单移动平均策略"""
        strategy = SimpleMovingAverageStrategy(short_window=2, long_window=4)
        
        # 创建测试数据
        data = pd.DataFrame({
            'close': [100, 101, 102, 101, 100, 99, 98, 99, 100, 101]
        })
        
        signals = strategy.generate_signals(data)
        assert isinstance(signals, pd.DataFrame)
        assert 'signal' in signals.columns
        assert 'sma_short' in signals.columns
        assert 'sma_long' in signals.columns
    
    def test_rsi_strategy(self):
        """测试RSI策略"""
        from src.backtest.backtest_engine import RSIStrategy
        
        strategy = RSIStrategy()
        
        # 创建测试数据
        data = pd.DataFrame({
            'close': [100, 102, 101, 103, 105, 104, 106, 108, 107, 109]
        })
        
        signals = strategy.generate_signals(data)
        assert isinstance(signals, pd.DataFrame)
        assert 'signal' in signals.columns
        assert 'rsi' in signals.columns
    
    def test_calculate_position_size(self):
        """测试仓位计算"""
        test_data = pd.DataFrame({
            'close': [100, 101, 102],
            'price': [100, 101, 102]
        })
        
        self.engine.set_data(test_data)
        strategy = SimpleMovingAverageStrategy()
        self.engine.set_strategy(strategy)
        
        # 测试仓位计算
        signal = pd.Series({'price': 100})
        position_size = self.engine._calculate_position_size(signal)
        assert isinstance(position_size, int)
        assert position_size > 0

if __name__ == "__main__":
    pytest.main([__file__])