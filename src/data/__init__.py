"""
数据模块 - 负责数据获取、清洗、存储和管理

功能包括：
- 多数据源集成（Tushare、AkShare、Wind等）
- 实时行情获取
- 历史数据下载
- 数据清洗与验证
- 数据缓存与更新
- 数据质量检查
"""

from .data_manager import DataManager
from .market_data import MarketData
from .stock_data import StockData
from .fundamental_data import FundamentalData

__all__ = [
    'DataManager',
    'MarketData', 
    'StockData',
    'FundamentalData'
]