# 证据索引 — 18-cloudmosa-puffin

## Phase 1 — react 粗筛（WebSearch query 留痕）
1. `Puffin Browser CloudMosa cloud rendering how it works architecture`
   → 命中 CloudMosa 官方 overview、Medium 技术文、windowsforum 线程；确认远程浏览器架构（服务器渲染 95% / 端侧光栅化 5%、NVR、矢量绘制指令）。
2. `Puffin browser client display rasterization remote rendering vs local DOM parsing`
   → 确认服务器侧做 DOM 解析与渲染，端侧仅绘制渲染结果；pixel pushing / vector drawing 重建，端侧非本地 DOM 元素级优先调度。

## Phase 2 — react 深抓（WebFetch）证据明细

| # | 时间 | 类型 | URL / 本地路径 | 命中要点（verbatim） |
| --- | --- | --- | --- | --- |
| 1 | 2018 | 独立技术拆解 | https://medium.com/coding-neutrino-blog/how-the-puffin-browser-works-440c91cece8f | "heavy works before painting are done in the data center level ... client just need to draw the page"；无元素优先级/排序/延迟显示描述 |
| 2 | 长期产品页 | CloudMosa 官方 | https://www.cloudmosa.com/overview | "HTML Rendering on the server side" / "Display Rasterization on the client side ... only 5% ... HTML rendering ... 95%"；Network Vector Rendering (NVR) |
| 3 | 2018 | 独立技术拆解（镜像） | https://tigercosmos.xyz/post/2018/09/puffin/ | "server will send the rendering result to client, so client just need to draw the page"；"does not explicitly address element prioritization, element ordering, or delayed element-by-element display on the client side" |
| 4 | 检索摘要 | 远程浏览器线程 | https://windowsforum.com/threads/puffin-browser-on-windows-and-mac-cloud-rendering-speed-and-privacy.393588/ | NVR/矢量绘制指令、Blink/Chromium 在服务器侧、端侧绘制压缩视觉流 |

## 工具/数据限制说明
- 未对 cloudmosa.com Technical White Paper PDF 单独 WebFetch（架构事实已由 3 个独立来源 verbatim 三角验证一致，足以支撑第 5 档 (c) 判定）。
- 时间窗：架构为 Puffin 长期产品形态（2009 起 NVR 平台），跨越专利公开日 2023-08-30，时间合规性不构成本判定依据；本判定基于架构层级不同 (c)。
