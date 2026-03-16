# ruoyi-fastapi-desktop-web 部署与启动

这是一个**独立的电脑端 Web 前端项目**（Vite + React + TypeScript），用于调用 `ruoyi-fastapi-backend` 的接口并把数据渲染成桌面端 UI。

---

## 0) 前置条件

- Node.js（建议 ≥ 18）
- 后端可用（开发默认：`http://127.0.0.1:9099`）
  - Swagger：`http://127.0.0.1:9099/docs`

---

## 1) 本机启动（最简单：直接打开网页看）

进入目录：

```bash
cd ruoyi-fastapi-desktop-web
```

安装依赖：

```bash
npm install
```

启动开发模式（用于看页面/调接口）：

```bash
npm run dev
```

默认地址：`http://localhost:5175`

---

## 2) 本机启动（更接近部署：build + preview）

```bash
cd ruoyi-fastapi-desktop-web
npm install
npm run build
npm run preview -- --host 127.0.0.1 --port 5175
```

默认地址：`http://localhost:5175`

---

## 3) 一键启动脚本（Windows）

如果你不想敲命令，直接运行：

- `scripts/start-preview.ps1`：build + preview + 自动打开浏览器

示例（PowerShell）：

```powershell
cd ruoyi-fastapi-desktop-web
powershell -ExecutionPolicy Bypass -File .\scripts\start-preview.ps1
```

---

## 4) 环境变量与接口前缀

本项目默认把 API 前缀写成环境变量（注意：Vite 的 `VITE_*` 会在构建时注入）。

### 开发环境（`.env.development`）

- `VITE_API_BASE=/dev-api`
- `VITE_API_TARGET=http://127.0.0.1:9099`

含义：

- 浏览器请求走 `/dev-api/**`
- Vite 代理转发到 `VITE_API_TARGET`，并去掉 `/dev-api` 前缀（见 `vite.config.ts`）

### 生产环境（`.env.production`）

- `VITE_API_BASE=/prod-api`

含义：

- 浏览器请求走 `/prod-api/**`
- **需要由 Nginx 等反代到后端**（示例见下一节）

---

## 5) Nginx 部署示例（推荐）

假设：

- 前端构建产物在：`/var/www/deskops`（对应 `dist/` 内容）
- 后端在：`127.0.0.1:9099`
- 前端访问 API 前缀：`/prod-api/`

```nginx
server {
  listen 80;
  server_name your-domain.com;

  root /var/www/deskops;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  location /prod-api/ {
    proxy_pass http://127.0.0.1:9099/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

构建命令：

```bash
cd ruoyi-fastapi-desktop-web
npm install
npm run build
```

把 `dist/` 里的文件复制到 Nginx 的 `root` 目录即可。

