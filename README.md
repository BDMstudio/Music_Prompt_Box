# Music Prompt Box

音乐风格知识库看板 - 流行音乐发展史与风格提示词管理工具

## 快速开始

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（首次运行）
python seeds/seed_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端 API 文档: http://localhost:8000/docs

### 2. 前端启动

```bash
cd frontend

# 安装依赖
pnpm install  # 或 npm install

# 启动开发服务器
pnpm dev  # 或 npm run dev
```

前端访问: http://localhost:5173

## 技术栈

- **前端**: Vue 3 + Vite + TypeScript + Tailwind CSS + Pinia
- **后端**: Python FastAPI + SQLAlchemy + SQLite

## 项目结构

```
music_prompt_box/
├── backend/           # 后端 API
│   ├── app/           # 应用代码
│   ├── data/          # SQLite 数据库
│   ├── seeds/         # 初始化数据
│   └── storage/       # 音频文件存储
├── frontend/          # 前端应用
│   └── src/
│       ├── api/       # API 请求
│       ├── components/# Vue 组件
│       ├── composables/# 组合式函数
│       ├── stores/    # Pinia 状态
│       └── types/     # TypeScript 类型
└── development.md     # 开发文档
```
