<h1 align="center">
    <img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</h1>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">RuoYi-Vue3-FastAPI</h1>
<h4 align="center">基于 RuoYi-Vue3+FastAPI 前后端分离的快速开发框架</h4>

> **⚠️ 二次开发声明**  
> 本项目基于原 RuoYi-Vue3-FastAPI 框架进行二次开发，已根据实际业务需求进行了定制化修改。  
> 如需使用原始框架，请访问：[Gitee](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) | [GitHub](https://github.com/insistence/RuoYi-Vue3-FastAPI)

<p align="center">
    <a href="https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI/stargazers">
        <img alt="Gitee" src="https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI/badge/star.svg?theme=dark">
    </a>
    <a href="https://github.com/insistence/RuoYi-Vue3-FastAPI">
        <img alt="Github" src="https://img.shields.io/github/stars/insistence/RuoYi-Vue3-FastAPI?style=social">
    </a>
    <a href="https://github.com/insistence/RuoYi-Vue3-FastAPI/actions?query=branch%3Amaster+event%3Apush+workflow%3A%22%22Playwright+Tests%22%22">
        <img alt="Playwright Tests" src="https://github.com/insistence/RuoYi-Vue3-FastAPI/workflows/Playwright Tests/badge.svg">
    </a>
    <a href="https://github.com/insistence/RuoYi-Vue3-FastAPI/actions?query=branch%3Amaster+event%3Apush+workflow%3A%22%22Ruff+Check%22%22">
        <img alt="Ruff Check" src="https://github.com/insistence/RuoYi-Vue3-FastAPI/workflows/Ruff Check/badge.svg">
    </a>
    <a href="https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI">
        <img alt="project version" src="https://img.shields.io/badge/version-1.9.0-brightgreen.svg">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img alt="Ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json">
    </a>
    <a href="https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI/blob/master/LICENSE">
        <img alt="LICENSE" src="https://img.shields.io/github/license/mashape/apistatus.svg">
    </a>
    <img alt="node version" src="https://img.shields.io/badge/node-≥18-blue">
    <img alt="python version" src="https://img.shields.io/badge/python-≥3.10-blue">
    <img alt="mysql version" src="https://img.shields.io/badge/MySQL-≥5.7-blue">
    <img alt="redis version" src="https://img.shields.io/badge/redis-≥6.2-blue">
</p>

## 本仓库当前核心业务（SoftwareHub：软件库管理系统）

> 说明：本仓库基于 `RuoYi-Vue3-FastAPI` 二次开发，目前**核心业务**是「软件库/软件资源管理」。

### 你能用它做什么

- **后台管理（管理员）**：维护软件分类、软件基础信息与富文本说明（Markdown）、多平台下载地址、资源链接（第一阶段仅存 URL）。
- **用户端（普通用户）**：通过 Portal API/应用端展示「上架的软件」并支持筛选搜索（用户端 UI 可按需要再迭代）。

### 软件管理模块（业务核心）

- 分类管理：增删改查分类
- 软件列表：筛选/搜索、增删改查、上架/下架；支持 **表格/卡片** 两种展示模式切换
- 软件详情：用于查看/编辑单个软件的完整信息（保留列表弹窗编辑，同时提供独立详情页）

### 目录结构（后端 / 管理端 / 用户端）

| 目录 | 说明 | 文档 |
| --- | --- | --- |
| `ruoyi-fastapi-backend/` | FastAPI 后端（含后台管理 API + Portal API） | `ruoyi-fastapi-backend/README.md` |
| `ruoyi-fastapi-frontend/` | 后台管理系统 Web（Vue3 + ElementPlus + Vite） | `ruoyi-fastapi-frontend/README.md` |
| `ruoyi-fastapi-app/` | 用户端 App（uni-app，支持 H5/小程序/APP 等） | `ruoyi-fastapi-app/README.md` |

### 快速启动（本机开发，不使用 Docker）

1. 初始化数据库：导入基础 SQL + 软件库业务 SQL（见 `ruoyi-fastapi-backend/README.md`）。
2. 启动 Redis：可使用脚本 `scripts/dev/setup-redis.ps1` + `scripts/dev/start-redis.ps1`（Windows）。
3. 启动后端：见 `ruoyi-fastapi-backend/README.md`（默认端口 `9099`）。
4. 启动后台管理：见 `ruoyi-fastapi-frontend/README.md`（默认端口 `80`）。

---

## 平台简介

RuoYi-Vue3-FastAPI 是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

* 前端采用 Vue3、Element Plus，基于<u>[RuoYi-Vue3](https://github.com/yangzongzhuan/RuoYi-Vue3)</u>前端项目修改。
* 移动端采用 uni-app、Vue3、Vite，内置 tailwindcss，基于<u>[RuoYi-App](https://github.com/yangzongzhuan/RuoYi-App)</u>项目修改。
* 后端采用 FastAPI、sqlalchemy、MySQL（PostgreSQL）、Redis、OAuth2 & Jwt。
* 权限认证使用 OAuth2 & Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* Vue2 版本：
  * Gitte 仓库地址：<https://gitee.com/insistence2022/RuoYi-Vue-FastAPI>
  * GitHub 仓库地址：<https://github.com/insistence/RuoYi-Vue-FastAPI>
* 纯 Python 版本：
  * Gitte 仓库地址：<https://gitee.com/insistence2022/dash-fastapi-admin>
  * GitHub 仓库地址：<https://github.com/insistence/Dash-FastAPI-Admin>
* 特别鸣谢：<u>[RuoYi-Vue3](https://github.com/yangzongzhuan/RuoYi-Vue3)</u>、<u>[RuoYi-App](https://github.com/yangzongzhuan/RuoYi-App)</u>

## 内置功能

1. 用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2. 角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
3. 菜单管理：配置系统菜单，操作权限，按钮权限标识等。
4. 部门管理：配置系统组织机构（公司、部门、小组）。
5. 岗位管理：配置系统用户所属担任职务。
6. 字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7. 参数管理：对系统动态配置常用参数。
8. 通知公告：系统通知公告信息发布维护。
9. 操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
10. 登录日志：系统登录日志记录查询包含登录异常。
11. 在线用户：当前系统中活跃用户状态监控。
12. 定时任务：在线（添加、修改、删除）任务调度包含执行结果日志。
13. 服务监控：监视当前系统 CPU、内存、磁盘、堆栈等相关信息。
14. 缓存监控：对系统的缓存信息查询，命令统计等。
15. 在线构建器：拖动表单元素生成相应的 HTML 代码。
16. 系统接口：根据业务代码自动生成相关的 api 接口文档。
17. 代码生成：配置数据库表信息一键生成前后端代码（python、sql、vue、js），支持下载。
18. AI 管理：提供 AI 模型管理和 AI 对话功能。

## 演示图

<table>
    <tr>
        <td>
            <img alt="login" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/login.png">
        </td>
        <td>
            <img alt="dashboard" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/dashboard.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="user" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/user.png">
        </td>
        <td>
            <img alt="role" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/role.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="menu" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/menu.png">
        </td>
        <td>
            <img alt="dept" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/dept.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt=""post src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/post.png">
        </td>
        <td>
            <img alt="dict" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/dict.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="config" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/config.png">
        </td>
        <td>
            <img alt="notice" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/notice.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="operLog" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/operLog.png">
        </td>
        <td>
            <img alt="loginLog" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/loginLog.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="online" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/online.png">
        </td>
        <td>
            <img alt="job" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/job.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="server" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/server.png">
        </td>
        <td>
            <img alt="cache" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/cache.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="cacheList" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/cacheList.png">
        </td>
        <td>
            <img alt="form" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/form.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="api" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/api.png">
        </td>
        <td>
            <img alt="gen" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/gen.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="aiModel" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/aiModel.png">
        </td>
        <td>
            <img alt="aiChat" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/aiChat.png">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="profile" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/web/profile.png">
        </td>
    </tr>
</table>

<table>
    <tr>
        <td>
            <img alt="applogin" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/app/login.png">
        </td>
        <td>
            <img alt="appWorkbench" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/app/workbench.png">
        </td>
        <td>
            <img alt="appProfile" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/vue3/app/profile.png">
        </td>
    </tr>
</table>

## 在线体验

* *账号：admin*
* *密码：admin123*
* 演示地址：<a href="https://vfadmin.insistence.tech">vfadmin 管理系统<a>

## 项目开发及发布相关

### 开发

```bash
# 克隆项目
git clone https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI.git

# 进入项目根目录
cd RuoYi-Vue3-FastAPI
```

#### 前端

```bash
# 进入前端目录
cd ruoyi-fastapi-frontend

# 安装依赖
npm install 或 yarn --registry=https://registry.npmmirror.com

# 建议不要直接使用 cnpm 安装依赖，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npmmirror.com

# 启动服务
npm run dev 或 yarn dev
```

#### 移动端

```bash
# 进入移动端目录
cd ruoyi-fastapi-app

# 安装依赖
npm install -g pnpm
pnpm install

# 启动 H5
pnpm dev:h5

# 启动微信小程序
pnpm dev:mp-weixin
```

移动端详细文档请参考：[ruoyi-fastapi-app/README.md](./ruoyi-fastapi-app/README.md)

#### 后端

```bash
# 进入后端目录
cd ruoyi-fastapi-backend

# 如果使用的是 MySQL 数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements.txt
# 如果使用的是 PostgreSQL 数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements-pg.txt

# 配置环境
在.env.dev 文件中配置开发环境的数据库和 redis

# 运行 sql 文件
1.新建数据库 ruoyi-fastapi(默认，可修改)
2.如果使用的是 MySQL 数据库，使用命令或数据库连接工具运行 sql 文件夹下的 ruoyi-fastapi.sql；如果使用的是 PostgreSQL 数据库，使用命令或数据库连接工具运行 sql 文件夹下的 ruoyi-fastapi-pg.sql

# 运行后端
python3 app.py --env=dev
```

#### 访问

```bash
# 默认账号密码
账号：admin
密码：admin123

# 浏览器访问
地址：http://localhost:80
```

### 发布

#### 前端

```bash
# 构建测试环境
npm run build:stage 或 yarn build:stage

# 构建生产环境
npm run build:prod 或 yarn build:prod
```

#### 后端

```bash
# 配置环境
在.env.prod 文件中配置生产环境的数据库和 redis

# 运行后端
python3 app.py --env=prod
```

### Docker Compose 部署方式

> ⚠️ **警告：** 默认未做数据持久化配置，请注意数据备份或自行配置持久化

#### MySQL 版本

```bash
docker compose -f docker-compose.my.yml up -d --build
```

#### PostgreSQL 版本

```bash
docker compose -f docker-compose.pg.yml up -d --build
```

## 交流与赞助

如果有对本项目及 FastAPI 感兴趣的朋友，欢迎加入知识星球一起交流学习，让我们一起变得更强。如果你觉得这个项目帮助到了你，你可以请作者喝杯咖啡表示鼓励☕。扫描下面微信二维码添加微信备注 VF-Admin 即可进群。
<table>
    <tr>
        <td>
            <img alt="zsxq" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/common/zsxq.jpg">
        </td>
        <td>
            <img alt="zanzhu" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/common/zanzhu.jpg">
        </td>
    </tr>
    <tr>
        <td>
            <img alt="wxcode" src="https://gitee.com/insistence2022/ruoyi-fastapi-pictures/raw/master/common/wxcode.jpg">
        </td>
    </tr>
</table>

## 版权说明

本项目基于 MIT 协议开源，允许商业使用，但请保留原作者版权信息。二次开发版本请自行标注。
