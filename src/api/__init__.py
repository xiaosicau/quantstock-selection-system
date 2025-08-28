"""
API模块 - 量化股票选股系统API接口

提供RESTful API和WebSocket接口，支持：
1. 实时行情数据获取
2. 策略回测服务
3. 因子分析计算
4. 选股结果推送
"""

__version__ = "1.0.0"
__author__ = "QuantStock Team"

from .rest_api import RestAPI
from .websocket_api import WebSocketAPI
from .data_api import DataAPI
from .backtest_api import BacktestAPI
from .factor_api import FactorAPI

__all__ = [
    'RestAPI',
    'WebSocketAPI', 
    'DataAPI',
    'BacktestAPI',
    'FactorAPI'
]