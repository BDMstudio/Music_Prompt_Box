# Music Prompt Box - 开发架构文档

> **项目名称**: music_prompt_box  
> **版本**: v1.0  
> **最后更新**: 2026-01-19  

---

## 目录

1. [项目概述](#1-项目概述)
2. [功能需求](#2-功能需求)
3. [数据结构设计](#3-数据结构设计)
4. [技术架构](#4-技术架构)
5. [目录结构](#5-目录结构)
6. [交互设计](#6-交互设计)
7. [API 接口设计](#7-api-接口设计)
8. [开发计划](#8-开发计划)
9. [附录](#9-附录)

---

## 1. 项目概述

### 1.1 核心定位

**Music Prompt Box** 是一个**音乐风格知识库看板**，服务于 AI 音乐创作者（如 Suno 用户）。它将流行音乐发展史的知识体系与风格提示词（Style Prompt）管理相结合，帮助用户：

1. **学习与探索** - 通过可视化的流派分支图，理解音乐风格的演变脉络
2. **创作辅助** - 快速检索、复制经过校准的风格提示词
3. **听觉校准** - 播放示例音频，确保提示词与预期听感一致

### 1.2 目标用户

- AI 音乐生成工具（Suno、Udio 等）的重度用户
- 音乐制作人 / 编曲师
- 音乐爱好者 / 学习者

### 1.3 设计原则

| 原则 | 说明 |
|------|------|
| **数据即资产** | 用户积累的风格提示词库是核心价值，必须支持备份与迁移 |
| **所听即所得** | 每个提示词都应有对应的示例音频，避免"盲写" |
| **快速复制** | 最小化从"找到风格"到"粘贴到 Suno"的操作路径 |
| **可扩展** | 流派树和卡片数据由用户自主维护，系统不做硬编码限制 |

---

## 2. 功能需求

### 2.1 功能模块总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        Music Prompt Box                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────────────────────────────┐  │
│  │              │  │                                         │  │
│  │   流派时间线   │  │            风格卡片网格                  │  │
│  │   (左侧导航)  │  │            (主内容区)                    │  │
│  │              │  │                                         │  │
│  │  - 流派分支   │  │  - 卡片展示                              │  │
│  │  - 折叠/展开  │  │  - 搜索/筛选                            │  │
│  │  - 筛选联动   │  │  - 添加/编辑/删除                        │  │
│  │              │  │  - 复制提示词                            │  │
│  │              │  │  - 音频播放                              │  │
│  └──────────────┘  └─────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  顶部导航栏: 收藏夹入口 | 导入/导出 | 热门标签                     │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 流派时间线（左侧导航）

#### 2.2.1 视觉呈现

- **样式**: 水平时间线 + 垂直分支（类似地铁线路图）
- **层级**: 最多支持 **3 层**嵌套
  ```
  Rock (L1)
  ├── Punk Rock (L2)
  │   ├── Post-Punk (L3)
  │   └── Hardcore Punk (L3)
  └── Progressive Rock (L2)
  ```

#### 2.2.2 交互行为

| 操作 | 行为 |
|------|------|
| **展开/折叠按钮** | 点击 `▶`/`▼` 图标，展开或收起子分类 |
| **筛选按钮** | 点击流派名称旁的筛选图标，筛选右侧卡片（包含所有子分类的卡片） |
| **默认状态** | 全部展开 |

#### 2.2.3 数据维护

- 流派树结构由用户**手动维护**（通过管理界面或直接编辑数据）
- 初始数据基于原型中的 1950s-2020s 年代分类

---

### 2.3 风格卡片（主内容区）

#### 2.3.1 卡片字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 自动 | 唯一标识符，系统自动生成 |
| `name` | string | ✅ **必填** | 风格名称，如 "Synthwave" |
| `tags` | string[] | ✅ **必填** | 风格标签/提示词数组 |
| `genre_path` | string | 选填 | 所属流派路径，如 "Electronic/Synthwave" |
| `description` | string | 选填 | 风格描述 |
| `bpm_range` | string | 选填 | BPM 范围，如 "120-140" |
| `audio_type` | enum | 选填 | 音频类型：`local` \| `url` |
| `audio_source` | string | 选填 | 本地文件路径或外部 URL |
| `reference_url` | string | 选填 | 参考来源链接 |
| `is_favorite` | boolean | 自动 | 是否已收藏 |
| `copy_count` | number | 自动 | 被复制次数（用于热门标签统计） |
| `created_at` | datetime | 自动 | 创建时间 |
| `updated_at` | datetime | 自动 | 更新时间 |

#### 2.3.2 卡片操作

| 操作 | 入口 | 行为 |
|------|------|------|
| **添加** | 顶部"添加风格"按钮 | 弹出表单 Modal，填写后保存 |
| **编辑** | 卡片右上角编辑图标 | 弹出预填充的表单 Modal |
| **删除** | 卡片右上角删除图标 | 弹出确认框，确认后删除 |
| **收藏** | 卡片上的收藏图标 | 切换收藏状态，加入/移出收藏夹 |
| **播放** | 卡片上的播放按钮 | 播放示例音频（同时只能播放一个） |

#### 2.3.3 复制功能

| 操作 | 触发 | 输出格式 | 示例 |
|------|------|----------|------|
| **复制单个 Tag** | 点击单个 Tag 标签 | 单个词 | `synthwave` |
| **复制全部 Tags** | 点击"复制全部"按钮 | 空格分隔 | `synthwave retrowave analog synth` |

---

### 2.4 音频播放

#### 2.4.1 支持的音频来源

| 来源类型 | 说明 | 示例 |
|----------|------|------|
| **本地上传** | 用户上传 MP3 文件到服务器 | `/audio/synthwave_ref.mp3` |
| **外部链接** | 直接播放 `.mp3` 等音频链接 | `https://example.com/demo.mp3` |
| **iTunes 试听** | 通过 iTunes Search API 获取 30s 预览片段 | `https://audio.itunes.apple.com/...` |

#### 2.4.2 播放行为

- **互斥播放**: 同一时间只能播放一个音频，点击新的播放按钮会停止当前播放
- **播放状态**: 卡片内播放按钮显示播放/暂停状态，带脉冲动画
- **全局控制栏**: 底部固定 `AudioPlayerBar`，显示当前播放的封面、曲名、进度条、停止按钮
- **进度拖动**: 通过 `useAudio` composable 的 `seek(percent)` 方法实现拖动跳转
- **头部小球动画**: 播放期间头部三个圆球循环弹跳，空闲时 60s 周期性触发

#### 2.4.3 全局音频播放器 (AudioPlayerBar)

```
┌──────────────────────────────────────────────────────────────┐
│ [封面] 曲名 - 艺人          ━━━━━●━━━━━━━  [■ 停止]        │
└──────────────────────────────────────────────────────────────┘
  ↑ 固定在视口底部 (position: fixed, z-40)
```

特性：
- **fixed 定位** — 脱离文档流，不随页面滚动
- **滑入/滑出动画** — 播放时从底部滑入，停止时滑出
- **进度条** — 已播/未播双色显示，支持拖动 seek
- **曲目解析** — 从 style name 自动拆分曲名与艺人

---

### 2.5 收藏夹

#### 2.5.1 功能说明

| 功能 | 说明 |
|------|------|
| **多收藏夹** | 用户可创建多个收藏夹（如"EDM 常用"、"复古风格"） |
| **入口位置** | 顶部导航栏 |
| **操作** | 创建收藏夹、重命名、删除、查看收藏夹内容 |

#### 2.5.2 收藏夹字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识符 |
| `name` | string | 收藏夹名称 |
| `style_ids` | string[] | 包含的风格卡片 ID 列表 |
| `created_at` | datetime | 创建时间 |

---

### 2.6 热门标签

#### 2.6.1 统计逻辑

- **热门定义**: 基于用户**复制次数**统计
- 每次用户复制某个 Tag，该 Tag 的计数 +1
- 展示复制次数最多的 Top N 个标签

#### 2.6.2 展示位置

- **位置**: 右侧内容区顶部，搜索框附近
- **样式**: 可点击的标签云，点击后自动填入搜索框

---

### 2.7 搜索与筛选

#### 2.7.1 搜索功能

| 特性 | 说明 |
|------|------|
| **搜索范围** | 全字段搜索（name、tags、description、genre_path、bpm_range） |
| **实时搜索** | 输入时实时过滤，无需按回车 |
| **高亮匹配** | 搜索结果中高亮匹配的关键词（可选） |

#### 2.7.2 筛选功能

| 筛选维度 | 说明 |
|----------|------|
| **流派筛选** | 点击左侧时间线的流派节点 |
| **收藏筛选** | 只显示已收藏的卡片 |
| **组合筛选** | 流派 + 搜索关键词可叠加 |

---

### 2.8 数据导入/导出

#### 2.8.1 导出功能

| 特性 | 说明 |
|------|------|
| **格式** | JSON |
| **范围选择** | 可选择导出：全部数据 / 指定年代 / 指定流派 / 收藏夹 |
| **包含内容** | 风格卡片数据、流派树结构、收藏夹信息 |

#### 2.8.2 导入功能

| 特性 | 说明 |
|------|------|
| **格式** | JSON |
| **冲突处理** | 用户可选择：覆盖现有数据 / 合并（相同 ID 覆盖，新 ID 添加） |
| **校验** | 导入前校验 JSON 格式和必填字段 |

---

## 3. 数据结构设计

### 3.1 SQLite 数据库 Schema

```sql
-- 流派树表
CREATE TABLE genres (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT,
    level INTEGER NOT NULL DEFAULT 1,  -- 层级: 1, 2, 3
    sort_order INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    era_prompt TEXT,  -- 该年代/流派的通用提示词
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES genres(id) ON DELETE CASCADE
);

-- 风格卡片表
CREATE TABLE styles (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tags TEXT NOT NULL,  -- JSON 数组存储: ["tag1", "tag2"]
    genre_id TEXT,
    description TEXT,
    bpm_range TEXT,
    audio_type TEXT CHECK(audio_type IN ('local', 'url')),
    audio_source TEXT,
    reference_url TEXT,
    copy_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE SET NULL
);

-- 收藏夹表
CREATE TABLE folders (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 收藏夹-风格关联表 (多对多)
CREATE TABLE folder_styles (
    folder_id TEXT NOT NULL,
    style_id TEXT NOT NULL,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (folder_id, style_id),
    FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE,
    FOREIGN KEY (style_id) REFERENCES styles(id) ON DELETE CASCADE
);

-- 标签统计表 (用于热门标签)
CREATE TABLE tag_stats (
    tag TEXT PRIMARY KEY,
    copy_count INTEGER DEFAULT 0,
    last_copied_at DATETIME
);

-- 索引优化
CREATE INDEX idx_styles_genre ON styles(genre_id);
CREATE INDEX idx_styles_name ON styles(name);
CREATE INDEX idx_genres_parent ON genres(parent_id);
CREATE INDEX idx_tag_stats_count ON tag_stats(copy_count DESC);
```

### 3.2 JSON 导出格式

```json
{
  "version": "1.0",
  "exported_at": "2026-01-19T12:00:00Z",
  "data": {
    "genres": [
      {
        "id": "genre_1950s",
        "name": "1950s",
        "parent_id": null,
        "level": 1,
        "sort_order": 1,
        "description": "Rockabilly & Doo-Wop 时代",
        "era_prompt": "1950s style, mono recording, slapback delay on vocals"
      },
      {
        "id": "genre_rockabilly",
        "name": "Rockabilly",
        "parent_id": "genre_1950s",
        "level": 2,
        "sort_order": 1,
        "description": "Blues 遇见 Country，摇滚乐的诞生"
      }
    ],
    "styles": [
      {
        "id": "style_001",
        "name": "Doo-Wop Romance",
        "tags": ["doo-wop", "50s ballad", "finger snaps", "male quartet", "romantic"],
        "genre_id": "genre_1950s",
        "description": "经典的 50 年代浪漫情歌风格",
        "bpm_range": "60-80",
        "audio_type": "local",
        "audio_source": "/audio/1950s/doowop_romance.mp3",
        "reference_url": "https://everynoise.com/doowop",
        "copy_count": 42
      }
    ],
    "folders": [
      {
        "id": "folder_001",
        "name": "常用风格",
        "style_ids": ["style_001", "style_002"]
      }
    ]
  }
}
```

### 3.3 初始流派树数据

基于原型文件，初始流派树结构如下：

```
1950s (Rockabilly & Doo-Wop)
├── Doo-Wop
├── Rockabilly
└── Early Rock & Roll

1960s (Psychedelia & Motown)
├── British Invasion
├── Psychedelic Rock
├── Motown Soul
└── Folk Rock

1970s (Funk, Disco & Punk)
├── Disco
├── Funk
├── Hard Rock
├── Punk Rock
│   └── Ramones Style
└── Yacht Rock

1980s (Synthpop & Hair Metal)
├── Synthwave / Retrowave
├── New Wave
├── Post-Punk / Goth
├── Hair Metal
└── City Pop (J-Pop)

1990s (Hip-Hop & Grunge)
├── Boom Bap Hip-Hop
├── Grunge / Alternative
├── Eurodance
├── Britpop
└── Trip-Hop

2000s (Pop-Punk & R&B)
├── Pop Punk
├── Nu Metal
├── Millennium R&B
├── Emo
└── Crunk

2010s (EDM & Trap)
├── Big Room EDM
├── Trap
├── Dubstep
├── Tropical House
└── Lo-Fi Hip Hop

2020s (Hyperpop & Viral)
├── Hyperpop
├── Drift Phonk
├── Bedroom Pop
└── TikTok Viral
```

---

## 4. 技术架构

### 4.1 技术栈选型

| 层级 | 技术选型 | 理由 |
|------|----------|------|
| **前端框架** | Vue 3 + Vite | 快速启动、优秀的 HMR、适合仪表盘类应用 |
| **UI 框架** | Tailwind CSS | 原子化 CSS，快速迭代 UI，与原型风格兼容 |
| **状态管理** | Pinia | Vue 3 官方推荐，轻量简洁 |
| **后端框架** | Python FastAPI | 高性能异步框架，自动生成 API 文档 |
| **数据库** | SQLite | 轻量级、零配置、单文件存储，适合本地工具 |
| **ORM** | SQLAlchemy 2.0 | Python 生态最成熟的 ORM |
| **音频存储** | 本地文件系统 | SQLite 存储路径，文件存于 `/storage/audio/` |

### 4.2 系统架构图

#### 生产模式（单端口托管）

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户浏览器                               │
│               http://localhost:8000 或 http://<LAN_IP>:8000     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP (单端口 8000)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
│                   http://0.0.0.0:8000                           │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  静态文件中间件 (StaticFiles)                              │   │
│   │  托管 frontend/dist/ → SPA HTML + JS + CSS              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │   Routers   │  │  Services   │  │    Models   │            │
│   │  (API层)    │  │  (业务逻辑)  │  │  (数据模型)  │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ SQLAlchemy
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        SQLite                                   │
│                   /data/music_prompt_box.db                     │
└─────────────────────────────────────────────────────────────────┘
```

#### 开发模式（双进程热重载）

```
浏览器 → Vite Dev Server (:5173) ──proxy /api──→ FastAPI (:8000) → SQLite
```

> 开发模式下前端通过 `vite.config.ts` 配置 `/api` 代理转发到后端；生产模式下单端口对外，无需代理。

### 4.3 开发环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Node.js | >= 18.x | 前端构建 |
| Python | >= 3.10 | 后端运行 |
| pnpm | >= 8.x | 包管理器（推荐） |
| pip / poetry | 最新版 | Python 包管理 |

---

## 5. 目录结构

```
music_prompt_box/
├── frontend/                    # 前端项目
│   ├── dist/                    # Vite 构建产物（由后端托管）
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/              # 静态资源
│   │   │   └── styles/
│   │   │       └── main.css     # Tailwind 入口
│   │   ├── components/          # Vue 组件
│   │   │   ├── layout/
│   │   │   │   ├── AppHeader.vue      # 顶部标题 + 小球动画
│   │   │   │   ├── AppSidebar.vue     # 流派时间线导航
│   │   │   │   └── AppMain.vue        # 主内容区容器
│   │   │   ├── cards/
│   │   │   │   ├── StyleCard.vue      # 单张风格卡片
│   │   │   │   ├── StyleGrid.vue      # 卡片网格
│   │   │   │   └── StyleFormModal.vue # 添加/编辑表单
│   │   │   ├── tags/
│   │   │   │   ├── TagPill.vue        # 单个标签（点击复制）
│   │   │   │   └── HotTags.vue        # 热门标签云
│   │   │   ├── folders/
│   │   │   │   └── FolderList.vue     # 收藏夹
│   │   │   └── common/
│   │   │       ├── AudioPlayerBar.vue # 全局底部播放控制栏
│   │   │       ├── SearchBox.vue
│   │   │       ├── ConfirmModal.vue
│   │   │       └── Toast.vue
│   │   ├── composables/         # 组合式函数
│   │   │   ├── useAudio.ts      # 全局音频状态 + 播放控制 + seek
│   │   │   └── useClipboard.ts  # 剪贴板（SecureContext 降级）
│   │   ├── stores/              # Pinia 状态管理
│   │   │   ├── genres.ts
│   │   │   ├── styles.ts
│   │   │   ├── folders.ts
│   │   │   └── tags.ts
│   │   ├── api/                 # API 请求封装
│   │   │   └── client.ts        # Axios 实例（baseURL=/api）
│   │   ├── types/               # TypeScript 类型定义
│   │   │   └── index.ts
│   │   ├── App.vue              # 根组件（挂载 AudioPlayerBar）
│   │   └── main.ts
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/                     # 后端项目
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 入口 + SPA 路由 + 静态文件托管
│   │   ├── config.py            # 配置（含 FRONTEND_DIST_PATH）
│   │   ├── database.py          # 异步 SQLAlchemy 引擎
│   │   ├── models/              # SQLAlchemy 模型
│   │   │   ├── genre.py
│   │   │   ├── style.py
│   │   │   ├── folder.py
│   │   │   └── tag_stat.py
│   │   ├── schemas/             # Pydantic 模式
│   │   │   ├── genre.py
│   │   │   ├── style.py
│   │   │   └── folder.py
│   │   ├── routers/             # API 路由
│   │   │   ├── genres.py
│   │   │   ├── styles.py
│   │   │   ├── folders.py
│   │   │   ├── tags.py
│   │   │   ├── itunes.py        # iTunes Search API 代理
│   │   │   └── data.py          # 导入/导出
│   │   └── services/            # 业务逻辑
│   │       ├── genre_service.py
│   │       ├── style_service.py
│   │       └── export_service.py
│   ├── data/
│   │   └── music_prompt_box.db  # SQLite 数据库
│   ├── seeds/
│   │   ├── initial_data.json    # 初始种子数据
│   │   ├── seed_db.py           # 初始化脚本
│   │   └── add_styles.py        # 补充风格 + iTunes 音频匹配
│   ├── storage/audio/           # 本地音频文件存储
│   ├── requirements.txt
│   └── venv/
│
├── docs/
│   └── music-embed-research.md
├── .gitignore
├── README.md
└── development.md               # 本文档
```

---

## 6. 交互设计

### 6.1 页面布局

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ┌─ 顶部导航栏 ─────────────────────────────────────────────────────┐   │
│  │ [Logo] Music Prompt Box    [收藏夹▼] [导入] [导出]    [+ 添加风格] │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─ 左侧栏 (280px) ─┐  ┌─ 主内容区 ────────────────────────────────┐   │
│  │                   │  │                                           │   │
│  │  流派时间线        │  │  ┌─ 工具栏 ─────────────────────────┐   │   │
│  │                   │  │  │ [搜索框]  [热门: tag1 tag2 tag3]  │   │   │
│  │  ▼ 1950s          │  │  └───────────────────────────────────┘   │   │
│  │    ├─ Doo-Wop     │  │                                           │   │
│  │    └─ Rockabilly  │  │  ┌─ 卡片网格 ────────────────────────┐   │   │
│  │                   │  │  │                                     │   │   │
│  │  ▼ 1960s          │  │  │  [Card] [Card] [Card] [Card]       │   │   │
│  │    ├─ Psychedelic │  │  │                                     │   │   │
│  │    ├─ Motown      │  │  │  [Card] [Card] [Card] [Card]       │   │   │
│  │    └─ British     │  │  │                                     │   │   │
│  │                   │  │  │  [Card] [Card] [Card] ...          │   │   │
│  │  ▶ 1970s          │  │  │                                     │   │   │
│  │  ▶ 1980s          │  │  └─────────────────────────────────────┘   │   │
│  │  ...              │  │                                           │   │
│  └───────────────────┘  └───────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### 6.2 风格卡片设计

```
┌─────────────────────────────────────────┐
│  [1950s]                    [♡] [✎] [🗑] │  <- 年代标签 + 操作按钮
├─────────────────────────────────────────┤
│                                         │
│  Doo-Wop Romance              [▶ 播放]  │  <- 名称 + 播放按钮
│                                         │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │doo- │ │50s  │ │finger│ │male │       │  <- Tags (可点击复制)
│  │wop  │ │ballad│ │snaps │ │quartet│    │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
│                                         │
│  经典的 50 年代浪漫情歌风格...           │  <- 描述 (可选)
│                                         │
├─────────────────────────────────────────┤
│  [📋 复制全部 Tags]                      │  <- 一键复制
└─────────────────────────────────────────┘
```

### 6.3 表单设计（添加/编辑风格）

```
┌─────────────────────────────────────────────────────┐
│  添加新风格                                    [✕]  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  风格名称 *                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │ Synthwave                                    │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  风格标签 * (逗号分隔)                              │
│  ┌─────────────────────────────────────────────┐   │
│  │ retrowave, analog synth, 80s, neon          │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  所属流派                                           │
│  ┌─────────────────────────────────────────────┐   │
│  │ 1980s / Synthwave                        ▼  │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  风格描述                                           │
│  ┌─────────────────────────────────────────────┐   │
│  │ 80年代复古电子风格，特征是...                │   │
│  │                                              │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  BPM 范围                                          │
│  ┌─────────────────────────────────────────────┐   │
│  │ 100-120                                      │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  示例音频                                           │
│  ○ 上传本地文件   ● 外部链接                        │
│  ┌─────────────────────────────────────────────┐   │
│  │ https://example.com/synthwave.mp3           │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  参考来源 URL                                       │
│  ┌─────────────────────────────────────────────┐   │
│  │ https://everynoise.com/synthwave            │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
├─────────────────────────────────────────────────────┤
│                          [取消]  [保存]             │
└─────────────────────────────────────────────────────┘
```

### 6.4 UI 配色方案

沿用原型的暗色主题：

```css
:root {
  /* 背景色 */
  --bg-color: #09090b;
  --sidebar-bg: #101012;
  --card-bg: #18181b;
  
  /* 边框 */
  --border-color: #27272a;
  
  /* 强调色 (紫色) */
  --accent-color: #8b5cf6;
  --accent-glow: rgba(139, 92, 246, 0.3);
  
  /* 文字 */
  --text-main: #e4e4e7;
  --text-sub: #a1a1aa;
  
  /* 语义色 */
  --success: #22c55e;
  --warning: #f59e0b;
  --danger: #ef4444;
}
```

---

## 7. API 接口设计

### 7.1 接口总览

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| **流派** | GET | `/api/genres` | 获取流派树 |
| | POST | `/api/genres` | 创建流派 |
| | PUT | `/api/genres/{id}` | 更新流派 |
| | DELETE | `/api/genres/{id}` | 删除流派 |
| **风格** | GET | `/api/styles` | 获取风格列表（支持筛选、搜索、分页） |
| | GET | `/api/styles/{id}` | 获取单个风格详情 |
| | POST | `/api/styles` | 创建风格 |
| | PUT | `/api/styles/{id}` | 更新风格 |
| | DELETE | `/api/styles/{id}` | 删除风格 |
| | POST | `/api/styles/{id}/copy` | 记录复制行为（更新统计） |
| **收藏夹** | GET | `/api/folders` | 获取收藏夹列表 |
| | POST | `/api/folders` | 创建收藏夹 |
| | PUT | `/api/folders/{id}` | 更新收藏夹（重命名） |
| | DELETE | `/api/folders/{id}` | 删除收藏夹 |
| | POST | `/api/folders/{id}/styles` | 添加风格到收藏夹 |
| | DELETE | `/api/folders/{id}/styles/{style_id}` | 从收藏夹移除风格 |
| **标签** | GET | `/api/tags/hot` | 获取热门标签 |
| | POST | `/api/tags/copy` | 记录标签复制行为 |
| **数据** | GET | `/api/data/export` | 导出数据 |
| | POST | `/api/data/import` | 导入数据 |
| **文件** | POST | `/api/upload/audio` | 上传音频文件 |
| | GET | `/storage/audio/{path}` | 访问音频文件 |

### 7.2 核心接口详情

#### 7.2.1 获取风格列表

```http
GET /api/styles?genre_id=xxx&search=xxx&folder_id=xxx&page=1&size=20
```

**Query Parameters:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `genre_id` | string | 否 | 按流派筛选（包含子流派） |
| `search` | string | 否 | 全字段搜索关键词 |
| `folder_id` | string | 否 | 按收藏夹筛选 |
| `page` | int | 否 | 页码，默认 1 |
| `size` | int | 否 | 每页数量，默认 20 |

**Response:**

```json
{
  "total": 100,
  "page": 1,
  "size": 20,
  "items": [
    {
      "id": "style_001",
      "name": "Doo-Wop Romance",
      "tags": ["doo-wop", "50s ballad", "finger snaps"],
      "genre_id": "genre_1950s",
      "genre_name": "1950s",
      "description": "经典的 50 年代浪漫情歌风格",
      "bpm_range": "60-80",
      "audio_type": "local",
      "audio_source": "/storage/audio/1950s/doowop.mp3",
      "reference_url": "https://everynoise.com/doowop",
      "copy_count": 42,
      "is_favorited": true,
      "created_at": "2026-01-19T12:00:00Z"
    }
  ]
}
```

#### 7.2.2 创建风格

```http
POST /api/styles
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Synthwave",
  "tags": ["retrowave", "analog synth", "80s", "neon"],
  "genre_id": "genre_1980s_synthwave",
  "description": "80年代复古电子风格",
  "bpm_range": "100-120",
  "audio_type": "url",
  "audio_source": "https://example.com/synthwave.mp3",
  "reference_url": "https://everynoise.com/synthwave"
}
```

#### 7.2.3 导出数据

```http
GET /api/data/export?scope=all&genre_id=xxx&folder_id=xxx
```

**Query Parameters:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `scope` | string | 否 | 导出范围：`all` / `genre` / `folder` |
| `genre_id` | string | 否 | 当 scope=genre 时必填 |
| `folder_id` | string | 否 | 当 scope=folder 时必填 |

#### 7.2.4 导入数据

```http
POST /api/data/import?mode=merge
Content-Type: application/json
```

**Query Parameters:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mode` | string | 是 | 导入模式：`overwrite` / `merge` |

---

## 8. 开发计划

### 8.1 里程碑规划

| 阶段 | 目标 | 预计时间 |
|------|------|----------|
| **M1: 基础框架** | 前后端项目搭建、数据库设计、基础 CRUD | 1 周 |
| **M2: 核心功能** | 流派树、风格卡片展示、搜索筛选、复制功能 | 1.5 周 |
| **M3: 音频播放** | 本地上传、外链播放、互斥播放逻辑 | 0.5 周 |
| **M4: 收藏夹** | 多收藏夹管理、添加/移除风格 | 0.5 周 |
| **M5: 热门标签** | 复制统计、热门标签展示 | 0.5 周 |
| **M6: 数据管理** | 导入/导出功能 | 0.5 周 |
| **M7: 优化打磨** | 交互细节、错误处理、性能优化 | 0.5 周 |

### 8.2 M1 详细任务

```markdown
## M1: 基础框架 (Week 1)

### 后端
- [ ] 初始化 FastAPI 项目结构
- [ ] 配置 SQLite + SQLAlchemy
- [ ] 创建数据库模型 (Genre, Style, Folder, TagStat)
- [ ] 实现基础 CRUD API
- [ ] 配置 CORS
- [ ] 编写初始化数据脚本

### 前端
- [ ] 初始化 Vite + Vue 3 + TypeScript 项目
- [ ] 配置 Tailwind CSS
- [ ] 设置 Pinia 状态管理
- [ ] 封装 Axios API 客户端
- [ ] 创建基础布局组件 (Header, Sidebar, Main)
- [ ] 定义 TypeScript 类型
```

### 8.3 开发规范

#### 8.3.1 Git 提交规范

```
<type>(<scope>): <subject>

Types:
- feat: 新功能
- fix: Bug 修复
- docs: 文档更新
- style: 代码格式（不影响功能）
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

Examples:
- feat(styles): add copy all tags button
- fix(audio): fix playback mutex logic
- docs(readme): update installation guide
```

#### 8.3.2 代码风格

| 语言 | 规范 |
|------|------|
| TypeScript | ESLint + Prettier |
| Python | Black + isort + Ruff |
| SQL | 大写关键字，小写表名/字段名 |

---

## 9. 附录

### 9.1 参考资源

| 资源 | 链接 | 用途 |
|------|------|------|
| Every Noise at Once | https://everynoise.com | 流派参考、听感校准 |
| Suno AI | https://suno.com | 目标生成平台 |
| Rate Your Music | https://rateyourmusic.com/genres/ | 流派分类参考 |
| Music Genre List | https://www.musicgenreslist.com | 流派树结构参考 |

### 9.2 原型文件

- 原型 HTML: `pop-music-cards.html`
- 原型数据结构参考: 见原型文件中的 `timelineData` 和 `assetData`

### 9.3 术语表

| 术语 | 说明 |
|------|------|
| **Style Prompt** | 风格提示词，用于 AI 音乐生成 |
| **Genre** | 音乐流派/年代分类 |
| **Tag** | 风格标签，通常是单个描述词 |
| **Era Prompt** | 年代整体风格提示词（如"1980s style, gated reverb..."） |
| **校准 (Calibration)** | 确保提示词生成的音乐与预期听感一致的过程 |

---

## 更新日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-01-19 | 初始版本，完整需求定义 |
| v1.1 | 2026-05-18 | 生产架构变更 + 多项功能增强 |

### v1.1 变更明细 (2026-05-18)

**架构变更**
- 前后端双进程 → FastAPI 单端口 (8000) 生产托管，`StaticFiles` 中间件托管 `frontend/dist/`
- 后端绑定 `0.0.0.0:8000`，支持局域网直接访问
- 移除 Vite 前端服务器对生产环境的依赖

**新增功能**
- 全局音频播放控制栏 (`AudioPlayerBar`)：fixed 定位、进度拖动、停止按钮、滑入滑出动画
- `useAudio` composable 扩展：暴露 `currentTime`、`duration`、`currentStyle`、`seek()` 方法
- 头部小球弹跳动画：播放时循环，空闲时 60s 周期触发，物理弹跳 keyframes
- iTunes Search API 代理路由 (`/api/itunes/search`)
- 剪贴板 HTTP 降级：`window.isSecureContext === false` 时自动回退 `document.execCommand('copy')`

**数据补充**
- 新增 5 个子流派 (Funk, New Wave, Trap, Bedroom Pop, Punk Rock) 共 20 张卡片
- 全部卡片通过 iTunes API 匹配 30s 试听片段
- 当前总计：40 张风格卡片，25 个子流派

**Bug 修复**
- 修复播放器随页面滚动而非固定底部的问题：从 `AppMain` 内 absolute 改为 `App.vue` 根层级 fixed
- 修复 CSS 动画同名 class 切换不重启问题：拆分 DOM 分支 (`v-if/v-else`) + 独立类名
