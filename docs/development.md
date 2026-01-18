Suno Vibe Manager - 本地开发架构书

1. 技术选型 (Tech Stack)

为了保证开发效率和未来的可维护性，我们抛弃单文件 HTML，采用现代前端工程化方案。

核心框架: Vite + Vue 3 (或 React)。

理由: Vite 启动极快，热更新体验好；Vue 3 适合快速构建这种仪表盘应用，上手简单。

UI 框架: Tailwind CSS。

理由: 你不需要手写 CSS 类名，直接在 HTML 里写样式，非常适合快速迭代 UI。

数据管理: JSON (本地文件)。

理由: 既然是个人工具，初期不需要数据库（MySQL/Mongo）。一个 data.json 文件足够存几千条数据，而且方便 Git 版本控制。

音频托管: 本地 /public 目录 (初期) -> 对象存储 (R2/S3) (后期)。

警告: 千万不要把几百兆的 MP3 放到 Git 仓库里！ Git 是用来存代码的，不是存二进制大文件的。

2. 权威校准工作流 (The Calibration Workflow)

这是为了解决你“确保提示词正确”的核心需求。

源头确认 (Reference): * 打开 Every Noise at Once。

搜索目标风格（如 Nu-Disco）。

试听 Every Noise 提供的样本，确认这是你想要的“听感”。

Suno 验证 (Generation):

在 Suno 中输入 Nu-Disco 以及相关的描述词。

生成 4-6 个片段。

听感对齐 (Alignment):

关键步骤： 对比 Suno 生成的片段和 Every Noise 的样本。

如果听感一致，说明该 Tag 是“准确”的。

如果有偏差，说明 Suno 对该词的理解有歧义，需要增加修饰词（如 1980s, analog 等）。

入库 (Curate):

下载最符合标准的那个 Suno 片段。

将音频文件放入项目的 /public/audio/ 目录。

在 data.json 中录入数据。

3. 数据结构设计 (Data Schema)

这是整个系统的灵魂。不要随意写 JSON，要遵循规范。

// src/assets/data/styles.json

[
  {
    "id": "style_001",
    "name": "Cyberpunk Phonk",
    "era": "2020s",
    "bpm_range": "120-140", // 新增：BPM参考，这对Suno生成很重要
    "tags": [
      "drift phonk",
      "cowbell",
      "distorted 808",
      "high energy"
    ],
    "description": "适合赛博朋克驾驶场景，特征是高频的Cowbell和失真的贝斯。",
    "reference_source": "Every Noise: Drift Phonk", // 记录你的校准源
    "local_audio_path": "/audio/2020s/cyberpunk_phonk_ref.mp3", // 本地文件路径
    "suno_prompt_template": "A high energy [drift phonk] track with aggressive [cowbell] melodies and [distorted 808 bass], 130bpm" // 进阶：直接存完整的Prompt模板
  }
]


4. 目录结构规划 (Directory Structure)

建议在本地按以下结构建立文件夹：

music_prompt_box/
├── public/
│   └── audio/           # 存放音频文件，建议按年代分类
│       ├── 1980s/
│       └── 2020s/
├── src/
│   ├── assets/
│   │   └── data.json    # 你的核心数据库
│   ├── components/
│   │   ├── Timeline.vue # 左侧时间轴组件
│   │   └── StyleCard.vue# 右侧卡片组件
│   └── App.vue
├── package.json
└── vite.config.js


5. 关键功能实现思路

5.1 快速检索 (Fuzzy Search)

利用 JavaScript 的 filter 方法实现实时搜索。

// 伪代码：实现多维度搜索
const filteredStyles = styles.filter(style => {
  const searchText = query.toLowerCase();
  return (
    style.name.toLowerCase().includes(searchText) || 
    style.tags.includes(searchText) ||
    style.era === searchText
  );
});


5.2 音频播放互斥 (Audio Mutex)

确保同一时间只有一个音频在播放（避免吵闹）。

// 在 Vue/React 中维护一个全局状态
const currentPlayingId = ref(null);
const currentAudio = new Audio();

function play(url, id) {
  if (currentPlayingId.value === id) {
    currentAudio.pause(); // 再次点击则暂停
    currentPlayingId.value = null;
    return;
  }
  
  currentAudio.src = url;
  currentAudio.play();
  currentPlayingId.value = id;
}


6. 专家建议 (Pro Tips)

不要过度依赖 MP3: Suno 生成的链接其实是有时效性的（或者可能会变）。最好的方式是下载下来，或者上传到像 Cloudflare R2 这种对象存储（有免费额度），然后在 JSON 里存 CDN 链接。这能让你本地的项目体积保持轻量。

Tag 的权重: 在记录 Tag 时，建议区分 "流派(Genre)" 和 "音色(Timbre)"。

Genre: Synthwave

Timbre: Analog, Gated Reverb
Suno 对音色词的反应往往比流派词更敏感。

版本控制:
你的 styles.json 是最宝贵的资产。务必使用 Git 进行管理，这样你如果误删了某个神级 Prompt，还能找回来。