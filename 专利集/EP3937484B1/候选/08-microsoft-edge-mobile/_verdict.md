# 08-microsoft-edge-mobile verdict

## 候选基本信息
- 名称：Microsoft Edge（移动版）
- 组织：Microsoft
- 类型：产品
- 初判命中 F#（from _meta.json）：F1,F2,F3,F5,F6
- 专利公开（授权）日：2023-08-30（时间窗基准）

> 关键事实：Edge 移动版基于 Chromium（Blink 渲染引擎），叠加微软自有的"睡眠标签 / 效率模式 / 能源节省"省电特性。需区分两层：(a) Chromium/Blink 通用平台能力（懒加载、fetchpriority、资源优先级调度）——Edge 继承，可作 F1-F6 等同证据来源；(b) Edge 自有省电特性——经查为**标签页级**（CPU/内存冻结、背景标签睡眠、降视频/动画流畅度），非元素间显示节奏。

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素的标记语言文档 | 命中（等同） | Edge 移动版基于 Chromium/Blink，请求并解析 HTML 构建 DOM（含多元素节点）——属浏览器内核固有行为；睡眠特性 "builds on Chromium's freezing technology" 佐证内核为 Chromium | https://support.microsoft.com/en-us/topic/learn-about-performance-features-in-microsoft-edge-7b36f363-2119-448a-8de6-375cfd88ab25 | 浏览器通用能力，等同 |
| F2 基于规则集给元素分配优先级值 | 公开资料不足（未确定） | Chromium/Blink 平台支持 `loading=lazy`、`fetchpriority`、priority hints（"fetchpriority attribute ... supported in ... Edge"）——Edge 继承。但这些为**资源加载优先级**且多由网页作者声明，未见 Edge 自身按规则集对 DOM 元素赋优先级值的公开技术披露 | https://web.dev/articles/browser-level-image-lazy-loading | Blink 等同可作部分支撑，但 Edge 侧无独立证据 |
| F3 ≥2 规则 / ≥2 优先级值 / ≥2 子集 | 公开资料不足（未确定） | 未检索到 Edge（或其引用的 Blink 调度）"至少两条规则、产生两档以上优先级、作用于至少两个元素子集"的公开技术描述 | — | 整数限定，无证据达下界 |
| F4 子集含"父元素 + 其嵌套元素"（DOM 子树） | 公开资料不足（未确定） | 未检索到 Edge 按 DOM 父子/嵌套子树组织优先级子集的公开披露；fetchpriority/lazy 为按单个资源/元素粒度，非父+嵌套子树整体 | — | 结构限定，无证据 |
| F5 基于优先级值确定元素显示顺序 | 公开资料不足（未确定） | Blink 资源调度按优先级排序加载（Edge 继承），可视为加载顺序排序；但是否据此"确定元素显示（display）顺序"无 Edge 侧明示证据 | https://web.dev/articles/browser-level-image-lazy-loading | 加载顺序 ≠ 显示顺序的字面映射，存疑 |
| F6 按该顺序显示各元素对应渲染内容 | 公开资料不足（未确定） | 浏览器渐进渲染按内核调度上屏；无 Edge 侧"按优先级确定的元素顺序逐元素显示"的明示证据 | — | 通用渐进渲染 ≠ 字面映射 F5→F6 链路 |
| F7 相邻元素显示间有"预定延迟时长" | 公开资料不足（未确定） | Edge 省电特性经查均为**标签页级**："pauses a tab's script timers, which minimizes CPU usage"、能源节省 "puts background tabs to sleep after 30 minutes"/"five minutes"、"reducing CPU and memory usage"、视频 "less smooth"。**针对标签页 CPU/内存与背景活动，非元素与元素之间的固定显示延迟。** 懒加载=进入视口才加载（非固定时延），fetchpriority=排序提示（非"上一个显示后等固定时长再显示下一个"） | https://support.microsoft.com/en-us/topic/learn-about-performance-features-in-microsoft-edge-7b36f363-2119-448a-8de6-375cfd88ab25 ; https://www.microsoft.com/en-us/edge/features/energy-saver | 关键区分特征。Edge 已知机制（标签级、懒加载、fetchpriority）均**非** F7 的"元素间预定延迟时长"——但属**不同机制/作用域语**，未构成针对元素级 F7 的 verbatim 正向拒绝；记未确定 |

## 已检查文档清单
1. Microsoft 官方支持：Learn about performance features in Microsoft Edge（睡眠标签 / 效率模式 / 能源节省 / 性能检测器）
2. Microsoft Edge 官方：Energy saver 特性页
3. web.dev：Browser-level image lazy loading（Chromium/Blink 平台能力，Edge 继承）
4. （检索覆盖）Edge 睡眠标签官方说明、fetchpriority 相关资料

## 最终判定 **第 4 档：公开资料不足，未确定（<60% 确认命中，无第 5 档正向反据）**

判定依据：
- F1 可凭 Edge 基于 Chromium/Blink 作等同命中；F2/F5 仅有 Blink 平台通用能力间接支撑，无 Edge 侧明示证据；F3/F4/F6/F7 均无公开证据达字面/等同。确认命中（F1）远 < 60%。
- 同时**不满足第 5 档（已排除）任一硬条件**：(a) 无针对该候选元素级 F7 的 verbatim 正向反据——Edge 省电特性为标签页级，属"不同机制 / 作用域语"，不算反向证据；(b) 候选真实存在且持续运营，证据非全部早于 2023-08-30；(c) Edge 基于 Chromium/Blink，与专利"移动端 web 浏览/渲染"为同一架构领域，非"架构不同"。
- 故落第 4 档而非第 5 档：0 命中或缺证据 ≠ 已排除；缺的是 F2-F7 的正向命中证据，而非排除证据。

## 升级路径（第 4 档）
- 若能取得 Edge / Chromium 内部渲染调度的工程文档或源码，证明其在**元素与元素显示之间插入固定/预定延迟时长**（而非仅按视口/优先级即时调度），且优先级按 DOM 父+嵌套子树、≥2 规则 ≥2 档 ≥2 子集组织——可升至第 3 档乃至更高。
- 重点取证 F7：区分"睡眠标签/效率模式（标签页 CPU/内存）"与"元素间预定显示延迟"二者本质不同；需找到后者的正面工程证据，方能确认而非升级臆测。
- 反向取证亦可：若 Edge/Chromium 公开文档明确其渲染为"尽快上屏、无人为元素间延迟"，则可构成 F7 正向反据，反而下调至第 5 档（已排除）。

## 总结一句话
Microsoft Edge 移动版基于 Chromium/Blink（F1 可作等同命中），但其自有省电特性为标签页级 CPU/内存管理，未见元素间"预定延迟显示"（F7）及规则化父+嵌套子树优先级（F3/F4）的公开正向证据，确认命中 <60% 且无正向反据，**落第 4 档（公开资料不足，未确定）**。

---
> 免责声明：本判定仅为技术特征比对的线索与证据链梳理，不构成"已构成侵权"的法律结论。
