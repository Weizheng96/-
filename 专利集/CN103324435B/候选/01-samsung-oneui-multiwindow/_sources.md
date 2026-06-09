# 证据索引 — 01-samsung-oneui-multiwindow

专利公开（授权）日基准：2017.02.08

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行(官方) | WebSearch+WebFetch | https://www.samsung.com/us/support/answer/ANS10002022/ | 进入分屏：Multi Window tray 拖 app / Recents "Open in split screen view" / 两指底部上滑(One UI 6+)；换位：点 dotted divider 的 "two arrows" → 两 app 位置互换，双向(both exchange positions) |
| 2 | One UI 5.0=2022 | WebSearch | https://www.samsung.com/ph/support/mobile-devices/how-to-use-swipe-gestures-with-multi-window/ ; https://www.sammobile.com/news/one-ui-5-0-feature-focus-new-multitasking-swipe-gestures-labs/ | 两指从屏幕底部向上滑进入分屏（"Swipe for split screen"），One UI 5.0 Labs 起，后转正式 |
| 3 | 2025.05.28 | WebFetch | https://www.droid-life.com/2025/05/28/samsung-upgrades-split-screen-in-one-ui-8-update/ | One UI 8：把一 app 推到约 90% 边缘后 tap 小区域 flip 放大，反复切换大小屏 |

## Phase 1 — WebSearch query 留痕（react 串行）
- query 1: `Samsung One UI multi window split screen swap apps flip top bottom panes` → 强命中（分隔条 two-arrows/三点菜单 swap；One UI 8 flip）
- query 2: `Samsung Galaxy split screen swipe gesture two fingers swipe up to split screen enter` → 强命中（两指底部上滑进入分屏，One UI 5.0 2022）
- query 3: `Samsung split screen drag app from one window to other window swap drag and drop multi window` → 命中（换位=点分隔条 two-arrows；跨 app 拖放仅限文本/图片内容，非窗口内容互换）

## 工具受限说明
- 无付费墙/登录墙阻断；均为公开官方/媒体文档。
- 未检索到三星官方文档描述"以跨窗口滑动手势(window→window slide)触发分屏内容互换"——官方换位机制为分隔条 two-arrows 点按(tap)，非滑动手势。
