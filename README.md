# 🎯 量化股票选股系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xiaosicau/quantstock-selection-system)](https://github.com/xiaosicau/quantstock-selection-system/stargazers)

基于多因子模型的量化股票选股系统，集成多数据源、实时行情、智能因子分析与风险监控的完整量化交易平台。

## ✨ 核心特性

### 📊 **实时行情监控**
- 上证指数、深证成指、创业板指实时数据
- 热门股票排行（涨幅榜、跌幅榜、成交量榜）
- 技术指标实时计算（MA、MACD、RSI、KDJ）

### 🔄 **策略回测引擎**
- 支持多种经典策略：移动平均、RSI、MACD、布林带
- 可视化参数优化与策略比较
- 详细的绩效分析报告（夏普比率、最大回撤、胜率）

### 🎯 **智能因子分析**
- 内置五大类因子：价值、动量、质量、规模、波动率
- 因子有效性检验（IC分析、衰减分析）
- 多因子权重优化与组合构建

### 📈 **智能选股系统**
- 基于多因子模型的股票筛选
- 实时更新选股结果
- 支持CSV、Excel格式导出

### ⚠️ **风险监控预警**
- 实时仓位监控与风险计算
- 波动率、流动性风险预警
- 压力测试与情景分析

## 🚀 快速开始

### 1. 安装运行

#### 方式一：一键安装脚本（推荐）
```bash
# 克隆项目
git clone https://github.com/xiaosicau/quantstock-selection-system.git
cd quantstock-selection-system

# 运行安装脚本
./scripts/install.sh

# 启动系统
./scripts/start.sh
```

#### 方式二：Docker快速部署
```bash
# 克隆项目
git clone https://github.com/xiaosicau/quantstock-selection-system.git
cd quantstock-selection-system

# 启动Docker服务
./scripts/docker-start.sh
```

#### 方式三：手动安装
```bash
# 克隆项目
git clone https://github.com/xiaosicau/quantstock-selection-system.git
cd quantstock-selection-system

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp config/config.example.yaml config/config.yaml
# 编辑config/config.yaml，设置Tushare Token

# 启动应用
streamlit run frontend/app.py
```

### 2. 访问应用

启动成功后，打开浏览器访问：
- **Web界面**: http://localhost:8501
- **API文档**: http://localhost:5000/docs

### 3. 获取API密钥

1. 访问 [Tushare官网](https://tushare.pro) 注册账号
2. 在个人中心获取API Token
3. 在 `config/config.yaml` 中配置：`tushare.token: "your_token"`

## 📋 系统架构

```
quantstock-selection-system/
├── src/                    # 核心源码
│   ├── data/              # 数据管理模块
│   ├── backtest/          # 回测引擎模块
│   ├── factor/            # 因子分析模块
│   ├── api/               # API接口模块
│   └── utils/             # 工具模块
├── frontend/              # Web前端界面
├── tests/                 # 测试套件
├── config/                # 配置文件
├── scripts/               # 启动脚本
├── docs/                  # 项目文档
└── data/                  # 数据存储
```

## 🎯 功能演示

### 1. 实时行情监控
![实时行情](docs/images/market_overview.png)

### 2. 策略回测分析
![策略回测](docs/images/backtest_results.png)

### 3. 因子权重优化
![因子分析](docs/images/factor_analysis.png)

### 4. 智能选股结果
![选股结果](docs/images/stock_selection.png)

## 🛠️ 开发指南

### 环境要求
- **Python**: 3.8+
- **内存**: 8GB+ (推荐16GB)
- **存储**: 10GB+ 可用空间
- **系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+

### 开发环境搭建
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python run_tests.py

# 代码质量检查
python run_tests.py --lint

# 生成覆盖率报告
python run_tests.py --cov
```

### API使用示例

#### REST API
```python
import requests

# 获取股票列表
response = requests.get('http://localhost:5000/api/stocks')
stocks = response.json()['data']

# 运行策略回测
backtest_data = {
    'symbols': ['000001.SZ', '600000.SH'],
    'strategy': 'sma',
    'parameters': {'short_window': 5, 'long_window': 20}
}
response = requests.post('http://localhost:5000/api/backtest', json=backtest_data)
results = response.json()['data']
```

#### Python SDK
```python
from src.data.data_manager import DataManager
from src.factor.factor_engine import FactorEngine

# 初始化组件
data_manager = DataManager()
factor_engine = FactorEngine()

# 获取股票数据
stocks = data_manager.get_stock_list()
data = data_manager.get_daily_data('000001.SZ', '20240101', '20240131')

# 计算因子
factors = factor_engine.calculate_all_factors(data)
```

## 📊 性能优化

### 1. 数据缓存
```yaml
# config.yaml
performance:
  cache:
    enabled: true
    ttl: 3600
    redis:
      host: localhost
      port: 6379
```

### 2. 并行处理
```yaml
performance:
  parallel:
    enabled: true
    max_workers: 4
```

### 3. 内存优化
- 使用数据分块处理
- 定期清理缓存
- 限制并发股票数量

## 🔧 配置文件

### 数据源配置
```yaml
data_sources:
  tushare:
    enabled: true
    token: "your_tushare_token"
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

## 🐛 常见问题

### Q1: 安装失败怎么办？
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 检查Python版本
python --version  # 需要3.8+
```

### Q2: 数据获取失败？
- 检查网络连接
- 验证Tushare Token是否有效
- 查看API调用限制

### Q3: 内存不足？
- 减少处理股票数量
- 增加虚拟内存
- 使用64位Python

### Q4: Web界面无法访问？
- 检查端口占用：`lsof -i :8501`
- 使用其他端口：`--server.port 8502`
- 检查防火墙设置

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范
- 使用Black格式化代码
- 遵循PEP 8规范
- 添加类型注解
- 编写单元测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Tushare](https://tushare.pro) - 提供高质量金融数据
- [Streamlit](https://streamlit.io) - 快速构建Web应用
- [Pandas](https://pandas.pydata.org) - 数据处理和分析
- [NumPy](https://numpy.org) - 数值计算基础库

## 📞 联系方式

- **项目地址**: [GitHub Repository](https://github.com/xiaosicau/quantstock-selection-system)
- **问题反馈**: [GitHub Issues](https://github.com/xiaosicau/quantstock-selection-system/issues)
- **讨论交流**: [GitHub Discussions](https://github.com/xiaosicau/quantstock-selection-system/discussions)

---

<div align="center">
  <p><strong>⭐ 如果这个项目对你有帮助，请给个Star支持！</strong></p>
</div>