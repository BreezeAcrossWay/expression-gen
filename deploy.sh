#!/bin/bash

# 明星表情包生成器 - 一键部署脚本

echo "================================"
echo "  明星表情包生成器 部署脚本"
echo "================================"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    echo "安装指南: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    echo "安装指南: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker 和 Docker Compose 已安装"
echo ""

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 构建镜像
echo "🔨 构建 Docker 镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

echo ""
echo "================================"
echo "  部署完成！"
echo "================================"
echo ""
echo "📱 前端访问地址: http://localhost"
echo "🔧 后端API地址: http://localhost:5000"
echo ""
echo "查看日志:"
echo "  docker-compose logs -f"
echo ""
echo "停止服务:"
echo "  docker-compose down"
echo ""
