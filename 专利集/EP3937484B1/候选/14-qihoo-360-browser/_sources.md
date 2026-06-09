# 证据索引 — 14-qihoo-360-browser（query 留痕）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| S1 | 2026-06 | WebSearch | `360 手机浏览器 内核 省流 渲染 加载 原理` → https://browser.360.cn/se/help/kernel.html | 多为 PC 双核(Webkit/Trident)内核切换说明，非移动省流/分级加载机制 |
| S2 | 2026-06 | WebSearch | `360浏览器 省电 省流 分级加载 延迟 渲染 优先级 移动` → https://browser.360.cn/se/help/feature-detail_hxgn_shll.html | 仅列"省电模式/加速器/睡眠标签"功能名，无渲染调度/元素优先级/延迟机制细节 |
| S3 | 2026-06 | WebSearch | `360 mobile browser Chromium kernel rendering element priority delay power saving architecture` → https://developer.chrome.com/docs/chromium/renderingng-architecture | 确认 360 属 Chromium 系；返回的"元素优先级/延迟渲染"均为 Chromium/Blink 上游通用机制，非 360 自有改动披露 |
| F1 | 2026-06 | WebFetch | https://browser.360.cn/se/help/feature-detail_hxgn_shll.html | 仅以链接形式提及"省电模式"功能名，无任何实现机制（无元素优先级/延迟渲染/预定延迟时长描述） |

## Phase 1 — react 粗筛 WebSearch（串行，3 次）
1. `360 手机浏览器 内核 省流 渲染 加载 原理`
2. `360浏览器 省电 省流 分级加载 延迟 渲染 优先级 移动`
3. `360 mobile browser Chromium kernel rendering element priority delay power saving architecture`

## Phase 2 — react 深抓 WebFetch（串行，1 次）
1. WebFetch https://browser.360.cn/se/help/feature-detail_hxgn_shll.html → 仅提及"省电模式"功能名，无实现机制。

## 工具受限 / 资料受限说明
- 无受限工具。
- 360 移动浏览器闭源，无公开架构文档/技术白皮书披露其省电模式内部渲染调度机制，故 F2/F3/F4/F5/F7 机制细节无公开来源可引。
