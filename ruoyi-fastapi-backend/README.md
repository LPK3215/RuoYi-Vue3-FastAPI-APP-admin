# ruoyi-fastapi-backend（后端）

本目录是 **FastAPI 后端**，同时提供：

- 后台管理 API（管理端登录后使用）
- Portal API（用户端/公开展示使用）

> 本项目优先按 **本机方式**运行（不依赖 Docker）。

---

## 开发启动（本机）

### 1) 环境依赖

- Python ≥ 3.10
- MySQL ≥ 5.7（或 MariaDB）
- Redis ≥ 6.2

### 2) 初始化数据库（必须）

1. 创建数据库（默认名见 `.env.dev`：`DB_DATABASE = 'ruoyi-fastapi'`）
2. 依次导入 SQL：
   - 基础表/权限/字典：`sql/ruoyi-fastapi.sql`
   - 软件库业务表 + 菜单：`sql/ruoyi-fastapi-software.sql`

> 如果你是“已有库升级”，并且只想同步软件菜单顺序/授权，可单独执行：`sql/ruoyi-fastapi-software-menu-migrate.sql`。

### 3) Redis（必须）

确保 Redis 可用，且数据库编号与 `.env.dev` 一致（默认：`REDIS_DATABASE = 2`）。

Windows 可选脚本：

- 下载/准备：`../scripts/dev/setup-redis.ps1`
- 启动：`../scripts/dev/start-redis.ps1`

### 4) 安装依赖 & 启动

进入目录：

```bash
cd ruoyi-fastapi-backend
```

创建虚拟环境（示例）：

```bash
python -m venv .venv
```

- Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py --env dev
```

- macOS/Linux：

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py --env dev
```

启动成功后默认：

- API：`http://127.0.0.1:9099`
- Swagger：`http://127.0.0.1:9099/docs`

---

## 部署（非 Docker）

### 1) 生产配置（必须）

修改：`.env.prod`

重点关注：

- `DB_HOST / DB_PORT / DB_USERNAME / DB_PASSWORD / DB_DATABASE`
- `REDIS_HOST / REDIS_PORT / REDIS_PASSWORD / REDIS_DATABASE`
- `APP_PORT`（默认 `9099`）
- `APP_ROOT_PATH`（默认 `/prod-api`，用于配合 Nginx 反代前缀）
- `APP_RELOAD=false`（生产环境不要开热重载）
- `APP_DISABLE_SWAGGER=true`（默认关闭 Swagger）

### 2) 初始化数据库（首次部署必须）

同开发启动：执行 `sql/ruoyi-fastapi.sql` + `sql/ruoyi-fastapi-software.sql`。

### 3) 启动方式

最简单（推荐先跑通）：

```bash
python app.py --env prod
```

如需 `uvicorn`（更可控）：

> 注意：直接运行 `uvicorn` 时无法使用 `--env` 这种自定义参数，需要用环境变量指定环境。

- Windows PowerShell：

```powershell
$env:APP_ENV="prod"
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

- macOS/Linux：

```bash
export APP_ENV=prod
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

### 4) Nginx 反向代理（推荐）

典型部署建议：

- 管理端静态资源：`/`（来自 `ruoyi-fastapi-frontend/dist`）
- API：`/prod-api/` 代理到后端 `9099`，并 **去掉** `/prod-api` 前缀再转发

示例（注意 `proxy_pass` 结尾的 `/`）：

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

### 1) 登录被锁定（密码输错太多次）

锁定信息在 Redis（db=2）里。可删除这些 Key 解锁：

- `account_lock:admin`
- `password_error_count:admin`

### 2) 改了代码但接口没变化

`.env.dev` 默认 `APP_RELOAD = false`，需要手动重启后端进程。

