# 量化选股系统快速开始指南

## 概述
量化选股系统是一个基于多因子模型的智能股票选股工具，提供Web界面、API接口和桌面应用三种使用方式。

## 系统要求

### 硬件要求
- **内存**: 4GB RAM 或更高
- **存储**: 2GB 可用空间
- **网络**: 稳定的互联网连接

### 软件要求
- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10/11, macOS 10.13+, Linux Ubuntu 18.04+

## 安装方法

### 方法1：直接运行（推荐开发者）

1. **克隆项目**
   ```bash
   git clone https://github.com/xiaosicau/quantstock-selection-system.git
   cd quantstock-selection-system
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置API密钥**（可选）
   ```bash
   # 编辑配置文件
   cp config/config.yaml config/user_config.yaml
   # 在user_config.yaml中添加您的API密钥
   ```

### 方法2：使用安装包（推荐用户）

#### Windows
1. 下载 `QuantStock-1.0.0-Windows-Setup.exe`
2. 双击运行安装程序
3. 按照向导完成安装

#### macOS
1. 下载 `QuantStock-1.0.0-macOS.dmg`
2. 双击打开DMG文件
3. 拖拽应用到Applications文件夹

#### Linux
1. 下载对应的安装包（.deb 或 .tar.gz）
2. 对于.deb包：
   ```bash
   sudo dpkg -i quantstock_1.0.0_amd64.deb
   ```
3. 对于.tar.gz包：
   ```bash
   tar -xzf quantstock-1.0.0-linux-x86_64.tar.gz
   cd quantstock-1.0.0
   sudo ./install.sh
   ```

### 方法3：Docker部署

1. **构建镜像**
   ```bash
   docker build -t quantstock .
   ```

2. **运行容器**
   ```bash
   docker run -p 8501:8501 -p 8000:8000 quantstock
   ```

## 快速使用

### 1. 启动Web界面
```bash
# 在项目根目录
streamlit run frontend/app.py
```
浏览器访问：http://localhost:8501

### 2. 启动API服务
```bash
# 在项目根目录
python src/api/rest_api.py
```
API文档：http://localhost:8000/docs

### 3. 运行示例程序
```bash
# 简单演示
python simple_demo.py

# 完整演示
python comprehensive_demo.py
```

## 基本功能

### 股票筛选
1. **选择市场**: 沪深A股、美股、港股
2. **设置条件**: PE、PB、ROE等财务指标
3. **运行筛选**: 一键获取符合条件的股票
4. **查看结果**: 排序、导出、保存

### 因子分析
1. **选择因子**: 价值、成长、质量、动量因子
2. **权重配置**: 自定义因子权重
3. **评分计算**: 自动生成股票评分
4. **结果可视化**: 图表展示因子表现

### 策略回测
1. **选择策略**: 内置多种经典策略
2. **设置参数**: 回测时间、资金规模
3. **运行回测**: 模拟历史表现
4. **结果分析**: 收益、风险、回撤指标

## 配置文件说明

### 主配置文件 (config/config.yaml)
```yaml
data_sources:
  akshare:
    enabled: true
    base_url: "https://www.akshare.xyz"
  
factors:
  value:
    weight: 0.3
    pe_threshold: 15
  growth:
    weight: 0.3
    revenue_growth: 0.15
  quality:
    weight: 0.2
    roe_threshold: 0.1

backtest:
  start_date: "2020-01-01"
  end_date: "2023-12-31"
  initial_capital: 1000000
  commission: 0.001
```

### 用户配置 (config/user_config.yaml)
创建此文件以覆盖默认配置：
```yaml
data_sources:
  tushare:
    token: "YOUR_TUSHARE_TOKEN"
  wind:
    path: "/path/to/wind/windcode"
```

## 使用示例

### 示例1：基础股票筛选
```python
from src.factor.factor_engine import FactorEngine
from src.data.data_manager import DataManager

# 初始化
data_manager = DataManager()
factor_engine = FactorEngine()

# 获取股票数据
stocks = data_manager.get_stock_list()

# 设置筛选条件
conditions = {
    'pe': {'min': 5, 'max': 20},
    'pb': {'min': 0.5, 'max': 3},
    'roe': {'min': 0.1}
}

# 运行筛选
results = factor_engine.screen_stocks(stocks, conditions)
print(f"筛选结果: {len(results)} 只股票")
```

### 示例2：策略回测
```python
from src.backtest.backtest_engine import BacktestEngine

# 初始化回测引擎
engine = BacktestEngine()

# 设置策略
strategy = {
    'name': '价值策略',
    'factors': ['pe', 'pb', 'roe'],
    'weights': [0.4, 0.3, 0.3]
}

# 运行回测
results = engine.run_backtest(
    strategy=strategy,
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=1000000
)

# 查看结果
print(f"年化收益: {results['annual_return']:.2%}")
print(f"最大回撤: {results['max_drawdown']:.2%}")
```

## 常见问题

### Q1: 安装依赖时出现错误
**问题**: pip install 失败
**解决**: 
```bash
# 更新pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 运行时报错找不到模块
**问题**: ImportError
**解决**:
```bash
# 设置PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 或在代码中添加
import sys
sys.path.append('.')
```

### Q3: 数据获取失败
**问题**: 无法获取股票数据
**解决**:
1. 检查网络连接
2. 确认数据源配置正确
3. 查看错误日志定位问题

### Q4: Web界面无法打开
**问题**: 浏览器无法访问localhost:8501
**解决**:
1. 确认streamlit已安装: `pip install streamlit`
2. 检查端口是否被占用
3. 尝试其他端口: `streamlit run frontend/app.py --server.port 8502`

## 技术支持

### 获取帮助
- **GitHub Issues**: https://github.com/xiaosicau/quantstock-selection-system/issues
- **文档**: https://github.com/xiaosicau/quantstock-selection-system/wiki
- **邮件**: support@quantstock.com

### 报告问题
遇到问题时，请提供：
1. 操作系统版本
2. Python版本
3. 错误信息截图
4. 复现步骤

## 下一步

完成基础使用后，您可以：

1. **深入学习**: 阅读 `INSTALLER_GUIDE.md` 了解高级配置
2. **自定义策略**: 修改因子权重和筛选条件
3. **扩展功能**: 添加新的数据源和因子
4. **性能优化**: 调整回测参数和缓存设置

## 版本更新

关注项目GitHub仓库获取最新版本和更新日志：
https://github.com/xiaosicau/quantstock-selection-system/releases