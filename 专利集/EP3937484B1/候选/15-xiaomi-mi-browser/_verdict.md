# 15-xiaomi-mi-browser verdict

## 候选基本信息
- 名称：Mi Browser / Mint Browser
- 组织：Xiaomi
- 类型：产品（移动端浏览器，Chromium / Blink 内核 + 自有省流模式）
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6
- 专利公开日基准：2023-08-30
- 在用状态 / 时间窗：Mint Browser 当前仍在 Google Play 上架（com.mi.globalbrowser.mini）；Mi Browser 预装于 MIUI / HyperOS。产品在用，时间窗合规。

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素的标记语言文档 | 命中（等同） | Mi Browser「is a chromium-based web browser ... renders web pages using the Blink engine」 | https://www.guidingtech.com/mi-browser-vs-chrome-difference/ | Chromium/Blink 内核必然请求并解析 HTML 构建含多元素的 DOM。等同基础 = 通用内核行为，非小米自有改动 |
| F2 基于规则集给元素分配优先级值 | 命中（等同） | 同上：Chromium/Blink 内核 | https://trust.mi.com/docs/miui-privacy-white-paper-global/4/7 | Blink 资源加载内置 ResourceFetcher priority（VeryHigh..VeryLow）属内核通用机制，可作等同。非小米 verbatim 自有改动 |
| F3 ≥2 规则 / ≥2 优先级档 / ≥2 子集（整数限定） | 公开资料不足（未确定） | — | — | 小米自有省流 / MiCT 文档均未披露"≥2 条规则产生 ≥2 档作用于 ≥2 子集"的具体机制；内核默认实现是否满足该整数限定无公开证据。闭源 |
| F4 子集含"父元素+其嵌套元素"（DOM 父子结构限定） | 公开资料不足（未确定） | — | — | 无任何公开资料显示优先级挂在 DOM 父+嵌套子树上。闭源，未确定 |
| F5 基于优先级值确定显示顺序 | 命中（等同） | Chromium/Blink 内核 | https://www.guidingtech.com/mi-browser-vs-chrome-difference/ | 内核按资源优先级调度加载/绘制顺序，通用等同。非小米自有改动 |
| F6 按该顺序显示各元素渲染内容 | 命中（等同） | Chromium/Blink 渐进式渲染 | https://www.guidingtech.com/mi-browser-vs-chrome-difference/ | 内核渐进绘制，通用等同。非小米自有改动 |
| F7 相邻元素显示间有"预定延迟时长"（关键区分特征） | 公开资料不足（未确定） | MiCT：「网页预热及预加载能力，提升网页打开速度」；Mint：「data compression」 | https://dev.mi.com/xiaomihyperos/MICT ; https://www.xda-developers.com/mint-browser-xiaomi-lightweight/ | 小米自有能力为：无图模式、云加速省流、MiCT 预热/预加载 WebView、数据压缩——均为"加快打开 / 减少流量"方向，与"相邻元素显示间插入预定延迟"语义相反或无关。无证据显示存在 F7 预定延迟机制；亦无 verbatim 正向否认。未确定 |

## 已检查文档清单
1. https://www.guidingtech.com/mi-browser-vs-chrome-difference/ — Mi Browser = Chromium/Blink 内核
2. https://trust.mi.com/docs/miui-privacy-white-paper-global/4/7 — Mi Browser 内核/隐私白皮书
3. https://www.xda-developers.com/mint-browser-xiaomi-lightweight/ — Mint Browser 功能（数据压缩 + 可配置项）
4. https://www.digit.in/news/apps/xiaomi-mint-lightweight-browser-with-dark-mode-voice-search-data-saver-feature-and-more-launched-for-45465.html — Mint Browser data saver = 无图/拦广告
5. https://dev.mi.com/xiaomihyperos/MICT — MiCT 网页秒开引擎（WebView 预热/预加载，非元素级调度）
6. https://play.google.com/store/apps/details?id=com.mi.globalbrowser.mini — Mint Browser 在用状态确认

## 最终判定

**第 4 档：公开资料不足，关键区分特征未确定（<60% 确认命中，无第 5 档正向反据）**

判定依据：候选为真实在用产品，Chromium/Blink 内核给 F1/F2/F5/F6 提供通用等同基础（4/7，约 57%），但这些命中来自内核通用行为而非小米 verbatim 自有改动；专利三项关键限定 F3（整数限定）、F4（DOM 父+嵌套子树结构限定）、F7（相邻元素预定延迟——本专利相对 prior art 的最关键区分特征）均因产品闭源、无公开机制文档而记"未确定"。小米自有省流机制（无图、云加速、MiCT 预热、数据压缩）方向是"加速/减流量"，与 F7"插入预定延迟"无对应，但也未见针对该候选的 verbatim 正向否认，不构成第 5 档反向证据，故不落已排除。综合 <60% 确认且无正向反据 → 第 4 档。

## 升级路径（第3-4档填）
- F7：若取得 Mi Browser / Mint Browser 内核反编译或官方技术文档，证明其在元素/批次显示之间存在确定的预定延迟时长（time-sliced display with preset gap），可显著推升档位。
- F3 / F4：若证明其自有加载调度含 ≥2 条规则产生 ≥2 档优先级、且优先级以 DOM 父+嵌套子树为子集组织，可补齐整数与结构限定。
- 可行手段：APK 反编译（com.mi.globalbrowser / com.mi.globalbrowser.mini）静态分析渲染调度模块；或检索小米浏览器内核（基于 Chromium 的自有 patch）开源/泄露代码中的 delay/throttle/stagger 关键词。

## 总结一句话
Mi Browser / Mint Browser 为真实在用的 Chromium 内核浏览器，F1/F2/F5/F6 凭内核通用行为构成等同（约 57%），但关键区分特征 F7（相邻元素预定延迟）及 F3/F4 因闭源无机制披露全部未确定，无正向反据，落第 4 档。
