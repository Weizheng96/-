# 06-brave-browser verdict

## 候选基本信息
- 名称：Brave Browser（Chromium 内核 Blink + 自有省流/拦截 + Energy/Memory/Data Saver）
- 组织：Brave Software
- 类型：产品
- 初判命中 F#（from _meta.json）：F1,F2,F3,F4,F5,F6
- 专利公开（授权）日：2023-08-30

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素的标记语言文档 | 命中（字面，继承 Blink） | Brave「is built on top of the open-source Chromium project. Brave adds features on top of what is already there」（Deviations Wiki，间接确认内核为 Chromium/Blink，HTML 解析+DOM 构建为引擎原生能力） | github.com/brave/brave-browser/wiki/Deviations-from-Chromium-(features-we-disable-or-remove) | Blink 原生解析 markup→DOM 即满足 F1 字面 |
| F2 基于规则集给元素分配优先级值 | 公开资料不足（未确定，倾向字面）| Blink 原生有资源加载优先级/fetchpriority/loading=lazy；但未见 Brave 自有「基于规则给元素分配优先级值」之公开 verbatim | 同上 / web.dev | F2 若以 Blink 原生 ResourceFetcher 优先级论可字面，但本候选(Brave)自有层未叠加此机制，归未确定 |
| F3 ≥2规则/≥2优先级值/≥2元素子集 | 公开资料不足（未确定） | 无 Brave 公开资料明示「≥2 条规则、≥2 优先级档、≥2 元素子集」结构 | — | 整数限定无正向证据，默认未确定 |
| F4 元素子集含父元素+其嵌套元素（DOM子树优先级） | 公开资料不足（未确定） | 无 Brave 公开资料明示按 DOM 父+嵌套子树组织优先级 | — | 结构限定无正向证据 |
| F5 基于优先级值确定显示顺序 | 公开资料不足（未确定） | Blink 原生有加载/绘制调度；无 Brave 自有 verbatim | — | 未确定 |
| F6 按该顺序显示各元素渲染内容 | 公开资料不足（未确定，倾向字面） | Blink 渐进式渲染为引擎原生；无 Brave 自有叠加 verbatim | — | 未确定 |
| F7 相邻元素显示间有「预定延迟时间」（关键区分特征） | 公开资料不足（未确定） | Brave 省电 verbatim：「Brave reduces its image capture rate and other background tasks」（Energy Saver，降帧/后台任务，非元素间定时延迟）；「deactivates tabs that you aren't currently using」（Memory Saver，标签页级）；Deviations Wiki 无任何渲染调度/元素间延迟改动 | support.brave.app/.../13383683902733 ; Deviations Wiki | Brave 自有省电=帧率/后台/标签/代理层，非「上一元素显示后延迟固定时长再显示下一元素」；Blink 渲染由 vsync 帧节拍驱动而非元素间预定时延，Brave 未叠加该机制。无正向反据（无 verbatim 排他），故记未确定而非反据 |

## 已检查文档清单
1. Brave Help Center — Memory and Energy Saver 合页（本地 energy_saver.html，curl 抓取）
2. brave/brave-browser Wiki — Deviations from Chromium（features we disable or remove）（WebFetch）
3. Brave Energy Saver 专页（13380606172557）— WebFetch 403，未取；同段 verbatim 由 #1 合页覆盖
4. WebSearch 命中的 Brave Data Saver/Lite Mode、社区延迟标签加载帖（旁证，未单独深抓）

## 最终判定 **第 4 档：<60%确认命中、无第5档正向反据>**

判定依据：Brave 内核为 Chromium/Blink，F1（及 F6）可凭引擎原生能力字面成立；但 F2-F5、F7 在 Brave **自有层**均无公开正向证据——尤其 F7 这一关键区分特征，Brave 自有省电机制（Energy Saver 降 image capture rate/后台任务、Memory Saver 停用标签、Data Saver 压缩代理）全部位于帧率/后台/标签/代理层，与权 1 要求的「相邻元素显示之间预定延迟时间 + DOM 子树优先级」机制不同质。确认字面命中 < 60%（仅 F1 稳、F6 倾向），但官方 Deviations Wiki 仅为「未叠加该机制」之缺失沉默，非针对 Brave 的 verbatim 正向排他拒绝，按判定纪律（缺失沉默/通用反推不算反向证据、0命中≠已排除）不入第 5 档，落第 4 档。

## 升级路径
- 提级至第 3 档需：在 brave-core 源码（github.com/brave/brave-core）grep 是否存在自有「按 DOM 父+嵌套子树规则分配优先级 + 元素间预定延迟显示」的 patch（如 renderer/painting/loading 相关）；若仅证实 Blink 原生 ResourceFetcher 优先级（fetchpriority/资源优先级），可论证 F2/F5 字面+F3 等同，但 F7「元素间预定延迟」仍是缺口。
- 入第 5 档（已排除）需：找到 Brave/Blink 源码 verbatim 证明渲染由 vsync 帧节拍驱动且结构性不存在「元素间预定延迟显示」机制（针对该候选的正向反据）。当前 Deviations Wiki 之缺失沉默不足以构成反据。

## 总结一句话
Brave 基于 Chromium/Blink，F1（及 F6）凭引擎字面可命中，但其自有省电（Energy Saver 降帧/后台、Memory Saver 停用标签、Data Saver 代理压缩）均非「元素级优先级+元素间预定延迟显示」，关键区分特征 F7 及 F2-F5 无 Brave 正向证据、亦无正向反据，落第 4 档。
