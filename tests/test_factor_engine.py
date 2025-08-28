"""
因子引擎测试
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.factor.factor_engine import FactorEngine, ValueFactor, MomentumFactor, QualityFactor

class TestFactorEngine:
    """因子引擎测试类"""
    
    def setup_method(self):
        """每个测试方法前运行"""
        self.config = {'cache_enabled': False}
        self.engine = FactorEngine(self.config)
    
    def test_initialization(self):
        """测试初始化"""
        assert self.engine.config == self.config
        assert isinstance(self.engine.factors, dict)
        assert isinstance(self.engine.factor_data, dict)
    
    def test_register_factor(self):
        """测试注册因子"""
        factor = ValueFactor()
        self.engine.register_factor(factor)
        assert 'value_factor' in self.engine.factors
    
    def test_value_factor(self):
        """测试价值因子"""
        factor = ValueFactor()
        
        # 创建测试数据
        data = pd.DataFrame({
            'pe_ratio': [10, 15, 20, 25, 30]
        })
        
        values = factor.calculate(data)
        assert isinstance(values, pd.Series)
        assert len(values) == 5
    
    def test_momentum_factor(self):
        """测试动量因子"""
        factor = MomentumFactor()
        
        # 创建测试数据
        data = pd.DataFrame({
            'close': [100, 102, 101, 103, 105]
        })
        
        values = factor.calculate(data)
        assert isinstance(values, pd.Series)
    
    def test_quality_factor(self):
        """测试质量因子"""
        factor = QualityFactor()
        
        # 创建测试数据
        data = pd.DataFrame({
            'roe': [0.1, 0.15, 0.2, 0.25, 0.3]
        })
        
        values = factor.calculate(data)
        assert isinstance(values, pd.Series)
    
    def test_calculate_all_factors(self):
        """测试计算所有因子"""
        # 注册多个因子
        self.engine.register_factor(ValueFactor())
        self.engine.register_factor(MomentumFactor())
        self.engine.register_factor(QualityFactor())
        
        # 创建测试数据
        data = pd.DataFrame({
            'close': [100, 102, 101, 103, 105],
            'pe_ratio': [10, 15, 20, 25, 30],
            'roe': [0.1, 0.15, 0.2, 0.25, 0.3]
        })
        
        factor_data = self.engine.calculate_all_factors(data)
        assert isinstance(factor_data, pd.DataFrame)
        assert len(factor_data.columns) >= 3
    
    def test_factor_names(self):
        """测试因子名称"""
        value_factor = ValueFactor()
        momentum_factor = MomentumFactor()
        
        assert value_factor.get_name() == "value_factor"
        assert momentum_factor.get_name() == "momentum_factor"
    
    def test_save_and_load_factors(self):
        """测试因子保存和加载"""
        # 创建测试数据
        data = pd.DataFrame({
            'close': [100, 102, 101],
            'pe_ratio': [10, 15, 20],
            'roe': [0.1, 0.15, 0.2]
        })
        
        # 计算因子
        self.engine.register_factor(ValueFactor())
        self.engine.register_factor(MomentumFactor())
        self.engine.calculate_all_factors(data)
        
        # 保存和加载
        self.engine.save_factors('test_factors.csv')
        self.engine.load_factors('test_factors.csv')
        
        # 清理测试文件
        import os
        try:
            os.remove('test_factors.csv')
        except:
            pass

if __name__ == "__main__":
    pytest.main([__file__])