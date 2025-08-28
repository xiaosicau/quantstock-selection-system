"""
RESTful API接口实现

提供标准的HTTP接口，支持：
- 股票数据查询
- 策略回测
- 因子计算
- 选股结果
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from ..data.data_manager import DataManager
from ..backtest.backtest_engine import BacktestEngine, SimpleMovingAverageStrategy
from ..factor.factor_engine import FactorEngine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class APIResponse:
    """API响应格式"""
    success: bool
    data: Any = None
    message: str = ""
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class RestAPI:
    """RESTful API服务"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.app = Flask(__name__)
        CORS(self.app)
        
        # 初始化组件
        self.data_manager = DataManager(self.config.get('data', {}))
        self.factor_engine = FactorEngine(self.config.get('factor', {}))
        
        # 注册路由
        self._register_routes()
    
    def _register_routes(self):
        """注册API路由"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """健康检查"""
            return jsonify(APIResponse(
                success=True,
                message="服务运行正常"
            ).__dict__)
        
        @self.app.route('/api/stocks', methods=['GET'])
        def get_stocks():
            """获取股票列表"""
            try:
                stocks = self.data_manager.get_stock_list()
                return jsonify(APIResponse(
                    success=True,
                    data=stocks.to_dict('records')
                ).__dict__)
            except Exception as e:
                logger.error(f"获取股票列表失败: {e}")
                return jsonify(APIResponse(
                    success=False,
                    message=str(e)
                ).__dict__), 500
        
        @self.app.route('/api/stocks/<symbol>/data', methods=['GET'])
        def get_stock_data(symbol: str):
            """获取股票历史数据"""
            try:
                start_date = request.args.get('start_date')
                end_date = request.args.get('end_date')
                
                if not start_date:
                    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
                if not end_date:
                    end_date = datetime.now().strftime('%Y%m%d')
                
                data = self.data_manager.get_daily_data(symbol, start_date, end_date)
                
                return jsonify(APIResponse(
                    success=True,
                    data=data.to_dict('records')
                ).__dict__)
                
            except Exception as e:
                logger.error(f"获取股票数据失败: {e}")
                return jsonify(APIResponse(
                    success=False,
                    message=str(e)
                ).__dict__), 500
        
        @self.app.route('/api/factors', methods=['GET'])
        def get_factors():
            """获取因子列表"""
            factors = [
                {'name': 'pe_ratio', 'description': '市盈率'},
                {'name': 'pb_ratio', 'description': '市净率'},
                {'name': 'roe', 'description': '净资产收益率'},
                {'name': 'rsi', 'description': '相对强弱指标'},
                {'name': 'macd', 'description': 'MACD指标'}
            ]
            
            return jsonify(APIResponse(
                success=True,
                data=factors
            ).__dict__)
        
        @self.app.route('/api/factors/calculate', methods=['POST'])
        def calculate_factors():
            """计算因子值"""
            try:
                req_data = request.get_json()
                symbols = req_data.get('symbols', [])
                factors = req_data.get('factors', [])
                
                if not symbols:
                    return jsonify(APIResponse(
                        success=False,
                        message="股票代码不能为空"
                    ).__dict__), 400
                
                # 获取数据
                data = self.data_manager.get_multiple_stocks(symbols)
                
                # 计算因子
                factor_data = self.factor_engine.calculate_factors(data, factors)
                
                return jsonify(APIResponse(
                    success=True,
                    data=factor_data.to_dict('records')
                ).__dict__)
                
            except Exception as e:
                logger.error(f"计算因子失败: {e}")
                return jsonify(APIResponse(
                    success=False,
                    message=str(e)
                ).__dict__), 500
        
        @self.app.route('/api/backtest', methods=['POST'])
        def run_backtest():
            """运行策略回测"""
            try:
                req_data = request.get_json()
                symbols = req_data.get('symbols', [])
                strategy_type = req_data.get('strategy', 'sma')
                parameters = req_data.get('parameters', {})
                
                if not symbols:
                    return jsonify(APIResponse(
                        success=False,
                        message="股票代码不能为空"
                    ).__dict__), 400
                
                # 获取历史数据
                data = self.data_manager.get_multiple_stocks(symbols)
                
                # 创建回测引擎
                engine = BacktestEngine({
                    'initial_capital': parameters.get('initial_capital', 1000000),
                    'commission_rate': parameters.get('commission_rate', 0.001)
                })
                
                # 设置策略
                if strategy_type == 'sma':
                    strategy = SimpleMovingAverageStrategy(**parameters)
                else:
                    return jsonify(APIResponse(
                        success=False,
                        message=f"不支持的策略类型: {strategy_type}"
                    ).__dict__), 400
                
                engine.set_data(data)
                engine.set_strategy(strategy)
                
                # 运行回测
                results = engine.run_backtest()
                
                return jsonify(APIResponse(
                    success=True,
                    data=results
                ).__dict__)
                
            except Exception as e:
                logger.error(f"回测失败: {e}")
                return jsonify(APIResponse(
                    success=False,
                    message=str(e)
                ).__dict__), 500
        
        @self.app.route('/api/stock-screener', methods=['POST'])
        def stock_screener():
            """股票筛选器"""
            try:
                req_data = request.get_json()
                filters = req_data.get('filters', {})
                
                # 获取股票列表
                stocks = self.data_manager.get_stock_list()
                
                # 应用筛选条件
                filtered_stocks = self._apply_filters(stocks, filters)
                
                return jsonify(APIResponse(
                    success=True,
                    data=filtered_stocks.to_dict('records')
                ).__dict__)
                
            except Exception as e:
                logger.error(f"股票筛选失败: {e}")
                return jsonify(APIResponse(
                    success=False,
                    message=str(e)
                ).__dict__), 500
    
    def _apply_filters(self, stocks: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """应用筛选条件"""
        filtered = stocks.copy()
        
        # 市值筛选
        if 'min_market_cap' in filters:
            filtered = filtered[filtered['market_cap'] >= filters['min_market_cap']]
        
        if 'max_market_cap' in filters:
            filtered = filtered[filtered['market_cap'] <= filters['max_market_cap']]
        
        # 市盈率筛选
        if 'min_pe' in filters:
            filtered = filtered[filtered['pe_ratio'] >= filters['min_pe']]
        
        if 'max_pe' in filters:
            filtered = filtered[filtered['pe_ratio'] <= filters['max_pe']]
        
        # 排序
        if 'sort_by' in filters:
            sort_column = filters['sort_by']
            ascending = filters.get('ascending', True)
            filtered = filtered.sort_values(by=sort_column, ascending=ascending)
        
        # 限制数量
        limit = filters.get('limit', 50)
        return filtered.head(limit)
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """启动API服务"""
        logger.info(f"启动REST API服务: http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    api = RestAPI()
    api.run(debug=True)