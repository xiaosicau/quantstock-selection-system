"""
量化股票选股系统 - 核心模块

这是一个基于多因子模型的量化股票选股系统，包含以下核心模块：

1. api - API接口模块
2. backtest - 回测引擎
3. data - 数据获取与处理
4. factor - 因子分析与计算
5. models - 机器学习模型
6. risk - 风险管理系统
7. strategy - 策略实现
8. utils - 工具函数

系统特点：
- 多数据源集成
- 实时行情获取
- 智能因子分析
- 风险监控预警
- Web可视化界面
"""

__version__ = "1.0.0"
__author__ = "QuantStock Team"
__email__ = "quantstock@example.com"

# 导入核心模块
from . import api
from . import backtest
from . import data
from . import factor
from . import models
from . import risk
from . import strategy
from . import utils

# 定义公共API
__all__ = [
    'api',
    'backtest', 
    'data',
    'factor',
    'models',
    'risk',
    'strategy',
    'utils'
]