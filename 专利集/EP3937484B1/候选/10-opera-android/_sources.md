# 证据索引 — 10-opera-android（query 留痕）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| S1 | 2016 | 官方功能页/博客 | https://blogs.opera.com/desktop/2016/05/introducing-power-saving-mode/ | 电池保护 verbatim 机制：降帧率至30fps / JS定时器优化调度让CPU少唤醒 / 暂停未用插件 / 调视频参数+强制硬件加速 / 停主题动画 / 限后台标签活动。无逐元素错峰渲染或元素间预定延迟。 |
| S2 | 2016 | 官方博客 | https://blogs.opera.com/news/2016/09/data-saving-tips/ | 数据节省=服务器端压缩图文。 |
| S3 | 2009/2019 | 百科/媒体 | https://en.wikipedia.org/wiki/Opera_Mini_Proxy | Opera Turbo=服务器端HTTP代理压缩图文，客户端正常渲染；2019移除。 |

## Phase 1 — react 粗筛 WebSearch（3 条，串行）
1. `Opera for Android battery saver data savings how it works rendering`
   - 结论：电池保护=后台标签限活/JS定时器调度/暂停插件/视频参数；数据节省=服务器端图文压缩。均非元素间显示延迟。
2. `Opera Android battery saver mechanism CPU network JavaScript timers background tabs`
   - 结论：机制 verbatim=降帧率30fps / JS定时器优化调度CPU少唤醒 / 暂停插件 / 调视频参数 / 停背景动画 / 限后台标签。安卓端电池保护多依赖系统级电池设置。
3. `Opera Turbo data compression server-side proxy how it works client rendering`
   - 结论：Turbo=服务器端HTTP代理压缩图文，客户端正常渲染；不做元素优先级/元素间延迟；2019移除。

## Phase 2 — react 深抓 WebFetch（1 条）
1. WebFetch https://blogs.opera.com/desktop/2016/05/introducing-power-saving-mode/
   - verbatim：Reduced activity in background tabs / Waking CPU less often due to more optimal scheduling of JavaScript timers / Automatically pausing unused plug-ins / Reduced frame rate to 30 frames per second / Tuning video-playback parameters + 强制硬件加速编解码 / Paused animations of browser themes
   - 明确：文档不含"逐元素错峰渲染 / 元素间预定延迟"机制。

## 工具受限说明
无受限；WebSearch/WebFetch 均正常返回。
