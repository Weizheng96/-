# 证据索引 — 08-apple-ipados-splitview

## Phase 1 粗筛 WebSearch（react 串行）
1. `iPadOS Split View how to enter multitasking drag from Dock or three dots menu`
   → 命中：进入 Split View 由 ① 三点 Multitasking 菜单按钮选 Split View，② 从 Dock 拖第二个 App 图标到屏幕左/右边缘。非"沿屏滑动划分当前区域"。
2. `iPad Split View swap two apps left right swap positions drag divider`
   → 命中：长按窗口顶部/三点把手，拖过中间分隔条，两 App "trade places"（互换左右位置）；拖分隔条调整占比。
3. `iPad Split View vertical orientation top bottom or only left right side by side windows`
   → 命中：iPad Split View **仅支持左右并排**，不支持上下（top/bottom）分屏；长期为用户请求但 Apple 未实现。

## Phase 2 深抓 WebFetch
- Apple 官方 Support「Multitask on iPad with iPadOS 26」 https://support.apple.com/en-us/125309
  - 进入：从 Dock / App Library / Spotlight 拖另一 App 到左或右边缘；iPadOS 26 另有"quickly swipe a window to the left or right side, then quickly swipe another window to the other side"。
  - 排布：两 App **左右并排（side-by-side horizontally）**，非上下堆叠。
  - 互换：官方页未明确描述两 App 互换位置手势（沉默，非反向证据）。
- iDownloadBlog「How to use Split View on iPad」 https://www.idownloadblog.com/2023/01/16/how-to-use-split-view-ipad/
  - 互换 verbatim：「touch the three-dotted menu at the top of either app and drag it left or right to switch your Split View arrangement」——长按窗口顶部三点菜单，左右拖动跨分隔条，互换两 App 左右位置。
  - 排布：「Split View divides the iPad's screen in the middle, with each app taking up one half」左右各半。
  - 进入：三点菜单选 Split View / 从 Dock 拖图标到边缘 / App Switcher 拖动 / Spotlight 拖动。

## 工具状态
- WebSearch / WebFetch 均正常，无受限兜底。Apple 官方 support 正文以 WebFetch 提取，第三方教程交叉印证互换手势（官方页对互换沉默，故采信第三方 verbatim）。
- 全部证据来源描述的 iPadOS 多任务模型自 iPadOS 13（2019）延续至 iPadOS 26（2025/2026），均晚于专利公开（授权）日 2017.02.08，时间合规。
