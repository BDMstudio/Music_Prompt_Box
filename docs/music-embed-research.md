# 音乐外链嵌入方案调研报告

> **项目**: Music Prompt Box  
> **需求**: 风格卡片的"听觉校准"——通过外链嵌入 15-30s 片段试听  
> **偏好**: 外链挂载（iframe/SDK/直接音频URL），不自托管音频文件  
> **调研日期**: 2026-05-14

---

## 一、总览对比表

| 平台 | iframe嵌入 | JS SDK | 免费试听 | 片段时长 | 需认证 | 中国可用 | 官方文档 |
|------|-----------|--------|---------|---------|--------|---------|---------|
| **Spotify** | ✅ | ✅ Web API | ✅ | 30s | OAuth (Web API) / 无(iframe) | ❌ 需VPN | ✅ |
| **Apple Music** | ⚠️ 有限 | ✅ MusicKit JS | ✅ | 30s | Apple Dev Token ($99/yr) | ❌ 需VPN | ✅ |
| **YouTube** | ✅ | ✅ IFrame API | ✅ | 完整 | API Key (可选) | ❌ 需VPN | ✅ |
| **SoundCloud** | ✅ oEmbed | ✅ Widget API | ✅ | 完整(免费曲目) | 无(嵌入) / Client ID(API) | ⚠️ 不稳定 | ✅ |
| **Deezer** | ✅ | ✅ Player SDK | ✅ | 30s | App ID (免费注册) | ⚠️ 未正式入华 | ✅ |
| **Jamendo** | ❌ | REST API | ✅ CC全曲 | 完整 | client_id (免费) | ✅ | ✅ |
| **Audius** | ❌ | REST API | ✅ 全曲开放 | 完整 | 无 | ⚠️ 可能需VPN | ✅ |
| **Bandcamp** | ✅ | ❌ | ⚠️ 部分曲目 | 视曲目 | 无 | ✅ | ⚠️ 有限 |
| **网易云音乐** | ✅ outchain | ❌ | ⚠️ 需合作 | 完整 | 无(iframe) / 合作(API) | ✅ | ⚠️ 半官方 |
| **QQ音乐** | ❌ | ❌ | ⚠️ 非官方 | 完整 | Cookie/非官方 | ✅ | ❌ 无官方 |
| **iTunes Search** | ❌ | REST API | ✅ | 30s | 无 | ✅ | ✅ |

---

## 二、各平台详细分析

### 1. Spotify

**嵌入方式 (iframe)**

最简单的方案，无需 API Key：

```html
<iframe 
  src="https://open.spotify.com/embed/track/6rqhFgbbKwnb9MLmUQDhG6?utm_source=generator&theme=0" 
  width="100%" height="80" frameborder="0" 
  allowtransparency="true" allow="encrypted-media">
</iframe>
```

- 未登录用户：可播放 30s 预览片段
- 登录 Spotify 账户：可播放完整曲目
- 支持紧凑模式 (height=80) 和大模式 (height=352)
- 支持深色/浅色主题

**Web API (preview_url)**

```bash
GET https://api.spotify.com/v1/tracks/{id}
Authorization: Bearer {token}
```

- 返回 `preview_url` 字段 → 指向 30s MP3 文件
- ⚠️ **关键问题**：preview_url 不稳定——部分曲目返回 `null`，且 URL 会过期
- 需要 OAuth：推荐用 Client Credentials Flow（服务端），无需用户授权
- 免费配额：未明确公布，默认速率限制约 180 请求/30s
- 注册：https://developer.spotify.com/dashboard （免费，不需信用卡）

**中国可用性**: ❌ open.spotify.com 被墙，iframe 嵌入在国内无法加载

**文档**: https://developer.spotify.com/documentation/embeds  
**文档**: https://developer.spotify.com/documentation/web-api

**推荐指数**: ⭐⭐⭐⭐ (海外场景首选，iframe 嵌入最简单)

---

### 2. Apple Music

**嵌入方式: MusicKit JS**

```html
<script src="https://js-cdn.music.apple.com/musickit/v3/musickit.js"></script>
```

```javascript
MusicKit.configure({
  developerToken: 'YOUR_DEVELOPER_TOKEN',  // JWT
  app: { name: 'Music Prompt Box' }
});

// 播放预览
const music = MusicKit.getInstance();
music.setQueue({ song: 'TRACK_ID' });
music.play();  // 未订阅用户自动播放 30s 预览
```

- 未订阅用户：自动获得 30s 预览
- 订阅用户：播放完整曲目
- 需要 Apple Developer Program 会员 ($99/年) 来生成 Developer Token (JWT)
- ⚠️ **无简单 iframe 嵌入**，必须用 MusicKit JS SDK
- 曲目库庞大，古典/爵士/世界音乐覆盖特别好

**中国可用性**: ❌ Apple Music 中国区存在但 API 调用需经 apple.com 域名，部分被墙

**文档**: https://developer.apple.com/documentation/musickitjs

**推荐指数**: ⭐⭐ (门槛高，需付费开发者账户，且无简单 iframe)

---

### 3. YouTube

**嵌入方式: IFrame Player API**

```html
<div id="yt-player"></div>
<script src="https://www.youtube.com/iframe_api"></script>
<script>
  const player = new YT.Player('yt-player', {
    height: '0',        // 隐藏视频画面
    width: '0',
    videoId: 'VIDEO_ID',
    playerVars: { 
      start: 30,         // 从30秒开始
      end: 60            // 到60秒结束（30s片段）
    }
  });
</script>
```

- 完全免费，无需 API Key 即可嵌入播放
- YouTube Data API v3 需 API Key（免费层：10,000 单位/天，足够搜索曲目）
- 支持程序化控制：play(), pause(), seekTo(), setVolume()
- 事件回调：onReady, onStateChange
- 曲目覆盖面极广——几乎所有音乐风格都有上传
- ⚠️ TOS 限制：不允许分离音视频（不能只提取音频URL）
- ⚠️ 视频区域隐藏需要 CSS hack（height=0 或 position offscreen）
- ⚠️ 部分视频因版权限制可能禁止嵌入

**中国可用性**: ❌ youtube.com 被墙

**文档**: https://developers.google.com/youtube/iframe_api_reference

**推荐指数**: ⭐⭐⭐⭐⭐ (海外场景最灵活，API 最成熟，但中国不可用)

---

### 4. SoundCloud

**嵌入方式: oEmbed + Widget API**

```html
<iframe 
  id="sc-widget" 
  src="https://w.soundcloud.com/player/?url=https%3A//soundcloud.com/artist/track&color=%23ff5500&auto_play=false&hide_related=true&show_comments=false&show_user=false&show_reposts=false&visual=false" 
  width="100%" height="120" scrolling="no" frameborder="no">
</iframe>

<script src="https://w.soundcloud.com/player/api.js"></script>
<script>
  const widget = SC.Widget(document.getElementById('sc-widget'));
  widget.bind(SC.Widget.Events.READY, () => widget.play());
</script>
```

- oEmbed 端点：`https://soundcloud.com/oembed?url={track_url}&format=json`
  - 返回可直接使用的 iframe HTML
- Widget JS API：完整播放控制 + 事件回调
- 免费上传的曲目可完整播放
- SoundCloud Go+ 付费曲目可能无法嵌入播放
- 独立音乐人 / 电子音乐覆盖特别好
- 注册开发者获取 Client ID：https://soundcloud.com/developers （免费）

**中国可用性**: ⚠️ w.soundcloud.com 偶尔不稳定，部分地区可能需 VPN

**文档**: https://developers.soundcloud.com/docs/api/html5-widget

**推荐指数**: ⭐⭐⭐⭐ (独立音乐/电子音乐首选，Widget API 成熟)

---

### 5. Deezer

**嵌入方式: iframe + Player SDK**

iframe 嵌入：
```html
<iframe 
  src="https://www.deezer.com/plugins/player?format=square&type=tracks&id=3135556&color=0070C0&playlist=false&layout=dark&size=small&app_id=YOUR_APP_ID" 
  width="300" height="80" scrolling="no" frameborder="0">
</iframe>
```

Player SDK：
```html
<script src="https://e-cdn-files.dzcdn.net/js/min/dz.js"></script>
<script>
  DZ.init({
    appId: 'YOUR_APP_ID',
    channelUrl: 'https://yourdomain.com/channel.html',
    player: { container: 'player', format: 'square' }
  });
  DZ.player.playTracks([3135556]);  // 30s preview for free users
</script>
```

**REST API (预览 URL)**:
```bash
GET https://api.deezer.com/track/3135556
# 返回: { "preview": "https://cdnt-preview.dzcdn.net/...", ... }
```

- ⭐ **关键优势**: REST API 无需认证即可获取 30s 预览 MP3 URL
- preview URL 指向直接的 MP3 文件，可用 HTML5 Audio 播放
- 注册 App：https://developers.deezer.com （免费，不需信用卡）
- 30s 预览免费；完整播放需 Deezer Premium 订阅
- 曲目库覆盖全球主流音乐
- 支持 CORS（API 响应允许跨域）

**中国可用性**: ⚠️ Deezer 未正式进入中国，但 API 端点 (api.deezer.com) 目前可直连

**文档**: https://developers.deezer.com/api  
**文档**: https://developers.deezer.com/sdk/js

**推荐指数**: ⭐⭐⭐⭐⭐ (API 最友好——免费、无认证、直接 MP3 URL、30s 预览)

---

### 6. Jamendo

**嵌入方式: REST API (无官方 embed widget)**

```bash
# 搜索曲目
GET https://api.jamendo.com/v3.0/tracks/?client_id=YOUR_ID&namesearch=synthwave&limit=10

# 获取音频流
GET https://api.jamendo.com/v3.0/tracks/file?client_id=YOUR_ID&id=TRACK_ID

# 返回直接 MP3 流 URL，可用 HTML5 <audio> 播放
```

- 所有音乐均为 **Creative Commons 授权**，完全合法免费
- 全曲播放，不限时长
- 注册获取 client_id：https://developer.jamendo.com （免费，不需信用卡）
- ⚠️ 曲目库较小，主要是独立音乐人作品
- ⚠️ 无官方 iframe embed widget，需自建播放器 UI
- 对特定风格（电子、独立、氛围音乐）覆盖尚可

**中国可用性**: ✅ api.jamendo.com 可直连

**文档**: https://developer.jamendo.com/v3.0

**推荐指数**: ⭐⭐⭐ (CC免费合法，但曲目库有限，无现成embed组件)

---

### 7. Audius

**嵌入方式: REST API**

```bash
# 搜索曲目
GET https://discoveryprovider.audius.co/v1/tracks/search?query=synthwave&app_name=MusicPromptBox

# 流式播放
GET https://discoveryprovider.audius.co/v1/tracks/{id}/stream?app_name=MusicPromptBox
```

- 去中心化音乐平台，开放 API
- 全曲播放，无需认证（只需 app_name 参数）
- 无请求费用，限制宽松
- 独立音乐人为主，电子/实验音乐较多
- ⚠️ 无官方 iframe embed

**中国可用性**: ⚠️ 去中心化节点可能需要 VPN

**文档**: https://docs.audius.co

**推荐指数**: ⭐⭐⭐ (API 极简，但曲目偏小众，中国可达性不确定)

---

### 8. Bandcamp

**嵌入方式: iframe**

```html
<iframe 
  src="https://bandcamp.com/EmbeddedPlayer/track=TRACK_ID/size=small/bgColor=333333/linkColor=0f91ff/tracklist=false/transparent=true/" 
  width="300" height="42" frameborder="0">
</iframe>
```

- 可嵌入专辑或单曲
- 紧凑模式 (size=small, height=42px) 非常适合卡片场景
- 独立音乐人 / 实验音乐覆盖极佳
- 免费 Bandcamp Friday 曲目 + 付费曲目均可嵌入播放
- ⚠️ 无 JS Player API（无法程序化控制播放）
- ⚠️ 无官方目录搜索 API（需手动获取 track ID）
- ⚠️ 部分专辑仅播放片段（由艺术家设定）

**中国可用性**: ✅ bandcamp.com 可直连

**文档**: 无官方开发者文档，嵌入参数通过社区发现

**推荐指数**: ⭐⭐⭐ (iframe 最简单，但缺乏 API 支持，无法程序化搜索/控制)

---

### 9. 网易云音乐

**嵌入方式: outchain iframe**

```html
<iframe 
  src="https://music.163.com/outchain/player?type=2&id=SONG_ID&auto=0&height=66" 
  width="330" height="66" frameborder="0">
</iframe>
```

- type: 0=歌单, 1=单曲, 2=专辑
- 中国市场覆盖最好的平台
- ⚠️ 无官方 JS Player API
- ⚠️ 完整 API 需商务合作
- ⚠️ 存在大量非官方 API 封装（GitHub: NeteaseCloudMusicApi），但违反 TOS 且不稳定
- outchain iframe 是唯一官方支持的嵌入方式

**中国可用性**: ✅ 完全可用

**文档**: https://music.163.com/#/api （有限）

**推荐指数**: ⭐⭐⭐ (中国市场必备，但 API 生态封闭)

---

### 10. QQ音乐

**嵌入方式**: ❌ 无官方嵌入方案

- 无 oEmbed、无公开 iframe embed、无官方 JS SDK
- 存在一些非公开的内部 API 端点（如 fcg_bin 系列），但不稳定且违反 TOS
- 不推荐用于正式项目

**中国可用性**: ✅

**推荐指数**: ⭐ (不推荐，无官方支持)

---

### 11. iTunes Search API (特别推荐)

**嵌入方式: REST API (返回 30s 预览 URL)**

```bash
# 搜索曲目
GET https://itunes.apple.com/search?term=synthwave&entity=song&limit=10

# 返回:
# {
#   "previewUrl": "https://audio-ssl.itunes.apple.com/itunes-assets/.../mzaf_123456789.m4a",
#   "trackName": "...",
#   "artistName": "...",
#   "artworkUrl100": "..."
# }
```

- ⭐ **关键优势**: 完全免费，无需 API Key，无需注册
- 返回 30s AAC 预览文件 URL，可直接用 HTML5 Audio 播放
- 曲目库覆盖全球主流音乐（与 Apple Music 曲库基本一致）
- 支持 CORS
- 唯一的限制是合理使用（不要滥用）
- ⚠️ 预览 URL 可能过期（通常较长，但不是永久）
- ⚠️ 无官方 iframe embed

**中国可用性**: ✅ itunes.apple.com API 可直连

**文档**: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/

**推荐指数**: ⭐⭐⭐⭐⭐ (零门槛，免费，无需认证，30s预览，覆盖面广)

---

## 三、方案推荐

### 场景 A: 面向全球用户（不考虑中国）

**首选方案**: YouTube IFrame API + Spotify iframe 嵌入

- YouTube：曲目最全，API 最成熟，免费
- Spotify iframe：紧凑美观，30s 预览，嵌入极简

**辅助方案**: Deezer API (获取 30s MP3 URL) + SoundCloud Widget

### 场景 B: 面向中国用户

**首选方案**: 网易云音乐 outchain iframe + iTunes Search API (30s预览)

- 网易云 iframe：中国市场覆盖最好，官方支持嵌入
- iTunes Search API：免费无需认证，30s 预览 URL，国内可访问

**辅助方案**: Jamendo API (CC音乐) + Bandcamp iframe (独立音乐)

### 场景 C: 全球 + 中国双覆盖（推荐实施）

**分层策略**:

```
┌────────────────────────────────────────────────────────┐
│  风格卡片 audio_source 字段                              │
│                                                        │
│  方案 1: 直接音频 URL (首选)                              │
│  ├─ iTunes Search API → 30s AAC 预览 (全球+中国)        │
│  └─ Deezer API → 30s MP3 预览 (全球，中国需验证)         │
│                                                        │
│  方案 2: iframe 嵌入 (按地区切换)                         │
│  ├─ 中国用户 → 网易云音乐 outchain iframe                │
│  └─ 海外用户 → Spotify iframe / YouTube iframe          │
│                                                        │
│  方案 3: CC 免费音乐 (补充)                              │
│  ├─ Jamendo API → CC 授权全曲 (全球+中国)               │
│  └─ Bandcamp iframe → 独立音乐 (全球+中国)               │
└────────────────────────────────────────────────────────┘
```

---

## 四、最终推荐：数据模型适配

当前 `styles` 表的 `audio_type` 字段已有 `local | url` 枚举。建议扩展为：

```sql
ALTER TABLE styles ADD COLUMN audio_platform TEXT 
  CHECK(audio_platform IN ('local', 'url', 'spotify', 'youtube', 'netease', 'soundcloud', 'deezer', 'bandcamp', 'jamendo', 'itunes'));
```

或者更灵活的方案——保持 `audio_type` 不变，新增 `audio_metadata` JSON 字段：

```sql
ALTER TABLE styles ADD COLUMN audio_metadata TEXT;  -- JSON: {"platform": "itunes", "trackId": "xyz", "previewUrl": "..."}
```

这样前端可以根据 platform 字段选择不同的播放器组件：

| platform | 播放器组件 |
|----------|-----------|
| `local` / `url` | HTML5 `<audio>` |
| `spotify` | Spotify iframe embed |
| `youtube` | YouTube IFrame API |
| `netease` | 网易云 outchain iframe |
| `soundcloud` | SoundCloud Widget |
| `deezer` | Deezer iframe 或 HTML5 `<audio>` (preview URL) |
| `bandcamp` | Bandcamp iframe |
| `jamendo` | HTML5 `<audio>` (stream URL) |
| `itunes` | HTML5 `<audio>` (preview URL) |

---

## 五、法律风险提示

1. **30s 预览片段**: Spotify/Apple/Deezer/iTunes 官方提供的 30s 预览 URL 是平台授权的，嵌入使用属于合理使用范围
2. **CC 授权音乐**: Jamendo 的 CC 音乐可合法嵌入播放，需标注署名
3. **YouTube**: TOS 禁止分离音视频，但 iframe 嵌入本身合规
4. **网易云音乐**: outchain iframe 是官方支持的嵌入方式，合规
5. **通用建议**: 不缓存/不转存第三方平台的音频文件，仅做链接引用

---

## 六、快速决策矩阵

如果你的时间有限，按这个顺序实施：

1. **iTunes Search API** — 零门槛，30s 预览，全球+中国，今天就能接入
2. **Deezer API** — 免费注册，30s MP3 URL，曲目库大
3. **网易云音乐 outchain** — 中国市场必选
4. **Spotify iframe** — 海外用户体验最好
5. **YouTube IFrame API** — 曲目最全，但中国不可用
6. **Jamendo** — CC 免费音乐，合规无忧
