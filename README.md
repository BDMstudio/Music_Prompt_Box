# Music Prompt Box

音乐风格知识库看板 — 流行音乐发展史与风格提示词管理工具

## 快速开始

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（首次运行）
python seeds/seed_db.py

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

后端 API 文档: http://localhost:8000/docs

### 2. 前端开发（仅开发时需要）

```bash
cd frontend

# 安装依赖
pnpm install  # 或 npm install

# 启动开发服务器
pnpm dev  # 或 npm run dev
```

前端开发访问: http://localhost:5173

### 3. 生产部署

生产环境下前端构建产物由 FastAPI 托管，单端口对外服务：

```bash
# 构建前端
cd frontend && pnpm build

# 启动后端（自动托管 frontend/dist/）
cd ../backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问: http://localhost:8000

局域网访问: http://<局域网IP>:8000

## 技术栈

- **前端**: Vue 3 + Vite + TypeScript + Tailwind CSS + Pinia
- **后端**: Python FastAPI + SQLAlchemy + SQLite
- **音频来源**: iTunes Search API（30s 试听片段）

## 核心功能

- **流派时间线** — 左侧导航，按年代(1950s-2020s)浏览音乐风格
- **风格卡片** — 每张卡片包含提示词标签、描述、BPM、试听片段
- **一键复制** — 单标签复制 / 全部标签复制，HTTP 环境自动降级兼容
- **全局播放器** — 底部控制栏：唱片封面、进度滑块、停止按钮
- **收藏夹** — 多收藏夹管理，快速收藏/取消
- **热门标签** — 基于复制次数的标签热度排行
- **搜索与筛选** — 实时搜索 + 流派筛选联动

## 项目结构

```
music_prompt_box/
├── backend/              # 后端 API + 前端静态托管
│   ├── app/
│   │   ├── main.py       # FastAPI 入口 + SPA 路由 + 静态文件托管
│   │   ├── config.py     # 配置（含 FRONTEND_DIST_PATH）
│   │   ├── database.py   # SQLAlchemy 异步引擎
│   │   ├── models/       # ORM 模型
│   │   ├── schemas/      # Pydantic 模式
│   │   └── routers/      # API 路由（styles, genres, folders, tags, itunes, data）
│   ├── data/             # SQLite 数据库
│   ├── seeds/            # 初始化 + 补充数据脚本
│   │   ├── initial_data.json
│   │   ├── seed_db.py
│   │   └── add_styles.py
│   └── venv/
├── frontend/             # 前端应用
│   └── src/
│       ├── api/          # API 请求
│       ├── components/
│       │   ├── layout/   # AppHeader, AppSidebar, AppMain
│       │   ├── cards/    # StyleCard, StyleGrid, StyleFormModal
│       │   ├── tags/     # TagPill, HotTags
│       │   ├── folders/  # FolderList
│       │   └── common/   # AudioPlayerBar, SearchBox, Toast, ConfirmModal
│       ├── composables/  # useAudio, useClipboard
│       ├── stores/       # Pinia 状态
│       └── types/        # TypeScript 类型
├── docs/
│   └── music-embed-research.md
├── README.md
└── development.md        # 开发架构文档
```

## 数据概览

- 8 个年代流派（1950s-2020s）+ 25 个子流派
- 40 张风格卡片，每张含 5-6 个 AI 音乐提示词标签
- 所有卡片均配有 iTunes 30s 试听片段
