# 15-asus-zenui-splitscreen verdict

## 候选基本信息
- 名称：ZenUI 分屏 / 双应用 / 组织：华硕 ASUS / 类型：产品 / 初判命中 F#：F1, F2 / 专利公开日：2017.02.08

## 检索粗筛（query 留痕）
- WebSearch: "ASUS ZenUI split screen swipe gesture enter dual app multitasking how to" → 命中官方 FAQ 1039586 / ZenTalk FAQ（有信号）
- WebSearch: "ASUS Zenfone ZenUI split screen multitasking recent apps button how to enter swap apps" → 命中：长按 app switcher 进入、↑↓/switch bubble 键 swap（有信号，定位手段）

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 公开资料不足（未确定） | "Open recent apps." → "Tap the icon of the app." → "Tap **Split top**." | https://www.asus.com/support/faq/1039586/ | 官方 FAQ 记录的进入路径为「最近应用键 + 点击 Split top 菜单」（按钮/菜单手段）；但「记录了菜单进入路径」**不等于**「不支持滑动进入」——按钮与滑动为**非互斥手段**，未检索到针对 ZenUI 的「不支持滑动分屏」正向否定，按判定纪律第三步落公开资料不足（**非正向反据**，修正原误判） |
| F2 | 公开资料不足（未确定） | "Tap **Split top**" + "Choose the second recent app that you want for Multi-tasking." + "Rotate your phone to change to landscape mode." | https://www.asus.com/support/faq/1039586/ | 「划分为上/下≥2 窗口」效果存在；专利「滑动方向→布局方向」的映射未获证实（ZenUI 由按钮选 Split top、横竖靠旋转设备）——属**不同机制实现同一划分效果**，按「不同机制≠反据」记公开资料不足（**非正向反据**） |
| F3 | 公开资料不足（未确定） | "Tap the **switch bubble** to reverse the order of two apps." | https://www.asus.com/support/faq/1039586/ | 互换由「点击 switch bubble 按钮」触发，与专利「窗口间滑动触摸信号」为**非互斥的不同手段**；「记录了按钮互换」不能推出「不支持滑动互换」，按纪律落公开资料不足（**非反据**，修正原误判），不据此判第5档 |
| F4 | 命中（功能/效果等同） | "Tap the switch bubble to **reverse the order of two apps**." | https://www.asus.com/support/faq/1039586/ | 双向互换效果存在：reverse the order = 两应用位置对调（A→B 且 B→A），落入 F4 的[AND]双向互换效果。但触发手段为按钮而非滑动（见 F3） |

## 已检查文档清单
- ASUS 官方 FAQ「[Phone] How to use Split Screen Multitasking?」verbatim 步骤（Open recent apps → Tap icon → Split top → 选第二应用；switch bubble 互换；中部拖条调大小；上下拖到底退出）— https://www.asus.com/support/faq/1039586/（HTML 已落盘 asus-faq-1039586.html，curl 已 grep 校验 verbatim）
- ASUS ZenTalk FAQ（WebFetch 403，改 WebSearch 官方摘要交叉印证：长按方块键进入分屏、右侧 ↑↓/switch bubble 键 swap，与官方 FAQ 一致）— https://zentalk.asus.com/t5/faq/phone-how-to-use-split-screen-multitasking/ta-p/66485

## 最终判定
**第 4 档：公开资料不足（弱候选）**

判定依据：ZenUI 已确认具备本专利最具区分性的 **F4「两个已分屏窗口内容双向互换」效果**（switch bubble 使两 app reverse order = A↔B 对调，等同命中）。F1/F2/F3 的「滑动」相关限定未获证实：官方 FAQ 记录的是按钮/菜单进入与按钮互换，而**按钮与滑动是非互斥的不同手段**——「记录了按钮路径」不能推出「不支持滑动」，按判定纪律第三步「非互斥手段不是反向证据、缺失→未确定」，F1/F2/F3 均记公开资料不足（**非正向反据**）。确认命中约 1/4（<60%）、无任何针对该候选 verbatim 的「不支持」正向否定，故落第 4 档（**修正**：原 sub-agent 将「按钮而非滑动」误判为正向反据→第5档，违反「非互斥手段不是反向证据」纪律，经主 agent 6.2 复核打回至第 4 档）。

## 升级路径（第3-4档填）
- 实测 ZenUI 是否支持「滑动手势进入分屏」「滑动方向决定上下/左右」「从一窗口向另一窗口滑动触发互换」（区别于 switch bubble 按钮）→ 若任一支持则相应 F# 命中、可升第 2-3 档。
- 查华硕 2017.02.08 后是否有同主题分屏专利，比对其披露的实际实现。

## 总结一句话
ZenUI 已具备「两分屏窗口内容双向互换」效果（F4 等同命中），但进入与互换均由按钮/菜单触发、未证实滑动手段——按钮与滑动属非互斥不同手段（非反据）→ F1/F2/F3 公开资料不足，落第 4 档（公开资料不足-弱候选）。
