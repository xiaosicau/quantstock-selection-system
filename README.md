# 量化股票选股系统 (QuantStock Selection System)

基于多因子模型的量化股票选股系统，集成多数据源、实时行情、智能因子分析与风险监控的完整量化交易平台。

## 🌟 核心特性

### 📊 多因子模型
- **价值因子**: PE、PB、PS、PCF、股息率等
- **成长因子**: 营收增长率、净利润增长率、ROE增长率等
- **质量因子**: ROE、ROA、毛利率、净利率等
- **技术因子**: 动量、RSI、MACD、布林带等
- **情绪因子**: 分析师推荐、资金流向等

### 🔄 多数据源集成
- **Wind金融终端**: 专业金融数据
- **Tushare**: 国内股票数据
- **Yahoo Finance**: 国际股票数据
- **实时行情**: 支持A股、港股、美股
- **财务数据**: 三大财务报表数据

### 🤖 智能分析
- **因子有效性检验**: IC分析、分组测试、回归分析
- **机器学习模型**: 支持XGBoost、LightGBM、神经网络
- **策略回测**: 完整的历史回测框架
- **风险监控**: 实时风险指标计算

### 🎨 用户界面
- **Web界面**: 基于Streamlit的现代化界面
- **实时图表**: 交互式K线图、因子图表
- **策略配置**: 可视化策略参数配置
- **结果展示**: 回测结果、持仓分析、绩效报告

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 推荐: Anaconda/Miniconda

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/xiaosicau/quantstock-selection-system.git
cd quantstock-selection-system
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置数据接口**
```bash
# 编辑配置文件
cp config/config.example.py config/config.py
# 在config.py中填入您的API密钥
```

4. **启动应用**
```bash
# 启动Web界面
streamlit run frontend/app.py

# 或运行演示程序
python comprehensive_demo.py
```

## 📁 项目结构

```
quantstock-selection-system/
├── src/                    # 核心源码
│   ├── api/               # API接口
│   ├── backtest/          # 回测引擎
│   ├── data/              # 数据处理
│   ├── factors/           # 因子计算
│   ├── models/            # 机器学习模型
│   ├── risk/              # 风险监控
│   └── selection/         # 选股逻辑
├── frontend/              # Web界面
├── config/                # 配置文件
├── docs/                  # 文档资料
├── tests/                 # 测试用例
├── data/                  # 数据目录
└── installer/             # 安装程序
```

## 📊 功能演示

### 1. 因子分析
```python
from src.factors.factor_processor import FactorProcessor

# 创建因子处理器
processor = FactorProcessor()

# 计算所有因子
factors = processor.calculate_all_factors(stocks, start_date, end_date)

# 因子有效性分析
analysis = processor.analyze_factor_effectiveness(factors, returns)
```

### 2. 策略回测
```python
from src.backtest.engine import BacktestEngine

# 创建回测引擎
engine = BacktestEngine()

# 配置策略参数
config = {
    'start_date': '2020-01-01',
    'end_date': '2023-12-31',
    'initial_capital': 1000000,
    'factor_weights': {'pe': -0.5, 'roe': 0.8}
}

# 运行回测
results = engine.run_backtest(strategy, config)
```

### 3. 实时选股
```python
from src.selection.stock_screener import StockScreener

# 创建选股器
screener = StockScreener()

# 设置筛选条件
criteria = {
    'pe_max': 20,
    'roe_min': 0.15,
    'market_cap_min': 100e8
}

# 获取推荐股票
recommendations = screener.screen_stocks(criteria)
```

## 🎯 使用场景

### 📈 个人投资者
- 基于科学方法的选股决策
- 风险控制与仓位管理
- 历史回测验证策略

### 🏢 机构投资者
- 多因子量化策略研究
- 组合优化与风险管理
- 绩效归因分析

### 🎓 教育研究
- 量化投资教学案例
- 金融工程研究工具
- 因子模型实证研究

## 📊 性能指标

- **数据覆盖**: A股全市场股票
- **历史数据**: 10+年完整历史
- **因子数量**: 100+有效因子
- **回测速度**: 1000只股票3年数据<30秒
- **实时更新**: 分钟级数据更新

## 🔧 技术栈

- **后端**: Python 3.8+, Pandas, NumPy, SciPy
- **机器学习**: scikit-learn, XGBoost, LightGBM
- **数据接口**: Wind, Tushare, Yahoo Finance
- **Web框架**: Streamlit, FastAPI
- **数据库**: SQLite, MySQL, MongoDB
- **可视化**: Plotly, Matplotlib, ECharts

## 🤝 贡献指南

我们欢迎社区贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/xiaosicau/quantstock-selection-system/issues)
- **邮箱**: your-email@example.com

## 🙏 致谢

- Wind金融终端提供数据支持
- Tushare社区提供开源数据接口
- Streamlit团队提供优秀的Web框架

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！