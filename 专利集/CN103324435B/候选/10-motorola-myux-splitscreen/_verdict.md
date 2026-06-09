# 10-motorola-myux-splitscreen verdict

## 候选基本信息
- 名称：MyUX 分屏 / swipe-to-split / 组织：摩托罗拉 Motorola（联想） / 类型：产品 / 初判命中 F#：F1, F2, F3 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 确认命中 | "swipe once back and forth across the screen"（在第一个 app 中来回横扫进入分屏）；"swipe back and forth across the screen to bring up multitasking. It immediately splits the app you're using" | https://en-us.support.motorola.com/app/answers/detail/a_id/146923/~/view-two-apps-on-screen ; https://www.androidpolice.com/swipe-to-split-setting/ | 触摸屏滑动手势触发分屏=F1 字面命中（F1 为 [OR]，命中横向滑动分支即满足） |
| F2 | 公开资料不足 | （官方/媒体均未说明滑动方向决定上下/左右布局；Motorola 分屏为固定上下排列，单一横向来回手势） | 同上 | 缺"横向→上下 或 纵向→左右"方向映射的正向证据；"划分为≥2 个并排窗口"本身成立，但 F2 区分性的方向映射未见；无正向反据 |
| F3 | 公开资料不足 | （官方页未提任何"窗口间滑动"跨窗口手势；仅通用 Android 指南提到"double-tap the divider"对调，非 Motorola 官方、非滑动手势） | https://www.positioniseverything.net/how-to-split-screen-on-android-2-proven-ways/ | 候选若有互换，疑似"双击分隔条"实现而非"窗口间滑动"——按判定纪律 F3 落公开资料不足，不据此判第5档 |
| F4 | 公开资料不足 | （无"以窗口间滑动手势双向互换两窗口内容"的 verbatim；双击分隔条对调虽近似互换效果，但不由 F3 的窗口间滑动信号触发，且非 Motorola 官方确证） | 同 F3 | 互换效果存在与否不确定；即便存在亦由不同手段（双击分隔条）实现，缺 F3 触发链的正向证据；非正向反据 |

## 已检查文档清单
- Motorola 官方支持「View two apps on screen」：Swipe to split 开启与使用步骤、退出方式 — https://en-us.support.motorola.com/app/answers/detail/a_id/146923/~/view-two-apps-on-screen
- AndroidPolice「I've used Moto Gestures... swipe-to-split setting」：手势机制描述 — https://www.androidpolice.com/swipe-to-split-setting/
- positioniseverything「How to Split Screen on Android」：通用 Android 双击分隔条对调 — https://www.positioniseverything.net/how-to-split-screen-on-android-2-proven-ways/

## 最终判定
**第 4 档：命中不足 60%，无第 5 档正向反据**

判定依据（1-3 句）：MyUX「Swipe to split」确证 F1（触摸屏滑动手势进入分屏，字面命中），但 F2 的"滑动方向→分屏布局映射"、F3 的"窗口间滑动手势"、F4 的"由窗口间滑动触发的双向内容互换"均无公开正向证据——确认命中仅 1/4=25%（<60%）。同时不存在针对本候选的正向反据（官方页对方向映射与窗口间互换是"沉默/未提"，非 verbatim 拒绝；通用 Android 的"双击分隔条对调"是不同手段且非 Motorola 官方确证，按判定纪律为限定/沉默而非反向证据），故不落第 5 档。

## 升级路径（第3-4档填）
- 找 Motorola 官方/媒体是否确认「Swipe to split」横扫与竖扫分别映射上下/左右分屏（核 F2 方向映射）。
- 核查 MyUX 是否提供"跨分屏窗口拖拽/滑动以互换两 app 内容"的官方操作（区别于双击分隔条对调；核 F3+F4）。若仅"双击分隔条对调"，F3 仍判公开资料不足，整体维持第 4 档。
- 优先比对 Motorola/Lenovo 2017.02.08 之后同主题分屏专利的权利要求，确认其互换交互是否为"窗口间滑动"。

## 总结一句话
MyUX「Swipe to split」仅确证 F1（滑动手势进分屏），F2 方向映射与 F3/F4 窗口间滑动互换均公开资料不足、亦无正向反据，落第 4 档。
