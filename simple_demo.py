#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化股票选股系统 - 简单演示程序

这是一个简化版的演示程序，展示系统的核心功能：
1. 数据获取演示
2. 因子计算演示
3. 选股逻辑演示
4. 结果展示

运行前请确保已安装：
pip install akshare pandas numpy
"""

import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SimpleQuantStockDemo:
    """简单量化选股演示类"""
    
    def __init__(self):
        print("🚀 初始化量化选股系统演示...")
        
    def get_stock_list(self):
        """获取股票列表"""
        print("📊 获取A股股票列表...")
        try:
            # 使用akshare获取股票列表
            stock_list = ak.stock_zh_a_spot()
            stock_list = stock_list[['代码', '名称', '最新价', '涨跌幅', '成交量']]
            stock_list = stock_list.dropna()
            
            # 筛选出主板股票（简化演示）
            stock_list = stock_list[stock_list['代码'].str.len() == 6]
            
            print(f"✅ 获取到 {len(stock_list)} 只股票")
            return stock_list.head(50)  # 演示用前50只
        except Exception as e:
            print(f"❌ 获取股票列表失败: {e}")
            # 返回模拟数据
            return self._get_mock_stock_list()
    
    def _get_mock_stock_list(self):
        """获取模拟股票列表"""
        mock_data = [
            {'代码': '000001', '名称': '平安银行', '最新价': 15.68, '涨跌幅': 2.1, '成交量': 120000000},
            {'代码': '000002', '名称': '万科A', '最新价': 25.32, '涨跌幅': 1.8, '成交量': 89000000},
            {'代码': '600519', '名称': '贵州茅台', '最新价': 1680.00, '涨跌幅': 0.5, '成交量': 1200000},
            {'代码': '601318', '名称': '中国平安', '最新价': 45.67, '涨跌幅': 1.2, '成交量': 210000000},
            {'代码': '000858', '名称': '五粮液', '最新价': 178.45, '涨跌幅': 3.2, '成交量': 56000000}
        ]
        return pd.DataFrame(mock_data)
    
    def calculate_factors(self, stock_data):
        """计算简单因子"""
        print("🔢 计算选股因子...")
        
        # 添加因子列
        stock_data['价值因子'] = 1 / (stock_data['最新价'] / 10)  # 简单的价格因子
        stock_data['动量因子'] = stock_data['涨跌幅']  # 当日涨幅作为动量
        stock_data['流动性因子'] = stock_data['成交量'] / 1000000  # 成交量因子
        
        # 标准化因子
        for factor in ['价值因子', '动量因子', '流动性因子']:
            stock_data[f'{factor}_标准化'] = (stock_data[factor] - stock_data[factor].mean()) / stock_data[factor].std()
        
        # 计算综合得分
        stock_data['综合得分'] = (
            stock_data['价值因子_标准化'] * 0.4 +
            stock_data['动量因子_标准化'] * 0.3 +
            stock_data['流动性因子_标准化'] * 0.3
        )
        
        return stock_data
    
    def select_stocks(self, stock_data, top_n=5):
        """选股"""
        print("🎯 开始选股...")
        
        # 按综合得分排序
        selected = stock_data.nlargest(top_n, '综合得分')
        
        print(f"✅ 选出 {len(selected)} 只股票")
        return selected
    
    def display_results(self, selected_stocks):
        """展示选股结果"""
        print("\n🎉 选股结果:")
        print("=" * 50)
        
        # 格式化输出
        for idx, row in selected_stocks.iterrows():
            print(f"📈 {row['名称']} ({row['代码']})")
            print(f"   最新价: ¥{row['最新价']:.2f}")
            print(f"   涨跌幅: {row['涨跌幅']:+.1f}%")
            print(f"   综合得分: {row['综合得分']:.3f}")
            print(f"   价值因子: {row['价值因子_标准化']:.3f}")
            print(f"   动量因子: {row['动量因子_标准化']:.3f}")
            print("-" * 30)
    
    def run_demo(self):
        """运行完整演示"""
        print("🚀 开始量化选股演示...")
        print("=" * 60)
        
        # 1. 获取股票列表
        stock_list = self.get_stock_list()
        
        # 2. 计算因子
        stock_data = self.calculate_factors(stock_list)
        
        # 3. 选股
        selected_stocks = self.select_stocks(stock_data, top_n=5)
        
        # 4. 展示结果
        self.display_results(selected_stocks)
        
        # 5. 保存结果
        selected_stocks.to_csv('selected_stocks_demo.csv', index=False, encoding='utf-8-sig')
        print(f"\n📁 结果已保存到: selected_stocks_demo.csv")
        
        return selected_stocks

def main():
    """主函数"""
    print("🎯 量化股票选股系统 - 简单演示")
    print("=" * 60)
    print("这是一个简化版的演示程序，展示核心功能")
    print("\n功能包括:")
    print("1. 获取股票列表")
    print("2. 计算选股因子")
    print("3. 执行选股策略")
    print("4. 展示选股结果")
    print("=" * 60)
    
    # 创建演示实例
    demo = SimpleQuantStockDemo()
    
    try:
        # 运行演示
        results = demo.run_demo()
        
        print("\n✅ 演示完成！")
        print("\n下一步:")
        print("1. 运行完整系统: python comprehensive_demo.py")
        print("2. 启动Web界面: streamlit run frontend/app.py")
        print("3. 查看项目文档: README.md")
        
        return results
        
    except Exception as e:
        print(f"❌ 演示运行失败: {e}")
        print("请检查网络连接或依赖安装")
        return None

if __name__ == "__main__":
    results = main()