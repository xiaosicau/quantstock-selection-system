#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化股票选股系统 - Streamlit Web界面

基于Streamlit的现代化Web界面，提供：
- 实时行情展示
- 策略回测可视化
- 因子分析图表
- 选股结果展示
- 风险监控面板
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))

# 页面配置
st.set_page_config(
    page_title="量化股票选股系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .warning-message {
        color: #ffc107;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主函数"""
    
    # 标题
    st.markdown('<h1 class="main-header">📊 量化股票选股系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    st.sidebar.title("🎯 导航菜单")
    
    menu_items = [
        "📈 实时行情",
        "🔄 策略回测", 
        "📊 因子分析",
        "🎯 选股结果",
        "⚠️ 风险监控",
        "📋 系统配置"
    ]
    
    selected_page = st.sidebar.selectbox("选择功能", menu_items)
    
    # 页面内容
    if "📈 实时行情" in selected_page:
        show_realtime_market()
    elif "🔄 策略回测" in selected_page:
        show_backtest()
    elif "📊 因子分析" in selected_page:
        show_factor_analysis()
    elif "🎯 选股结果" in selected_page:
        show_stock_selection()
    elif "⚠️ 风险监控" in selected_page:
        show_risk_monitor()
    elif "📋 系统配置" in selected_page:
        show_system_config()

def show_realtime_market():
    """实时行情页面"""
    st.header("📈 实时行情监控")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("上证指数", "3,247.56", "+1.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("深证成指", "12,456.78", "+0.8%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("创业板指", "2,789.12", "+2.1%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 模拟数据
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    prices = 3000 + np.cumsum(np.random.randn(len(dates)) * 10)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name='上证指数'))
    fig.update_layout(
        title="上证指数走势图",
        xaxis_title="日期",
        yaxis_title="点位",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 热门股票
    st.subheader("🔥 热门股票")
    
    # 模拟热门股票数据
    hot_stocks = pd.DataFrame({
        '股票代码': ['000001.SZ', '000002.SZ', '000858.SZ', '600519.SH', '601318.SH'],
        '股票名称': ['平安银行', '万科A', '五粮液', '贵州茅台', '中国平安'],
        '最新价': [15.68, 25.32, 178.45, 1680.00, 45.67],
        '涨跌幅': ['+2.1%', '+1.8%', '+3.2%', '+0.5%', '+1.2%'],
        '成交量': ['1.2亿', '8900万', '5600万', '120万', '2.1亿']
    })
    
    st.dataframe(hot_stocks, use_container_width=True)

def show_backtest():
    """策略回测页面"""
    st.header("🔄 策略回测")
    
    # 策略选择
    col1, col2 = st.columns(2)
    
    with col1:
        strategy = st.selectbox(
            "选择策略",
            ["简单移动平均", "RSI策略", "MACD策略", "多因子策略"]
        )
    
    with col2:
        benchmark = st.selectbox(
            "基准指数",
            ["上证指数", "沪深300", "中证500", "创业板指"]
        )
    
    # 参数设置
    st.subheader("⚙️ 策略参数")
    
    if strategy == "简单移动平均":
        short_window = st.slider("短期窗口", 5, 50, 20)
        long_window = st.slider("长期窗口", 20, 200, 50)
    elif strategy == "RSI策略":
        rsi_period = st.slider("RSI周期", 5, 30, 14)
        oversold = st.slider("超卖阈值", 10, 40, 30)
        overbought = st.slider("超买阈值", 60, 90, 70)
    
    # 回测按钮
    if st.button("🚀 开始回测", type="primary"):
        with st.spinner("正在执行回测..."):
            # 模拟回测结果
            results = run_mock_backtest(strategy)
            
            # 显示结果
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("总收益率", f"{results['total_return']:.2%}")
            with col2:
                st.metric("年化收益率", f"{results['annual_return']:.2%}")
            with col3:
                st.metric("最大回撤", f"{results['max_drawdown']:.2%}")
            with col4:
                st.metric("夏普比率", f"{results['sharpe_ratio']:.2f}")
            
            # 收益曲线
            fig = px.line(
                x=results['dates'], 
                y=results['portfolio_values'],
                title="策略收益曲线"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_factor_analysis():
    """因子分析页面"""
    st.header("📊 因子分析")
    
    # 因子选择
    factors = st.multiselect(
        "选择分析因子",
        ["价值因子", "动量因子", "质量因子", "规模因子", "波动率因子"],
        default=["价值因子", "动量因子"]
    )
    
    # 因子表现
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 因子收益率")
        
        # 模拟因子收益数据
        factor_returns = pd.DataFrame({
            '价值因子': [0.02, 0.015, 0.025, 0.018, 0.022],
            '动量因子': [0.018, 0.025, 0.015, 0.028, 0.02],
            '质量因子': [0.015, 0.012, 0.018, 0.016, 0.019]
        }, index=['2024-01', '2024-02', '2024-03', '2024-04', '2024-05'])
        
        fig = px.bar(factor_returns, barmode='group')
        fig.update_layout(
            title="因子月度收益率",
            xaxis_title="月份",
            yaxis_title="收益率"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 因子相关性")
        
        # 模拟相关性矩阵
        corr_data = np.random.randn(100, len(factors))
        corr_df = pd.DataFrame(
            corr_data,
            columns=factors
        ).corr()
        
        fig = px.imshow(corr_df, text_auto=True)
        fig.update_layout(title="因子相关性矩阵")
        st.plotly_chart(fig, use_container_width=True)
    
    # IC分析
    st.subheader("📈 IC分析")
    
    ic_data = pd.DataFrame({
        '因子': factors,
        'IC均值': [0.05, 0.04, 0.03, 0.045, 0.035][:len(factors)],
        'IC标准差': [0.02, 0.025, 0.018, 0.022, 0.02][:len(factors)],
        'IR比率': [2.5, 1.6, 1.67, 2.05, 1.75][:len(factors)]
    })
    
    st.dataframe(ic_data, use_container_width=True)

def show_stock_selection():
    """选股结果页面"""
    st.header("🎯 今日选股结果")
    
    # 选股策略
    strategy = st.selectbox(
        "选股策略",
        ["价值选股", "成长选股", "动量选股", "多因子选股", "风险调整后选股"]
    )
    
    # 选股条件
    col1, col2 = st.columns(2)
    
    with col1:
        market_cap_min = st.number_input("最小市值(亿)", 0, 10000, 50)
        pe_max = st.number_input("最大PE", 0.0, 100.0, 30.0)
    
    with col2:
        pb_max = st.number_input("最大PB", 0.0, 20.0, 3.0)
        roe_min = st.number_input("最小ROE(%)", 0.0, 50.0, 10.0)
    
    # 执行选股
    if st.button("🔍 开始选股"):
        # 模拟选股结果
        selected_stocks = get_mock_selected_stocks(strategy)
        
        st.success(f"✅ 选出 {len(selected_stocks)} 只股票")
        
        # 显示选股结果
        st.dataframe(selected_stocks, use_container_width=True)
        
        # 导出按钮
        if st.button("📥 导出结果"):
            st.download_button(
                label="下载CSV",
                data=selected_stocks.to_csv(index=False),
                file_name=f"selected_stocks_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def show_risk_monitor():
    """风险监控页面"""
    st.header("⚠️ 风险监控")
    
    # 风险指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("VaR(95%)", "-2.3%", "-0.1%")
    with col2:
        st.metric("最大回撤", "-8.5%", "+1.2%")
    with col3:
        st.metric("夏普比率", "1.45", "+0.05")
    with col4:
        st.metric("贝塔系数", "0.95", "-0.02")
    
    # 风险预警
    st.subheader("🚨 风险预警")
    
    alerts = [
        {"时间": "2024-01-15 10:30", "类型": "仓位预警", "描述": "单只股票仓位超过10%", "等级": "⚠️"},
        {"时间": "2024-01-15 09:45", "类型": "波动率预警", "描述": "市场波动率超过阈值", "等级": "⚠️"},
        {"时间": "2024-01-14 15:00", "类型": "流动性预警", "描述": "部分股票流动性不足", "等级": "ℹ️"}
    ]
    
    st.dataframe(pd.DataFrame(alerts), use_container_width=True)
    
    # 压力测试
    st.subheader("💪 压力测试")
    
    stress_scenarios = ["市场下跌10%", "市场下跌20%", "市场下跌30%"]
    stress_results = ["-8.5%", "-15.2%", "-22.8%"]
    
    fig = px.bar(
        x=stress_scenarios,
        y=[float(r.strip('%')) for r in stress_results],
        labels={"x": "压力情景", "y": "预期损失(%)"},
        title="压力测试结果"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_system_config():
    """系统配置页面"""
    st.header("📋 系统配置")
    
    # API配置
    st.subheader("🔑 API配置")
    
    tushare_token = st.text_input("Tushare Token", type="password")
    akshare_config = st.checkbox("启用AkShare")
    
    if st.button("保存配置"):
        st.success("✅ 配置已保存")
    
    # 数据源配置
    st.subheader("📊 数据源")
    
    data_sources = {
        "Tushare": {"状态": "✅ 正常", "延迟": "1分钟"},
        "AkShare": {"状态": "✅ 正常", "延迟": "5分钟"},
        "Wind": {"状态": "❌ 未配置", "延迟": "实时"}
    }
    
    st.json(data_sources)
    
    # 日志查看
    st.subheader("📝 系统日志")
    
    log_level = st.selectbox("日志级别", ["DEBUG", "INFO", "WARNING", "ERROR"])
    
    if st.button("查看日志"):
        # 模拟日志
        logs = [
            "2024-01-15 10:30:15 [INFO] 数据更新完成",
            "2024-01-15 10:29:45 [INFO] 策略回测完成",
            "2024-01-15 10:29:30 [INFO] 因子计算完成",
            "2024-01-15 10:29:15 [INFO] 数据获取完成"
        ]
        
        for log in logs:
            st.text(log)

def run_mock_backtest(strategy: str) -> Dict:
    """模拟回测结果"""
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    portfolio_values = [1000000]
    
    for i in range(1, len(dates)):
        returns = np.random.randn() * 0.02 + 0.0005  # 模拟日收益
        portfolio_values.append(portfolio_values[-1] * (1 + returns))
    
    total_return = (portfolio_values[-1] - portfolio_values[0]) / portfolio_values[0]
    annual_return = total_return / (len(dates) / 252)
    max_drawdown = np.min(portfolio_values) / np.max(portfolio_values) - 1
    sharpe_ratio = np.mean(np.diff(portfolio_values)) / np.std(np.diff(portfolio_values)) * np.sqrt(252)
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'dates': dates,
        'portfolio_values': portfolio_values
    }

def get_mock_selected_stocks(strategy: str) -> pd.DataFrame:
    """模拟选股结果"""
    stocks = [
        {'股票代码': '000001.SZ', '股票名称': '平安银行', '最新价': 15.68, '市值': 3041, 'PE': 8.5, 'PB': 0.8, 'ROE': 12.5},
        {'股票代码': '000002.SZ', '股票名称': '万科A', '最新价': 25.32, '市值': 2856, 'PE': 9.2, 'PB': 0.9, 'ROE': 10.8},
        {'股票代码': '000858.SZ', '股票名称': '五粮液', '最新价': 178.45, '市值': 6924, 'PE': 25.8, 'PB': 5.2, 'ROE': 22.1},
        {'股票代码': '600519.SH', '股票名称': '贵州茅台', '最新价': 1680.00, '市值': 21096, 'PE': 28.5, 'PB': 8.9, 'ROE': 31.2},
        {'股票代码': '601318.SH', '股票名称': '中国平安', '最新价': 45.67, '市值': 8345, 'PE': 8.8, 'PB': 0.9, 'ROE': 10.2}
    ]
    
    return pd.DataFrame(stocks)

if __name__ == "__main__":
    main()