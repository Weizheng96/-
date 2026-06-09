# 04-google-chrome-lite-mode verdict

## 候选基本信息
- 名称：Chrome Lite mode / Data Saver（含离屏图片/iframe 自动懒加载、代理压缩）
- 组织：Google
- 类型：产品
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6, F7
- 专利公开（授权）日：2023-08-30（时间窗基准）

## 关键事实（时间窗）
- Chrome Lite mode（前身 Data Saver）于 **2022-03-29 随 Chrome M100 稳定版关闭**（Google 官方公告原文："On March 29th, 2022, with the release of Chrome M100 to the stable channel, we'll turn off Lite mode"，公告发布日 2022-02-23 / 2022-02-26）。
- 本候选赖以"自动懒加载离屏图片/iframe"的能力是 **Lite mode 专属特性**（Chromium 博客 2019-10-24 引入，仅对开启 Lite mode 的用户生效）。该模式在专利公开日 2023-08-30 之前已整体下线、不再分发/在用。
- 因此本候选的相关功能在专利公开日时已不再作为在用产品存在 → 命中 **第5档(b)**（全部可核实证据材料均早于 2023-08-30，且功能已于公开日前停用）。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注（含证据发布日期） |
|----|------|---------------|-----|------------------------|
| F1 | 未确定 | Chrome/WebView 解析 HTML 构建 DOM 含多元素——浏览器通用能力，文档未就 Lite mode 单独描述 | — | 通用能力可推定，但与本候选特异机制无关 |
| F2 | 部分（懒加载优先级） | "Images below the viewport are loaded with a lower priority, but they're still fetched as the page loads."（web.dev，2019 起） | https://web.dev/articles/browser-level-image-lazy-loading | 仅"视口下方=低优先"二值，非规则集分级 |
| F3 | 未命中 | 懒加载触发为单一规则——按"与视口的距离阈值"决定（4G 1250px / 3G 2500px），仅"在/不在阈值内"二值 | https://web.dev/articles/browser-level-image-lazy-loading | F3 要求 ≥2 条规则 / ≥2 档优先级 / ≥2 子集；此处为单一视口距离规则，整数限定不满足 |
| F4 | 未命中 | "the lazy-loading mechanism addresses individual images based solely on their viewport distance"——按单张图片处理，无按 DOM 父+嵌套子树组织优先级 | https://web.dev/articles/browser-level-image-lazy-loading | 结构限定（父元素+其嵌套元素子集）未见 |
| F5 | 部分 | 低优先图片"fetched as the page loads"/滚动近时加载——存在加载先后，但非按优先级值显式排序的"显示顺序" | https://web.dev/articles/browser-level-image-lazy-loading | 与 F5 字面"基于优先级值确定显示顺序"不严格对应 |
| F6 | 部分 | 渐进渲染/滚动近视口时加载并显示 | https://web.dev/articles/browser-level-image-lazy-loading | 通用渐进渲染 |
| F7 | **未命中（正向反据）** | "Images far below the device viewport are only fetched when the user scrolls near them"；触发依"distance-from-viewport thresholds"（4G 3000→1250px，3G 4000→2500px）——**按与视口的距离/滚动位置触发，非元素间预定延迟时长**（web.dev，2019 起） | https://web.dev/articles/browser-level-image-lazy-loading | F7 要求"上一元素显示后延迟一个 predetermined delay time 再显示下一元素"。本候选机制为"进入/接近视口才加载"——正是专利 [0057] 明确区分的普通懒加载，**机制不同**：等同三要素（手段=视口距离阈值 vs 预定定时器；功能=按需省流量 vs 错峰省功耗；效果不同）均不一致，不构成等同。此为针对本候选 verbatim 的正向反向证据。 |

## 已检查文档清单
- Chromium Blog "Automatically lazy-loading offscreen images & iframes for Lite mode users"（2019-10-24，已 curl 下载本地副本 chromium-blog-lazyload-2019.html，正文为 Blogger JS/CSS 壳未渲染，机制以 web.dev 同源文档为准）
- web.dev "Browser-level image lazy loading for the web"（懒加载触发机制权威说明）
- chromeunboxed.com "Chrome for Android 'Data Saver' is being deprecated"（2022-02-26，下线时间）
- ghacks.net "Google ends Lite Mode data saving feature for Chrome on Android"（2022-02-23，官方下线公告原文）

## 最终判定 **第5档：已排除**

判定依据：
1. 时间窗（主因，第5档(b)）：本候选赖以成立的"Lite mode 自动懒加载离屏图片/iframe"是 Lite mode 专属特性，而 Lite mode 已于 2022-03-29（Chrome M100）整体关闭、停止分发，早于专利公开日 2023-08-30 约 17 个月；公开日时该功能已不作为在用产品存在。
2. 机制反据（独立第5档(c)，F7 正向未命中）：即便不计时间窗，Chrome 懒加载按"与视口距离阈值/滚动位置"触发（"only fetched when the user scrolls near them"），而非 F7 限定的"相邻元素显示间插入一个 predetermined delay time"；同时 F3（≥2 规则/≥2 档/≥2 子集）、F4（父+嵌套子树优先级）均无证据支持。

两条理由各自独立支撑"已排除"，互为印证。

## 升级路径
不适用（第5档）。

## 总结一句话
Chrome Lite mode 的自动懒加载按"与视口距离阈值/滚动位置"触发（非 F7 的预定元素间延迟），且该 Lite-mode 专属功能已于 2022-03-29（Chrome M100）在专利公开日 2023-08-30 前整体下线，机制不符 + 时间窗不合规双重支撑——**落第5档（已排除）**。
