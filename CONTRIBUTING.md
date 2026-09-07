# 贡献指南

感谢您关注本项目！请阅读以下指南参与贡献。

## 开发环境搭建

请先阅读 [README.md](./README.md) 中的启动顺序部分，完成本地环境搭建。

## 分支策略

- `main` — 稳定发布分支
- `dev` — 日常开发分支
- `feature/*` — 新功能分支
- `fix/*` — Bug 修复分支

## 提交规范

推荐使用以下前缀：

| 前缀 | 用途 | 示例 |
|---|---|---|
| `feat:` | 新功能 | `feat: 添加软件搜索功能` |
| `fix:` | Bug 修复 | `fix: 修复登录超时问题` |
| `docs:` | 文档更新 | `docs: 更新部署文档` |
| `refactor:` | 代码重构 | `refactor: 重构后端路由` |
| `chore:` | 构建/工具 | `chore: 升级依赖版本` |
| `test:` | 测试相关 | `test: 添加 API 测试` |

## Pull Request 流程

1. Fork 本仓库
2. 从 `main` 分支创建特性分支
3. 编写代码并确保本地编译/运行通过
4. 提交 PR，描述变更内容和动机

## 代码规范

### 后端（Python / FastAPI）

- 使用 Python 3.10+ 风格
- 遵循 PEP 8 规范
- 提交前确保后端可正常启动

### 前端（Vue 3 / React）

- Vue 项目使用 Element Plus 组件库
- React 项目（Portal Web）使用 TypeScript
- 提交前确保 `npm run dev` 可正常启动

### uni-app（移动端）

- 使用 HBuilderX 或 CLI 方式开发
- 确保 H5 模式可正常运行
