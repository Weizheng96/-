# 证据索引 — 09-realme-ui-splitscreen

## Phase 1 WebSearch（react 粗筛）
1. `realme UI split screen how to enter swipe gesture three finger`
   → 信号：realme UI 支持"三指上滑进入分屏"（Settings > Split-screen > Swipe Up With 3 Fingers）。来源 rmupdate / clearnightsky / itigic。
2. `realme UI ColorOS split screen swap two windows drag swap positions multi-window`
   → 信号：分屏窗口上下排列；存在"对调两窗口位置"功能，触发方式为"分隔线上的小按钮（双箭头）/ 点击中间分隔条箭头图标"。来源 androidguias / clearnightsky / rmupdate。
3. `realme ColorOS split screen swap apps middle bar drag swipe up down switch positions gesture`
   → 交叉印证：对调由"分隔线上的双箭头小按钮"触发；拖动中间条仅用于调整窗口大小，非互换。ColorOS/realme/OPPO/OnePlus 同源，三指上滑进入分屏。

## Phase 2 WebFetch（深抓）
- https://rmupdate.com/2020/09/14/realme-ui-split-screen-multi-window/ （2020-09-14）
  → verbatim 三种进入方式（Recent 按钮 / 三指上滑 / 长按多任务键）；未述方向映射与互换。
- https://en.androidguias.com/How-to-activate-and-use-split-screen-mode-on-your-android-device/
  → ColorOS（realme/OPPO/OnePlus）三指上滑进入分屏；该页未给互换 verbatim。
- https://www.realme.com/in/support/kw/doc/2206738 （官方 realme UI 6.0 Split View）
  → SPA 外壳，正文未随 HTML 返回，无法采信正文。
- https://techsarjan.com/2025/07/how-to-use-split-screen-and-floating-windows-on-realme-devices.html （2025-07-22）
  → 进入分屏（Recent Apps）；拖动分隔线调窗口大小；未述互换触发方式。
- https://clearnightsky.com/how-to-split-screen-realme-p455/ （2025-03-07）
  → verbatim：进入"swipe upwards on the screen with three fingers simultaneously"；
    排列"pushed to the top portion ... appear at the bottom"（上下排列）；
    互换"A small button (often represented by two arrows) located on the dividing line allows you to quickly swap the positions of the two apps"（分隔线上的双箭头按钮点击对调，非窗口间滑动）。

## 工具受限说明
- realme 官方支持页（doc/2206738）为 SPA，WebFetch 仅得外壳；以多家第三方教程 + rmupdate 交叉印证替代，互换机制描述在 androidguias / clearnightsky 多源一致。
- 所有证据发布日期（2020–2025）均晚于专利公开（授权）日 2017.02.08。
