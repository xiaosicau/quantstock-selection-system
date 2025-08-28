#!/bin/bash
# 量化股票选股系统启动脚本

set -e

echo "🚀 启动量化股票选股系统..."

# 检查环境变量
if [[ -z "$TUSHARE_TOKEN" ]]; then
    echo "⚠️  警告: TUSHARE_TOKEN 未设置，请在环境变量中配置"
fi

# 创建必要目录
mkdir -p data logs cache config

# 检查配置文件
if [[ ! -f "config/config.yaml" ]]; then
    echo "📋 创建默认配置文件..."
    cp config/config.example.yaml config/config.yaml
fi

# 安装依赖（如果是首次运行）
if [[ ! -d "venv" ]]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 启动服务
echo "🌐 启动Web服务..."
streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0 &

# 启动API服务（可选）
# python src/api/rest_api.py &

echo "✅ 系统启动完成！"
echo "📊 Web界面: http://localhost:8501"
echo "🔌 API接口: http://localhost:5000"

# 等待进程
wait