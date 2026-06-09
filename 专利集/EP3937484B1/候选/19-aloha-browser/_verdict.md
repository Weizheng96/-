# 19-aloha-browser verdict

## 候选基本信息
- 名称：Aloha Browser（宣称自研 "Aloha Core" 渲染引擎）
- 组织：Aloha Mobile
- 类型：产品（移动端隐私/VPN 浏览器 + 开源浏览器引擎 Aloha Core）
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6
- 专利公开（授权）日：2023-08-30（时间窗基准）
- 关键待核结论：**Aloha Core 并非全自研引擎，而是 Chromium 的分支/封装**。官方博客明确"从未自研引擎、起点为 Android WebView"，GitHub repo README 明示 "forked from chromium/chromium"。因此 F1-F6 的渲染/加载行为系**继承自 Chromium 上游**，而非 Aloha 自有的独立实现；Aloha 自有特性为 VPN/数据压缩、广告拦截、adaptive tab loading、缓存管理、硬件加速。

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素的标记语言文档 | 命中（字面，经 Chromium 引擎） | Aloha Core = "Browser Web Engine"，"forked from chromium/chromium"；作为浏览器引擎请求并解析 HTML 构建 DOM 是其固有行为 | https://github.com/AlohaBrowser/aloha-core | 行为来自 Chromium 上游，非 Aloha 自有实现 |
| F2 基于规则集给元素分配优先级值 | 命中（字面，经 Chromium 引擎） | Chromium 资源/元素加载优先级（priority hints、fetchpriority、loading=lazy）为内置能力；Aloha Core 直接继承 | https://github.com/AlohaBrowser/aloha-core | 同上，继承自上游；无 Aloha 自有规则证据 |
| F3 规则集 ≥2 规则/≥2 优先级值/≥2 元素子集 | 公开资料不足（未确定） | 未检索到关于 Aloha 自有的"≥2 条规则、≥2 档优先级、≥2 子集"机制细节的公开描述 | — | 整数限定仅描述下界以下信息缺失→默认未确定 |
| F4 元素子集含"父元素+其嵌套元素"（DOM 树父子优先级） | 公开资料不足（未确定） | 未检索到 Aloha 自有的"按 DOM 父+嵌套子树组织优先级"的公开机制描述 | — | 结构限定无证据→未确定 |
| F5 基于优先级值确定元素显示顺序 | 命中（字面，经 Chromium 引擎） | Chromium 渲染管线按资源优先级调度加载/绘制顺序，Aloha Core 继承 | https://github.com/AlohaBrowser/aloha-core | 行为来自上游 |
| F6 按该顺序显示各元素对应渲染内容 | 命中（字面，经 Chromium 引擎） | 渐进式渲染（按优先级先后贴屏）为 Chromium 固有；"hardware acceleration displays pages up to 2x faster" | https://alohabrowser.com/ ; https://github.com/AlohaBrowser/aloha-core | 行为来自上游 |
| F7 相邻元素显示间有"预定延迟时长"（错峰/分批延迟显示） | 公开资料不足（未确定） | 官方博客与 GitHub README 均无"元素间预定延迟显示/错峰分批渲染"的任何描述；Aloha 自有特性（VPN/压缩/广告拦截/adaptive tab loading）均非元素间定时延迟显示机制 | https://alohabrowser.com/posts-aloha-core-i-love-and-hate-you/ ; https://github.com/AlohaBrowser/aloha-core | 关键区分特征无任何正向证据；亦无候选 verbatim 正向否认 → 记未确定（非已排除） |

## 已检查文档清单
1. https://alohabrowser.com/posts-aloha-core-i-love-and-hate-you/（官方博客，引擎架构来源，WebFetch verbatim）
2. https://github.com/AlohaBrowser/aloha-core（GitHub repo README，WebFetch verbatim）
3. https://alohabrowser.com/ ; https://www.techradar.com/pro/aloha-browser（官方站 + 评测，自有特性盘点，WebSearch）

## 最终判定 **第 4 档：低度疑似（机制证据不足，无正向反据）**

判定依据：Aloha Core 是真实存在且在专利公开日（2023-08-30）后持续维护/开源的移动浏览器引擎，作为 Chromium 分支，F1/F2/F5/F6（解析标记文档、按优先级调度、确定显示顺序、渐进显示）以字面/继承方式成立；但这些行为均继承自 Chromium 上游、非 Aloha 自有实现。专利的三项关键区分限定——F3（≥2 规则/≥2 档/≥2 子集）、F4（DOM 父+嵌套子树优先级）、尤其 F7（相邻元素间**预定延迟时长**显示）——在 Aloha 公开资料中均无任何正向证据。但同样**无针对该候选的 verbatim 正向反据**（无声明"不做元素间延迟显示"，0 命中≠已排除；"Chromium 分支"≠架构不同到不渲染网页的程度，故不构成第5档(c)）。确认命中 4/7 < 60%，关键特征 F7 缺证，无第5档正向反据 → 落第 4 档。

## 升级路径
- 抓取 aloha-core GitHub 源码（宣称 30GB）中渲染调度/加载优先级相关模块，核查 Aloha 是否在 Chromium 之上叠加了"按 DOM 子树的多规则优先级 + 元素间定时延迟显示"的自有逻辑（若仅原样使用 Chromium 默认调度，则 F7 应判未命中而非升级）。
- 检索 Aloha 是否有独立的"省电/低功耗渲染模式"技术文档或专利，定位是否存在 F7 式的相邻元素定时错峰显示机制。
- 若确认 Aloha 仅继承 Chromium 默认异步/懒加载（非元素间固定延迟显示），F7 应转为"未命中"，候选随之向第5档移动——但需 Aloha 自身的正向反据，而非对 Chromium 通用行为的反推。

## 总结一句话
Aloha Core 实为 Chromium 分支、并非全自研引擎，F1/F2/F5/F6 经上游引擎字面成立但关键区分特征 F3/F4/F7（尤其元素间"预定延迟显示"）无任何公开证据亦无正向反据，**落第 4 档**。
