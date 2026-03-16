# RuoYi-FastAPI-Frontend 部署文档

## 项目简介

基于 Vue3 + Vite + Element Plus 开发的前端管理系统。

## 环境要求

- **Node.js**: 18+ (推荐 20+)
- **npm**: 9+ 或 **pnpm**: 8+ 或 **yarn**: 1.22+

## 手动部署步骤

### 1. 安装 Node.js

从 [Node.js 官网](https://nodejs.org/) 下载并安装 LTS 版本。

验证安装：

```bash
node -v
npm -v
```

### 2. 安装依赖

```bash
# 进入项目目录
cd ruoyi-fastapi-frontend

# 安装依赖（选择一种包管理器）
npm install
# 或
pnpm install
# 或
yarn install
```

### 3. 配置环境变量

根据部署环境选择对应的配置文件：

- `.env.development` - 开发环境
- `.env.production` - 生产环境
- `.env.staging` - 测试环境
- `.env.docker` - Docker 环境

**关键配置项**：

```ini
# 开发环境配置 (.env.development)
VITE_APP_BASE_API = '/dev-api'
VITE_APP_API_URL = 'http://localhost:9099'

# 生产环境配置 (.env.production)
VITE_APP_BASE_API = '/prod-api'
VITE_APP_API_URL = 'http://your-server-ip:9099'
```

### 4. 运行应用

#### 开发模式

```bash
# 启动开发服务器（支持热重载）
npm run dev
# 或
pnpm dev
# 或
yarn dev
```

默认访问地址：http://localhost:3000

#### 生产构建

```bash
# 构建生产版本
npm run build:prod

# 构建 Docker 版本
npm run build:docker

# 构建测试环境版本
npm run build:stage
```

构建产物输出到 `dist/` 目录。

#### 预览生产构建

```bash
# 本地预览生产构建
npm run preview
```

### 5. 部署到服务器

#### 方式 1: 静态文件部署

```bash
# 1. 构建项目
npm run build:prod

# 2. 将 dist/ 目录上传到 Web 服务器（Nginx/Apache）
# 3. 配置 Web 服务器指向 dist 目录
```

#### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dist;
    index index.html;

    # 开启 gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理配置
    location /prod-api/ {
        proxy_pass http://localhost:9099/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 方式 2: Docker 部署

```bash
# 1. 构建 Docker 镜像
docker build -t ruoyi-fastapi-frontend .

# 2. 运行容器
docker run -d -p 80:80 ruoyi-fastapi-frontend
```

## 常见问题

### 1. 依赖安装失败

```bash
# 清除缓存后重新安装
npm cache clean --force
npm install

# 或使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### 2. 开发服务器启动失败

```bash
# 检查端口是否被占用
# Windows
netstat -ano | findstr :3000

# Linux/Mac
lsof -i :3000

# 修改 vite.config.js 中的端口配置
```

### 3. 构建失败

```bash
# 检查 Node.js 版本是否符合要求
node -v

# 删除 node_modules 和 lock 文件后重新安装
rm -rf node_modules package-lock.json
npm install

# 检查是否有 TypeScript 错误
```

### 4. 部署后页面空白

```bash
# 检查浏览器控制台是否有错误
# 检查 API 地址配置是否正确
# 检查 Nginx 配置是否正确
# 检查后端服务是否正常运行
```

### 5. 刷新页面 404

这是 SPA 路由问题，需要配置 Nginx 的 `try_files`：

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

## 停止服务

```bash
# 开发服务器按 Ctrl+C 停止
```

## 默认登录信息

- **用户名**: admin
- **密码**: admin123
