# 09-realme-ui-splitscreen verdict

## 候选基本信息
- 名称：realme UI 分屏 / 组织：realme 真我 / 类型：产品 / 初判命中 F#：F1, F2, F3 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 命中（字面） | "simply swipe upwards on the screen with three fingers simultaneously"；"swipe up with three fingers to enable"（Settings → Split-screen → Swipe Up With 3 Fingers for Split-screen） | clearnightsky.com/how-to-split-screen-realme-p455/ · rmupdate.com/2020/09/14/realme-ui-split-screen-multi-window/ | 分屏由触摸屏上的滑动手势（三指上滑=纵向/竖直滑动）触发 → F1 [OR] 中"纵向滑动信号"分支命中。亦存在 Recent 按钮/长按多任务键非滑动入口，但滑动入口已足以命中 F1。 |
| F2 | 命中（含等同） | "The app will be pushed to the top portion of the screen, and your home screen or app drawer will appear at the bottom"（上下排列两个窗口） | clearnightsky.com/how-to-split-screen-realme-p455/ | 进入分屏后当前显示区域被划分为上下排列的两个（≥2）显示窗口，满足 F2 [OR] 的"上下排列至少两个窗口"分支与整数限定 N≥2。等同点：realme 三指上滑固定映射上下分屏，未演示"纵向滑动→左右"的方向映射，但 [OR] 命中"划分为至少两个窗口"核心即满足。 |
| F3 | 公开资料不足 | 互换由"A small button (often represented by two arrows) located on the dividing line"点击触发；"dragging the divider line"仅用于调整窗口大小 | clearnightsky.com/how-to-split-screen-realme-p455/ · en.androidguias.com/.../split-screen-mode... | F3 要求"第一↔第二窗口之间的滑动触摸信号"。realme 互换的触发是点击分隔条上的双箭头按钮，非窗口间滑动手势。按判定纪律：候选用"点击分隔条对调"而非"窗口间滑动"，F3 落公开资料不足（不同手段，未检索到窗口间滑动触发互换的 verbatim，亦无针对滑动的正向反据）。 |
| F4 | 命中（含等同） | "a small button ... allows you to quickly swap the positions of the two apps"（两窗口位置/内容双向对调） | clearnightsky.com/how-to-split-screen-realme-p455/ · en.androidguias.com/... | F4 的效果（两窗口内容双向互换 swap）确实存在且为双向对调，满足 F4 [AND]。但触发手段为按钮点击而非 F3 要求的窗口间滑动信号——效果等同、触发手段不同。 |

## 已检查文档清单
- Realme UI: Split Screen (Multi-Window) Feature Full Guide（2020-09-14，三种进入方式 verbatim） — https://rmupdate.com/2020/09/14/realme-ui-split-screen-multi-window/
- Split Screen Realme: Step-by-Step Tutorial（2025-03-07，进入/上下排列/双箭头对调按钮 verbatim） — https://clearnightsky.com/how-to-split-screen-realme-p455/
- How to activate and use split screen mode（ColorOS realme/OPPO/OnePlus 三指上滑；互换为分隔线按钮） — https://en.androidguias.com/How-to-activate-and-use-split-screen-mode-on-your-android-device/
- How to Use Split Screen and Floating Windows on Realme Devices（2025-07-22，进入/拖分隔线调大小） — https://techsarjan.com/2025/07/how-to-use-split-screen-and-floating-windows-on-realme-devices.html
- realme UI 6.0 New Split View 官方支持页（SPA 外壳，正文未取得） — https://www.realme.com/in/support/kw/doc/2206738

## 最终判定
**第 3 档：命中 F1/F2/F4，F3 公开资料不足（其余无反据）**

判定依据（1-3 句）：F1（三指/纵向滑动触发分屏）、F2（划分为上下排列≥2 窗口）字面命中；F4（两分屏窗口内容双向互换）效果命中且为双向对调。唯 F3（"窗口间滑动触摸信号"这一触发手段）——realme 实测互换由分隔线上的双箭头按钮点击触发，非窗口间滑动手势，按纪律落"公开资料不足"（不同手段且无 verbatim 窗口间滑动证据，亦非正向反据）。命中特征达 75%（F1/F2/F4 命中、F3 不足），无任何正向反据，故落第 3 档。

## 升级路径（第3-4档填）
- 取证 realme/ColorOS 是否存在"从一个分屏窗口向另一窗口滑动/拖动即互换内容"的窗口间滑动手势（区别于点击分隔条按钮）——若有 verbatim 演示，则 F3 命中、可升至第 2 档（含等同）甚至第 1 档。
- 直接核验 realme 官方用户手册 PDF（realme UI 6.0 User Manual: image05.realme.net/.../*.pdf）中"分屏/互换"原文，以及 OPPO/ColorOS 2017.02.08 后同主题专利，比对互换触发手段是否含滑动。
- 进一步确认 F2"纵向滑动→左右排列"方向映射在 realme 上是否存在（目前仅见三指上滑→上下分屏）。

## 总结一句话
realme UI 分屏：三指滑动进入(F1)、上下双窗(F2)、双箭头按钮双向对调内容(F4)均命中，唯互换由点击分隔条按钮而非窗口间滑动手势触发致 F3 公开资料不足，落第 3 档。
