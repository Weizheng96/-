# 09-opera-mini 检索留痕

候选：Opera Mini（Turbo/极速 / Mini-mode，服务端渲染压缩） | vendor：Opera Limited
专利公开（授权）日基准：2023-08-30

## Phase 1 — react 粗筛 WebSearch（串行）

1. `Opera Mini server-side rendering OBML compression how it works`
   - 命中：Wikipedia (Opera Mini / OBML)、Wikitech Proxy browsers、dev.opera 内容编写指南、Chen Hui Jing 博客、Opera 论坛
   - 要点：请求经 Opera 代理服务器 → 服务端用 Presto 引擎**渲染**整页 → 压缩成 OBML（Opera Binary Markup Language 二进制标记）→ 发送"tiny version"到手机；端侧仅解释/显示 OBML。服务端"takes a snapshot of the page after it has been loaded, pauses all running scripts, and sends that to the phone"。
2. `Opera Mini client display OBML page server renders device shows compressed page`
   - 要点确认：服务器 fetch 整站 → render → compress(OBML) → 发送页面快照；端侧显示快照，**非**端侧 DOM 元素级渲染。

## Phase 2 — react 深抓 WebFetch（串行）

3. WebFetch https://en.wikipedia.org/wiki/Opera_Mini
   - verbatim: "Opera Mini fetches all content through a proxy server, renders it using the Presto layout engine, and reformats web pages into a format more suitable for small screens."
   - verbatim: "A page is compressed, then delivered to the phone in an interpreted markup language called Opera Binary Markup Language (OBML) supported by Opera Mini."
   - 无任何端侧 DOM 解析 / 元素级优先级排序 / 元素间预定延迟显示的描述。
4. WebFetch https://wikitech.wikimedia.org/wiki/Performance/Proxy_browsers
   - verbatim: "the rendering engine used is Opera Presto"（Mini-mode 远程浏览器，服务端渲染）；代理"before it sends the responses back to the client browser, it tries to minimize the content by adding compression"。
   - 未描述端侧做 DOM 元素优先级排序或预定延迟。

## 工具/资料限制
- 未检索到 Opera Mini 端侧实现"元素级按优先级错峰、相邻元素间预定延迟显示"的任何公开来源。多个权威来源（Wikipedia / Wikitech）一致表明端侧仅解释/显示服务端渲染并压缩后的 OBML 页面，非端侧 DOM 级渲染调度。
