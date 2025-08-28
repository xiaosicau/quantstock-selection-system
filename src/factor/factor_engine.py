"""
因子引擎 - 因子计算与管理的核心模块
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from abc import ABC, abstractmethod

class Factor(ABC):
    """因子基类"""
    
    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """
        计算因子值
        
        Args:
            data: 输入数据
            
        Returns:
            因子值序列
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取因子名称"""
        pass

class FactorEngine:
    """因子引擎类"""
    
    def __init__(self, config: Dict = None):
        """
        初始化因子引擎
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 因子注册表
        self.factors = {}
        
        # 因子数据缓存
        self.factor_data = {}
        
        self.logger.info("因子引擎初始化完成")
    
    def register_factor(self, factor: Factor):
        """注册因子"""
        name = factor.get_name()
        self.factors[name] = factor
        self.logger.info(f"注册因子: {name}")
    
    def calculate_all_factors(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算所有因子"""
        self.logger.info("开始计算所有因子...")
        
        factor_data = pd.DataFrame(index=data.index)
        
        for name, factor in self.factors.items():
            try:
                factor_values = factor.calculate(data)
                factor_data[name] = factor_values
                self.logger.info(f"计算因子 {name} 完成")
            except Exception as e:
                self.logger.error(f"计算因子 {name} 失败: {e}")
        
        self.factor_data = factor_data
        return factor_data
    
    def get_factor_data(self, factor_name: str = None) -> pd.DataFrame:
        """获取因子数据"""
        if factor_name:
            return self.factor_data[[factor_name]]
        return self.factor_data
    
    def save_factors(self, filepath: str):
        """保存因子数据"""
        if self.factor_data is not None:
            self.factor_data.to_csv(filepath)
            self.logger.info(f"因子数据已保存: {filepath}")
    
    def load_factors(self, filepath: str):
        """加载因子数据"""
        try:
            self.factor_data = pd.read_csv(filepath, index_col=0)
            self.logger.info(f"因子数据已加载: {filepath}")
        except Exception as e:
            self.logger.error(f"加载因子数据失败: {e}")

class ValueFactor(Factor):
    """价值因子"""
    
    def __init__(self, pe_window: int = 252):
        self.pe_window = pe_window
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算价值因子"""
        # 使用市盈率倒数作为价值因子
        pe_ratio = data['pe_ratio']
        value_factor = 1 / pe_ratio
        return value_factor
    
    def get_name(self) -> str:
        return "value_factor"

class MomentumFactor(Factor):
    """动量因子"""
    
    def __init__(self, lookback_period: int = 252):
        self.lookback_period = lookback_period
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算动量因子"""
        # 使用过去252天的收益率作为动量因子
        returns = data['close'].pct_change(self.lookback_period)
        momentum_factor = returns
        return momentum_factor
    
    def get_name(self) -> str:
        return "momentum_factor"

class QualityFactor(Factor):
    """质量因子"""
    
    def __init__(self, roe_window: int = 4):
        self.roe_window = roe_window
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算质量因子"""
        # 使用ROE作为质量因子
        roe = data['roe']
        quality_factor = roe
        return quality_factor
    
    def get_name(self) -> str:
        return "quality_factor"

class SizeFactor(Factor):
    """规模因子"""
    
    def __init__(self):
        pass
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算规模因子"""
        # 使用市值对数作为规模因子（负相关）
        market_cap = data['market_cap']
        size_factor = -np.log(market_cap)
        return size_factor
    
    def get_name(self) -> str:
        return "size_factor"

class VolatilityFactor(Factor):
    """波动率因子"""
    
    def __init__(self, volatility_window: int = 252):
        self.volatility_window = volatility_window
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算波动率因子"""
        # 使用负波动率作为因子（低波动率偏好）
        returns = data['close'].pct_change()
        volatility = returns.rolling(window=self.volatility_window).std()
        volatility_factor = -volatility
        return volatility_factor
    
    def get_name(self) -> str:
        return "volatility_factor"

class LiquidityFactor(Factor):
    """流动性因子"""
    
    def __init__(self, liquidity_window: int = 20):
        self.liquidity_window = liquidity_window
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算流动性因子"""
        # 使用成交额对数作为流动性因子
        turnover = data['turnover']
        liquidity_factor = np.log(turnover)
        return liquidity_factor
    
    def get_name(self) -> str:
        return "liquidity_factor"

class GrowthFactor(Factor):
    """成长因子"""
    
    def __init__(self, growth_window: int = 4):
        self.growth_window = growth_window
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """计算成长因子"""
        # 使用净利润增长率作为成长因子
        net_profit_growth = data['net_profit_growth']
        growth_factor = net_profit_growth
        return growth_factor
    
    def get_name(self) -> str:
        return "growth_factor"