# 证据索引 — 03-tech-gecko

## 检索粗筛 query 留痕（Phase 1，react 串行）
1. WebSearch: `Gecko Firefox resource scheduler priority loading HTML elements`
   → 命中官方 prioritization 文档 + IJERT 2013 论文 + fetchpriority bug。信号：Gecko 有 ClassOfService / fetchpriority 优先级机制（F2/F3/F5 正向）。
2. WebSearch: `Firefox Gecko rendering delay timer element display predetermined interval paint`
   → nglayout.initialpaint.delay（一次性初始绘制抑制）、content.notify.interval（解析批处理）。信号：延迟机制是页面级/解析级，非元素间错峰（F7 反向）。
3. WebSearch: `Gecko nsHttpConnectionMgr ClassOfService priority tail delay request scheduling`
   → tailing.enabled / tailing.delay-quantum（0–60000ms 可配）。信号：存在按 Tail 类的延迟，但作用于网络请求。
4. WebSearch: `Firefox source docs networking http tailing delay quantum tracker requests`
   → tailing 是延后 tracker/async 网络请求（600ms/20ms delay-quantum）；明示"delays network requests themselves, not display rendering"（F7 决定性反向证据）。

## 深抓 WebFetch 留痕（Phase 2，react 串行）
- WebFetch prioritization.html → ClassOfService 数值（Leader 1 / Tail 256 / TailAllowed 512 / TailForbidden 1024）、urgency 0–7、多规则（位置/属性/destination）；优先级按资源类型组织（F4 未获父+嵌套子树正向证据）。
- WebFetch IJERT PDF（WebFetch 无法解析二进制）→ 改用 curl 下载 + pdfplumber 提取文本：确认为 2013-05 学术提案（非 shipped），含父→子优先级下传规则但无预定元素间延迟。
- WebFetch tailing.html → 404（官方该路径不存在；改用作者博客）。
- WebFetch janbambas.cz tailing 博客 → verbatim 确认 tailing"delays network requests themselves, not display rendering"，只作用于 tracker/async。

## 工具受限说明
- IJERT PDF WebFetch 返回二进制不可读 → 已 curl 下载至本地 ijert-priority-gecko.pdf 并用 pdfplumber 提取（第3页 GBK 编码报错不影响关键文本）。
- 官方 tailing.html 路径 404 → 用 tailing 作者（Honza Bambas / janbambas.cz）原始博客替代，证据等效。

## 证据索引表
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | — | 官方源码文档 | https://firefox-source-docs.mozilla.org/networking/http/prioritization.html | ClassOfService/urgency 多规则多档优先级（F2/F3/F5 正向）；按资源类型组织（F4 无父+子树正向证据） |
| 2 | Firefox 57 (2017) | 作者博客（tailing 实现者） | https://www.janbambas.cz/firefox-57-delays-requests-tracking-domains/ | tailing 延后 tracker/async 网络请求，"delays network requests, not display rendering"（F7 决定性反向） |
| 3 | — | Bugzilla | https://bugzilla.mozilla.org/show_bug.cgi?id=180241 | nglayout.initialpaint.delay 一次性初始绘制抑制（非 F7 元素间错峰） |
| 4 | 2013-05 | 学术论文（提案，超时间窗） | 本地 ijert-priority-gecko.pdf / https://www.ijert.org/research/priority-based-loading-of-html-elements-for-gecko-rendering-engine-IJERTV2IS50077.pdf | 提案非 shipped Gecko；含父→子优先级（F4 雏形）但无预定元素间延迟（F7 缺）；2013 早于 2023-08-30 时间窗 |
