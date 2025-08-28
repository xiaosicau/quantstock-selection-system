# 量化选股系统安装指南

## 目录
1. [系统架构](#系统架构)
2. [安装准备](#安装准备)
3. [安装方法](#安装方法)
4. [配置说明](#配置说明)
5. [验证安装](#验证安装)
6. [故障排除](#故障排除)
7. [高级配置](#高级配置)

## 系统架构

### 核心组件
```
quantstock-selection-system/
├── src/                    # 核心源码
│   ├── data/              # 数据管理模块
│   ├── factor/            # 因子分析引擎
│   ├── backtest/          # 回测引擎
│   ├── api/               # REST API服务
│   └── utils/             # 工具模块
├── frontend/              # Web界面
├── tests/                 # 测试套件
├── config/                # 配置文件
├── installer/             # 安装程序
└── docs/                  # 文档
```

### 技术栈
- **后端**: Python 3.8+, FastAPI, Pandas, NumPy
- **前端**: Streamlit, Plotly, Bootstrap
- **数据**: AkShare, Yahoo Finance, Tushare Pro
- **部署**: Docker, Docker Compose

## 安装准备

### 系统要求

#### 最低配置
- **CPU**: 2核
- **内存**: 4GB RAM
- **存储**: 2GB可用空间
- **网络**: 稳定互联网连接

#### 推荐配置
- **CPU**: 4核以上
- **内存**: 8GB RAM
- **存储**: 10GB SSD
- **网络**: 高速宽带

### 环境检查

运行环境检查脚本：
```bash
python validate_project.py
```

## 安装方法

### 方法1：源码安装（推荐开发者）

#### 1. 环境准备
```bash
# 更新系统（Linux/macOS）
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
brew update && brew upgrade             # macOS

# 安装Python（如未安装）
# Ubuntu/Debian
sudo apt install python3.8 python3.8-pip

# macOS
brew install python@3.8

# Windows: 从python.org下载安装
```

#### 2. 克隆项目
```bash
git clone https://github.com/xiaosicau/quantstock-selection-system.git
cd quantstock-selection-system
```

#### 3. 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv quantstock-env

# 激活虚拟环境
# Linux/macOS
source quantstock-env/bin/activate

# Windows
quantstock-env\Scripts\activate
```

#### 4. 安装依赖
```bash
# 升级pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 或使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 5. 配置环境变量
```bash
# Linux/macOS
export PYTHONPATH=$PYTHONPATH:$(pwd)
export QUANTSTOCK_CONFIG_PATH=$(pwd)/config

# Windows
set PYTHONPATH=%PYTHONPATH%;%CD%
set QUANTSTOCK_CONFIG_PATH=%CD%\config
```

### 方法2：安装包安装（推荐用户）

#### Windows安装
1. 下载 `QuantStock-1.0.0-Windows-Setup.exe`
2. 以管理员身份运行
3. 选择安装路径（默认：C:\Program Files\QuantStock）
4. 选择数据源（可选配置）
5. 完成安装

#### macOS安装
1. 下载 `QuantStock-1.0.0-macOS.dmg`
2. 双击打开DMG文件
3. 拖拽应用到Applications
4. 首次运行允许权限

#### Linux安装

##### Ubuntu/Debian (.deb)
```bash
sudo dpkg -i quantstock_1.0.0_amd64.deb
sudo apt-get install -f  # 修复依赖
```

##### CentOS/RHEL (.rpm)
```bash
sudo rpm -i quantstock-1.0.0-1.x86_64.rpm
```

##### 通用安装 (.tar.gz)
```bash
tar -xzf quantstock-1.0.0-linux-x86_64.tar.gz
cd quantstock-1.0.0
sudo ./install.sh
```

### 方法3：Docker安装

#### 1. 安装Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# macOS
brew install --cask docker

# Windows
# 下载Docker Desktop for Windows
```

#### 2. 构建镜像
```bash
# 克隆项目
git clone https://github.com/xiaosicau/quantstock-selection-system.git
cd quantstock-selection-system

# 构建镜像
docker build -t quantstock:latest .
```

#### 3. 运行容器
```bash
# 基本运行
docker run -p 8501:8501 -p 8000:8000 quantstock:latest

# 带数据卷
mkdir -p ~/quantstock-data
docker run -p 8501:8501 -p 8000:8000 \
  -v ~/quantstock-data:/app/data \
  -v $(pwd)/config:/app/config \
  quantstock:latest
```

#### 4. Docker Compose
```bash
# 使用docker-compose.yml
docker-compose up -d
```

## 配置说明

### 配置文件结构
```
config/
├── config.yaml          # 主配置文件
├── user_config.yaml     # 用户自定义配置（可选）
├── data_sources.yaml    # 数据源配置
└── factors.yaml         # 因子配置
```

### 主配置示例 (config/config.yaml)
```yaml
# 数据源配置
data_sources:
  akshare:
    enabled: true
    base_url: "https://www.akshare.xyz"
    timeout: 30
  
  tushare:
    enabled: false
    token: "YOUR_TUSHARE_TOKEN"
    timeout: 30
  
  yahoo:
    enabled: true
    base_url: "https://finance.yahoo.com"
    timeout: 30

# 因子配置
factors:
  value:
    weight: 0.3
    pe_threshold: 15
    pb_threshold: 2
    ps_threshold: 3
  
  growth:
    weight: 0.3
    revenue_growth: 0.15
    profit_growth: 0.15
    roe_growth: 0.1
  
  quality:
    weight: 0.2
    roe_threshold: 0.1
    roa_threshold: 0.05
    debt_ratio_max: 0.6
  
  momentum:
    weight: 0.2
    lookback_days: 252
    momentum_threshold: 0.1

# 回测配置
backtest:
  start_date: "2020-01-01"
  end_date: "2023-12-31"
  initial_capital: 1000000
  commission: 0.001
  slippage: 0.0005
  rebalance_frequency: "monthly"
  max_positions: 20

# 风险管理
risk_management:
  max_position_size: 0.1
  max_sector_weight: 0.3
  stop_loss: 0.1
  take_profit: 0.3
  max_drawdown: 0.2

# 日志配置
logging:
  level: "INFO"
  file: "logs/quantstock.log"
  max_size: "10MB"
  backup_count: 5
```

### 用户配置覆盖
创建 `config/user_config.yaml` 覆盖默认配置：
```yaml
# 用户自定义配置
factors:
  value:
    weight: 0.4  # 提高价值因子权重
    pe_threshold: 12  # 更严格的PE筛选

# 添加自定义数据源
data_sources:
  wind:
    enabled: true
    path: "/path/to/wind/windcode"
```

## 验证安装

### 1. 环境验证
```bash
python validate_project.py
```

### 2. 运行测试
```bash
# 运行单元测试
python -m pytest tests/ -v

# 运行演示程序
python simple_demo.py

# 运行完整演示
python comprehensive_demo.py
```

### 3. 启动服务验证
```bash
# 启动Web界面
streamlit run frontend/app.py --server.port 8501

# 启动API服务（新终端）
python src/api/rest_api.py --port 8000
```

### 4. 访问验证
- Web界面: http://localhost:8501
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 故障排除

### 常见问题

#### Python环境问题
```bash
# 检查Python版本
python --version

# 检查pip版本
pip --version

# 检查虚拟环境
which python
```

#### 依赖安装失败
```bash
# 更新pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 单独安装问题包
pip install pandas --upgrade
```

#### 端口冲突
```bash
# 检查端口占用
# Linux/macOS
lsof -i :8501
lsof -i :8000

# Windows
netstat -ano | findstr :8501
netstat -ano | findstr :8000
```

#### 数据获取失败
1. 检查网络连接
2. 验证API密钥配置
3. 查看错误日志: `logs/quantstock.log`
4. 测试数据源连接

#### 权限问题（Linux/macOS）
```bash
# 添加执行权限
chmod +x deploy.py
chmod +x validate_project.py

# 使用sudo运行（谨慎）
sudo python deploy.py
```

### 日志分析

#### 查看日志
```bash
# 实时查看日志
tail -f logs/quantstock.log

# 搜索错误
grep ERROR logs/quantstock.log

# 按日期查看
less logs/quantstock.log
```

#### 调试模式
```bash
# 启用调试日志
export QUANTSTOCK_LOG_LEVEL=DEBUG

# 运行调试模式
python -m pdb simple_demo.py
```

## 高级配置

### 性能优化

#### 1. 缓存配置
```yaml
# config/config.yaml
cache:
  enabled: true
  type: "redis"
  host: "localhost"
  port: 6379
  ttl: 3600
```

#### 2. 并发配置
```yaml
# config/config.yaml
concurrency:
  max_workers: 4
  thread_pool_size: 8
  async_workers: 16
```

#### 3. 数据库配置
```yaml
# config/config.yaml
database:
  type: "sqlite"
  path: "data/quantstock.db"
  
  # 或使用PostgreSQL
  # type: "postgresql"
  # host: "localhost"
  # port: 5432
  # database: "quantstock"
  # username: "user"
  # password: "password"
```

### 安全配置

#### 1. API密钥管理
```bash
# 使用环境变量
export TUSHARE_TOKEN=your_token_here
export WIND_PATH=/path/to/wind

# 或使用配置文件
# config/user_config.yaml
```

#### 2. 访问控制
```yaml
# config/config.yaml
security:
  api_key_required: true
  rate_limit: "100/hour"
  cors_origins: ["http://localhost:3000"]
```

### 监控配置

#### 1. 健康检查
```bash
# 检查服务状态
curl http://localhost:8000/health

# 检查Web界面
curl http://localhost:8501/_stcore/health
```

#### 2. 监控指标
```yaml
# config/config.yaml
monitoring:
  enabled: true
  metrics_endpoint: "/metrics"
  prometheus:
    enabled: true
    port: 9090
```

## 升级指南

### 版本升级
1. 备份配置文件
2. 下载新版本
3. 运行升级脚本
4. 验证升级结果

### 数据迁移
```bash
# 备份数据
cp -r data/ data-backup-$(date +%Y%m%d)

# 升级后恢复数据
cp -r data-backup-20240101/* data/
```

## 技术支持

### 获取帮助
- **文档**: https://github.com/quantstock/quantstock-selection-system/wiki
- **Issues**: https://github.com/quantstock/quantstock-selection-system/issues
- **Discussions**: https://github.com/quantstock/quantstock-selection-system/discussions

### 联系方式
- **邮箱**: support@quantstock.com
- **微信群**: 扫码加入技术支持群
- **QQ群**: 123456789

### 社区资源
- **教程视频**: B站搜索"量化选股系统"
- **技术博客**: https://blog.quantstock.com
- **示例代码**: https://github.com/quantstock/examples