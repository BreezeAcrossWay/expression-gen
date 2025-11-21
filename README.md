# 🎭 明星表情包生成器

一个强大的AI驱动的表情包生成工具，可以将明星照片转换为可爱的卡通形象，并生成各种表情包。

## ✨ 功能特性

- 📸 **照片上传**: 支持上传明星照片
- 🎨 **多风格生成**: 自动生成4种不同风格的卡通形象
- 😊 **表情包制作**: 默认生成开心、难过、思考等表情
- ✍️ **自定义表情**: 支持输入自定义提示词生成个性化表情
- 🗑️ **灵活管理**: 可以添加和删除表情包
- 💾 **便捷导出**: 支持单个导出和一键打包下载

## 🛠️ 技术栈

- **前端**: Vue 3 + Element Plus + Vite
- **后端**: Python + Flask + Pillow
- **部署**: Docker + Docker Compose + Nginx

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

这是最简单的部署方式，一键启动完整服务。

#### 前置要求
- Docker 20.10+
- Docker Compose 2.0+

#### 部署步骤

1. **克隆项目**
```bash
cd /workspace
```

2. **一键部署**
```bash
chmod +x deploy.sh
./deploy.sh
```

3. **访问应用**
- 前端界面: http://localhost
- 后端API: http://localhost:5000

4. **查看日志**
```bash
docker-compose logs -f
```

5. **停止服务**
```bash
docker-compose down
```

### 方式二：开发环境

适合需要修改代码或调试的开发者。

#### 前置要求
- Python 3.9+
- Node.js 16+
- npm 或 yarn

#### 启动步骤

1. **使用启动脚本（推荐）**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

2. **或手动启动**

**后端:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**前端:**
```bash
cd frontend
npm install
npm run dev
```

3. **访问应用**
- 前端开发服务器: http://localhost:3000
- 后端API: http://localhost:5000

## 📖 使用指南

### 1️⃣ 上传照片
- 点击上传区域或拖拽照片
- 支持 JPG、PNG、GIF 格式
- 文件大小限制 16MB

### 2️⃣ 选择卡通形象
- 系统自动生成4种不同风格的卡通形象
- 点击选择你最喜欢的风格

### 3️⃣ 生成表情包
- 自动生成开心、难过、思考三种基础表情
- 输入自定义提示词（如"生气"、"大笑"）生成更多表情
- 可以删除不满意的表情

### 4️⃣ 导出下载
- 单击下载按钮导出单个表情包
- 点击"一键导出全部"打包下载所有表情包

## 🔧 配置说明

### AI API配置（可选）

项目默认使用本地图像处理。如需使用真实的AI生成功能，可以配置以下API：

1. **复制环境变量文件**
```bash
cp backend/.env.example backend/.env
```

2. **编辑 `.env` 文件，添加你的API密钥**
```bash
# Stability AI
STABILITY_API_KEY=your-api-key-here

# 或使用其他AI服务
# REPLICATE_API_TOKEN=your-token-here
# OPENAI_API_KEY=your-key-here
```

3. **重启服务**
```bash
docker-compose restart  # Docker部署
# 或重新运行开发脚本
```

### 支持的AI服务

- **Stability AI**: 高质量图像生成
- **Replicate**: 多种AI模型选择
- **OpenAI DALL-E**: 智能图像生成
- **本地 Stable Diffusion**: 完全私有部署

## 📁 项目结构

```
/workspace/
├── backend/                 # 后端服务
│   ├── app.py              # Flask应用主文件
│   ├── requirements.txt    # Python依赖
│   ├── Dockerfile          # 后端Docker配置
│   ├── .env.example        # 环境变量示例
│   ├── uploads/            # 上传文件目录
│   └── outputs/            # 生成文件目录
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   └── main.js        # 入口文件
│   ├── index.html         # HTML模板
│   ├── package.json       # Node依赖
│   ├── vite.config.js     # Vite配置
│   ├── Dockerfile         # 前端Docker配置
│   └── nginx.conf         # Nginx配置
├── docker-compose.yml     # Docker编排配置
├── deploy.sh              # 生产部署脚本
├── start-dev.sh           # 开发环境启动脚本
└── README.md              # 项目文档
```

## 🐛 常见问题

### 1. Docker构建失败
```bash
# 清理Docker缓存后重试
docker system prune -a
./deploy.sh
```

### 2. 端口被占用
修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:80"    # 前端改为8080
  - "5001:5000"  # 后端改为5001
```

### 3. 图像生成失败
- 检查是否配置了AI API密钥
- 确认网络连接正常
- 查看后端日志：`docker-compose logs backend`

### 4. 前端无法访问后端API
- 检查 `nginx.conf` 中的代理配置
- 确认后端服务已启动：`docker-compose ps`

## 🔄 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动
./deploy.sh
```

## 🛡️ 生产环境建议

1. **使用HTTPS**: 配置SSL证书
2. **设置防火墙**: 限制不必要的端口访问
3. **配置反向代理**: 使用Nginx或Traefik
4. **备份数据**: 定期备份uploads和outputs目录
5. **监控日志**: 使用日志聚合工具
6. **限制上传**: 设置合理的文件大小和频率限制

## 📝 API文档

### 上传照片
```
POST /api/upload
Content-Type: multipart/form-data
Body: file (image file)
```

### 生成表情包
```
POST /api/generate-expressions
Content-Type: application/json
Body: {
  "variant_id": "uuid",
  "expressions": ["开心", "难过", "思考"]
}
```

### 生成自定义表情
```
POST /api/generate-custom
Content-Type: application/json
Body: {
  "variant_id": "uuid",
  "prompt": "生气"
}
```

### 导出单个表情
```
GET /api/export-single/{expression_id}
```

### 导出全部表情
```
POST /api/export-all
Content-Type: application/json
Body: {
  "expression_ids": ["uuid1", "uuid2", ...]
}
```

### 删除表情
```
DELETE /api/delete-expression/{expression_id}
```

## 🤝 贡献

欢迎提交问题和拉取请求！

## 📄 许可证

MIT License

## 🎉 致谢

- Vue.js 团队
- Element Plus 团队
- Flask 社区
- 所有开源贡献者

---

**Made with ❤️ by AI Assistant**
