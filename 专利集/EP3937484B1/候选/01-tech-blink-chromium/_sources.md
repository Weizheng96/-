# 证据索引 — 01-tech-blink-chromium

## Phase 1 — WebSearch（react 串行）
1. `Chromium Blink resource scheduler priority hints rendering fetchpriority`
   - 命中：Priority Hints / fetchpriority（auto/low/high），web.dev、chromestatus、blink-dev intent。
   - 要点：开发者用 `fetchpriority` 属性提示资源 fetch 优先级，浏览器据此排序资源加载。→ F2/F5 基线信号（资源 fetch 优先级），属"资源 fetch 优先级"。
2. `Chromium Blink render element predetermined delay timer staggered display power saving`
   - 命中：RenderingNG、Blink Scheduler README、timer throttling 文档。
   - 要点：Blink 渲染管线按 style/layout/paint 阶段推进；timer throttling 仅针对**视口外 frame** 降低 setTimeout/setInterval 频率（非"相邻元素间预定延迟显示"）。未见"元素间预定延迟"机制。
3. `Blink ResourceScheduler priority DOM subtree parent child element loading order`
   - 命中：TaskSchedulingInBlink.md、DOM README、Priority Hints intent。
   - 要点：调度按 task type/runner（input/compositor/frame）排优先级；subresource 继承 parent 的 fetch 优先级（资源 fetch 优先级继承，非"DOM 父+嵌套元素作为优先级子集子树"）。

## Phase 2 — WebFetch（react 串行）
4. WebFetch `https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/renderer/platform/scheduler/TaskSchedulingInBlink.md`
   - verbatim："The scheduler selects the next task to run based on the priority (modulo some starvation logic)."
   - 结论：优先级挂在 **task type / runner**（input、compositor、frame-based），**不**按 DOM 父子子树组织；文档无任何"per-element display delay / staggered rendering / inter-element timing"。→ F4 正向反据信号、F7 机制不同信号。
5. WebFetch `https://developer.chrome.com/docs/chromium/renderingng`
   - 渲染管线分阶段（style/layout/paint/composite），含 re-entrant/delayed-rendering（指 content-visibility/container-queries，非元素间定时延迟）。无"per-element 固定延迟显示"。
6. WebSearch `Chromium rendering pipeline life of a frame vsync paint compositing requestAnimationFrame cadence`（补 react）→ RenderingNG architecture（developer.chrome.com）
   - verbatim 要点："schedules rendering to happen at **a cadence matching the device display**"；"BeginImplFrame starts a compositor frame (**with each vsync**)"。
   - 结论：Blink 显示节奏 = 设备显示刷新（vsync，固定显示刷新率，每帧绘制当时 ready 的内容），**不是**"显示上一个元素后延迟一个 predetermined delay time 再显示下一个元素"。→ F7 的机制层正向区分。

## 工具受限说明
- patents.google.com 本环境可能 SSL 不可达；本候选为开源引擎，源码/设计文档（chromium.googlesource.com / developer.chrome.com）已可达，未触发付费墙/登录墙。

## 粗筛结论
候选真实存在（Blink/Chromium，源码+设计文档公开，持续更新至 2023-08-30 之后）。F1/F2/F5/F6 基线齐备（解析 markup 建 DOM、fetchpriority 资源优先级、按优先级排资源、逐帧渐进绘制）。**关键区分特征 F7（相邻元素间 predetermined delay time 错峰显示）未在任何官方文档/调度文档出现**，RenderingNG 正向说明显示节奏由 vsync 帧节拍驱动（非元素间定时延迟）；F4（优先级子集=DOM 父+嵌套元素子树）被 TaskSchedulingInBlink 正向说明"优先级挂 task runner 而非 DOM 父子子树"。
