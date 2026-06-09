# 证据索引 — 10-motorola-myux-splitscreen

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 长期有效 | 官方支持页 | https://en-us.support.motorola.com/app/answers/detail/a_id/146923/~/view-two-apps-on-screen | Motorola 官方：「Swipe to split」手势=在屏幕来回横扫进入分屏（F1）；未提方向决定布局；未提两窗口内容互换 |
| 2 | 2024+（报道） | 媒体报道 | https://www.androidpolice.com/swipe-to-split-setting/ | "swipe back and forth across the screen to bring up multitasking. It immediately splits the app you're using"（F1）；未提方向映射、未提内容互换 |
| 3 | 通用指南 | 第三方指南 | https://www.positioniseverything.net/how-to-split-screen-on-android-2-proven-ways/ | 通用 Android：「double-tap the divider bar to swap which app is on top/bottom」——双击分隔条对调，非"窗口间滑动"，且非 Motorola 官方 |

## Phase 1 react 粗筛 query（WebSearch）
1. `Motorola MyUX split screen swipe to split gesture how to enter`
   - 命中 Motorola 官方支持页 + AndroidPolice / HowToGeek：MyUX「Swipe to split」= 屏幕来回横扫触发分屏。F1 强信号。
2. `Motorola split screen swap two apps switch positions divider drag swap panes`
   - Motorola 官方未提"窗口内容互换"；仅一篇通用 Android 指南提到「double-tap the divider bar to swap」（双击分隔条对调），非"窗口间滑动"、非 Motorola 官方。

## Phase 2 react 深抓（WebFetch）
- AndroidPolice：手势=横向来回滑动；未说明横扫/竖扫方向决定布局；未提两窗口内容互换。
- Motorola 官方支持页：进入分屏=Settings>System>Gestures>「Swipe to split」开启，第一个 app 中「swipe once back and forth across the screen」；官方未指明滑动方向决定上下/左右；未提任何"两 app 位置/内容互换"操作；退出=拖分隔条到顶/底。

## 工具受限说明
- WebSearch/WebFetch 均正常返回，无受限。
- 备注：Motorola 分屏为标准 Android 上下分屏，「Swipe to split」是单一横向来回手势，不存在"横向→上下 / 纵向→左右"方向映射；亦未见"窗口间滑动互换内容"。
