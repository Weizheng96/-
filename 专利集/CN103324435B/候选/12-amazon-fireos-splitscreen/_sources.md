# 证据索引 — 12-amazon-fireos-splitscreen

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2021 | WebSearch | `Fire OS tablet Split View split screen how to enable two apps` | 进入分屏=task switcher 菜单选 "Split Screen"，非滑动手势 |
| 2 | 2021 | WebSearch | `Fire OS split screen swap two apps switch positions divider drag` | 拖分隔条=resize/退出；未见两窗口内容互换交互 |
| 3 | 2021 | WebFetch | https://www.lovemyfire.com/how-to-use-split-screen-on-fire-tablet.html | task switcher→菜单 Split Screen；首 app 左半屏，再手动选右半屏 app |
| 4 | 2021-04-27 (Fire OS 7) | WebFetch | https://developer.amazon.com/apps-and-games/blogs/2021/04/new-fire-hd-10-tablets | 官方：side-by-side + 窗口间 drag-and-drop 文件；无"互换 app 位置" |
| 5 | 2021 | curl(本地) | kindlefireforkid-splitscreen.html (WebFetch 403→curl 兜底, 262KB) | L350 仅 task-switching 按钮进入；L385 首 app 固定左/上，**不允许互换 app 槽位** |

## Phase 1 react 粗筛 query 留痕
1. `Fire OS tablet Split View split screen how to enable two apps` → 进入分屏 = Recents/Overview（task switcher）按钮 → 点应用图标 → 菜单选 "Split Screen"；非滑动手势触发。键盘 Fn+S。退出 = 拖中央分隔条到另一侧。
2. `Fire OS split screen swap two apps switch positions divider drag` → 拖分隔条用于 resize / 退出（拖太靠边关闭一个 app，另一占满全屏退出分屏）；无"两窗口内容互换"独立交互。

## Phase 2 react 深抓
- lovemyfire.com（200，2021）：进入 = task switcher 方块 → 应用图标 → 下拉菜单 "Split Screen"；首 app 移到左半屏，用户"select an app to show on the right half"。未提滑动方向决定分屏方向。
- developer.amazon.com 官方（2021-04-27，Fire OS 7）："open two compatible apps side-by-side ... drag and drop files and objects between windows." 仅窗口间拖放文件/对象，无互换两 app 位置。
- kindlefireforkid.com（WebFetch 403 → curl 兜底成功，落盘 kindlefireforkid-splitscreen.html，2021）关键 verbatim：
  - L350：「you can only initiate the multiwindow mode through the task-switching button」（仅经 task-switching 按钮进入 — 反 F1）
  - L385：「the first app always occupies the left (in landscape orientation) or top (in portrait orientation) of the screen. Fire HD 10 and Fire HD 10 Plus do not allow you to switch the app slots.」（首 app 固定左/上；不允许互换 app 槽位 — 正向反证据，反 F3+F4）
  - 方向由设备朝向决定（横屏→左右，竖屏→上下），用户手动选第二 app（反 F2）
  - L408-414：退出 = Back 关一个 app（另一占满）或拖分隔条到边缘关闭，非互换。

## 时间合规
- 全部证据 2021 年（Fire OS 7 / Fire HD 10 2021），均晚于专利公开日 2017.02.08，时间合规。
