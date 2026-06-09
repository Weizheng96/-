# 10-opera-android verdict

## 候选基本信息
- 名称：Opera for Android（含电池保护模式 / 数据节省 / 广告拦截）
- 组织：Opera Limited
- 类型：产品
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6
- 专利公开（授权）日：2023-08-30（时间窗基准）
- 内核：Chromium / Blink（自有电池保护、数据节省、广告拦截层叠加于 Blink 之上）

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素标记文档 | 等同命中 | Opera 为 Chromium/Blink 内核浏览器，请求并解析 HTML 构建 DOM 树 | （Blink 架构继承，通用浏览器行为） | 架构继承可作等同证据；非 Opera 独有特征 |
| F2 基于规则集给元素分配优先级 | 等同命中 | Blink 资源调度器对资源/元素赋加载优先级（priority hints / fetchpriority / loading=lazy） | （Blink 架构继承） | 同上，继承自 Chromium |
| F3 ≥2规则/≥2优先级值/≥2子集 | 公开资料不足（未确定） | 无 Opera 公开文档明确"≥2条规则共同决定+≥2档+≥2子集" | — | 0命中≠已排除；仅未确定 |
| F4 子集=父元素+其嵌套元素（DOM子树优先级） | 公开资料不足（未确定） | 无 Opera 公开文档明确优先级挂在"父+嵌套子树"结构上 | — | Blink 多按资源类型/视口位置赋优先级，未见父+嵌套子树子集表述；未确定 |
| F5 基于优先级值确定显示顺序 | 等同命中 | Blink 按资源优先级排序加载/绘制队列 | （Blink 架构继承） | 继承自 Chromium |
| F6 按该顺序显示渲染内容 | 等同命中 | Blink 渐进式渲染，按优先级先后绘制 | （Blink 架构继承） | 继承自 Chromium |
| F7 相邻元素显示间预定延迟时长（关键区分特征） | 公开资料不足（未确定）〔主 agent 复核下调〕 | Opera 电池保护 verbatim 机制：「Reduced activity in background tabs」「Waking CPU less often due to more optimal scheduling of JavaScript timers」「Automatically pausing unused plug-ins」「Reduced frame rate to 30 frames per second」「Tuning video-playback parameters」；数据节省=服务器端图文压缩。文档未提及逐元素错峰渲染/元素间预定延迟。 | https://blogs.opera.com/desktop/2016/05/introducing-power-saving-mode/ ; https://en.wikipedia.org/wiki/Opera_Mini_Proxy | **复核说明**：上列电池保护手段（降帧率/CPU定时器/后台/网络压缩）与 F7 不在同一作用层，但"产品有省电手段 A"**不能推出**"它没有元素间延迟手段 B"（非互斥手段 + 文档没提）；Opera for Android 本身为端侧 Blink 浏览器（非服务端架构），不适用第 5 档(c)。按全局规则改记未确定 |

## 已检查文档清单
- https://blogs.opera.com/desktop/2016/05/introducing-power-saving-mode/（官方博客，电池保护 verbatim 机制，已 WebFetch）
- https://www.opera.com/features/battery-saver（官方功能页，WebSearch 摘要）
- https://blogs.opera.com/news/2016/09/data-saving-tips/（数据节省=服务器端压缩）
- https://en.wikipedia.org/wiki/Opera_Mini_Proxy（Opera Turbo=服务器端代理压缩，2019 移除）

## 最终判定

**第 4 档：公开资料不足（弱候选）**〔主 agent 复核：原 sub-agent 判第 5 档，复核下调〕

判定依据：F1/F2/F5/F6 因 Blink 内核继承可作等同命中（通用浏览器行为，非 Opera 自有特征）；F3/F4/F7 未确定。关键区分特征 F7：Opera 电池保护/数据节省经官方博客 verbatim 为「降帧率/CPU定时器/后台限活/服务器端压缩」等手段——这属"产品另有省电手段"，但**不能据此 verbatim 排他否定** Opera 端侧不存在元素间预定延迟显示（非互斥手段 + 文档没提）。Opera for Android 为端侧 Blink 浏览器、与专利同抽象层（非服务端架构），不适用第 5 档(c)；亦无针对 Opera 的正向反据，不适用第 5 档(a)。按"0 命中≠已排除"，F7 改记未确定，确认命中 <60% → 第 4 档（与同族 Blink 系候选对齐）。

## 升级路径（第 4 档）
- 核 Opera 相对 Chromium 的渲染/加载改动（若有公开仓库/技术博客）确认是否在 Blink 之上叠加"按 DOM 父+嵌套子树优先级 + 相邻元素间预定延迟显示"；若取到 Opera 自有文档 verbatim 排他否定该机制，F7 可升为"确认未命中（有正向反据）"→第 5 档；若发现该机制则坐实升档。

## 总结一句话
Opera for Android 凭 Blink 内核等同覆盖 F1/F2/F5/F6，但关键区分特征 F7（元素间预定延迟显示）无针对 Opera 的 verbatim 正向排他否定（电池保护属非互斥的另类省电手段、文档没提），按"0命中≠已排除"**落第 4 档（公开资料不足）**。
