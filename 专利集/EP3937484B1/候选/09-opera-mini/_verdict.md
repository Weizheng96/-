# 09-opera-mini verdict

## 候选基本信息
- 名称：Opera Mini（Turbo/极速 / Mini-mode，服务端渲染压缩）
- 组织：Opera Limited
- 类型：产品
- 初判命中 F#（from _meta.json）：F1,F2,F5,F6,F7
- 专利公开（授权）日基准：2023-08-30
- 专利权 1 内核：**移动设备端**接收标记文档 → 端侧对元素按规则集分配优先级 → 按优先级定显示顺序 → 按序逐元素显示，且相邻元素显示间有预定延迟（client-implemented method for web browsing on a mobile device）。

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（端侧接收含多元素的标记文档并解析） | 未命中（有正向反据） | "Opera Mini fetches all content through a proxy server, renders it using the Presto layout engine, and reformats web pages into a format more suitable for small screens." / "A page is compressed, then delivered to the phone in an interpreted markup language called Opera Binary Markup Language (OBML)." | en.wikipedia.org/wiki/Opera_Mini | 端侧收到的是**服务端已渲染并压缩成 OBML 的页面快照**，而非原始 HTML 标记文档；端侧不解析多元素 markup 构建 DOM。 |
| F2（端侧基于规则集给元素分配优先级） | 未命中（有正向反据） | 同上：渲染与排版（reformats）发生在**代理服务器**侧（Presto）；端侧仅解释/显示 OBML。 | en.wikipedia.org/wiki/Opera_Mini ; wikitech.wikimedia.org/wiki/Performance/Proxy_browsers | 端侧无 DOM 元素级优先级分配环节。 |
| F3（≥2 规则 / ≥2 优先级值 / ≥2 子集） | 公开资料不足（未确定） | — | — | 端侧无元素级优先级机制，子结构无从谈起；无正向证据。 |
| F4（子集含父元素及其嵌套元素，DOM 树父子结构定优先级） | 公开资料不足（未确定） | — | — | OBML 为压缩后的展示格式，端侧未基于 DOM 父子嵌套结构排优先级。 |
| F5（基于优先级值确定元素显示顺序） | 未命中（有正向反据） | "the servers would fetch the full website, render it, compress it (using the OBML format), and then send a tiny version of the page to your phone." / "takes a snapshot of the page after it has been loaded ... and sends that to the phone." | en.wikipedia.org/wiki/Opera_Mini（含 OBML 条目）；搜索结果聚合 | 端侧显示的是服务端**快照**，无端侧"按优先级排序元素显示顺序"步骤。 |
| F6（按顺序逐元素显示渲染内容） | 公开资料不足（未确定） | — | en.wikipedia.org/wiki/Opera_Mini | OBML 逐步加载（progressively loaded）属传输层渐进，不等于权 1 的"端侧按元素优先级顺序显示"；无正向证据证明端侧按元素优先级序绘制。 |
| F7（相邻元素显示间预定延迟时间 — 关键区分特征） | 公开资料不足（未确定） | — | — | 未检索到 Opera Mini 端侧"相邻元素显示间插入预定延迟"的任何描述；服务端 2 秒脚本执行上限是服务端处理时限，非端侧元素间显示延迟。 |

## 已检查文档清单
- en.wikipedia.org/wiki/Opera_Mini（含 OBML 重定向/条目内容）— WebFetch
- wikitech.wikimedia.org/wiki/Performance/Proxy_browsers — WebFetch
- WebSearch 聚合：Opera 论坛、dev.opera 内容编写指南、Chen Hui Jing 博客、convert.guru OBML 说明

## 最终判定 **第 5 档：已排除**

判定依据：触发第 5 档 (c) 架构层级不同，并辅以 (a) 多个 F# 有针对该候选的 verbatim 正向反据。Opera Mini 的核心架构是**服务端代理渲染**——请求经 Opera 代理服务器，由服务端 Presto 引擎渲染整页并压缩为 OBML 二进制标记，再把"tiny version / 页面快照"发到手机；端侧仅解释/显示该压缩页面。这与权 1 主张的"**移动设备端**接收原始标记文档、在端侧对 DOM 元素按规则集分级、按优先级定显示顺序、相邻元素间预定延迟逐元素显示"处于**不同抽象层 / 不同架构层级**：优先级排序与渲染在云端、非端侧 DOM 元素级调度。F1/F2/F5 有 verbatim 正向反据（渲染/排版在服务器、端侧收快照），F3/F4/F6/F7 无任何正向命中证据。该判断基于针对 Opera Mini 自身的 verbatim 架构事实（Wikipedia/Wikitech），非单纯推断。

## 升级路径
不适用（第 5 档）。理论上若有公开来源证明 Opera Mini **端侧**（非服务端）对 OBML 内部元素做按优先级排序并以相邻元素间预定延迟逐个上屏，可重新评估 F5-F7，进而上抬档位；目前无此类来源。

## 总结一句话
Opera Mini 走服务端代理渲染 + OBML 压缩、端侧仅显示云端页面快照，与本专利"端侧 DOM 元素级优先级 + 相邻元素预定延迟显示"属不同架构层级，**落第 5 档（已排除）**。
