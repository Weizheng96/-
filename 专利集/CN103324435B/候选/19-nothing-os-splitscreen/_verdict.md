# 19-nothing-os-splitscreen verdict

## 候选基本信息
- 名称：Nothing OS 分屏 / 组织：Nothing / 类型：产品 / 初判命中 F#：F1, F2 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 未命中 | "Swipe up from the bottom of the screen to access the recent apps menu... Select the 'Split screen' option from the menu that appears."（进入分屏=最近任务菜单"Split screen"项，非沿触摸屏横向/纵向滑动手势触发） | https://umatechnology.org/how-to-split-screen-multitask-on-nothing-phone-1/ | F1 核心=分屏由"沿触摸屏横向/纵向滑动信号"触发；Nothing OS 进入分屏是从最近任务卡片菜单选项进入（原生 AOSP 行为），有 verbatim 正向描述其为"菜单选项"而非滑动手势；不构成"按滑动信号触发分屏"，且无方向映射→不落字面，亦非等同（手段与方向映射效果均不同） |
| F2 | 部分命中（划分≥2窗口✓ / 按滑动方向划分✗） | "The selected app will now occupy the top half of the screen"（选中应用占上半屏，第二应用占下半屏=上下两个窗口）；方向由设备朝向决定非由滑动方向决定 | https://clearnightsky.com/how-to-split-screen-nothing-phone-p430/ | 确把当前显示区域划分为上下排列的≥2窗口（N≥2 满足）；但 F2 的"[OR] 根据横向/纵向滑动信号划分"前提缺失——分屏不由滑动信号触发、方向不由滑动方向决定→F2 仅"划分≥2窗口"成立，"按滑动方向划分"未命中 |
| F3 | 未命中 | "tap the three dots in the center of the dividing bar. A small menu will appear, allowing you to switch the apps' positions."（互换由点分隔条中央三点弹菜单触发，非跨窗口滑动触摸信号）；uma 源亦未提及任何跨窗滑动/拖内容手势 | https://clearnightsky.com/how-to-split-screen-nothing-phone-p430/ | F3 核心=存在"第一窗口↔第二窗口之间的滑动触摸信号"；Nothing OS 无此跨窗滑动/拖动手势，互换走三点菜单——有 verbatim 正向描述其为菜单触发，非"窗口间滑动信号"→F3 未命中 |
| F4 | 命中（效果命中·等同信号） | "switch the apps' positions"（两个分屏应用位置对调=两窗口内容双向互换 swap） | https://clearnightsky.com/how-to-split-screen-nothing-phone-p430/ | F4 效果=两窗口内容双向互换；Nothing OS 确支持 swap two apps' positions（双向对调效果达成）；触发手段是三点菜单而非跨窗滑动——按判定纪律"不同交互手段实现同一效果=等同信号、非反据"，故 F4 效果命中（属等同），但其依赖的 F3"窗口间滑动信号"前提不成立 |

## 已检查文档清单
- Clearnightsky《How to Split Screen on Nothing Phone》(2025-03-10)：进入=最近任务菜单"Split screen"；上下分屏；互换=分隔条三点菜单"switch positions" — https://clearnightsky.com/how-to-split-screen-nothing-phone-p430/
- UMA Technology《How To Split Screen Multitask On Nothing Phone 1》：进入=上滑最近任务→点应用图标→"Split screen"；拖分隔条调比例；未提及跨窗滑动/拖内容互换 — https://umatechnology.org/how-to-split-screen-multitask-on-nothing-phone-1/
- ManualsLib《How to Enable Split-Screen Multitasking on Nothing Phone》（交叉印证最近任务菜单进入、垂直拖分隔条）— https://www.manualslib.com/how-to/4062063/how-to-enable-split-screen-multitasking-on-nothing-phone.html

## 最终判定
**第 4 档：命中<60%（无第5档反据）**

判定依据（1-3 句）：4 个 F# 中，F1 未命中（进入分屏走最近任务菜单选项而非沿触摸屏横向/纵向滑动手势触发，且无"滑动方向→分屏方向"映射）、F3 未命中（互换走分隔条三点菜单而非跨窗口滑动触摸信号）；F2 仅"划分≥2窗口"成立、"按滑动方向划分"前提缺失；F4 互换效果命中（等同信号）。命中（含等同）的实质特征仅 F4 一项 + F2 半项，远低于 60%，故落第 4 档。注意 F1/F3 是"菜单/三点"取代"滑动"的手段差异——本专利最具区分性的特征"以触摸屏滑动手势触发分屏 + 以窗口间滑动手势互换内容"两处均不具备（用菜单替代），但 swap 效果存在；这属"同效果不同手段"，未构成针对该候选的正向"不支持互换"反据，故不落第 5 档。

## 升级路径（第3-4档填）
- 核查 Nothing OS 较新版本（Nothing OS 3.x，2025+）是否新增"双击分隔条/捏合手势/边缘滑动"等手势化分屏入口或跨窗拖放互换——若引入手势触发分屏或跨窗滑动互换，F1/F3 可重判等同甚至字面，整体或升至第 3 档。
- 取证 Nothing 自有 launcher/系统 UI 源（官方 nothing.community 帮助页正文、官方 user guide PDF）确认互换是否仅菜单一种交互；区分原生 AOSP 继承与 Nothing 自有增量。

## 总结一句话
Nothing OS 分屏走原生最近任务菜单进入、三点菜单互换，无"滑动触发分屏/跨窗滑动互换"两大区分性手段（仅 swap 效果存在为等同信号），命中实质特征不足 60% 且无正向反据，落第 4 档。
