# 证据索引 — 04-google-chrome-lite-mode

## Phase 1 — react 粗筛（WebSearch，串行）
1. `Chrome Lite mode Data Saver lazy loading offscreen images`
   - 命中：Chromium Blog 2019-10-24（Lite mode 用户自动懒加载离屏图片/iframe）；web.dev browser-level lazy loading；ghacks；css-tricks 等。
   - 关键信号：Lite mode 自动懒加载 = "load when scrolling into view"（进入/接近视口才加载）；摘要明确 "Lite mode and loading='auto' have been deprecated"。
2. `Chrome Lite mode deprecated timeline 2022 2023 end of life Data Saver removed`
   - 命中：chromeunboxed / ghacks(2022) / androidpolice / makeuseof / techrepublic / xda。
   - 关键信号：Lite mode 于 2022-03-29 随 Chrome 100 稳定版关闭。

## Phase 2 — react 深抓（WebFetch / curl，串行）
1. WebFetch https://blog.chromium.org/2019/10/automatically-lazy-loading-offscreen.html
   - 仅取到发布日 2019-10-24；正文为 Blogger JS/CSS 壳，机制段未渲染。
   - 兜底：`curl -ksSL -A "Mozilla/5.0 ..."` 下载本地副本 chromium-blog-lazyload-2019.html；strip 后仍为模板 CSS，正文未分离 → 机制以 web.dev 同源权威文档替代。
2. WebFetch https://chromeunboxed.com/chrome-for-android-lite-mode-deprecation
   - 发布日 2022-02-26；下线时间 "March 29, 2022 / Chrome 100"。
3. WebFetch https://web.dev/articles/browser-level-image-lazy-loading
   - 机制权威：触发按 distance-from-viewport thresholds（4G 3000→1250px，3G 4000→2500px），"only fetched when the user scrolls near them"；按单张图片处理，无 DOM 父+嵌套子树优先级，无元素间预定延迟。
4. WebFetch https://www.ghacks.net/2022/02/23/google-ends-lite-mode-data-saving-feature-for-chrome-on-android/
   - 发布日 2022-02-23；官方原文 "On March 29th, 2022, with the release of Chrome M100 to the stable channel, we'll turn off Lite mode"。

## 证据时间一览（相对专利公开日 2023-08-30）
| 证据 | 日期 | 与 2023-08-30 关系 |
| --- | --- | --- |
| Chromium Blog 自动懒加载引入 | 2019-10-24 | 早于 |
| Lite mode 下线公告（ghacks/chromeunboxed） | 2022-02 | 早于 |
| Lite mode 实际关闭（Chrome M100） | 2022-03-29 | 早于（约 17 个月） |
| web.dev 懒加载机制文档 | 2019 起 | 早于 |

## 工具受限说明
- Chromium 博客正文为 Blogger 动态模板，WebFetch 与 curl 均仅取到 CSS/JS 壳，正文机制段未渲染；已用同源、同机制的 web.dev 官方文档替代，结论不受影响。
