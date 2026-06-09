# 证据索引 — 15-xiaomi-mi-browser（query 留痕）

候选：Mi Browser / Mint Browser（Xiaomi）｜专利公开日基准 2023-08-30

## Phase 1 — react 粗筛 WebSearch
1. `Xiaomi Mi Browser Mint Browser data saver rendering loading feature`
   - 结论：data saver = 屏蔽广告 / 限制图片加载（无图模式）；轻量内核。无元素优先级 / 延迟显示机制。
   - 来源：https://www.xda-developers.com/mint-browser-xiaomi-lightweight/ ; https://www.digit.in/news/apps/xiaomi-mint-lightweight-browser-with-dark-mode-voice-search-data-saver-feature-and-more-launched-for-45465.html
2. `Mi Browser Chromium kernel based engine version Xiaomi browser rendering engine`
   - 结论：Mi Browser 为 Chromium 内核、Blink 渲染引擎，预装于 MIUI。→ 通用加载管线可作 F1/F2/F5/F6 等同基础。
   - 来源：https://trust.mi.com/docs/miui-privacy-white-paper-global/4/7 ; https://www.guidingtech.com/mi-browser-vs-chrome-difference/
3. `小米浏览器 省流 省电 分级加载 元素 优先级 延迟显示`
   - 结论：小米自有能力 = 无图模式、云加速 / 省流（流量约 −40%）、MiCT 网页秒开引擎（预热 / 预加载 WebView）。未见"分级加载 / 元素优先级 / 延迟显示"具体技术披露。
   - 来源：https://dev.mi.com/xiaomihyperos/MICT
4. `Mint Browser Xiaomi removed delisted Google Play discontinued status 2024 2025`
   - 结论：Mint Browser 当前仍在 Google Play 上架（com.mi.globalbrowser.mini），在用状态成立，时间窗合规。
   - 来源：https://play.google.com/store/apps/details?id=com.mi.globalbrowser.mini

## Phase 2 — react 深抓 WebFetch
A. https://dev.mi.com/xiaomihyperos/MICT （MiCT 秒开引擎官方文档）
   - verbatim：「通过小米浏览器内核，提供网页预热及预加载能力，提升网页打开速度及加载成功率」「无需跳转浏览器，直接在应用内打开网页」
   - 机制为 WebView 级预热 / 预加载 / 状态共享，**非**元素级优先级调度；无父+嵌套子树优先级，无相邻元素预定延迟。
B. https://www.xda-developers.com/mint-browser-xiaomi-lightweight/ （Mint Browser 评测）
   - verbatim：「Mint Browser features data compression and allows you to configure even more from the settings.」
   - 仅数据压缩 / 可配置项（禁 cookie、关 JS、拦弹窗、UA 切换），无元素优先级 / DOM 父子排序 / 元素间预定延迟披露。

## 工具受限说明
- 无（WebSearch / WebFetch 均正常返回）。
- Mi Browser / Mint Browser 为闭源商业产品，F3 / F4 / F7 的内核实现细节无公开技术文档，属"公开资料不足（未确定）"，非工具受限。
