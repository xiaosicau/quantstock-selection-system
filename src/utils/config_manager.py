"""
配置管理模块

提供统一的配置文件管理和访问功能
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = 'config/config.yaml'):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = Path(config_file)
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"配置文件加载成功: {self.config_file}")
            else:
                logger.warning(f"配置文件不存在: {self.config_file}")
                self.config = self._get_default_config()
        except Exception as e:
            logger.error(f"配置文件加载失败: {e}")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'data_sources': {
                'tushare': {
                    'enabled': True,
                    'token': os.getenv('TUSHARE_TOKEN', ''),
                    'timeout': 30
                },
                'akshare': {
                    'enabled': True,
                    'timeout': 60
                }
            },
            'backtest': {
                'initial_capital': 1000000,
                'commission_rate': 0.0003,
                'slippage_rate': 0.0001,
                'risk_control': {
                    'max_position_size': 0.1,
                    'stop_loss': 0.08,
                    'take_profit': 0.15
                }
            },
            'factors': {
                'value': {'enabled': True, 'weight': 0.25},
                'momentum': {'enabled': True, 'weight': 0.2},
                'quality': {'enabled': True, 'weight': 0.2},
                'size': {'enabled': True, 'weight': 0.15},
                'volatility': {'enabled': True, 'weight': 0.2}
            },
            'performance': {
                'cache': {'enabled': True, 'ttl': 3600},
                'parallel': {'enabled': True, 'max_workers': 4}
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/quantstock.log',
                'max_size': '10MB',
                'backup_count': 5
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点分路径（如 'data_sources.tushare.token'）
            default: 默认值
        
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self):
        """保存配置到文件"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"配置文件保存成功: {self.config_file}")
        except Exception as e:
            logger.error(f"配置文件保存失败: {e}")
    
    def get_data_sources(self) -> Dict[str, Any]:
        """获取数据源配置"""
        return self.get('data_sources', {})
    
    def get_backtest_config(self) -> Dict[str, Any]:
        """获取回测配置"""
        return self.get('backtest', {})
    
    def get_factor_config(self) -> Dict[str, Any]:
        """获取因子配置"""
        return self.get('factors', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self.get('logging', {})
    
    def validate_config(self) -> bool:
        """验证配置有效性"""
        required_keys = [
            'data_sources.tushare.token',
            'backtest.initial_capital',
            'logging.level'
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                logger.warning(f"配置缺失: {key}")
                return False
        
        return True
    
    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any):
        """支持字典式设置"""
        self.set(key, value)

if __name__ == "__main__":
    # 测试配置管理器
    config = ConfigManager()
    
    print("Tushare Token:", config.get('data_sources.tushare.token'))
    print("初始资金:", config.get('backtest.initial_capital'))
    print("日志级别:", config.get('logging.level'))
    
    # 设置新值
    config.set('test.key', 'test_value')
    print("测试值:", config.get('test.key'))