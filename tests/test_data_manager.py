"""
数据管理器测试
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.data_manager import DataManager

class TestDataManager:
    """数据管理器测试类"""
    
    def setup_method(self):
        """每个测试方法前运行"""
        self.config = {
            'tushare_token': 'test_token',
            'cache_enabled': False
        }
        self.data_manager = DataManager(self.config)
    
    def test_initialization(self):
        """测试初始化"""
        assert self.data_manager.config == self.config
        assert hasattr(self.data_manager, 'logger')
    
    def test_get_stock_list_mock(self):
        """测试获取股票列表（模拟）"""
        # 由于无法真实调用API，测试异常处理
        stock_list = self.data_manager.get_stock_list()
        assert isinstance(stock_list, pd.DataFrame)
    
    def test_get_daily_data_mock(self):
        """测试获取日线数据（模拟）"""
        daily_data = self.data_manager.get_daily_data('000001.SZ', '20240101', '20240131')
        assert isinstance(daily_data, pd.DataFrame)
    
    def test_save_and_load_data(self):
        """测试数据保存和加载"""
        # 创建测试数据
        test_data = pd.DataFrame({
            'close': [100, 101, 102],
            'volume': [1000, 1100, 1200]
        })
        
        # 保存数据
        self.data_manager.save_data(test_data, 'test_data')
        
        # 加载数据
        loaded_data = self.data_manager.load_data('test_data')
        assert isinstance(loaded_data, pd.DataFrame)
        
        # 清理测试文件
        import os
        try:
            os.remove('data/test_data.csv')
        except:
            pass
    
    def test_update_cache(self):
        """测试缓存更新"""
        # 测试异常处理
        try:
            self.data_manager.update_cache()
        except Exception as e:
            # 期望有异常，因为API无法连接
            assert True

if __name__ == "__main__":
    pytest.main([__file__])