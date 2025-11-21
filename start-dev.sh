#!/bin/bash

# 开发环境启动脚本

echo "================================"
echo "  启动开发环境"
echo "================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

echo "✅ 依赖检查通过"
echo ""

# 启动后端
echo "🔧 启动后端服务..."
cd backend

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f "venv/.installed" ]; then
    echo "安装 Python 依赖..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# 启动Flask
echo "启动 Flask 服务器 (端口 5000)..."
python app.py &
BACKEND_PID=$!

cd ..

# 启动前端
echo ""
echo "🎨 启动前端服务..."
cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "安装 Node.js 依赖..."
    npm install
fi

# 启动Vite
echo "启动 Vite 开发服务器 (端口 3000)..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "================================"
echo "  开发环境已启动！"
echo "================================"
echo ""
echo "📱 前端开发地址: http://localhost:3000"
echo "🔧 后端API地址: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
