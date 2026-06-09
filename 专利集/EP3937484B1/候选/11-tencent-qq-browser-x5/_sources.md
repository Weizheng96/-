# 证据索引 — 11-tencent-qq-browser-x5

候选：QQ Browser (X5/TBS kernel) / Tencent ｜ 专利公开日基准：2023-08-30

## Phase 1 — WebSearch query 留痕（react 串行，每次 1 条）
1. `腾讯 X5内核 TBS 渲染 加载 优化 原理`
   - 命中：X5/TBS 是腾讯移动端浏览器内核，基于 Chromium/Chrome 开源项目优化；提速 30%+、省流 20%+；供微信/手机QQ/空间/QQ浏览器复用。确认真实产品。
2. `QQ浏览器 X5 内核 省电 分级加载 延迟 元素优先级`
   - 命中（腾讯云开发者社区 article/1083770）："资源优先级：希望在首屏内的资源可以快速加载下来，首屏外的资源优先级可以低一些，往后做一些延迟"；"目前大家在线上使用的是基于 Blink m53 的版本"。
3. `Tencent TBS X5 kernel rendering scheduling resource priority Blink energy saving`
   - 命中：X5 = Blink 分支（Blink 是 WebKit 分支）；提速/省流定位；无 F3/F4/F7 机制细节。
4. `腾讯 专利 网页 元素 优先级 分批 延迟 显示 渲染 省电 移动设备`
   - 未检索到腾讯自有"元素优先级 + 分批固定延迟显示"专利；命中 fetchpriority 优先级提示文章（article/2355175）。

## Phase 2 — WebFetch 留痕（react 串行）
- WebFetch https://cloud.tencent.com/developer/article/1083770
  - 资源优先级=按"首屏内/首屏外"位置划分（单一规则），未述档位数/嵌套结构；明确未提固定延迟分批显示机制；策略集中在并发/Socket 重用/预连接（异步并发，而非顺序延迟）；确认"将整体内核架构切换到了 Blink 内核……基于 Blink m53 的版本"。
- WebFetch https://cloud.tencent.com/developer/article/2355175
  - 使用 fetchpriority(high/low)/async/loading=lazy 等独立优先级提示作用于不同资源类型；优先级"非嵌套父子关系"；明确"完全不包含"定时器/固定延迟/分批延迟显示机制。

## 证据索引表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行 | 技术博客 | https://cloud.tencent.com/developer/article/1083770 | X5 切换到 Blink（m53）；资源优先级按首屏内/外划分，"往后做一些延迟"；策略偏异步并发 |
| 2 | 现行 | 技术博客 | https://cloud.tencent.com/developer/article/2355175 | fetchpriority/async/lazy 优先级提示；非嵌套父子；无固定延迟分批显示 |
| 3 | 现行 | 官方/百科 | https://www.tencentcloud.com/techpedia/109193 | X5 = Blink 分支；微信/手机QQ/空间/QQ浏览器内置；提速 30%+/省流 20%+ |

## 工具限制说明
- patents.google.com 本环境 SSL 可能不可达；改用 WebSearch 找腾讯自有专利，未检索到对应机制专利。
- X5/TBS 内核闭源，仅有营销/技术博客层面公开资料；腾讯自有改动（相对 Blink 基线）的渲染调度细节无公开机制文档可核验。
