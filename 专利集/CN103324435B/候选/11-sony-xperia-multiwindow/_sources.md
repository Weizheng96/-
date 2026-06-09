# 证据索引 — 11-sony-xperia-multiwindow

## Phase 1 WebSearch（react 串行）
1. `Sony Xperia split screen multi-window how to enter swipe gesture`
   → 命中 Sony 官方 helpguide.sony.net 多代机型「Split-screen mode (Multi-window switch)」页。信号：进入分屏=Overview 键 / Side sense 菜单；非"滑动手势分屏"。
2. `Sony Xperia split screen swap windows switch top bottom apps positions multi-window`
   → 命中同批官方页。信号：① 分屏方向由设备方向决定（竖屏=上下/垂直，横屏=左右/水平），非滑动方向决定；② "Multi-window switch" 为"换某个窗口里的应用"（swipe 选 app），非"两窗口内容互换"；无 swap 功能。

## Phase 2 WebFetch（深抓 verbatim）
- Xperia 1 VI 官方 Help Guide — Split-screen mode（2024 机型，Android 14）
  https://helpguide.sony.net/mobile/xperia-1m6/v1/en/contents/split_screen_mode.html
  verbatim 要点：
  - 进入："Tap (Overview button) in the navigation bar" → "[Multi-window switch]"；备选 "flicking up the Side sense bar, and then tapping [Multi-window] or swiping left on the screen."
  - 方向："A window in the Split-screen mode is split vertically in the portrait orientation and horizontally in the landscape orientation."（由设备方向决定，非滑动方向）
  - 换 app："Swipe left or right to select the desired apps, and then tap [Done]."（选窗口里显示哪个 app）
  - **无任何"互换两窗口内容 / swap two panes"指令**。
- Xperia 1 II 官方 Help Guide — Using the Split-screen mode（2020 机型，历史交叉印证）
  https://helpguide.sony.net/mobile/xperia-1m2/v1/en/contents/TP0003101962.html
  verbatim 要点：Multi-window switch icon "appears when you drag the split-screen border"，用于"select applications"；"Split-screen button – Select a recently used application for the lower window"；**无 swap/exchange 功能**。

## 时间合规
- 所引官方页覆盖 Xperia 1 II（2020）至 Xperia 1 VI（2024）多代，均晚于专利公开日 2017.02.08。时间合规。

## 工具/资料局限
- Sony helpguide 为静态 HTML，WebFetch 正常返回正文，无 SPA 兜底需要。
- 已交叉两代机型，机制一致，未见 swap 功能的官方记载。
