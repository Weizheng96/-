# 12-tencent-wechat-webview verdict

## 候选基本信息
- 名称：微信内置浏览器（TBS/X5，2020 后为 XWEB 内核）
- 组织：Tencent
- 类型：产品
- 初判命中 F#（from _meta.json）：F1, F2, F3, F5, F6
- 专利公开（授权）日：2023-08-30（时间窗基准）
- 时间状态：微信内置浏览器为持续在用的活跃产品（2023-08-30 之后仍在运营、更新），时间窗合规 → 不构成第 5 档 (b)。

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素的标记语言文档 | 命中 | 微信内置浏览器（XWEB，基于 Mobile Chromium）"supporting the rendering of HTML and the execution of JavaScript"；作为通用 WebView 请求并解析 H5/HTML 页面构建 DOM 树 | https://blog.talosintelligence.com/vulnerability-in-tencent-wechat-custom-browser-could-lead-to-remote-code-execution/ | 通用 webview 必然接收并解析含多元素的 markup 文档，字面满足 |
| F2 基于规则集给元素分配优先级值 | 公开资料不足（未确定） | "根据页面内容优先级，优先展示页面的关键部分，对于非关键部分或者不可见的部分可以延迟更新" | https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/start_optimizeC.html | 该文为小程序开发者指引层"内容优先级"概念，是否对应内核给 DOM 元素赋"优先级值"的规则化机制未公开；TBS/XWEB 内核闭源 |
| F3 ≥2 规则 / ≥2 优先级档 / ≥2 子集 | 公开资料不足（未确定） | 同上，仅"关键/非关键(不可见)"二分概念，未见 ≥2 条规则、≥2 档优先级、≥2 元素子集的机制描述 | 同上 | 整数限定下界以下信息缺失 → 默认未确定（非排除） |
| F4 优先级子集 = DOM 父元素 + 其嵌套元素 | 公开资料不足（未确定） | 无任何公开文档描述优先级按 DOM 父子/嵌套子树组织 | — | 内核闭源，无可核证据 |
| F5 基于优先级值确定元素显示顺序 | 公开资料不足（未确定） | "渐进式的渲染，根据页面内容优先级，优先展示页面的关键部分" | https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/start_optimizeC.html | "优先展示关键部分"是开发者层概念性表述，是否为内核按优先级值排序显示队列未公开 |
| F6 按该顺序显示各元素对应渲染内容 | 公开资料不足（未确定） | "渐进式的渲染" | 同上 | progressive rendering 概念存在，但未证实是"按 F5 确定顺序逐元素显示" |
| F7 相邻元素显示间有"预定延迟时长" | 公开资料不足（未确定） | "对于非关键部分或者不可见的部分可以延迟更新" | 同上 | 关键区分特征。该表述接近懒/条件更新（非关键、不可见才延迟），非"上一元素显示后等待固定时长再显示下一元素"的预定逐元素延迟；无公开证据证实存在 predetermined delay time 机制 |

## 已检查文档清单
1. 知乎《微信 H5 兼容性测试理论和实践经验》— X5/TBS/XWEB 内核版本与兼容性背景
2. AppCan《腾讯 X5 内核引擎》— X5 内核通用渲染说明
3. Talos Intelligence — WeChat custom browser（XWEB 基于 Mobile Chromium / XWalk）架构与动态下载
4. 微信开放文档《运行环境》(env) — Android XWEB 渲染、V8 逻辑层
5. 微信开放文档《首屏渲染优化》(start_optimizeC) — 内容优先级、渐进式渲染、延迟更新非关键内容（Phase 2 WebFetch 重点核证）

## 最终判定

**第 4 档：证据不足（<60% 确认命中，且无第 5 档正向反据）**

判定依据：仅 F1 字面确认命中（通用 webview 必然接收解析多元素 markup）。F2/F5/F6 在微信开放文档存在"内容优先级 + 渐进式渲染 + 延迟更新非关键内容"的概念性表述，但停留在开发者指引层、未证实为内核级规则化机制，记未确定；F3（≥2 规则/档/子集）、F4（DOM 父+嵌套子树优先级结构）、F7（相邻元素预定延迟时长这一最关键区分特征）均无公开可核证据，且 TBS/X5/XWEB 内核闭源无法验证。确认命中仅 1/7（<60%），未达第 3 档；但不存在任何针对本候选的 verbatim 正向反据（无文档说"不做元素优先级"或"无逐元素延迟"），故不落第 5 档（公开资料不足 ≠ 已排除，0 命中亦 ≠ 已排除）。

## 升级路径（第 3-4 档填）
- 取得微信 XWEB/TBS 内核渲染调度器的反编译/源码或腾讯内部技术披露，核证：(a) 是否对 DOM 元素按 ≥2 条规则赋 ≥2 档优先级（F2/F3）；(b) 优先级子集是否挂 DOM 父+嵌套子树结构（F4）；(c) 相邻元素显示间是否插入 predetermined delay time（F7，最关键）。
- 旁证：候选 11（QQ 浏览器 X5）同属腾讯 TBS/X5/XWEB 同源内核，若 11 取得内核级调度证据，可作为本候选同源旁证（但仍须本候选自身可核证据方能升档）。
- 若内核确为基于 Chromium/Blink 标准渲染（无定制逐元素预定延迟），则 F7 将转为正向反据，候选下沉第 5 档。

## 总结一句话
微信内置浏览器（TBS/X5/XWEB）仅 F1 字面命中、其余因内核闭源 + 公开文档仅停留在"内容优先级/渐进式渲染/延迟更新非关键内容"概念层而记未确定（关键区分特征 F7 无证据），无正向反据，落第 4 档（证据不足）。
