# 证据索引 — 16-vivo-browser（query 留痕）

## Phase 1 — WebSearch（react 串行，4 条）
1. `vivo浏览器 内核 省流 省电 渲染 加载 原理`
   - 命中：vivo 浏览器基于 Chromium / Blink 内核深度优化；有"极速模式 / 兼容模式"切换；"上网快 5 倍"、节省流量等宣传；标准 preload 机制。无元素级延迟显示机制。
   - https://www.cnblogs.com/vivotech/p/13680373.html ; https://www.zhihu.com/question/60009800 ; https://bbs.vivo.com.cn/newbbs/thread/5623343
2. `vivo browser power saving mode rendering element priority delay staggered loading`
   - 命中：仅返回通用 Chromium Fetch Priority / 资源优先级文档，无 vivo 专属延迟显示机制。
   - https://web.dev/articles/fetch-priority ; https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/fetchpriority
3. `vivo浏览器 省电模式 极简模式 无图模式 分级加载 延迟显示 错峰渲染 机制`
   - 命中：vivo 浏览器有"无图模式"（省流量）、"极简模式"（简化布局、去广告弹窗）；系统级超级省电；未见元素间预定延迟 / 错峰渲染机制。
   - https://bbs.vivo.com.cn/newbbs/thread/30020619 ; https://bbs.vivo.com.cn/newbbs/thread/39019005
4. `vivo互联网技术 浏览器 内核 渲染调度 优先级 加载顺序 element priority scheduler`
   - 命中：vivo 自研"奇点内核"（WebView 引擎）；系统级 UI 交互渲染优先级提升（触控响应优先级）；资源调度偏向前台应用；标准 preload。无元素级优先级 + 预定延迟显示机制。
   - https://www.cnblogs.com/vivotech/p/15681665.html ; https://www.cnblogs.com/vivotech/p/13680373.html

## Phase 2 — WebFetch（react 串行，2 条）
1. https://www.cnblogs.com/vivotech/p/13680373.html （"非主流"的纯前端性能优化）
   - 结论：仅讲变量缓存 / Object.freeze / preload-prefetch-preconnect 资源提示 / 并行加载。无 DOM 元素优先级排序 + 元素间预定延迟显示 + 父子树优先级子集。
2. https://www.cnblogs.com/vivotech/p/15681665.html （vivo 浏览器快速开发平台实践-总览篇）
   - 结论：讲后端低代码开发平台"后羿"，与浏览器渲染调度无关。无相关机制描述。

## 工具受限说明
无；WebSearch / WebFetch 均正常返回。vivo 浏览器内核（奇点内核）为闭源，机制级实现细节无公开文档，F3/F4/F7 缺机制证据。
