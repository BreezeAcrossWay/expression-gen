#!/bin/bash

echo "🎭 启动明星表情包生成器..."

# 启动后端
echo "🔧 启动后端服务..."
cd /workspaces/*/backend
python app.py > backend.log 2>&1 &

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务..."
cd /workspaces/*/frontend
npm run dev -- --host 0.0.0.0 > frontend.log 2>&1 &

# 等待服务启动
sleep 5

echo ""
echo "=========================================="
echo "  ✅ 服务启动成功！"
echo "=========================================="
echo ""
echo "📱 前端: http://localhost:3000"
echo "🔧 后端: http://localhost:5000"
echo ""
echo "提示: 点击弹出的端口转发通知访问应用"
echo "=========================================="
