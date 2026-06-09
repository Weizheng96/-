# 证据索引 — 06-brave-browser

公开（授权）日基准：2023-08-30

## Phase 1 — WebSearch（react 串行）
1. `Brave browser data saver power saving rendering element loading`
   - 命中：Brave Help Center「Memory and Energy Saver」「Energy Saver」；Browserfy 电池/数据节省说明；brave/brave-browser GitHub issues（能耗/省电）。
   - 信号：Brave 省电功能 = Energy Saver（降低 image capture rate + 其他后台任务）、Memory Saver（停用不活跃标签页）、Data Saver/Lite Mode（压缩代理）。均为 tab/帧率/代理层，未见元素级优先级或元素间延迟显示。
2. `brave-core lazy loading defer rendering delay element priority Chromium changes`
   - 命中：web.dev 浏览器级图片懒加载；Chromium Blog Lite mode 懒加载；brave/brave-browser Wiki「Deviations from Chromium」；Brave 社区延迟标签页加载帖。
   - 信号：Brave 相对 Chromium 改动以「禁用/移除」隐私相关功能为主，经 patch 实现；懒加载属 Chromium/Blink 原生（loading=lazy，进入视口前抓取），非"元素间预定延迟"。

## Phase 2 — WebFetch / curl（react 串行）
1. WebFetch `https://github.com/brave/brave-browser/wiki/Deviations-from-Chromium-(features-we-disable-or-remove)`
   - 结果：文档三大类（完全禁用的服务/功能、经 Brave 服务器代理的服务、修改的功能）中**均无**渲染调度、元素加载优先级分配、懒/延迟渲染、错峰/元素间延迟显示、DOM 子树优先级 任何条目；改动聚焦隐私/安全（遥测、Google 集成、API、cookie、referrer）。
   - 引用：「Brave does not appear to add custom element-priority or inter-element delay rendering mechanisms beyond standard Chromium/Blink functionality」。
2. WebFetch `https://support.brave.app/.../13380606172557-...Energy-Saver...` → HTTP 403。改用 curl 抓 Memory&Energy Saver 合页（见下）。
3. curl `https://support.brave.app/hc/en-us/articles/13383683902733-How-do-I-use-the-Memory-and-Energy-Saver-features-in-Brave` → 本地 energy_saver.html，本地 Grep 提取 verbatim。
   - Energy Saver verbatim：「To extend your device's battery, Brave reduces its image capture rate and other background tasks. When Energy Saver is on, it works automatically whenever your device is unplugged, or when your battery is low.」
   - Memory Saver verbatim：「deactivates tabs that you aren't currently using. When you access an inactive tab, it automatically reloads.」

## 工具受限说明
- Brave Energy Saver 官方专页（13380606172557）WebFetch 返回 403；已用 curl 抓同主题 Memory&Energy Saver 合页（13383683902733）获 Energy Saver 同段 verbatim，证据等价。
- 未逐文件深挖 brave-core 源码：官方「Deviations from Chromium」Wiki 已系统列出 Brave 全部增量改动且无渲染/元素延迟相关条目；如需提级再补 brave-core grep。

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行 | 官方帮助 | support.brave.app/.../13383683902733 (本地 energy_saver.html) | Energy Saver=降 image capture rate+后台任务；Memory Saver=停用非活跃标签 |
| 2 | 现行 | 官方 Wiki | github.com/brave/brave-browser/wiki/Deviations-from-Chromium-(features-we-disable-or-remove) | Brave 增量改动全为隐私/安全禁用项，无渲染调度/元素优先级/元素间延迟 |
