# 证据索引 — 07-samsung-internet

专利公开（授权）日基准：2023-08-30。Samsung Internet 当前在售版本远晚于该日，时间窗满足。

## Phase 1 — react 粗筛（WebSearch，串行）

| # | 类型 | URL | 命中要点 |
| --- | --- | --- | --- |
| 1 | WebSearch query | `Samsung Internet browser data saver power saving rendering loading feature` | 基于 Blink 渲染引擎；省电/省流量 = 数据压缩、移除非必要图片、限制后台数据、超级省电模式（灰度简化主题）、Night Mode。未见"元素间预定延迟显示"机制 |
| 2 | WebSearch query | `Samsung Internet high contrast data saver image defer rendering developer blog` | High Contrast Mode（v6.2 起，无障碍白字黑底）、Night/Dark Mode、Responsive Design——均为显示外观/无障碍特性，非元素优先级+错峰延迟 |
| 3 | WebSearch query | `Samsung Internet browser staggered rendering element priority predetermined delay loading scheduler` | **0 有效命中**——仅 troubleshooting / 用户 bug 帖 / Web Engine 规格页，无任何错峰渲染 / 元素优先级 / 预定延迟 / 加载调度器的三星自有实现说明 |

## Phase 2 — react 深抓（WebFetch，串行）

| # | URL | 命中要点 |
| --- | --- | --- |
| 1 | https://www.samsung.com/ae/support/mobile-devices/what-is-the-data-saver-feature/ | Data Saver = "prevents some apps from sending or receiving data in the background"，限制后台数据；明确不涉及 DOM 元素渲染优先级 / 逐元素显示延迟 / 排序规则 |
| 2 | https://developer.samsung.com/internet/android/overview.html | 概览页未描述自定义渲染调度器 / 按规则给元素赋优先级 / 父+嵌套子集优先级 / 元素间预定延迟 |
| 3 | https://medium.com/samsung-internet-dev/samsung-internet-v6-2-now-stable-ab7f95ed8b4b | 明确未描述 (a) 按规则给 DOM 元素赋优先级 (b) 父+嵌套子集优先级 (c) 元素间预定延迟错峰渲染；实际特性 = Night Mode / High Contrast / CSS Grid / Tracking Blocker |

## 工具受限说明
无工具受限；WebSearch / WebFetch 均正常返回。未触发 SPA 空壳 / 登录墙，无需 curl 兜底。
