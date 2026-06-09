# 证据索引 — 12-tencent-wechat-webview

## Phase 1 — react 粗筛 WebSearch（串行）
1. `微信 内置浏览器 X5 TBS 渲染 H5 加载 优化`
   - 命中：X5/TBS 是腾讯基于 Webkit/Chromium 魔改的渲染内核（X5 1.x=webkit，2.x=blink，2020 后微信改用 XWEB）；30+ App 内置；同层播放器；静态集成。均为通用网页渲染/兼容性内容，无元素优先级 + 预定延迟显示机制。
   - 代表 URL：https://zhuanlan.zhihu.com/p/11843864537 ；https://newdocx.appcan.cn/app-engine/appcan-tencent-x5-core-engine
2. `微信 webview 省电 分级加载 延迟 渲染 优先级`
   - 命中：Skyline 渲染引擎（逻辑-渲染分离 + 并行 + GPU 合成）；WebView 预加载控制 handleWebviewPreload；首屏 FCP 优化、按需注入。均为减少初始化/并行渲染，非"相邻元素间预定延迟错峰显示"。
   - 代表 URL：https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/start_optimizeC.html
3. `WeChat builtin browser XWEB TBS rendering priority loading mechanism`
   - 命中：微信 Android 用 XWEB 引擎（基于 Mobile Chromium，定制 XWalk，V8 8.6，落后官方 Chrome 版本）；动态下载更新；通用 HTML 渲染 + JS 执行。无元素优先级 + 预定延迟显示机制公开细节。
   - 代表 URL：https://blog.talosintelligence.com/vulnerability-in-tencent-wechat-custom-browser-could-lead-to-remote-code-execution/ ；https://developers.weixin.qq.com/miniprogram/en/dev/framework/runtime/env.html

## Phase 2 — react 深抓 WebFetch（串行）
1. WebFetch https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/start_optimizeC.html
   - 结论：仅有"根据页面内容优先级，优先展示页面的关键部分，对于非关键部分或者不可见的部分可以延迟更新"+"渐进式的渲染"。无 ≥2 规则/≥2 档/≥2 子集（F3 未确定）；无 DOM 父+嵌套子树优先级子集（F4 未确定）；无相邻元素间"预定延迟时长"机制（F7 未确定——"延迟更新非关键内容"接近懒/条件更新，非固定逐元素延迟）。

## 工具受限说明
- TBS/X5/XWEB 内核闭源，渲染调度器内部机制（是否有元素级预定延迟、优先级子集挂 DOM 父子结构）无公开文档可核证 → F3/F4/F7 记"公开资料不足（未确定）"。
- 与候选 11（QQ 浏览器 X5）同属腾讯 TBS/X5/XWEB 同源内核；若 11 取得内核调度证据可旁证，但本候选按微信内置浏览器自身可核公开证据独立定档。
