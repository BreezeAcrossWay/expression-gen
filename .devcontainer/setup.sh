#!/bin/bash

echo "🚀 正在设置明星表情包生成器开发环境..."

# 安装Python依赖
echo "📦 安装Python依赖..."
cd /workspaces/*/backend
pip install -r requirements.txt

# 安装Node依赖
echo "📦 安装Node依赖..."
cd /workspaces/*/frontend
npm install

echo "✅ 环境设置完成！"
