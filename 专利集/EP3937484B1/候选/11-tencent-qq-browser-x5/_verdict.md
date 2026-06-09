# 11-tencent-qq-browser-x5 verdict

## 候选基本信息
- 类型：产品
- 名称：QQ Browser（X5/TBS 内核）
- 组织：Tencent（腾讯）
- 初判命中 F#（from _meta.json）：F1,F2,F3,F5,F6
- 公开度：低
- 一句话定位：腾讯自研 X5(TBS) 内核（Blink 分支），同时供 QQ 浏览器与微信/手机QQ/空间复用。
- 专利公开（授权）日基准：2023-08-30
- 产品现状：X5/TBS 为现行在用产品，处于时间窗内（持续运营，远晚于 2023-08-30）。

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（接收含多元素标记文档） | 命中（等同） | X5"将整体内核架构切换到了 Blink 内核上……基于 Blink m53 的版本" | https://cloud.tencent.com/developer/article/1083770 | X5 为 Blink/Chromium 分支，浏览器内核必然请求并解析 HTML 构建含多元素的 DOM——属 Blink 基线能力，等同命中 |
| F2（基于规则集给元素分配优先级值） | 命中（等同） | "资源优先级：希望在首屏内的资源可以快速加载下来，首屏外的资源优先级可以低一些，往后做一些延迟"；fetchpriority(high/low)/async/loading=lazy | https://cloud.tencent.com/developer/article/1083770 ; https://cloud.tencent.com/developer/article/2355175 | 确有按规则给资源/元素赋优先级（首屏位置 + fetchpriority 等）——属 Blink 基线 + X5 调整，等同命中 |
| F3（≥2 规则/≥2 档/≥2 子集，结构化规则集） | 公开资料不足（未确定） | 公开资料仅述"首屏内/首屏外"单一位置规则；fetchpriority 规则"独立应用于不同类型资源……不是嵌套的父子关系" | https://cloud.tencent.com/developer/article/1083770 ; https://cloud.tencent.com/developer/article/2355175 | 含整数限定。公开层面看到的是离散的位置规则 + 资源类型优先级提示；是否构成权 1 意义上"≥2 条规则产生≥2 档、作用于≥2 子集"的结构化 set of rules 无机制文档可核验。非排他描述，记未确定 |
| F4（子集=父元素+其嵌套元素 / DOM 子树优先级） | 公开资料不足（未确定） | "优先级属性仅作用于标记所在的单个元素"（针对 fetchpriority 而言） | https://cloud.tencent.com/developer/article/2355175 | 该句仅描述 fetchpriority 这一机制非父子结构，属"不同机制下的非父子"，非针对 X5 整体调度的 verbatim 正向拒绝；X5 内部是否有 subtree/容器级优先级（Blink 本身按 frame/容器调度资源存在相关能力）无公开机制可核验，记未确定 |
| F5（基于优先级值确定显示/加载顺序） | 命中（等同） | "首屏内的资源可以快速加载下来，首屏外的资源优先级可以低一些，往后做一些延迟" | https://cloud.tencent.com/developer/article/1083770 | 按优先级排序加载/渲染顺序——属 Blink 资源调度基线 + X5 调整，等同命中 |
| F6（按该顺序显示各元素渲染内容） | 命中（等同） | 同上（按优先级先加载首屏内资源并渲染）；X5 基于 Blink m53 渐进式渲染 | https://cloud.tencent.com/developer/article/1083770 | 浏览器内核按调度顺序渐进绘制到窗口——Blink 基线能力，等同命中 |
| F7（相邻元素显示间有 predetermined delay time） | 公开资料不足（未确定） | article/1083770 明确未提固定延迟分批显示，策略"集中在并发控制、Socket 重用和预连接……倾向于异步并发加载而非顺序延迟"；article/2355175"完全不包含任何关于定时器、固定延迟或分批延迟显示的内容" | https://cloud.tencent.com/developer/article/1083770 ; https://cloud.tencent.com/developer/article/2355175 | 关键区分特征。注意："首屏外……往后做一些延迟"指对低优先级资源的加载延后（异步/优先级降级），不等于"上一元素显示后等待一个预定固定时长再显示下一元素"。两篇文章"未提及/不包含"是缺失沉默 + 不同机制（异步并发），非针对 X5 显示调度的 verbatim 正向拒绝；X5 闭源无机制文档可核验是否存在元素间预定延迟，记未确定 |

## 已检查文档清单
1. https://cloud.tencent.com/developer/article/1083770 — 腾讯云：通过 QQ 浏览器内核看 browser 性能优化（已 WebFetch）
2. https://cloud.tencent.com/developer/article/2355175 — 腾讯云：如何优雅地控制网页请求的优先级（已 WebFetch）
3. https://www.tencentcloud.com/techpedia/109193 — X5/TBS 概述（WebSearch 摘要）
4. WebSearch 4 条 query 留痕见 _sources.md

## 最终判定

**第 4 档：疑似命中（公开资料不足，关键区分特征未确定）**

判定依据：候选为真实现行产品（X5/TBS，Blink 分支，时间窗内）。F1/F2/F5/F6 凭 Blink/Chromium 内核基线能力可作等同命中（4/7 ≈ 57%）；但关键区分特征 F7（元素间 predetermined delay time）及结构限定 F4、整数限定 F3 因 X5 闭源、仅有营销/技术博客资料而无机制文档可核验，均记"公开资料不足（未确定）"。无任一针对该候选的 verbatim 正向反证（"未提及/不包含"系缺失沉默；"首屏外往后延迟"系异步降级而非元素间定时延迟，属不同机制），故不落第 5 档；确认命中 < 60% 且无第 5 档反据，落第 4 档。

## 升级路径（→ 第 2/3 档所需证据）
1. **F7（最关键）**：找到 X5/TBS 内核中"相邻元素/批次显示之间插入一个预先设定的固定延迟时长"的 verbatim 机制描述（腾讯 TBS 开发者文档、内核源码注释、腾讯自有相关专利权利要求、或定时分批上屏的技术分享）。若证实存在元素间预定延迟 → F7 命中，整体可升至第 3 档甚至更高。
2. **F3**：证实 X5 优先级调度由 ≥2 条规则产生 ≥2 个优先级档、作用于 ≥2 个元素子集（结构化 set of rules，而非单一首屏位置规则）。
3. **F4**：证实优先级挂在 DOM 父元素 + 其嵌套子元素（子树/容器级）上，而非扁平资源列表。
4. 可核验路径：腾讯 TBS 官方开发者文档（x5.tencent.com）、Espacenet/freepatentsonline/专利之星 检索腾讯网页渲染调度专利。

## 总结一句话
QQ 浏览器 X5/TBS 内核为现行 Blink 分支产品，F1/F2/F5/F6 凭内核基线可作等同命中，但关键区分特征 F7（元素间预定延迟）及 F3/F4 因内核闭源、公开资料仅营销/博客层面而无机制可核验，无正向反证，落第 4 档（疑似命中、待补 F7 机制证据）。

---
> 免责声明：本报告为技术比对线索与证据链梳理，不构成"已构成侵权"的法律结论。F# 判定基于公开可检索资料，X5/TBS 内核闭源致关键机制无法核验；最终侵权认定须由权利人结合内核实现细节、源码/反编译证据及法律程序判断。
