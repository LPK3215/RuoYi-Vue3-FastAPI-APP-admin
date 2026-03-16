<h1 align="center">
    <img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</h1>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">RuoYi-Vue3-FastAPI</h1>
<h4 align="center">基于 RuoYi-Vue3+FastAPI 前后端分离的快速开发框架</h4>

> **⚠️ 二次开发声明**  
> 本项目基于原 RuoYi-Vue3-FastAPI 框架进行二次开发，已根据实际业务需求进行了定制化修改。  
> 原始框架地址：[Gitee](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) | [GitHub](https://github.com/insistence/RuoYi-Vue3-FastAPI)

---

## 核心业务：软件库管理系统（SoftwareHub）

本系统是一套**软件资源管理平台**，用于管理和分发软件资源。

### 功能模块

#### 后台管理（管理员）

| 功能 | 说明 |
|------|------|
| 分类管理 | 软件分类的增删改查 |
| 软件管理 | 软件基础信息、富文本说明（Markdown）、多平台下载地址管理 |
| 上架/下架 | 控制软件资源的展示状态 |
| 展示模式 | 支持表格/卡片两种视图切换 |

#### 用户端（普通用户）

| 功能 | 说明 |
|------|------|
| 软件浏览 | 查看已上架的软件资源 |
| 搜索筛选 | 按分类、名称等条件筛选软件 |
| 软件详情 | 查看软件完整信息和下载链接 |

### 项目结构

| 目录 | 说明 |
|------|------|
| `ruoyi-fastapi-backend/` | FastAPI 后端（后台管理 API + 用户端 API） |
| `ruoyi-fastapi-frontend/` | 后台管理系统（Vue3 + Element Plus + Vite） |
| `ruoyi-fastapi-desktop-web/` | 桌面端 Web 应用（React + TypeScript + Vite） |
| `ruoyi-fastapi-app/` | 用户端 App（uni-app，支持 H5/小程序/APP） |

---

## 快速启动

### 环境要求

- **Python**: 3.10+
- **Node.js**: 18+
- **MySQL**: 5.7+ 或 PostgreSQL 13+
- **Redis**: 6.0+

### 启动步骤

```bash
# 1. 克隆项目
git clone https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI.git
cd RuoYi-Vue3-FastAPI

# 2. 启动后端
cd ruoyi-fastapi-backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
# 配置 .env.dev 文件（数据库、Redis）
# 导入 SQL 文件初始化数据库
python server.py

# 3. 启动后台管理
cd ruoyi-fastapi-frontend
npm install
npm run dev

# 4. 启动桌面端（可选）
cd ruoyi-fastapi-desktop-web
npm install
npm run dev
```

### 默认登录信息

- **地址**: http://localhost:80
- **账号**: admin
- **密码**: admin123

---

## 部署文档

各子项目的详细部署文档：

- [后端部署](./ruoyi-fastapi-backend/DEPLOY.md)
- [前端部署](./ruoyi-fastapi-frontend/DEPLOY.md)
- [桌面端部署](./ruoyi-fastapi-desktop-web/DEPLOY.md)

---

## 技术栈

**后端**
- FastAPI + SQLAlchemy + MySQL/PostgreSQL + Redis + OAuth2 & JWT

**前端**
- Vue3 + Element Plus + Vite + Pinia + Vue Router

**桌面端**
- React 19 + TypeScript + Vite + TanStack Query + Ant Design

---

## 版权说明

本项目基于 MIT 协议开源，允许商业使用，但请保留原作者版权信息。
