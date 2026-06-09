# 17-oppo-heytap-browser verdict

## 候选基本信息
- 名称：Heytap / OPPO 浏览器（com.heytap.browser）
- 组织：OPPO / Heytap（OPPO/OnePlus/realme 设备内置）
- 类型：产品
- 内核：Blink / Chromium（搜索确认 "renders web pages using the Blink engine"）
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6
- 专利公开（授权）日：2023-08-30（候选为现行在售产品，时间窗合规）

## 检索粗筛
见 _sources.md。4 条 WebSearch（串行）确认：产品真实存在、现行、Blink/Chromium 内核；但无任何公开资料披露其加载/渲染调度内部机制。系统级省电模式（ColorOS）属设备层（CPU 降频/降亮度），非权 1 的"浏览/渲染引擎层元素优先级 + 预定延迟显示"机制。Phase 2 无可抓机制 URL，未深抓（已在 _sources.md 说明）。

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 接收含多元素标记文档 | 命中（等同） | "renders web pages using the Blink engine"（Chromium 内核请求并解析 HTML → 构建含多元素 DOM 树，为浏览器固有行为） | https://brand.heytap.com/en/index.html | 内核标准行为等同；非 OPPO 自有改动 |
| F2 基于规则集给元素分配优先级 | 命中（等同） | Chromium/Blink 对资源与渲染按内置启发式分配 fetch/render priority（内核标准行为） | https://web.dev/articles/fetch-priority | 内核通用机制等同；非 OPPO 自有 verbatim 证据 |
| F3 ≥2 规则 / ≥2 优先级值 / ≥2 子集（整数限定） | 公开资料不足（未确定） | 无公开资料披露 OPPO 浏览器是否有 ≥2 条规则、≥2 档、≥2 子集的优先级机制 | — | 整数限定无法仅凭"内核存在优先级"确认下界；闭源缺机制细节 |
| F4 子集含父元素+其嵌套元素（DOM 树父子结构） | 公开资料不足（未确定） | 无公开资料披露其优先级是否挂在 DOM 父+嵌套子树结构上 | — | 结构限定无证据；闭源 |
| F5 基于优先级确定显示顺序 | 命中（等同） | Chromium 渲染/加载调度按 priority 排序出队（内核标准行为） | https://web.dev/articles/fetch-priority | 内核通用机制等同；非 OPPO 自有 verbatim 证据 |
| F6 按该顺序显示渲染内容 | 命中（等同） | Blink 渐进式渲染按调度顺序逐步绘制到窗口（内核标准行为） | https://brand.heytap.com/en/index.html | 内核通用机制等同 |
| F7 相邻元素显示间有"预定延迟时长"（关键区分特征） | 公开资料不足（未确定） | 无任何公开资料披露 OPPO 浏览器在相邻元素显示之间插入预定延迟时长机制 | — | 本专利相对 prior art 的最关键区分特征；无证据，且通用 Chromium 懒加载/异步加载≠"上一元素显示后等固定时长再显示下一元素"，不能反推命中 |

## 已检查文档清单
- Google Play com.heytap.browser 商店页
- HeyTap 官网（brand.heytap.com）
- udger / user-agents UA 列表（内核 = Blink）
- web.dev fetchpriority（Chromium 通用优先级行为，仅作内核等同推理背景）
- 多篇 OPPO/ColorOS 系统级省电模式文章（确认属设备层而非浏览器渲染层）

## 最终判定 **第 4 档：命中率不足（<60% 确认命中，且无第 5 档正向反据）**

判定依据：F1/F2/F5/F6 可凭 Blink/Chromium 内核标准行为作等同命中（4/7）；但权 1 的三个核心区分限定 F3（整数限定）、F4（DOM 父+嵌套子树结构限定）、F7（预定延迟时长——本专利最关键区分特征）均无公开机制证据，记"公开资料不足（未确定）"。确认命中仅约 57%（4/7），未达第 3 档 ≥60% 门槛；同时无任何针对该候选的 verbatim 正向反据（未检索到"无延迟机制""非父子树优先级"等正向拒绝），不满足第 5 档。0 命中以外的未确定不构成排除，故落第 4 档。注意：F1/F2/F5/F6 的等同均来自 Chromium 内核通用行为，并非 OPPO 自有改动证据；权 1 的发明点恰在 F3/F4/F7，而这三项正是证据缺口所在。

## 升级路径（第 3-4 档填）
- 升 3 档需：补充 ≥1 项 F3/F4/F7 的命中证据（任一项确认即达 5/7 ≥60%）。
- 关键取证方向：(a) 反编译 com.heytap.browser APK 或抓取其渲染/加载调度配置，查是否有 ≥2 条优先级规则、≥2 档、≥2 子集（F3）及是否按 DOM 父+嵌套子树组织（F4）；(b) 在 OPPO 设备上实测开启省流/省电模式时，相邻元素显示之间是否存在可观测的固定延迟时长（F7，区别于普通懒加载）；(c) 检索 OPPO/Heytap 自身专利或技术白皮书是否披露"元素间预定延迟显示"。
- 降 5 档需：取得针对该候选的正向反据（如官方/反编译确认其仅用 Chromium 原生异步加载、无任何元素间预定延迟、优先级不挂 DOM 父子树）。

## 总结一句话
Heytap/OPPO 浏览器为 Blink/Chromium 内核，F1/F2/F5/F6 可凭内核标准行为等同命中，但本专利三个核心区分限定 F3（≥2 规则/≥2 档/≥2 子集）、F4（父+嵌套子树优先级）、F7（相邻元素间预定延迟时长）均因闭源无公开机制资料而"未确定"，确认命中不足 60% 且无正向反据，**落第 4 档**。

---
免责声明：本报告仅产出技术比对线索与证据链，不构成"已构成侵权"的法律结论。
