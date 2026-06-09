# 01-tech-blink-chromium verdict
## 候选基本信息
- 名称：Blink / Chromium 渲染引擎
- 组织：Google（开源，主 maintainer）
- 类型：技术
- 初判命中 F#：F1,F2,F3,F4,F5,F6
- 专利公开（授权）日：2023-08-30
## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 确认命中（字面） | Blink 解析 markup 文档建 DOM 树（含多元素节点）；"apply CSS to the DOM" / 渲染管线以 DOM 为输入 | https://developer.chrome.com/docs/chromium/renderingng-architecture | 字面：接收并解析含多元素的 markup 文档建 DOM，属浏览器引擎基础能力。 |
| F2 | 确认命中（字面/等同） | "the computed priority of a resource fetch ... Supported priority values are auto, low, and high"（fetchpriority/Priority Hints） | https://web.dev/articles/fetch-priority | 字面/等同：基于规则（开发者 hint + 浏览器内部启发式）给元素/资源分配优先级值。 |
| F3 | 公开资料不足（未确定） | Priority Hints 产生 ≥2 档（auto/low/high）；浏览器内部另有按资源类型/视口的启发式规则 | https://web.dev/articles/fetch-priority | ≥2 优先级档可证；"≥2 条规则 且 ≥2 个元素子集"的整数限定无官方逐条描述→未确定（非排他）。 |
| F4 | 公开资料不足（未确定） | "priority is not organized by DOM parent/child subtrees ... priorities attach to task types and runners"；另有"subresources getting the same priority as their parent"（fetch 优先级继承） | https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/renderer/platform/scheduler/TaskSchedulingInBlink.md | 任务调度优先级不挂 DOM 父子子树（反向信号）；但 fetch 优先级存在 parent→subresource 继承（部分等同信号）。两信号方向相反、均非针对"优先级子集=父+嵌套元素子树"的正向否定→记未确定，不判反据。 |
| F5 | 确认命中（字面） | "the browser ... prioritizing the request" / 调度器"selects the next task to run based on the priority" — 按优先级确定资源加载/任务顺序 | https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/renderer/platform/scheduler/TaskSchedulingInBlink.md | 字面：基于优先级值确定（资源/任务）顺序。 |
| F6 | 确认命中（字面） | 渲染管线 Style→Layout→Pre-paint→Raster/Paint→Activate→Draw 逐阶段把内容绘制上屏（progressive rendering） | https://developer.chrome.com/docs/chromium/renderingng-architecture | 字面：按管线顺序逐步把渲染内容绘制到窗口。 |
| F7 | 公开资料不足（未确定，**源码级强负向**） | **直读 Chromium 源码 `core/frame/local_frame_view.cc`（v.main，已存档 src_local_frame_view.cc）**：绘制生命周期 `void LocalFrameView::RunPaintLifecyclePhase(...)` 内 `PaintTree(benchmark_mode, paint_controller); ... PushPaintArtifactToCompositor(...)` —— **整树一次性绘制后整体提交合成器**，无逐元素延迟门控；文件内全部计时/延迟均为功能性：`update_plugins_timer_`（插件更新）、`delayed_intersection_timer_`（IntersectionObserver）、`kCommitDelayDefaultInMs = 500 // 30 frames @ 60hz`（注释："delay the compositor commit ... to avoid flash between navigations"——**一次性页面级**导航防闪，非元素间）、`ShouldThrottleRendering()`（视口外帧节流）。 | https://raw.githubusercontent.com/chromium/chromium/main/third_party/blink/renderer/core/frame/local_frame_view.cc | 关键区分特征。**源码证实**主线绘制为整树批绘制（vsync 帧驱动）、无"显示上一元素后等待 predetermined delay time 再显示下一元素"的 per-element 错峰门控；唯一页面级延迟（commit hold）是导航防闪、非元素间。按 SKILL 保守标准（整树批绘制属"另一种手段"、与逐元素延迟非严格互斥可叠加，且本次核查覆盖核心绘制路径而非穷举全部子系统）仍记"未确定（源码级强负向）"，未升为"确认未命中"。 |
## 已检查文档清单
- Priority Hints / fetchpriority（资源 fetch 优先级 auto/low/high）— https://web.dev/articles/fetch-priority
- TaskSchedulingInBlink（优先级挂 task runner，非 DOM 父子子树；无 per-element 延迟）— https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/renderer/platform/scheduler/TaskSchedulingInBlink.md
- RenderingNG / RenderingNG architecture（管线分阶段；显示按 vsync 帧节拍）— https://developer.chrome.com/docs/chromium/renderingng-architecture
- **【源码 L1】Chromium `core/frame/local_frame_view.cc`（main 分支，已 curl 存档于本目录 `src_local_frame_view.cc`，211KB）** — `RunPaintLifecyclePhase`=整树批绘制+整体提交；全部 timer/delay 功能性枚举（plugin/intersection/commit-hold-nav-flash/offscreen-throttle）；无 per-element 预定延迟门控 — https://raw.githubusercontent.com/chromium/chromium/main/third_party/blink/renderer/core/frame/local_frame_view.cc
## 最终判定
**第4档：公开资料不足（弱候选）**
五档定义（"命中"=三态中"确认命中"，含字面/等同）：
  - 第1档：确认侵权（高）— F1-F7 全部"确认命中·字面"
  - 第2档：确认侵权（中）— F1-F7 全部确认命中，含 ≥1 等同
  - 第3档：公开资料不足（强候选）— "确认命中" ≥60%，其余"公开资料不足（未确定）"且无"确认未命中（有正向反据）"
  - 第4档：公开资料不足（弱候选）— "确认命中" <60%，且无足以触发第5档的正向反据
  - 第5档：已排除 — 仅当：(a) ≥1 条 F# 为"确认未命中（有正向反据）"，或 (b) 全部证据 < 2023-08-30（现有技术），或 (c) 架构层级不同
第5档硬门槛：必须是针对该候选产品的正向事实，不是推断也不是缺失。行业通用反推/"同类一般如此"/"公开未提及"/"非互斥手段"一律不算反向证据→只是公开资料不足。0 命中 ≠ 已排除。
判定依据（1-3 句，基于上表 F# 分布）：确认命中 4/7（F1/F2/F5/F6，占 ~57% < 60%）；F3/F4 为"公开资料不足（未确定）"。最关键区分特征 F7（相邻元素间 predetermined delay time 错峰显示）——**已按升级路径直读 Chromium 源码 `local_frame_view.cc` 核实**：主线绘制生命周期为整树一次性批绘制后整体提交合成器（vsync 帧驱动），文件内全部 timer/delay 均为功能性（插件/intersection/导航防闪 commit-hold/视口外节流），无"按元素优先级排序后相邻元素间插入预定时延上屏"的 per-element 门控。这是**源码级强负向证据**。
**关于档位（主 agent 复核裁定）**：源码证实主线绘制管线不含 F7，构成很强的非侵权证据；但按 SKILL 保守标准——(1)"整树批绘制"是另一种渲染手段，与"逐元素预定延迟"非严格互斥（理论可叠加），不等于针对该候选"排他地不做 F7"的正向声明；(2) 本次核查覆盖核心绘制路径（local_frame_view.cc 绘制生命周期）而非穷举 Blink 全部子系统（如各类省电/实验特性）——故仍不满足第5档(a) 的"确认未命中（有正向反据）"硬门槛，保守维持第4档（公开资料不足），但 F7 证据等级已由"文档缺失"提升为"源码级强负向"。确认命中 <60% → 第4档。
## 升级路径（仅第3-4档填）
- **F7 已直读 `local_frame_view.cc` 核实（见上）**；若要进一步落"确认未命中（有正向反据）"→第5档，需：(a) 穷举 `core/paint/` + `platform/scheduler/` + 省电/实验 flag 路径，确认无任一处实现"元素间预定延迟显示"；或 (b) 取到 Google 对该机制的明文排他声明。反之若在上述路径发现 per-element 定时上屏，则 F7 坐实、整体升档。
- F3/F4：核 `core/loader/` 优先级计算（ComputeLoadPriority）确认"≥2 规则/≥2 子集"与"优先级子集=DOM 父+嵌套子树"是否成立。
## 总结一句话
Blink/Chromium 命中 F1/F2/F5/F6；关键区分特征 F7"相邻元素间预定延迟错峰显示"经**直读源码 `local_frame_view.cc` 核实**：主线绘制为整树批绘制+整体提交（vsync 驱动）、无 per-element 预定延迟门控（源码级强负向）——非侵权证据很强，但按保守标准（批绘制非严格排他+未穷举全部子系统）仍维持第4档（公开资料不足·弱候选），F7 证据已升至源码级。
