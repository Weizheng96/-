# 证据索引 — 02-tech-webkit

## Phase 1 — react 粗筛 query（串行）
1. `WebKit resource load scheduler priority rendering`
   - 命中：WebKit ResourceLoadScheduler / ResourceLoadPriority enum；优先级按资源类型 + 文档中引用位置决定（stylesheet 最高、视口内 image high、视口外 image low、async script low→medium）。
2. `WebKit incremental rendering layout timer delay paint elements progressively`
   - 命中：painting 为 global 或 incremental（按 damage rect 重绘 delta）；渲染按 60fps 帧预算（16.667ms/frame）；idle 时机会性调度。未见"按优先级排序后元素间预定延迟显示"机制。
3. `WebKit FrameView layout delay timer cLayoutScheduleThreshold first paint suppress`
   - 命中：定位到 WebKit 官方源码 LocalFrameView.cpp / FrameView.cpp（github raw 可取）。

## Phase 2 — 深抓（WebFetch + curl raw 源码）
| # | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- |
| 1 | WebFetch | https://github.com/WebKit/webkit/blob/main/Source/WebCore/page/FrameView.cpp | blob 仅渲染片段，改用 raw |
| 2 | curl raw | https://raw.githubusercontent.com/WebKit/webkit/main/Source/WebCore/page/FrameView.cpp → ./FrameView.cpp (16KB) | FrameView 已重构为壳，layout 逻辑迁至 LocalFrameView |
| 3 | curl raw | https://raw.githubusercontent.com/WebKit/webkit/main/Source/WebCore/page/LocalFrameView.cpp → ./LocalFrameView.cpp (273KB) | 全部 layout/timer/throttle 逻辑；Grep 确认所有延迟均为功能性（scroll 节流 / 视口外节流 / scrollToTextFragment 100ms / speculativeTiling 500ms），无"按优先级排序后元素间预定延迟显示" |
| 4 | WebFetch | https://trac.webkit.org/changeset/274145/webkit | ResourceLoadPriority 按单个资源的类型 + 执行特性赋值（async script low→medium），非按 DOM 父+嵌套子树子集赋值 |

## 工具受限说明
- 首次 curl 取 LocalFrameView 触发 schannel SSL 握手失败（exit 35），重试循环第 2 次成功。
- GitHub blob view（WebFetch）对超大文件仅返回片段，故改 curl raw + 本地 Grep 取 verbatim。
- curl 取 LayoutContext.cpp 返回 404（14 字节），已删除；layout 调度逻辑实际在 LocalFrameView.cpp 内。
