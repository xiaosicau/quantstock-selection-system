"""
数据管理器 - 统一的数据获取和管理接口
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Union
import akshare as ak
import tushare as ts

class DataManager:
    """数据管理器类"""
    
    def __init__(self, config: Dict = None):
        """
        初始化数据管理器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 初始化数据源
        self._init_data_sources()
        
    def _init_data_sources(self):
        """初始化数据源"""
        # Tushare初始化
        ts_token = self.config.get('tushare_token', 'your_token_here')
        ts.set_token(ts_token)
        self.pro = ts.pro_api()
        
        self.logger.info("数据管理器初始化完成")
    
    def get_stock_list(self) -> pd.DataFrame:
        """获取股票列表"""
        try:
            # 使用Tushare获取股票列表
            stock_list = self.pro.stock_basic(
                exchange='',
                list_status='L',
                fields='ts_code,symbol,name,area,industry,list_date'
            )
            return stock_list
        except Exception as e:
            self.logger.error(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def get_daily_data(self, 
                      stock_code: str, 
                      start_date: str, 
                      end_date: str) -> pd.DataFrame:
        """获取日线数据"""
        try:
            # 使用Tushare获取日线数据
            daily_data = self.pro.daily(
                ts_code=stock_code,
                start_date=start_date,
                end_date=end_date
            )
            
            if not daily_data.empty:
                daily_data['trade_date'] = pd.to_datetime(daily_data['trade_date'])
                daily_data = daily_data.sort_values('trade_date')
                daily_data.set_index('trade_date', inplace=True)
                
            return daily_data
        except Exception as e:
            self.logger.error(f"获取{stock_code}日线数据失败: {e}")
            return pd.DataFrame()
    
    def get_fundamental_data(self, 
                           stock_code: str, 
                           date: str) -> pd.DataFrame:
        """获取基本面数据"""
        try:
            # 获取财务指标数据
            financial = self.pro.fina_indicator(
                ts_code=stock_code,
                start_date=date,
                end_date=date
            )
            return financial
        except Exception as e:
            self.logger.error(f"获取{stock_code}基本面数据失败: {e}")
            return pd.DataFrame()
    
    def get_market_data(self, date: str) -> pd.DataFrame:
        """获取市场整体数据"""
        try:
            # 获取市场整体数据
            market_data = self.pro.index_daily(
                ts_code='000001.SH',  # 上证指数
                start_date=date,
                end_date=date
            )
            return market_data
        except Exception as e:
            self.logger.error(f"获取市场整体数据失败: {e}")
            return pd.DataFrame()
    
    def save_data(self, data: pd.DataFrame, filename: str):
        """保存数据到本地"""
        try:
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            file_path = data_dir / f"{filename}.csv"
            data.to_csv(file_path, index=True)
            self.logger.info(f"数据已保存: {file_path}")
        except Exception as e:
            self.logger.error(f"保存数据失败: {e}")
    
    def load_data(self, filename: str) -> pd.DataFrame:
        """从本地加载数据"""
        try:
            file_path = Path("data") / f"{filename}.csv"
            if file_path.exists():
                return pd.read_csv(file_path, index_col=0)
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"加载数据失败: {e}")
            return pd.DataFrame()
    
    def update_cache(self, force_update: bool = False):
        """更新数据缓存"""
        self.logger.info("开始更新数据缓存...")
        
        # 获取股票列表
        stock_list = self.get_stock_list()
        if not stock_list.empty:
            self.save_data(stock_list, "stock_list")
        
        # 获取最近交易数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        # 分批获取数据，避免API限制
        for idx, row in stock_list.head(100).iterrows():  # 限制前100只股票
            stock_code = row['ts_code']
            daily_data = self.get_daily_data(stock_code, start_date, end_date)
            if not daily_data.empty:
                self.save_data(daily_data, f"daily_{stock_code}")
        
        self.logger.info("数据缓存更新完成")