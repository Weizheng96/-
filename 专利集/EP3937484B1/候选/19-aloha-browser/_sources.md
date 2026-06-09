# 证据索引 — 19-aloha-browser

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | Phase1 search | 官方博客 | https://alohabrowser.com/posts-aloha-core-i-love-and-hate-you/ | Aloha 从未自研引擎；早期用系统 WebView，经 Chromium 底层 API 交互；引擎随 Chromium 57→130 升级 |
| 2 | Phase1 search | GitHub | https://github.com/AlohaBrowser/aloha-core | Aloha Core = "forked from Chromium" 的 web engine；渲染/JS 引擎为开源(Chromium)组件 |
| 3 | Phase1 search | 官方站/评测 | https://alohabrowser.com/ , https://www.techradar.com/pro/aloha-browser | Aloha 自有特性=广告拦截/VPN+数据压缩/adaptive tab loading/缓存/硬件加速；均非"元素级优先级+元素间预定延迟显示" |
| 4 | Phase2 fetch | 官方博客 verbatim | https://alohabrowser.com/posts-aloha-core-i-love-and-hate-you/ | "using Chromium was orders of magnitude simpler than building our own engine"；起点 WebView 重打包 AAR；无元素优先级/延迟渲染/DOM调度/省电描述 |
| 5 | Phase2 fetch | GitHub README verbatim | https://github.com/AlohaBrowser/aloha-core | README 明示 "forked from chromium/chromium"；无元素优先级/渲染延迟/DOM树调度/省电机制描述 |

## Phase 1 — react 粗筛 WebSearch（串行）
1. `Aloha Browser Aloha Core engine technology rendering`
2. `Aloha Core browser engine Chromium based fork open source GitHub`
3. `Aloha browser data saver power saving battery feature rendering`

## Phase 2 — react 深抓 WebFetch（串行）
1. `https://alohabrowser.com/posts-aloha-core-i-love-and-hate-you/`
2. `https://github.com/AlohaBrowser/aloha-core`

## 工具受限说明
无受限；WebSearch / WebFetch 均正常返回。aloha-core 源码（宣称 30GB）未逐文件抓取——其渲染/加载调度等同 Chromium 上游、非 Aloha 自有实现，故机制层以官方架构声明 + README 定性为准。
