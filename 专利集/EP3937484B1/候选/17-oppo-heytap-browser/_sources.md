# 17-oppo-heytap-browser sources（query 留痕）

候选：Heytap / OPPO 浏览器（com.heytap.browser，OPPO/OnePlus/realme 内置，Blink/Chromium 内核）
专利公开（授权）日基准：2023-08-30

## Phase 1 — react 粗筛 WebSearch（串行，4 条）

1. `OPPO浏览器 Heytap浏览器 内核 省流 渲染 加载 原理`
   - 命中：包名 com.heytap.browser；Google Play / 各下载站 / 开发者社区帖。
   - 无内核加载/渲染机制细节。仅确认产品存在且为系统内置浏览器。

2. `Heytap OPPO browser com.heytap.browser Chromium data saver rendering feature`
   - 命中：Google Play、HeyTap 官网、udger/user-agents UA 列表、APKMirror。
   - 确认：HeyTap 为 OPPO/OnePlus/realme 提供官方互联网服务；浏览器使用 **Blink 引擎**（Chromium 内核）。
   - 无 data saver / 渲染机制实现细节。

3. `OPPO浏览器 省电模式 省流模式 分级加载 延迟 渲染优先级 原理`
   - 命中：均为 OPPO **系统级**（ColorOS）省电模式文章（CPU 降频 / 降亮度 / 单 App 策略），非浏览器渲染层。
   - 无浏览器"分级加载 / 元素间延迟 / 渲染优先级"机制证据。

4. `"heytap" OR "OPPO" browser engine source code Blink modification rendering priority lazy load patent`
   - 命中：Chromium Blink LazyLoad / fetchpriority 通用文档（web.dev、debugbear 等）、若干第三方懒加载专利、oppo-source GitHub 组织（无浏览器内核仓库）。
   - 无 OPPO/Heytap 对 Blink 的自有改动证据，无相关浏览器内核源码或机制说明。

## Phase 2 — 深抓

未执行 WebFetch：Phase 1 未产出任何承载 F3/F4/F7 机制细节的强 URL（全部为下载站 / UA 列表 / 系统级省电文章 / Chromium 通用文档）。该候选为闭源产品，无公开开发者文档披露其加载/渲染调度内部机制，深抓无可抓的机制来源。F1-F6 的判断基于 "Blink/Chromium 内核标准行为" 等同推理（通用事实，无需抓取确认）；F3/F4/F7 缺机制证据，记 "公开资料不足（未确定）"。

## 工具受限说明
- 无工具受限；WebSearch 正常返回。属 "目标候选闭源、无机制级公开资料"（证据不足），而非工具受限。

## 主要参考 URL
- https://play.google.com/store/apps/details?id=com.heytap.browser
- https://brand.heytap.com/en/index.html
- https://udger.com/resources/ua-list/browser-detail?browser=HeyTap+Browser
- https://web.dev/articles/fetch-priority （Chromium 通用 fetchpriority 行为，仅作 F2/F5 内核等同推理背景）
