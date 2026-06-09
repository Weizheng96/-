# 02-tech-webkit verdict

## 候选基本信息
- 名称：WebKit 渲染引擎
- 组织：Apple（开源，主 maintainer）
- 类型：技术
- 初判命中 F#：F1,F2,F3,F4,F5,F6
- 专利公开（授权）日：2023-08-30

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素的标记语言文档 | 命中 | "These applications request markup language documents from a server, parse the markup language document, and then render the elements..."（专利背景描述的正是浏览器引擎行为）；WebKit 解析 HTML 构建含多元素节点的 DOM 树 | https://trac.webkit.org/changeset/274145/webkit | WebKit 作为渲染内核必然接收并解析 markup 为多元素文档，字面命中 |
| F2 基于规则集给元素分配优先级值 | 命中 | "WebKit makes stylesheets the highest priority instead of scripts."；"WebKit increased resource load priority of async scripts from low to medium" | https://labs.tadigital.com/index.php/2019/05/16/7415/ ; https://trac.webkit.org/changeset/274145/webkit | ResourceLoadPriority enum 按规则赋优先级，字面命中 |
| F3 ≥2 规则 / ≥2 优先级值 / ≥2 子集 | 命中 | "priorities depend on the resource type (such as script or image) and the placement of the resource reference in the document"（≥2 条规则：按类型 + 按位置）；"images in the viewport ... high, whereas images outside the viewport ... low"（≥2 优先级档，≥2 子集） | https://web.dev/articles/fetch-priority | 多规则、多档、多子集，字面命中 |
| F4 子集 = 父元素及其嵌套元素（DOM 子树） | 公开资料不足（未确定）〔主 agent 复核下调〕 | ResourceLoadPriority 主要按"个体资源的类型 + 执行特性"赋值（async vs non-async、文档位置）；未见把"父元素 + 其嵌套子元素"作为同一优先级子集整体赋值的正向证据 | https://trac.webkit.org/changeset/274145/webkit | **复核说明**：原"未命中（正向反据）"系由"优先级按资源类型"推断"非 DOM 子树"，属机制描述而非针对 WebKit 的 verbatim 排他否定；且同族引擎存在 parent→subresource 优先级继承（见候选 01 Blink），不能确证 WebKit 排他地不按 DOM 子树。按"非互斥/缺失沉默→未确定"改记未确定 |
| F5 基于优先级确定元素显示/加载顺序 | 命中 | "Requesting page resources in the correct order is critical..."；ResourceLoadScheduler 按 priority 排序加载队列 | https://labs.tadigital.com/index.php/2019/05/16/7415/ | 调度器按优先级决定先后，字面命中 |
| F6 按该顺序显示各元素渲染内容 | 命中 | "Painting can either be global (against the whole tree) or incremental (partial)."；WebKit 渐进/增量渲染按加载完成先后逐步上屏 | https://trac.webkit.org/wiki/Accelerated%20rendering%20and%20compositing | 增量渲染按顺序贴屏，字面命中 |
| F7 下一元素显示相对上一元素延迟"预定延迟时间" | 公开资料不足（未确定）〔主 agent 复核下调〕 | LocalFrameView.cpp 内全部延迟均为功能性：`m_delayedScrollEventTimer.startOneShot(throttlingDelay)`（滚动事件节流）、`m_speculativeTilingEnableTimer.startOneShot(500_ms)`、`m_delayedTextFragmentIndicatorTimer.startOneShot(100_ms)`、视口外帧 `setTimerThrottlingEnabled`；渲染本体按 60fps 帧预算驱动："the time budget for each frame is about 16.667 ms, or 1/60 of a second" | https://raw.githubusercontent.com/WebKit/webkit/main/Source/WebCore/page/LocalFrameView.cpp ; https://webkit.org/blog/category/performance/feed/ | **复核说明**：穷举 grep 表明"未发现 F7 机制"，但 vsync 帧驱动与"在帧节拍上额外对相邻元素插入预定延迟"在逻辑上并不互斥（可叠加），故 vsync 模型属"机制不同"而非对 F7 的 verbatim 排他否定。按全局规则改记未确定（与同族候选 01 Blink 对齐）|

## 已检查文档清单
- ./FrameView.cpp（WebKit raw, 16KB，已重构为壳）
- ./LocalFrameView.cpp（WebKit raw, 273KB，本地 Grep 全部 timer/delay/throttle/schedule/milestone）
- changeset/274145（ResourceLoadPriority 赋值规则 verbatim）
- web.dev fetch-priority / TA Digital labs（优先级规则与档位）
- WebKit Performance blog（帧预算 16.667ms）
- WebKit Accelerated rendering wiki（global/incremental painting）

## 最终判定
**第 4 档：公开资料不足（弱候选）**〔主 agent 复核：原 sub-agent 判第 5 档，复核下调〕

判定依据：F1/F2/F3/F5/F6 字面命中（5/7 ≈ 71%，但其中含 F3 这类需结构核实者）；两个关键区分特征 F4（DOM 父+嵌套子树优先级子集）与 F7（相邻元素显示间预定延迟）均**未取到针对 WebKit 的 verbatim 正向排他否定**——F4 的"非 DOM 子树"系由"按资源类型赋优先级"推断（且同族引擎存在 parent→subresource 优先级继承），F7 的 vsync 帧驱动模型与"在帧节拍上叠加元素间预定延迟"逻辑上不互斥。按全局规则"0 命中≠已排除 / 机制不同·非互斥·缺失沉默→未确定"，两条改记"公开资料不足（未确定）"，不满足第 5 档 (a)/(c) 硬门槛。WebKit 与专利同属端侧 DOM 渲染抽象层（非服务端架构），故不落第 5 档(c)。综合：确认命中含 F4/F7 未确定 → 第 4 档。**与同族开源引擎候选 01-Blink（第 4 档）跨候选对齐。**

## 升级路径（第 4 档）
- grep WebKit 源码 `Source/WebCore/loader/` + `rendering/` 确认是否存在"按 DOM 父+嵌套子树组织优先级子集"（坐实/否定 F4）。
- grep 渲染/合成路径确认是否存在"按优先级排序后、相邻元素显示之间插入预定固定时延上屏"逻辑：若源码明确仅 vsync 逐帧绘制、无 per-element 预定延迟，且有 WebKit 自有文档 verbatim 排他表述，则 F7 可升为"确认未命中（有正向反据）"→落第 5 档；若发现该机制则 F7 坐实、整体升档。

## 总结一句话
WebKit 有按规则的多档资源优先级与增量渲染（F1-F3、F5-F6 命中），但关键区分特征 F4（DOM 父+嵌套子树）与 F7（元素间预定延迟）均无针对 WebKit 的 verbatim 正向排他否定（vsync/资源类型优先级属机制不同·非互斥），按"0命中≠已排除"落第 4 档（公开资料不足），与同族 Blink 对齐。
