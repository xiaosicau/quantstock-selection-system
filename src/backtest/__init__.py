"""
回测引擎 - 策略回测与性能评估

功能包括：
- 策略回测框架
- 交易信号生成
- 持仓管理
- 绩效分析
- 风险控制
- 结果可视化
"""

from .backtest_engine import BacktestEngine
from .portfolio import Portfolio
from .performance import PerformanceAnalyzer
from .risk_manager import RiskManager

__all__ = [
    'BacktestEngine',
    'Portfolio',
    'PerformanceAnalyzer',
    'RiskManager'
]