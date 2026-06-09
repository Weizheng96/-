# 16-vivo-browser verdict

## 候选基本信息
- 名称：vivo 浏览器
- 组织：vivo
- 类型：产品（移动设备内置浏览器，Chromium / Blink 内核深度优化，自有"奇点内核"WebView；含极速/兼容模式、无图模式、极简模式）
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6
- 专利公开（授权）日：2023-08-30（时间窗基准）

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（接收含多元素的标记语言文档） | 命中（等同） | "vivo浏览器基于Chromium Blink内核深度优化" — Chromium/Blink 内核必然请求并解析 HTML 构建含多元素的 DOM | https://www.cnblogs.com/vivotech/p/13680373.html | Chromium 内核标准行为，作 F1 等同证据；vivo 自有改动无 verbatim 不另计 |
| F2（基于规则集给元素分配优先级值） | 命中（等同） | Chromium 内核内置资源/元素优先级机制（fetch priority / loading 调度）；"浏览器内核提供了丰富的预加载机制，通过preload可以标识需要浏览器提前加载的重要资源" | https://www.cnblogs.com/vivotech/p/13680373.html ; https://web.dev/articles/fetch-priority | Chromium 内核标准优先级机制，作 F2 等同证据 |
| F3（≥2 规则 / ≥2 优先级值 / ≥2 子集） | 公开资料不足（未确定） | 无 vivo 公开文档描述其规则集条数、优先级档数与作用子集数；通用 Chromium 优先级不能 verbatim 证明 ≥2 规则×≥2 值×≥2 子集这一整数+结构组合 | （4 条 query 无命中机制级证据） | 整数限定仅描述下界以下→默认未确定 |
| F4（子集含"父元素及其嵌套元素"——挂 DOM 父+嵌套子树） | 公开资料不足（未确定） | 无任何公开资料描述 vivo 浏览器按 DOM 父子/嵌套子树组织优先级子集 | （无命中） | 闭源，缺机制细节 |
| F5（基于优先级值确定显示顺序） | 命中（等同） | Chromium 内核按资源/元素优先级调度加载与绘制顺序（priority-based scheduling） | https://web.dev/articles/fetch-priority ; https://addyosmani.com/blog/script-priorities/ | Chromium 内核标准行为，作 F5 等同证据 |
| F6（按该顺序显示各元素渲染内容） | 命中（等同） | Chromium 内核 progressive rendering，按调度顺序逐步绘制内容上屏 | https://web.dev/articles/optimize-lcp | Chromium 内核标准行为，作 F6 等同证据 |
| F7（相邻元素显示间有"预定延迟时长"——错峰/分批延迟显示） | 公开资料不足（未确定） | 4 条 query + 2 次 WebFetch 均未发现 vivo 浏览器在相邻元素显示之间插入预定延迟时长的机制；其"无图模式"=省流量（不加载图片）、"极简模式"=去广告弹窗简化布局，均非"上一元素显示后延迟固定时长再显示下一元素"；通用 Chromium fetch priority / 懒加载 ≠ 元素间预定延迟显示 | （无命中机制级证据） | 这是相对 prior art 的关键区分特征；vivo 闭源内核（奇点内核）无机制级公开文档。缺失沉默→未确定，非反向证据 |

## 已检查文档清单
1. WebSearch ×4（见 _sources.md，query 留痕）
2. WebFetch https://www.cnblogs.com/vivotech/p/13680373.html —"非主流"的纯前端性能优化（仅变量缓存 / Object.freeze / preload 资源提示 / 并行加载，无元素级延迟显示）
3. WebFetch https://www.cnblogs.com/vivotech/p/15681665.html — vivo 浏览器快速开发平台实践-总览篇（后端低代码平台，与渲染调度无关）

## 最终判定 **第 4 档：公开资料不足（未达 60% 确认，无第 5 档正向反据）**

判定依据：vivo 浏览器真实存在且为 Chromium/Blink 内核（自有"奇点内核"），F1/F2/F5/F6 可凭 Chromium 内核标准行为作等同命中（4/7 ≈ 57%，且全为等同非字面）；但权 1 的三个核心区分限定 F3（≥2 规则×≥2 值×≥2 子集）、F4（父+嵌套子树优先级）、F7（相邻元素间预定延迟时长）均无任何公开机制级证据，内核闭源无法核实。检索未发现任何针对该候选的正向反向证据（"无图模式 / 极简模式"是内容过滤功能，属作用域不同的不同机制，非 verbatim 拒绝 F7），故 0 命中 ≠ 已排除，不入第 5 档。确认命中（含等同）4/7 < 60%，落第 4 档。

## 升级路径
- 若能取得 vivo"奇点内核"或省电/省流模式的技术白皮书 / 专利 / 源码片段，verbatim 证实：(a) 优先级规则集含 ≥2 条规则、产生 ≥2 档优先级、作用 ≥2 个元素子集（F3）；(b) 优先级子集按 DOM 父元素+其嵌套子节点组织（F4）；(c) 相邻元素显示之间存在一个预先设定的延迟时长（F7，最关键）——则可升至第 3 档（≥60% 确认）乃至第 1/2 档。
- 反向：若取得 vivo 内核文档 verbatim 表明其加载调度不含元素间预定延迟（仅懒加载/并行加载/按需），则 F7 转确认未命中，可降至第 5 档。

## 总结一句话
vivo 浏览器为 Chromium 内核、F1/F2/F5/F6 可作等同命中，但关键区分特征 F3/F4/F7（≥2 规则×子集、父+嵌套子树优先级、相邻元素预定延迟显示）因内核闭源无公开机制证据、亦无正向反据，确认命中 4/7 < 60%，**落第 4 档（公开资料不足，未确定）**。
