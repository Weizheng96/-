# 03-tech-gecko verdict

## 候选基本信息
- 名称：Gecko 渲染引擎
- 组织：Mozilla（开源，主 maintainer；源码公开可核）
- 类型：技术
- 初判命中 F#（from _meta.json）：F1,F2,F3,F4,F5,F6（F7 待核）
- 专利公开（授权）日：2023-08-30（时间窗基准）

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
|---|---|---|---|---|
| F1 接收含多元素的标记语言文档 | 命中（字面） | "Firefox … runs a background thread that scans HTML for resource URLs … makes requests for elements as the DOM tree is constructed"；"The DOM Parser … makes requests as the DOM tree is constructed" | https://firefox-source-docs.mozilla.org/networking/http/prioritization.html | Gecko 请求并解析 HTML 构建 DOM 树（含多元素），字面满足 |
| F2 基于规则集给元素分配优先级值 | 命中（字面） | "Firefox uses supportsPriority and classOfService to order requests"；ClassOfService 含 "Leader (1) … Tail (256) … TailAllowed (512) … TailForbidden (1024)"；"Extensible Prioritization Scheme … Urgency: Ranges from 0 (highest priority) to 7 (lowest priority)" | https://firefox-source-docs.mozilla.org/networking/http/prioritization.html | Gecko 按 ClassOfService / urgency / fetchpriority 给请求/元素赋优先级值，字面满足 |
| F3 ≥2 规则 / ≥2 优先级值 / ≥2 子集（整数限定） | 命中（字面） | "Other parameters are also taken into account … such as the position of the element in the page (e.g. blocking resources in `<head>`), other attributes on the element (`<script async>`, `<script defer>`, `<link media>`, `<link rel>`…) or the resource's destination"；urgency 0–7 多档；ClassOfService 多类 | https://firefox-source-docs.mozilla.org/networking/http/prioritization.html | 多条规则（位置 / 属性 / destination / tracker 分类）共同决定优先级，产生 ≥2 档（urgency 0–7、Leader/Normal/Follower/Tail），作用于多组元素子集，字面满足整数限定 |
| F4 元素子集 = 父元素及其嵌套元素（DOM 树父+子结构定优先级） | 未确定（公开资料不足） | 官方 prioritization 文档优先级表按资源类型组织（resource type），未见 shipped Gecko 把"父元素+其嵌套子元素"作为同一优先级子集整体赋值的正向证据 | https://firefox-source-docs.mozilla.org/networking/http/prioritization.html | 注：IJERT 2013 论文有"父优先级下传子元素"规则，但该论文为提案、非 shipped Gecko、且早于时间窗（见下）。shipped Gecko 的优先级以资源类型/请求类为主轴，F4 的"父+嵌套子树"结构未获正向证据，记未确定（既无确认命中也无正向排他） |
| F5 基于优先级值确定显示/加载顺序 | 命中（字面） | "Firefox uses supportsPriority and classOfService to order requests … request priority becomes crucial"；urgency 决定带宽/排序 | https://firefox-source-docs.mozilla.org/networking/http/prioritization.html | 按优先级排序请求/加载队列，字面满足 |
| F6 按该顺序显示各元素对应渲染内容 | 命中（字面） | "the frame constructor generates the layout using the Reflow module and the elements are painted on the browser from the frame tree"（Gecko 渲染流程描述） | https://www.ijert.org/research/priority-based-loading-of-html-elements-for-gecko-rendering-engine-IJERTV2IS50077.pdf（第2页 Gecko 主流程） | Gecko 按 reflow/paint 流程逐元素上屏，字面满足 |
| F7 下一元素显示相对上一元素延迟"预定延迟时间"（关键区分特征 + 时间限定） | 公开资料不足（未确定）〔主 agent 复核下调〕 | (a) tailing delay-quantum 600ms/20ms："delays **network requests themselves, not display rendering**"；只作用于 tracker/async 网络请求。(b) nglayout.initialpaint.delay：页面级一次性初始绘制抑制 | https://www.janbambas.cz/firefox-57-delays-requests-tracking-domains/ ; https://bugzilla.mozilla.org/show_bug.cgi?id=180241 | **复核说明**：已查到的两类延迟确非 F7（一为网络请求延后、一为页面级初始绘制抑制），但二者只是 Gecko 已知延迟机制中的两个，未穷举源码、也不能据此 verbatim 排他否定"Gecko 在元素显示层不存在任何预定延迟"。属"机制不同/枚举未尽"，按全局规则改记未确定（与同族候选 01 Blink、02 WebKit 对齐）|

## 已检查文档清单
1. Firefox Network Scheduling and Prioritization（官方源码文档）— https://firefox-source-docs.mozilla.org/networking/http/prioritization.html （ClassOfService / urgency / 多规则；优先级按资源类型组织）
2. Firefox 57 delays requests to tracking domains, janbambas/mayhemer 博客（tailing 作者）— https://www.janbambas.cz/firefox-57-delays-requests-tracking-domains/ （delay-quantum；明示"delays network requests, not display rendering"）
3. Bugzilla 180241 nglayout.initialpaint.delay — https://bugzilla.mozilla.org/show_bug.cgi?id=180241 （初始绘制抑制，一次性、页面级）
4. IJERT 2013《Priority Based Loading Of HTML Elements For Gecko Rendering Engine》（已 curl 下载 PDF 并提取文本 ijert-priority-gecko.pdf）— Vol.2 Issue 5, May 2013；自述为"we suggest / we propose / intended to be added to the HTML API / On successful implementation"的**提案**，非 shipped Gecko；含父→子优先级下传规则但**无预定元素间延迟**

## 最终判定 **第 4 档：公开资料不足（弱候选）**〔主 agent 复核：原 sub-agent 判第 5 档，复核下调〕

判定依据：
1. F1/F2/F3/F5/F6 字面命中（按 ClassOfService/urgency 多规则多档给元素/请求赋优先级并按序渲染）；F4（DOM 父+嵌套子树优先级）公开资料不足；F7（关键区分特征）**未取到针对 Gecko 的 verbatim 正向排他否定**——已查到的 tailing（网络请求延后）与 initialpaint.delay（页面级初始绘制抑制）确非 F7，但仅为已知延迟机制中的两个、未穷举源码，属"机制不同/枚举未尽"，不能据此 verbatim 排他否定 F7 存在。按"0 命中≠已排除"改记未确定。
2. Gecko 与专利同属端侧 DOM 渲染抽象层（非服务端架构），不满足第 5 档(c)；亦无针对 Gecko 的正向反据，不满足第 5 档(a)。
3. 关于 IJERT 2013 论文：与权利要求多处吻合（含 F4 式父→子优先级），但 (i) 为**学术提案**而非 shipped Gecko、无证据并入 Firefox；(ii) 发表 2013-05，早于专利公开日 2023-08-30，属时间窗外，仅可作背景、不能作命中证据。
4. 综合：关键区分特征 F4/F7 均"公开资料不足（未确定）"，确认命中 <60% 且无第 5 档硬条件 → 第 4 档。**与同族开源引擎候选 01-Blink、02-WebKit（均第 4 档）跨候选对齐。**

## 升级路径（第 4 档）
- grep shipped Gecko 源码（`layout/` + `dom/` + networking ClassOfService）确认是否存在"按 DOM 父+嵌套子树组织优先级子集"（坐实/否定 F4）与"相邻元素显示之间插入预定固定延迟时长上屏"（坐实/否定 F7）。
- 若源码 verbatim 表明渲染仅按 reflow/paint 帧驱动、无 per-element 预定延迟显示，且有 Mozilla 自有文档排他表述，则 F7 可升为"确认未命中（有正向反据）"→落第 5 档；若发现该机制且发布晚于 2023-08-30，则 F7 坐实、整体升档。

## 总结一句话
Gecko 在 F1/F2/F3/F5/F6 字面相符，但关键区分特征 F4（DOM 父+嵌套子树）与 F7（元素间预定延迟）均无针对 Gecko 的 verbatim 正向排他否定（已查到的延迟均为网络/页面级、未穷举源码），按"0命中≠已排除"**落第 4 档（公开资料不足）**，与同族 Blink/WebKit 对齐。
