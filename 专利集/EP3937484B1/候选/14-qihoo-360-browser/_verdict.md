# 14-qihoo-360-browser verdict

## 候选基本信息
- 名称：360 手机浏览器
- 组织：Qihoo 360
- 类型：产品
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6
- 公开度：低
- 一句话定位：360 移动浏览器（Chromium 内核 + 自有省流/安全层）
- 专利公开（授权）日：2023-08-30；时间窗：360 手机浏览器长期在售，在时间窗内有产品存在，时间不构成排除理由。

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（接收含多元素标记语言文档） | 公开资料不足（未确定，倾向等同） | 无 360 自有 verbatim；"360 是基于 Chromium 内核的浏览器之一" | https://developer.chrome.com/docs/chromium/renderingng-architecture | 作为 Chromium 系浏览器，解析 HTML→构建含多元素 DOM 属基线行为，可作 F1 等同证据；但 360 未 verbatim 披露 |
| F2（基于规则集给元素分配优先级值） | 公开资料不足（未确定） | 无 360 自有 verbatim；Chromium 上游有 Blink Scheduler / tile 优先级，但属上游通用机制非 360 改动 | https://www.chromium.org/developers/the-rendering-critical-path/ | 360 自有省流/省电层是否实现"基于规则集给元素赋优先级"无公开披露 |
| F3（≥2 规则 / ≥2 优先级档 / ≥2 元素子集） | 公开资料不足（未确定） | 无 | — | 整数+结构限定无任何公开机制细节可比对 |
| F4（子集含父元素及其嵌套元素 / DOM 子树优先级） | 公开资料不足（未确定） | 无 | — | DOM 父子/子树优先级结构无公开披露 |
| F5（基于优先级值确定显示顺序） | 公开资料不足（未确定，倾向等同） | 无 360 自有 verbatim；Chromium 渲染关键路径按优先级调度为基线 | https://www.chromium.org/developers/the-rendering-critical-path/ | 360 自有改动是否如此无 verbatim 披露 |
| F6（按顺序显示各元素渲染内容） | 公开资料不足（未确定，倾向等同） | 无 360 自有 verbatim；渐进式渲染为 Chromium 基线 | https://developer.chrome.com/docs/chromium/renderingng-architecture | 同上 |
| F7（相邻元素显示间有"预定延迟时长"机制） | 公开资料不足（未确定） | 无；360 公开仅提及"省电模式"功能名，无实现机制 | https://browser.360.cn/se/help/feature-detail_hxgn_shll.html | 关键区分特征；360 省电模式内部是否存在"上一元素显示后延迟固定时长再显示下一元素"无任何公开披露，无法确认 |

## 已检查文档清单
1. https://browser.360.cn/se/help/feature-detail_hxgn_shll.html（360 核心功能页，WebFetch；仅链接式提及"省电模式"）
2. https://browser.360.cn/se/help/kernel.html（360 内核控制 meta 说明，PC 双核切换，与移动渲染调度无关）
3. https://developer.chrome.com/docs/chromium/renderingng-architecture（Chromium 上游渲染架构，通用机制）
4. https://www.chromium.org/developers/the-rendering-critical-path/（Chromium 渲染关键路径，通用机制）

## 最终判定 **第 4 档：未确定（信息不足，无第 5 档反据）**

判定依据：360 手机浏览器真实存在且为 Chromium 内核（F1/F5/F6 可作基线等同的潜在依据），但产品闭源、无公开架构文档/技术白皮书披露其自有省电/省流层的内部渲染调度机制。决定命中与否的关键限定特征 F2/F3/F4 与最关键区分特征 F7（"相邻元素显示间预定延迟时长"）均无任何公开来源可比对，全部记"公开资料不足（未确定）"。同时不存在任何针对该候选的 verbatim 正向反据（无"360 不按优先级渲染""无元素间延迟"之类反向陈述），时间窗也合规，故不满足第 5 档排除条件（0 命中 ≠ 已排除）。确认命中比例 <60%（仅 F1/F5/F6 为"倾向等同"且无 360 自有 verbatim，F2/F3/F4/F7 全未确定），亦不足第 3 档（需 ≥60% 确认命中），故落第 4 档。

## 升级路径
- 取 360 手机浏览器安装包/APK 反编译或抓取其内核版本与自有渲染调度模块，确认 F2/F3（是否存在 ≥2 条规则、≥2 优先级档、≥2 元素子集的优先级分配逻辑）。
- 查 Qihoo 360 是否有对应的省电/分级加载技术专利或工程博客，定位 F4（DOM 父+嵌套子树优先级）与 F7（预定延迟时长）是否存在。
- 实测：在弱网/省电模式下用性能面板观测相邻元素上屏是否存在固定时间间隔（验证 F7）。

## 总结一句话
360 手机浏览器真实在售且为 Chromium 内核，但闭源无公开机制细节，关键特征 F2/F3/F4/F7 全部"公开资料不足（未确定）"、又无任何正向反据，落第 4 档（未确定，待反编译/实测升级）。
