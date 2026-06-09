# 02-google-android-multiwindow verdict
## 候选基本信息
- 名称：Android / AOSP 多窗口框架（含 Pixel 原生分屏、双击分隔条对调） / 组织：谷歌 Google / 类型：技术 / 初判命中 F#：F1, F2, F4 / 专利公开日：2017.02.08
## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 未命中 | "Tap the kebab menu (three dots) within the Recents app switcher" 并选 "Split-top"/"Split-screen"；Samsung 为 "Pressing and holding the app icon within the Recents menu" | https://9to5google.com/2023/01/13/split-screen-android-13/ | 原生进入分屏 = 在 Recents 菜单点三点菜单/长按图标，属菜单/按钮触发；非"沿触摸屏横向/纵向滑动信号"分屏。F1 要求滑动手势触发分屏——手段不同，有正向反据。SKILL 关键限定词亦明示"仅通过菜单/多任务卡片按钮进入分屏、无滑动手势触发分屏，则 F1 需个案判断是否等同"，此处判未命中。 |
| F2 | 部分/等同存疑 | "Layout follows device orientation: This will only work when viewing applications in portrait... When in landscape mode, apps will be held on the left and right halves" | https://9to5google.com/2023/01/13/split-screen-android-13/ | "把区域划分为≥2窗口（上下或左右）"的效果存在，但 F2 的限定是"根据横向滑动→上下/根据纵向滑动→左右"，即由滑动方向决定布局；原生布局由设备方向（竖屏→上下、横屏→左右）决定，无滑动方向驱动。划窗效果命中、滑动方向→布局映射不命中。 |
| F3 | 未命中 | "double-tap the separating line or bar to switch app positions"；resize 为"dragging the dividing line side-to-side or top-to-bottom" | https://9to5google.com/2023/01/13/split-screen-android-13/ ; https://source.android.com/devices/tech/display/split-screen | F3 要求"第一窗口至第二窗口的滑动触摸信号"（跨窗口方向性滑动）。原生互换由"双击分隔条"触发，分隔条交互非窗口间滑动；多源确认"drag-one-pane-onto-other 非标准原生手势"。双击分隔条 vs 窗口间滑动为不同手段，判未命中。 |
| F4 | 等同存疑 | "When you double tap on the dividing line between two apps in split screen, the two apps will swap places with each other" | https://9to5google.com/2023/01/13/split-screen-android-13/ ; https://www.ytechb.com/how-to-split-screen-on-android-13/ | F4"双向互换两窗口内容"的效果在 Android 13（2022 发布，晚于 2017.02.08）原生存在（两 app swap places=双向对调）。但 F4 文义锚定"根据所述滑动触摸信号"，原生触发为双击分隔条而非 F3 的窗口间滑动——效果命中、触发手段是否等同存疑（功能/效果相同，手段为局部双击 vs 方向性跨窗口拖动）。 |
## 已检查文档清单
- 9to5Google《How to enable split-screen multitasking in Android 13》(2023-01-13) — verbatim 进入方式=Recents 三点菜单/长按；布局随设备方向；互换=双击分隔条 — https://9to5google.com/2023/01/13/split-screen-android-13/
- ytechb《How to enable Split Screen on Android 13》— 双击分隔条两 app swap places — https://www.ytechb.com/how-to-split-screen-on-android-13/
- AOSP 官方《Split-screen interactions》(L1) — Android 7.0+ multi-window，divider 随方向 side-to-side/top-to-bottom 拖动调整尺寸；未述滑动进入或互换 — https://source.android.com/devices/tech/display/split-screen
- WebSearch 多源 — 确认"拖一个 pane 压到另一个 pane / 窗口间滑动互换内容"非标准原生手势；原生互换=双击分隔条或点分隔条控件翻转
## 最终判定
**第 4 档：命中<60%、含等同存疑、无第5档反据**
五档：第1档全部确认命中·字面；第2档全部命中含≥1等同；第3档命中≥60%其余公开资料不足且无反据；第4档命中<60%无第5档反据；第5档已排除（(a)≥1 F# 确认未命中有正向反据/(b)全部证据<公开日/(c)架构层级不同）。第5档硬门槛=针对该候选的正向事实，非推断非缺失。0 命中≠已排除。
判定依据（1-3 句）：F1（滑动触发分屏）有正向反据——原生由 Recents 菜单/长按图标进入，非滑动手势；F2 的"滑动方向→布局映射"不命中（原生布局随设备方向），仅"划分为≥2窗口"效果存在；F3"窗口间滑动信号"不命中——原生互换由双击分隔条触发。但 F4 的核心区分性效果"两窗口内容双向互换"在 Android 13+ 原生确实存在，仅触发手段（双击分隔条）与专利（窗口间滑动）是否等同存疑——该 swap 功能真实存在，不构成对该功能的正向否定，故不落第5档已排除。综合 4 项独立特征字面命中率<60%，落第 4 档。
## 升级路径（第3-4档填）
- 取证 Android 13+ 原生是否存在"在某窗口内向另一窗口方向拖动/滑动即触发互换"的隐藏手势（若有，F3/F4 可升等同命中）；目前多源仅见双击分隔条与拖分隔条控件翻转。
- 抓 AOSP 源码 SystemUI DividerView / Launcher3 split 相关 commit，确认互换的输入事件是否为 divider 上的 double-tap 而非跨窗口 MotionEvent，以坐实"非窗口间滑动"。
- 若聚焦三星等 OEM 的"分隔条控件点击翻转"或自有滑动手势，应单独立行评估（本条仅限 AOSP/Pixel 原生）。
## 总结一句话
AOSP/Pixel 原生分屏经菜单/长按进入（非滑动）、布局随设备方向、互换靠双击分隔条而非窗口间滑动；仅 F4"双向互换内容"效果在 Android 13+ 存在但触发手段等同存疑，F1/F2/F3 字面未命中，综合落第 4 档。
