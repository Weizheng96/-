# 06-oneplus-oxygenos-splitscreen verdict

## 候选基本信息
- 名称：OxygenOS 分屏 / Open Canvas（双指/三指上滑分屏） / 组织：一加 OnePlus / 类型：产品 / 初判命中 F#：F1, F2, F3, F4 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 命中（字面/等同） | "Swipe up on any screen with three fingers to activate split-screen mode"；设置项 "Swipe up with 3 fingers to enter Split view" | https://www.androidcentral.com/how-enable-split-screen-multitasking-oneplus-phone | 触摸屏滑动手势触发分屏，命中权1"分屏触摸信号=滑动信号"；三指上滑属触摸屏滑动信号（手指数不影响"滑动"本质） |
| F2 | 命中（等同） | 上滑后当前显示区域分为上下排列两个窗口；"long-press the slider in the middle of the screen and move up or down" 调整两窗口 | https://www.androidcentral.com/how-enable-split-screen-multitasking-oneplus-phone | 命中 F2 [OR] 的"上下排列至少两个显示窗口"分支（N≥2）；进入手势固定为上滑→上下分屏，未完整复现"横向↔上下/纵向↔左右"双向映射，故记等同 |
| F3 | 命中（等同） | "You can even switch app positions by dragging and dropping the app view to change the order." | https://www.pocket-lint.com/how-multitasking-works-on-the-oneplus-open/ | 拖放某窗口 app view 到另一窗口=跨窗口拖动手势，与权1"第一→第二显示窗口的滑动触摸信号"同手段类（拖动=滑动触摸信号的等同）；OnePlus Open 折叠屏特性 |
| F4 | 命中（等同） | "switch app positions by dragging and dropping the app view to change the order" | https://www.pocket-lint.com/how-multitasking-works-on-the-oneplus-open/ | "switch app positions...change the order"=两窗口位置对调=双向互换内容（A→B 且 B→A），命中 F4 [AND] 双向互换；非"仅替换一个窗口"（区别于三点菜单 Switch App） |

## 已检查文档清单
- Android Central《How to enable split-screen multitasking on a OnePlus phone》— 三指上滑进入分屏、长按中间滑块调整窗口 — https://www.androidcentral.com/how-enable-split-screen-multitasking-oneplus-phone
- Pocket-lint《How multitasking works on the OnePlus Open》(2023-11-03) — 拖放 app view 互换两窗口位置 — https://www.pocket-lint.com/how-multitasking-works-on-the-oneplus-open/
- XDA《4 OxygenOS features...OnePlus Open multitasking》(2023-10-25) — 分屏创建/全屏切换，未述互换手势（无反据）— https://www.xda-developers.com/oxygenos-open-multitasking/
- TechWiser / MashTips — 三指上滑进入分屏的第二来源交叉印证

## 最终判定
**第 2 档：命中含等同（F1-F4 全部命中，F2/F3/F4 经等同认定）**

判定依据（1-3 句）：F1 三指上滑进入分屏属触摸屏滑动信号，字面/等同命中；F2 上滑后分上下两个窗口、命中 [OR] 上下分屏分支（N≥2）；F3+F4 由 OnePlus Open "dragging and dropping the app view to change the order" 实现两窗口位置双向互换——拖放跨窗口手势与权1"窗口间滑动触摸信号→双向互换内容"为同手段/同功能/同效果，按判定纪律第二步以等同认定命中。证据均发布于公开日 2017.02.08 之后，时间合规。注意：本机型还提供三点菜单 Switch App 法，属"替换单窗口"非双向互换，不据其判 F4；F4 命中依据的是拖放对调位置这一交互。

## 升级路径（第3-4档填）
（不适用，本候选落第 2 档）
- 如需进一步坐实字面命中：可取证 OnePlus 官方手册中"互换/swap 两分屏窗口"的官方表述及具体触发手势截图，确认是否存在直接"窗口间滑动"而非仅"拖放 app view"，以判断能否从等同升至字面（升至第 1 档）。

## 总结一句话
OxygenOS（OnePlus Open）三指上滑进入上下分屏、并可拖放 app view 双向互换两窗口位置，F1-F4 全部命中（含等同），证据均晚于公开日，落第 2 档。
