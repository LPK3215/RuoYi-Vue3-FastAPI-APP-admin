# ruoyi-fastapi-frontend（后台管理系统）

本目录是 **后台管理系统 Web**（Vue3 + ElementPlus + Vite）。

> 你当前的核心业务是「SoftwareHub：软件库管理系统」，后台管理主要在「软件管理」菜单下维护分类/软件/软件详情。

---

## 开发启动（本机）

### 1) 环境依赖

- Node.js ≥ 18（推荐 20+）
- npm / pnpm / yarn 任一（本项目带 `package-lock.json`，默认按 npm 使用）

### 2) 启动前置条件

请先确保后端已启动（默认）：

- 后端：`http://127.0.0.1:9099`

开发环境 API 前缀（见 `.env.development`）：

- `VITE_APP_BASE_API = '/dev-api'`

并且 `vite.config.js` 已配置代理：

- `/dev-api` → `http://127.0.0.1:9099`（会自动把 `/dev-api` 前缀去掉再转发）

如果后端端口不是 `9099`，请修改 `vite.config.js` 的 `server.proxy['/dev-api'].target`。

### 3) 安装依赖 & 启动

进入目录：

```bash
cd ruoyi-fastapi-frontend
```

安装依赖：

```bash
npm install
```

启动开发服务器（默认端口 `80`）：

```bash
npm run dev
```

访问：

- `http://localhost:80`

默认账号密码（初始化 SQL 自带）：

- 账号：`admin`
- 密码：`admin123`

---

## 部署（静态资源 + 反向代理）

生产部署通常是：构建出静态文件 `dist/`，交给 Nginx（或任意静态服务器）托管，并将 `/prod-api` 反向代理到后端。

### 1) 构建

```bash
cd ruoyi-fastapi-frontend
npm ci
npm run build:prod
```

产物目录：

- `dist/`

### 2) 与后端的路径约定（重要）

前端生产环境默认（见 `.env.production`）：

- `VITE_APP_BASE_API = '/prod-api'`

后端生产环境默认（见 `ruoyi-fastapi-backend/.env.prod`）：

- `APP_ROOT_PATH = '/prod-api'`

因此建议使用 Nginx：

- 托管前端静态资源在 `/`
- 将 `/prod-api/` 代理到后端，并把 `/prod-api` 前缀去掉再转发

### 3) Nginx 示例

```nginx
server {
  listen 80;
  server_name your-domain.com;

  root /var/www/softwarehub-admin;
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

---

## 常见问题

### 1) 端口 80 被占用

修改 `vite.config.js`：

- `server.port: 80` → 换成可用端口（如 `5173`）

### 2) 登录/接口 502

通常是本机代理/抓包软件影响请求链路。建议：

- 先确认后端 `http://127.0.0.1:9099` 可访问
- 再确认 `vite.config.js` 的代理目标端口与后端一致

