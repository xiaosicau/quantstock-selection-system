# 量化股票选股系统使用指南

## 快速开始

### 1. 运行演示程序

```bash
# 运行简单演示
python simple_demo.py

# 运行完整演示
python comprehensive_demo.py
```

### 2. 启动Web界面

```bash
# 启动Streamlit应用
streamlit run frontend/app.py

# 指定端口启动
streamlit run frontend/app.py --server.port 8502
```

### 3. 访问应用

打开浏览器访问：`http://localhost:8501`

## 功能详解

### 📈 实时行情
- **市场概览**: 上证指数、深证成指、创业板指实时数据
- **热门股票**: 当日涨幅榜、跌幅榜、成交量排行
- **技术指标**: MA、MACD、RSI、KDJ等技术指标展示

### 🔄 策略回测
- **策略选择**: 支持多种经典策略
- **参数优化**: 可视化参数调优界面
- **绩效分析**: 夏普比率、最大回撤、胜率等指标

### 📊 因子分析
- **因子库**: 价值、动量、质量、规模、波动率因子
- **因子检验**: IC分析、因子收益率、衰减分析
- **因子组合**: 多因子权重优化

### 🎯 选股结果
- **智能选股**: 基于多因子模型的股票筛选
- **实时更新**: 每日自动更新选股结果
- **导出功能**: 支持CSV、Excel格式导出

### ⚠️ 风险监控
- **实时预警**: 仓位、波动率、流动性监控
- **压力测试**: 多种市场情景下的风险评估
- **风险报告**: 定期生成风险分析报告

## 命令行使用

### 数据管理

```bash
# 更新股票列表
python -c "from src.data.data_manager import DataManager; DataManager().update_cache()"

# 获取单只股票数据
python -c "from src.data.data_manager import DataManager; print(DataManager().get_daily_data('000001.SZ', '20240101', '20240131'))"
```

### 策略回测

```bash
# 运行回测
python -c "
from src.backtest.backtest_engine import BacktestEngine, SimpleMovingAverageStrategy
import pandas as pd

# 创建测试数据
data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})

# 运行回测
engine = BacktestEngine({'initial_capital': 100000})
engine.set_data(data)
engine.set_strategy(SimpleMovingAverageStrategy())
results = engine.run_backtest()
print(results)
"
```

### 因子计算

```bash
# 计算因子
python -c "
from src.factor.factor_engine import FactorEngine, ValueFactor
import pandas as pd

# 创建测试数据
data = pd.DataFrame({'pe_ratio': [10, 15, 20], 'roe': [0.1, 0.15, 0.2]})

# 计算因子
engine = FactorEngine()
engine.register_factor(ValueFactor())
factors = engine.calculate_all_factors(data)
print(factors)
"
```

## 配置文件详解

### 数据源配置

```yaml
data_sources:
  tushare:
    enabled: true
    token: "your_token"
    timeout: 30
  
  akshare:
    enabled: true
    timeout: 60
```

### 回测参数

```yaml
backtest:
  initial_capital: 1000000
  commission_rate: 0.0003
  slippage_rate: 0.0001
  
  risk_control:
    max_position_size: 0.1
    stop_loss: 0.08
    take_profit: 0.15
```

### 因子权重

```yaml
factors:
  value:
    enabled: true
    weight: 0.25
  
  momentum:
    enabled: true
    weight: 0.2
  
  quality:
    enabled: true
    weight: 0.2
```

## 使用场景示例

### 场景1：日常选股

```python
from src.data.data_manager import DataManager
from src.factor.factor_engine import FactorEngine
from src.factor.factor_calculator import FactorCalculator

# 1. 获取数据
data_manager = DataManager()
stock_list = data_manager.get_stock_list()

# 2. 计算因子
factor_engine = FactorEngine()
factors = factor_engine.calculate_all_factors(stock_list)

# 3. 选股
selected = factors.nlargest(10, '综合得分')
print("今日推荐股票:", selected[['代码', '名称']])
```

### 场景2：策略回测

```python
from src.backtest.backtest_engine import BacktestEngine, SimpleMovingAverageStrategy

# 1. 创建回测引擎
engine = BacktestEngine({
    'initial_capital': 1000000,
    'commission_rate': 0.001
})

# 2. 设置数据和策略
engine.set_data(historical_data)
engine.set_strategy(SimpleMovingAverageStrategy())

# 3. 运行回测
results = engine.run_backtest()
print("回测结果:", results)
```

### 场景3：风险监控

```python
from src.risk.risk_manager import RiskManager

# 1. 创建风险监控器
risk_manager = RiskManager()

# 2. 检查风险
portfolio_risk = risk_manager.calculate_portfolio_risk(positions)
print("组合风险:", portfolio_risk)

# 3. 生成预警
if portfolio_risk['var'] > threshold:
    risk_manager.send_alert("风险超限")
```

## 高级功能

### 自定义因子

```python
from src.factor.factor_engine import Factor

class MyCustomFactor(Factor):
    def calculate(self, data):
        # 自定义因子计算逻辑
        return data['close'] / data['volume']
    
    def get_name(self):
        return "my_custom_factor"

# 注册并使用
engine = FactorEngine()
engine.register_factor(MyCustomFactor())
```

### 批量处理

```bash
# 批量更新数据
python scripts/update_data.py --batch-size 100

# 批量回测
python scripts/batch_backtest.py --strategies sma,rsi,macd
```

### 定时任务

```bash
# 使用cron（Linux/macOS）
# 每日9:30更新数据
30 9 * * 1-5 /usr/bin/python /path/to/quantstock/scripts/update_daily.py

# 使用Windows任务计划程序
# 创建每日运行的任务
```

## 性能优化

### 1. 数据缓存

```python
# 启用缓存
from src.utils.cache_manager import CacheManager
cache = CacheManager(ttl=3600)  # 1小时缓存
```

### 2. 并行处理

```python
# 并行计算因子
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(calculate_factor, stock_list)
```

### 3. 内存优化

```python
# 分块处理大数据
chunk_size = 1000
for chunk in pd.read_csv('large_data.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

## 故障排除

### 常见问题

#### 1. 数据获取失败
- **检查网络连接**
- **验证API密钥**
- **查看API限制**

#### 2. 内存不足
- **减少处理股票数量**
- **增加虚拟内存**
- **使用64位Python**

#### 3. 回测结果异常
- **检查数据质量**
- **验证策略逻辑**
- **调整参数设置**

### 调试技巧

```python
# 启用调试模式
import logging
logging.basicConfig(level=logging.DEBUG)

# 检查数据
print(data.head())
print(data.info())

# 验证计算
assert not data.isnull().any().any()
```

## 最佳实践

### 1. 数据管理
- 定期备份重要数据
- 使用版本控制
- 建立数据验证流程

### 2. 策略开发
- 从简单策略开始
- 逐步增加复杂度
- 充分回测验证

### 3. 风险控制
- 设置止损止盈
- 分散投资
- 定期风险评估

## 更新和维护

### 系统更新
```bash
# 更新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 运行测试
python run_tests.py
```

### 数据维护
```bash
# 清理旧数据
python scripts/cleanup_data.py --days 30

# 验证数据完整性
python scripts/validate_data.py
```