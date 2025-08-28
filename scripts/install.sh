#!/bin/bash
# 量化股票选股系统安装脚本

set -e

echo "📦 开始安装量化股票选股系统..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [[ $(echo "$python_version >= $required_version" | bc) -eq 0 ]]; then
    echo "❌ Python版本过低，需要 $required_version 或更高"
    exit 1
fi

echo "✅ Python版本: $python_version"

# 创建虚拟环境
echo "🐍 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级pip
echo "⬆️  升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements.txt

# 创建目录结构
echo "📁 创建目录结构..."
mkdir -p data logs cache config tests

# 复制配置文件
echo "⚙️  设置配置文件..."
if [[ ! -f "config/config.yaml" ]]; then
    cp config/config.example.yaml config/config.yaml
    echo "📋 已创建默认配置文件，请编辑 config/config.yaml 设置API密钥"
fi

# 设置权限
echo "🔒 设置文件权限..."
chmod +x scripts/*.sh

# 运行测试
echo "🧪 运行安装测试..."
python -c "import src; print('✅ 安装测试通过')"

echo "🎉 安装完成！"
echo ""
echo "下一步:"
echo "1. 编辑 config/config.yaml 设置API密钥"
echo "2. 运行: ./scripts/start.sh 启动系统"
echo "3. 访问: http://localhost:8501"