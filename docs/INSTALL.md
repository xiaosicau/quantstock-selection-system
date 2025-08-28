# 量化股票选股系统安装指南

## 系统要求

### 硬件要求
- **内存**: 8GB RAM 或更高（推荐16GB）
- **存储**: 10GB 可用空间
- **CPU**: 4核心或更高（推荐8核心）
- **网络**: 稳定的互联网连接

### 软件要求
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 或更高版本
- **Git**: 最新版本

## 安装步骤

### 1. 获取项目代码

```bash
# 克隆项目
git clone https://github.com/xiaosicau/quantstock-selection-system.git
cd quantstock-selection-system
```

### 2. 创建虚拟环境

#### Windows
```bash
# 使用venv
python -m venv quantstock-env
quantstock-env\Scripts\activate

# 或者使用conda
conda create -n quantstock python=3.9
conda activate quantstock
```

#### macOS/Linux
```bash
# 使用venv
python3 -m venv quantstock-env
source quantstock-env/bin/activate

# 或者使用conda
conda create -n quantstock python=3.9
conda activate quantstock
```

### 3. 安装依赖

```bash
# 安装核心依赖
pip install -r requirements.txt

# 如果需要开发环境
pip install -r requirements-dev.txt
```

### 4. 配置系统

#### 4.1 配置文件
复制配置文件模板：
```bash
cp config/config.example.yaml config/config.yaml
```

#### 4.2 配置API密钥
编辑 `config/config.yaml`：

```yaml
data_sources:
  tushare:
    enabled: true
    token: "your_tushare_token_here"  # 替换为你的Tushare Token
```

#### 4.3 获取Tushare Token
1. 访问 [Tushare官网](https://tushare.pro)
2. 注册账号
3. 在个人中心获取API Token

### 5. 验证安装

#### 5.1 运行简单测试
```bash
python simple_demo.py
```

#### 5.2 运行测试套件
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_data_manager.py
```

#### 5.3 启动Web界面
```bash
streamlit run frontend/app.py
```

## Docker安装（可选）

### 1. 使用Docker Compose

#### 创建docker-compose.yml
```yaml
version: '3.8'
services:
  quantstock:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - PYTHONPATH=/app
```

#### 启动服务
```bash
docker-compose up -d
```

### 2. 手动构建Docker镜像

```bash
# 构建镜像
docker build -t quantstock .

# 运行容器
docker run -p 8501:8501 -v $(pwd)/data:/app/data quantstock
```

## 常见问题解决

### 1. 依赖安装失败

#### 问题：某些包安装失败
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 问题：编译错误
```bash
# Windows用户安装Visual Studio Build Tools
# 或者使用预编译包
pip install --only-binary=all -r requirements.txt
```

### 2. 运行时错误

#### 问题：找不到模块
```bash
# 确保在项目根目录运行
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

#### 问题：数据库连接失败
```bash
# 创建数据目录
mkdir -p data

# 检查数据库配置
python -c "from src.data.data_manager import DataManager; print('OK')"
```

### 3. Web界面无法启动

#### 检查端口占用
```bash
# 检查8501端口
lsof -i :8501

# 使用其他端口
streamlit run frontend/app.py --server.port 8502
```

## 性能优化建议

### 1. 数据缓存
```yaml
# 在config.yaml中启用缓存
performance:
  cache:
    enabled: true
    ttl: 3600
```

### 2. 并行处理
```yaml
performance:
  parallel:
    enabled: true
    max_workers: 4
```

### 3. 内存优化
- 减少同时处理的股票数量
- 使用数据分块处理
- 定期清理缓存

## 安全建议

### 1. API密钥管理
- 不要将API密钥提交到Git
- 使用环境变量存储敏感信息
- 定期更换API密钥

### 2. 网络安全
- 使用HTTPS协议
- 配置防火墙规则
- 限制API访问频率

## 后续步骤

### 1. 基础使用
- 运行简单演示：`python simple_demo.py`
- 启动Web界面：`streamlit run frontend/app.py`
- 查看帮助：`python comprehensive_demo.py --help`

### 2. 高级配置
- 配置多数据源
- 设置定时任务
- 配置通知系统

### 3. 开发扩展
- 添加自定义因子
- 开发新策略
- 集成更多数据源

## 获取帮助

### 1. 文档资源
- [项目Wiki](https://github.com/xiaosicau/quantstock-selection-system/wiki)
- [API文档](docs/API.md)
- [开发指南](docs/DEVELOPMENT.md)

### 2. 社区支持
- [GitHub Issues](https://github.com/xiaosicau/quantstock-selection-system/issues)
- [Discussions](https://github.com/xiaosicau/quantstock-selection-system/discussions)

### 3. 联系支持
- 邮箱：quantstock@example.com
- QQ群：123456789