#!/bin/bash
# Docker环境下的启动脚本

set -e

echo "🐳 在Docker环境中启动量化股票选股系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查环境变量文件
if [[ ! -f ".env" ]]; then
    echo "📋 创建环境变量文件..."
    cat > .env << EOF
# Tushare API Token
TUSHARE_TOKEN=your_tushare_token_here

# 数据库密码
DB_PASSWORD=quantstock123

# 日志级别
LOG_LEVEL=INFO
EOF
    echo "⚠️  请编辑 .env 文件设置您的API密钥"
fi

# 构建镜像
echo "🔨 构建Docker镜像..."
docker-compose build

# 启动服务
echo "🚀 启动Docker服务..."
docker-compose up -d

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

echo "✅ Docker服务启动完成！"
echo ""
echo "访问地址:"
echo "- Web界面: http://localhost:8501"
echo "- API接口: http://localhost:5000"
echo ""
echo "管理命令:"
echo "- 查看日志: docker-compose logs -f quantstock"
echo "- 停止服务: docker-compose down"
echo "- 重启服务: docker-compose restart"