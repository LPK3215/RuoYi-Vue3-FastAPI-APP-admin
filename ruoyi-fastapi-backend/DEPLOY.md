# RuoYi-FastAPI-Backend 部署文档

## 项目简介

基于 FastAPI 的后端服务，提供完整的 RBAC 权限管理系统功能。

## 环境要求

- **Python**: 3.10+
- **MySQL**: 5.7+ 或 PostgreSQL 13+
- **Redis**: 6.0+
- **Node.js**: 18+ (仅用于部分工具)

## 部署方式选择

### 方式一：本地服务（当前配置）

当前 `.env.dev` 配置连接的是 **本地** 的 MySQL 和 Redis：

```ini
DB_HOST = '127.0.0.1'
REDIS_HOST = '127.0.0.1'
```

### 方式二：Docker 服务

如需使用 Docker 运行 MySQL 和 Redis，参考下方「依赖服务部署」章节。

## 手动部署步骤

### 1. 创建虚拟环境

```bash
# 进入项目目录
cd ruoyi-fastapi-backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 2. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

本项目会按 `APP_ENV` 自动加载对应的环境文件：

- 默认加载：`.env.dev`
- 指定环境加载：`.env.<APP_ENV>`（例如 `.env.prod`、`.env.dockermy`、`.env.dockerpg`）

根据你的部署方式，选择并修改对应的 `.env.*` 文件即可。

```bash
# 示例：生产环境
# 1) 复制一份生产环境配置（可选）
# Windows
copy .env.dev .env.prod
# Linux/Mac
cp .env.dev .env.prod

# 2) 修改 .env.prod 中的 DB/Redis/JWT 等配置
```

**关键配置项**：

```ini
# 应用配置
APP_ENV = 'dev'
APP_HOST = '0.0.0.0'
APP_PORT = 9099
APP_RELOAD = false

# 数据库配置 (MySQL)
DB_TYPE = 'mysql'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_DATABASE = 'ruoyi-fastapi'

# Redis 配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_DATABASE = 2

# JWT 配置
JWT_SECRET_KEY = '你的密钥'
```

### 4. 初始化数据库

```bash
# 确保 MySQL/PostgreSQL 和 Redis 服务已启动

# 首次启动时，应用会自动创建表结构
# 无需手动执行 SQL
```

## 依赖服务部署

### 本地安装（当前使用方式）

**Windows:**
- MySQL: 从官网下载安装包安装
- Redis: 使用 WSL2 或下载 Windows 版本

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install mysql-server redis-server

# CentOS/RHEL
sudo yum install mysql-server redis
```

### Docker 安装（可选）

```bash
# 使用 Docker Compose 启动 MySQL 和 Redis
cd ..
docker-compose -f docker-compose.my.yml up -d
cd ruoyi-fastapi-backend

# 或单独启动
# MySQL
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=ruoyi-fastapi \
  -p 3306:3306 \
  mysql:8.0

# Redis
docker run -d --name redis \
  -p 6379:6379 \
  redis:latest
```

使用 Docker 时，确保对应的 `.env.*` 配置中的主机名正确：
- 如果后端也在 Docker 中运行，使用服务名称（如 `mysql`、`redis`）
- 如果后端在本地运行，使用 `host.docker.internal`（Windows/Mac）或 宿主机 IP（Linux）

### 6. 运行应用

#### 开发模式（支持热重载）

```bash
# 方式 1（推荐）: 使用 Python 入口启动（支持 --env 选择环境）
python app.py --env=dev

# 方式 2: 使用 uvicorn CLI 运行（需要通过环境变量 APP_ENV 选择环境）
# Windows (PowerShell)
$env:APP_ENV="dev"; uvicorn app:app --host 0.0.0.0 --port 9099 --reload
# Linux/Mac
APP_ENV=dev uvicorn app:app --host 0.0.0.0 --port 9099 --reload

# 方式 3: 直接使用工厂函数（同样需要 APP_ENV + --factory）
# uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --reload
```

#### 生产模式

```bash
# 方式 1: uvicorn 多进程运行（注意：--reload 仅用于开发环境）
# Windows (PowerShell)
$env:APP_ENV="prod"; uvicorn app:app --host 0.0.0.0 --port 9099 --workers 4
# Linux/Mac
APP_ENV=prod uvicorn app:app --host 0.0.0.0 --port 9099 --workers 4

# 或使用 gunicorn (Linux)
APP_ENV=prod gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:9099
```

### 7. 验证部署

访问以下地址验证服务是否正常运行：

- **应用地址**: http://localhost:9099
- **Swagger 文档**: http://localhost:9099/docs
- **ReDoc 文档**: http://localhost:9099/redoc

## 常见问题

### 1. 数据库连接失败

```bash
# 检查 MySQL/PostgreSQL 服务是否启动
# 检查数据库是否存在
# 检查用户名密码是否正确
```

### 2. Redis 连接失败

```bash
# 检查 Redis 服务是否启动
# 检查 Redis 密码配置
```

### 3. 依赖安装失败

```bash
# 确保 pip 是最新版本
pip install --upgrade pip

# 如果某些包安装失败，尝试单独安装
pip install <package_name>
```

## 日志查看

日志文件位于 `logs/` 目录下，按日期和大小自动分割。

## 停止服务

```bash
# Ctrl+C 停止前台运行的服务

# 如果是后台进程，使用 kill 命令
kill <PID>
```
