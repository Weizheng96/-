# 08-microsoft-edge-mobile sources (query 留痕)

## Phase 1 — react 粗筛 WebSearch
1. `Microsoft Edge mobile efficiency mode sleeping tabs rendering loading`
   - 命中：Edge 性能特性官方支持文档、睡眠标签、效率/能源节省模式说明
   - 结论：睡眠标签/效率模式针对**标签页级 CPU/内存**（Chromium freezing），非元素间显示节奏 → 与 F7 关键区分点直接相关
2. `Edge Android data saver image defer load element rendering priority`
   - 命中：web.dev 浏览器级懒加载、fetchpriority、priority hints（Chromium/Blink 平台能力，Edge 继承）
   - 结论：懒加载=进入视口才加载（非固定时延）；fetchpriority=仅排序提示（非"延迟固定时长再显示下一个"）
3. `Microsoft Edge mobile battery saver feature element staggered display delay rendering`
   - 命中：Edge 能源节省/效率模式官方页 + 媒体报道
   - 结论：机制=背景标签睡眠（5/30 分钟）、降 CPU/内存、降视频/动画流畅度；无"元素间预定延迟显示"措辞

## Phase 2 — react 深抓 WebFetch
1. https://support.microsoft.com/en-us/topic/learn-about-performance-features-in-microsoft-edge-7b36f363-2119-448a-8de6-375cfd88ab25
   - verbatim：睡眠标签 "pauses a tab's script timers, which minimizes CPU usage"，基于 "Chromium's freezing technology"；能源节省 "reducing resource usage through modifying background tab activity"
   - 结论：三项性能特性均为**整页/整标签级**资源管理，无 per-element display timing / 交错渲染 / DOM 元素优先级赋值
2. https://www.microsoft.com/en-us/edge/features/energy-saver
   - verbatim：能源节省 = "puts background tabs to sleep after 30 minutes"（均衡）/ "five minutes"（最大）、"reducing CPU and memory usage"、视频 "less smooth"
   - 结论：无固定/预定元素显示延迟、无父/子元素规则优先级体系

## 工具受限说明
无（WebSearch / WebFetch 均正常返回）。Edge 移动端内部渲染调度无公开技术文档披露元素级显示时序机制。
