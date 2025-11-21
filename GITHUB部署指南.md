# 🚀 GitHub云端部署指南

无需本地环境，直接在云端运行和部署你的明星表情包生成器！

---

## 方案一：GitHub Codespaces（推荐）⭐

**最简单的方式 - 5分钟完成，无需任何配置！**

### 什么是GitHub Codespaces？
GitHub提供的云端开发环境，直接在浏览器中运行完整项目（前端+后端）。

### 📋 使用步骤

#### 1. 推送代码到GitHub
```bash
# 如果还没有推送到GitHub
cd /workspace
git add .
git commit -m "初始化明星表情包生成器"
git push origin main
```

#### 2. 打开GitHub Codespaces

1. 访问你的GitHub仓库页面
2. 点击绿色的 **"<> Code"** 按钮
3. 选择 **"Codespaces"** 标签
4. 点击 **"Create codespace on main"**

#### 3. 等待环境启动

- Codespaces会自动：
  - ✅ 创建云端开发环境
  - ✅ 安装Python和Node.js
  - ✅ 安装所有依赖
  - ✅ 启动前后端服务
  - ✅ 自动转发端口

#### 4. 访问应用

启动完成后：
- 会自动弹出端口转发通知
- 点击 **"Open in Browser"** 访问前端（端口3000）
- 应用完全运行在云端！

### 💰 费用说明

- **免费额度**: 每月120核心小时（约60小时2核机器）
- **个人用户**: 完全免费够用
- **关闭环境**: 不使用时记得停止Codespace

### 🎯 优点

✅ 零配置，开箱即用  
✅ 完整的前后端环境  
✅ 直接在浏览器中使用  
✅ 自动保存代码  
✅ 可以修改和调试  
✅ 免费额度充足

---

## 方案二：Vercel + Railway 部署

**永久在线的生产环境 - 适合长期使用**

### 架构说明
- **前端**: 部署到Vercel（免费）
- **后端**: 部署到Railway（每月免费5美元额度）

### 📋 部署步骤

#### A. 部署后端到Railway

1. **访问Railway**
   - 打开 https://railway.app
   - 使用GitHub账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库

3. **配置服务**
   ```
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

4. **设置环境变量**（可选）
   - `STABILITY_API_KEY` - 如果使用AI服务

5. **生成域名**
   - 在Settings中点击 "Generate Domain"
   - 记下URL，例如：`https://xxx.railway.app`

#### B. 部署前端到Vercel

1. **访问Vercel**
   - 打开 https://vercel.com
   - 使用GitHub账号登录

2. **导入项目**
   - 点击 "Add New" → "Project"
   - 选择你的GitHub仓库
   - 点击 "Import"

3. **配置构建**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **配置环境变量**
   - 添加 `VITE_API_URL`
   - 值为Railway的后端URL：`https://xxx.railway.app`

5. **编辑前端API配置**
   
   修改 `frontend/src/App.vue`，将API请求改为：
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || '/api'
   ```

6. **部署**
   - 点击 "Deploy"
   - 等待部署完成
   - 访问Vercel提供的URL

#### C. 更新API地址

编辑 `vercel.json`，将后端URL替换：
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-railway-url.railway.app/api/:path*"
    }
  ]
}
```

### 💰 费用说明

**Railway:**
- 免费: $5/月额度
- 足够小项目使用
- 超出后按使用量计费

**Vercel:**
- 个人项目完全免费
- 无限带宽
- 自动HTTPS

### 🎯 优点

✅ 永久在线，24/7可访问  
✅ 自动HTTPS加密  
✅ 自定义域名（可选）  
✅ 自动部署（推送代码即更新）  
✅ CDN加速  
✅ 生产级性能

---

## 方案三：Render（一站式部署）

**最简单的一站式方案**

### 📋 部署步骤

#### 1. 访问Render
- 打开 https://render.com
- 使用GitHub账号登录

#### 2. 部署后端

1. 点击 "New +" → "Web Service"
2. 连接GitHub仓库
3. 配置：
   ```
   Name: sticker-backend
   Environment: Python
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && gunicorn app:app
   ```
4. 选择免费套餐
5. 点击 "Create Web Service"

#### 3. 部署前端

1. 点击 "New +" → "Static Site"
2. 连接同一个GitHub仓库
3. 配置：
   ```
   Name: sticker-frontend
   Build Command: cd frontend && npm install && npm run build
   Publish Directory: frontend/dist
   ```
4. 添加环境变量：
   - `VITE_API_URL`: 后端服务的URL
5. 点击 "Create Static Site"

### 💰 费用说明

- **免费套餐**: 750小时/月
- **自动休眠**: 15分钟无访问会休眠
- **唤醒时间**: 约30秒

### 🎯 优点

✅ 完全免费  
✅ 前后端一站式  
✅ 自动HTTPS  
✅ 简单配置

---

## 快速对比

| 方案 | 适用场景 | 优点 | 费用 |
|------|---------|------|------|
| **Codespaces** | 开发测试 | 零配置，完整环境 | 免费120小时/月 |
| **Vercel+Railway** | 生产使用 | 永久在线，高性能 | Railway $5/月 |
| **Render** | 个人项目 | 一站式，完全免费 | 完全免费 |

---

## 🎯 推荐选择

### 你想要什么？

**1. 快速试用/开发** → 选择 **GitHub Codespaces**
- 5分钟启动
- 无需配置
- 完整功能

**2. 分享给朋友使用** → 选择 **Vercel + Railway**
- 永久在线
- 稳定快速
- 自定义域名

**3. 个人长期使用** → 选择 **Render**
- 完全免费
- 简单易用
- 够用就好

---

## 📝 详细配置文件说明

### GitHub Codespaces配置
已创建 `.devcontainer/` 目录，包含：
- `devcontainer.json` - 环境配置
- `setup.sh` - 自动安装依赖
- `start.sh` - 自动启动服务

### Vercel配置
- `vercel.json` - Vercel部署配置
- 自动路由到后端API

### Railway配置
- `railway.json` - Railway部署配置
- `Procfile` - 启动命令
- `runtime.txt` - Python版本

---

## 🚀 立即开始

### 推荐：使用GitHub Codespaces

```bash
# 1. 推送代码到GitHub
git add .
git commit -m "添加云端部署配置"
git push

# 2. 在GitHub仓库页面点击 "Code" → "Codespaces" → "Create"
# 3. 等待启动（约2-3分钟）
# 4. 点击端口转发通知，访问应用！
```

---

## ❓ 常见问题

### Q: Codespaces会一直运行吗？
A: 不会，30分钟无操作会自动停止，再次打开即可恢复。

### Q: 免费额度够用吗？
A: 完全够用！120小时≈每天4小时，适合开发测试。

### Q: 可以自定义域名吗？
A: Codespaces不行，但Vercel和Railway支持。

### Q: 数据会丢失吗？
A: Codespaces的文件系统会保留，但生成的图片建议定期下载。

### Q: 如何关闭Codespace？
A: 在GitHub仓库的Codespaces页面点击"Stop"。

---

## 🎉 下一步

1. **选择方案**: Codespaces最简单
2. **推送代码**: `git push`
3. **创建环境**: 点击几下就完成
4. **开始使用**: 在浏览器中访问

---

## 📞 需要帮助？

查看详细文档：
- README.md - 完整项目文档
- 快速开始.md - 本地使用指南

---

**🎭 享受云端开发的便利！**

*推送代码后，在GitHub仓库点击 Code → Codespaces → Create codespace on main 即可开始！*
