"""
测试模块 - 量化股票选股系统测试套件

包含以下测试：
1. 单元测试 - 测试各个模块的功能
2. 集成测试 - 测试模块间的集成
3. 性能测试 - 测试系统性能
4. 回归测试 - 测试系统稳定性
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 测试配置
TEST_CONFIG = {
    'database': 'sqlite:///:memory:',
    'debug': True,
    'testing': True
}

def pytest_configure():
    """pytest配置"""
    pass