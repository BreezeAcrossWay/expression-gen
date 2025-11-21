# 🎭 明星表情包生成器

一个强大的AI驱动的表情包生成工具，可以将明星照片转换为可爱的卡通形象，并生成各种表情包。

[![GitHub Codespaces](https://img.shields.io/badge/Open%20in-GitHub%20Codespaces-blue?logo=github)](https://github.com/codespaces)
[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

---

## 🚀 快速开始（选择一种方式）

### 方式1️⃣：GitHub Codespaces ⭐ 推荐

**最简单！5分钟完成，无需本地环境！**

```bash
# 1. 推送代码到GitHub
git push

# 2. 在GitHub仓库页面：
#    点击 Code → Codespaces → Create codespace on main

# 3. 等待自动启动（2-3分钟）

# 4. 点击端口通知，访问应用！
```

✅ 完全在云端运行  
✅ 零配置，开箱即用  
✅ 免费120小时/月  

👉 **详细教程**: [一键部署.md](./一键部署.md) 或 [GITHUB部署指南.md](./GITHUB部署指南.md)

---

### 方式2️⃣：本地运行

#### 使用脚本启动（推荐）
```bash
chmod +x start-dev.sh
./start-dev.sh
```

#### 手动启动
```bash
# 后端
cd backend
pip install -r requirements.txt
python app.py

# 前端（新终端）
cd frontend
npm install
npm run dev
```

访问: http://localhost:3000

---

### 方式3️⃣：Docker部署

```bash
chmod +x deploy.sh
./deploy.sh
```

访问: http://localhost

---

## ✨ 功能特性

- 📸 **照片上传**: 支持多种图片格式，拖拽上传
- 🎨 **多风格生成**: 自动生成4种不同风格的卡通形象
  - 可爱卡通风格
  - Q版动漫风格
  - 像素艺术风格
  - 简约线条风格
- 😊 **表情包制作**: 默认生成开心、难过、思考等表情
- ✍️ **自定义表情**: 支持输入自定义提示词生成个性化表情
- 🗑️ **灵活管理**: 可以添加和删除表情包
- 💾 **便捷导出**: 支持单个导出和一键打包下载

---

## 🛠️ 技术栈

**后端**: Python 3.12 + Flask 3.0 + Pillow 10.1  
**前端**: Vue 3.3 + Element Plus 2.4 + Vite 5.0  
**部署**: Docker + Nginx / GitHub Codespaces

---

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

---

## 🌐 云端部署方案

### GitHub Codespaces（最简单）⭐
- 完全在云端运行
- 5分钟启动
- 免费120小时/月
- 👉 [一键部署教程](./一键部署.md)

### Vercel + Railway（生产环境）
- 前端部署到Vercel（免费）
- 后端部署到Railway（$5/月）
- 永久在线，自定义域名
- 👉 [详细配置](./GITHUB部署指南.md)

### Render（完全免费）
- 一站式部署
- 完全免费
- 自动HTTPS
- 👉 [部署步骤](./GITHUB部署指南.md#方案三render一站式部署)

---

## 📂 项目结构

```
/workspace/
├── backend/                 # 后端服务
│   ├── app.py              # Flask应用主文件
│   ├── requirements.txt    # Python依赖
│   └── Dockerfile          # 后端Docker配置
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   └── main.js        # 入口文件
│   ├── package.json       # Node依赖
│   └── Dockerfile         # 前端Docker配置
├── .devcontainer/         # GitHub Codespaces配置
├── .github/workflows/     # 自动部署配置
├── docker-compose.yml     # Docker编排配置
├── deploy.sh              # 生产部署脚本
├── start-dev.sh          # 开发环境启动脚本
├── 一键部署.md            # 云端部署快速指南
└── GITHUB部署指南.md      # 详细部署文档
```

---

## 🔧 配置说明

### AI API集成（可选）

项目默认使用本地图像处理。如需真实的AI生成功能：

```bash
# 复制环境变量文件
cp backend/.env.example backend/.env

# 编辑 .env 文件，添加你的API密钥
# STABILITY_API_KEY=sk-xxxxx
# 或 REPLICATE_API_TOKEN=r8-xxxxx
# 或 OPENAI_API_KEY=sk-xxxxx

# 重启服务
```

支持的AI服务：
- Stability AI
- Replicate
- OpenAI DALL-E
- 本地 Stable Diffusion

---

## 🐛 故障排查

### 本地运行问题

**服务无法启动？**
```bash
# 检查端口占用
netstat -tlnp | grep -E "3000|5000"

# 查看进程状态
ps aux | grep -E "(python|vite)"
```

**上传失败？**
- 检查文件格式和大小
- 确认uploads目录权限

**查看日志：**
```bash
tail -f backend/backend.log
tail -f frontend/frontend.log
```

### Codespaces问题

**服务未自动启动？**
```bash
bash .devcontainer/start.sh
```

**端口未转发？**
- 点击底部"端口"标签
- 手动添加3000和5000端口

---

## 📚 完整文档

- **快速开始**: [START_HERE.md](./START_HERE.md) - 30秒快速入门
- **云端部署**: [一键部署.md](./一键部署.md) - GitHub云端运行
- **详细部署**: [GITHUB部署指南.md](./GITHUB部署指南.md) - 所有部署方案
- **项目说明**: [项目说明.md](./项目说明.md) - 技术架构详解
- **文件清单**: [项目文件清单.txt](./项目文件清单.txt) - 完整文件列表

---

## 🎯 使用场景

- 📱 **个人创作**: 制作自己的专属表情包
- 👥 **团队协作**: 生成团队成员卡通形象
- 🎮 **游戏开发**: 快速生成游戏角色
- 📺 **内容创作**: 为视频、文章制作配图
- 🎨 **设计灵感**: 探索不同艺术风格

---

## 🛡️ 生产环境建议

1. **使用HTTPS**: 配置SSL证书
2. **设置防火墙**: 限制不必要的端口访问
3. **配置反向代理**: 使用Nginx或Traefik
4. **备份数据**: 定期备份uploads和outputs目录
5. **监控日志**: 使用日志聚合工具
6. **限制上传**: 设置合理的文件大小和频率限制

---

## 📈 路线图

- [ ] 用户账号系统
- [ ] 表情包分享社区
- [ ] 批量上传处理
- [ ] 更多卡通风格
- [ ] 表情包模板库
- [ ] 文字添加功能
- [ ] 动态GIF生成
- [ ] 移动端APP

---

## 🤝 贡献

欢迎提交问题和拉取请求！

---

## 📄 许可证

MIT License

---

## 🎉 快速开始

选择最适合你的方式：

| 方式 | 适用场景 | 时间 | 难度 |
|------|---------|------|------|
| **GitHub Codespaces** | 试用、开发 | 5分钟 | ⭐ 最简单 |
| **本地运行** | 开发调试 | 10分钟 | ⭐⭐ 简单 |
| **Vercel+Railway** | 生产环境 | 15分钟 | ⭐⭐ 简单 |
| **Docker** | 生产环境 | 10分钟 | ⭐⭐⭐ 中等 |

**推荐**: 先用 GitHub Codespaces 试用，满意后再考虑生产部署！

👉 **立即开始**: [一键部署.md](./一键部署.md)

---

**Made with ❤️ by AI Assistant**
