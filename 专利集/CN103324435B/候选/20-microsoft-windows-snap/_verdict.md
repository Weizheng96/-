# 20-microsoft-windows-snap verdict

## 候选基本信息
- 名称：Windows Snap / Surface Duo 多任务 / 组织：微软 Microsoft / 类型：产品 / 初判命中 F#：F1, F2 / 专利公开日：2017.02.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（触摸屏横向/纵向滑动信号触发分屏）| 未确定/偏未命中 | Windows 桌面 Snap："drag a window to the left or right edge of the screen to snap it"；"Windows key + [up/left/right] arrow"；"Windows key + Z to open Snap Layouts"——触发为鼠标拖拽/键盘，非触摸屏滑动一分为二。Surface Duo："swipe the app up... drag the app over to the center bezel"（上滑+拖到中缝 span），其"分屏"实为两块物理屏 | support.microsoft.com (Snap) / (Surface Duo) / nngroup.com | 桌面端：主输入鼠标/键盘，无"沿触摸屏横向/纵向滑动把单屏一分为二"。Duo：分屏来自硬件双屏而非软件滑动划分，F1 字面"沿触摸屏滑动信号划分显示区域"不满足 |
| F2（按滑动方向把当前显示区域划分为≥2窗口）| 未确定/偏未命中 | Duo："The Duo opens up like a book to show two screens side by side"——并排来自物理双屏（硬件），非"根据横向/纵向滑动信号将当前显示区域划分" | nngroup.com | 桌面 Snap 确有并排窗口，但划分由拖拽/键盘触发而非"按滑动方向"；Duo 由硬件提供两屏，均不落入 F2 的"滑动方向→分屏方向"映射 |
| F3（获取两个显示窗口间的滑动触摸信号）| 未确定/偏未命中 | Duo："swipe up an app... keep your finger held down and move across to the other screen... Let go to finish"——存在跨屏拖动手势 | support.microsoft.com (Surface Duo) | Duo 跨屏拖动是把"一个 app 移到另一屏"，方向单一；桌面 Snap 无跨窗口滑动手势（只能逐个拖窗/键盘挪位）。F3 字面"窗口间滑动触摸信号"在 Duo 仅部分形似 |
| F4（依滑动信号双向互换两窗口内容）| 未命中（正向反据）| Windows 11："Windows 11 doesn't have a built-in 'swap' feature to instantly exchange the positions of two snapped windows"；Duo 跨屏手势把单个 app 移到另一屏（单向），无"A→B 且 B→A 双向对调" | support.microsoft.com (Snap) / (Surface Duo) | F4 为 [AND] 双向互换缺一不可。桌面 Snap 官方明示无 swap；Duo 为单向移动一个 app。本专利最具区分性特征（两已分屏窗口内容互换）在两个子产品均无 |

## 已检查文档清单
- Microsoft 官方支持《Snap your windows》正文摘要（Snap 触发=拖拽/键盘 Win+方向/Win+Z）— https://support.microsoft.com/en-us/windows/snap-your-windows-885a9b1e-a983-a3b1-16cd-c531795e6241
- Microsoft 官方支持《Different ways to use Surface Duo》正文摘要（上滑+横移把 app 移到另一屏；上滑拖到中缝 span）— https://support.microsoft.com/en-us/surface/different-ways-to-use-surface-duo-2d8854da-a49f-ecaf-a99d-9f571a696d6e
- NN/g《Multitasking on Microsoft's Surface Duo》（分屏=两块物理屏/硬件，非软件滑动划分）— https://www.nngroup.com/articles/surface-duo/

## 最终判定
**第 5 档：已排除（(a) 正向事实反据 + (c) 架构层级不同）**

判定依据（1-3 句）：本候选含两个子产品。① Windows 桌面 Snap 定位为桌面 PC 操作系统，主输入为鼠标/键盘（拖拽到屏边、Win+方向键、Win+Z），不是"具有触摸屏的电子设备 + 沿触摸屏滑动信号"驱动——架构层级与权利要求限定不同（5档(c)）；且官方明示"无内置 swap 两个已贴靠窗口"，对 F4 双向内容互换构成针对该产品的正向反据（5档(a)）。② Surface Duo 虽为触摸设备，但其"分屏"来自两块物理屏幕（硬件）而非软件按滑动方向把单屏一分为二（F1/F2 字面不满足），跨屏手势仅把单个 app 单向移到另一屏、无两窗口内容双向互换（F4 不满足）。本专利最具区分性的 F3+F4"窗口间滑动手势→双向内容互换"在两个子产品均无对应正向事实。

## 升级路径（第3-4档填）
（不适用——第 5 档）

## 总结一句话
微软 Windows Snap 主输入为鼠标/键盘（架构层级不同）且官方明示无两窗口 swap、Surface Duo 分屏来自硬件双屏且跨屏仅单向移动单个 app，本专利区分性的"触摸屏窗口间滑动手势双向互换内容"(F3+F4) 均无对应正向事实，落第 5 档（已排除）。
