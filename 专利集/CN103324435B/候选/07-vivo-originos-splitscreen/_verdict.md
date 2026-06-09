# 07-vivo-originos-splitscreen verdict

## 候选基本信息
- 名称：OriginOS / Funtouch 分屏 / 原子窗口 / 组织：vivo / 类型：产品 / 初判命中 F#：F1, F2, F3 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 命中（等同） | "You can now enter the split-screen mode just by swiping up three fingers from any supported app." | https://www.gizmochina.com/2024/10/21/funtouch-os-15-new-features-and-major-changes/ | 三指上滑（触摸屏滑动手势）触发分屏=滑动信号触发分屏。注：vivo 是"三指上滑"单一方向触发，而非专利的"横向滑动 vs 纵向滑动"区分方向；同为"触摸屏滑动手势触发分屏"，落字面/等同区间，命中。 |
| F2 | 命中核心 + 方向映射限定公开资料不足 | "swiping up three fingers ... split the screen ... On the bottom half of the screen, you'll see a selection of apps"；"Vivo's split screen feature allows the screen to be shared both vertically and horizontally" | https://www.gizmochina.com/2024/10/21/funtouch-os-15-new-features-and-major-changes/ ; （搜索摘要）vivohelp.com | "把当前显示区域划分为至少两个显示窗口"（上下并排，N=2）核心命中。但专利 F2 含"滑动方向决定排列方向"（横向滑动→上下/纵向滑动→左右）的映射限定；vivo 三指上滑后布局随设备朝向（竖屏=上下、横屏=左右），未见"滑动方向↔排列方向"映射证据→该限定公开资料不足，无正向反据。 |
| F3 | 公开资料不足 | "The three dots in the middle let you swap the apps"；"some vivo phones provide a swap icon near the divider, allowing you to switch app positions"；"resize the window by dragging the splitting dot"（拖中间条仅为调整窗口大小） | https://www.gizmochina.com/2024/10/21/funtouch-os-15-new-features-and-major-changes/ ; （搜索摘要）mobigyaan.com | 专利 F3 要求"第一窗口→第二窗口的跨窗口滑动触摸信号"。vivo 对调由"中间三点菜单/分隔条旁 swap 图标"点击触发；中间分隔条的拖动仅用于调整窗口大小，非内容互换。未检索到"窗口间滑动手势触发互换"的公开证据，亦无"vivo 不支持窗口间滑动"的正向反据→公开资料不足（不剪枝）。 |
| F4 | 命中（效果在，手段不同） | "let you swap the apps"；"swap screens feature with two vertical arrows pointing in opposite directions ... switch app positions" | https://www.gizmochina.com/2024/10/21/funtouch-os-15-new-features-and-major-changes/ ; （搜索摘要）mobigyaan.com | 互换"效果"明确存在：两个分屏应用位置双向对调（A↔B），满足 F4 的"双向互换 vs 单向替换"区分。但触发手段是"点击菜单/swap 图标"而非专利的"窗口间滑动信号"；不同交互手段实现同一互换效果=等同信号，非反据。 |

## 已检查文档清单
- Funtouch OS 15 新特性（三指上滑进入分屏、中间三点菜单 swap apps + resize）— https://www.gizmochina.com/2024/10/21/funtouch-os-15-new-features-and-major-changes/
- vivo Smart Split 使用指南（swap icon near divider 切换位置、拖分隔条 resize、recents 替换某一侧）— https://www.mobigyaan.com/how-to-use-split-screen-feature-on-vivo-smartphones （WebFetch 403，采信 WebSearch 返回正文摘要，已交叉印证 gizmochina）
- vivohelp 分屏说明（竖向/横向皆可分屏）— https://vivohelp.com/en/razdelenie-ekrana-vivo/ （WebFetch 526，仅得搜索摘要，工具受限）

## 最终判定
**第 3 档：核心命中，关键区分特征公开资料不足，无反据**

判定依据（1-3 句）：F1（滑动手势触发分屏）、F4（双向互换效果）明确命中；F2 的"划分为≥2 窗口"核心命中，但"滑动方向决定排列方向"映射限定无证据；F3 的"窗口间跨窗滑动信号"无公开证据——vivo 实测以"菜单/swap 图标点击"实现互换，与专利"窗口间滑动"为不同交互手段（等同信号、非反据）。命中 F1+F4 确认、F2 核心命中、F3 待证，落第 3 档；未达第 5 档硬门槛（无任一 F# 的正向反证，无时间不合规，架构同层）。证据均晚于专利公开日 2017.02.08（Funtouch OS 15 = 2024），时间合规。

## 升级路径（第3-4档填）
- 取证 vivo 是否存在"从一个分屏窗口向另一个分屏窗口的跨窗口滑动/拖动手势触发内容互换"（F3 关键）——查 vivo 官方帮助中心/中文社区"分屏 互换/对调"原文、OriginOS 原子窗口拖拽动作演示视频。
- 取证 vivo 进入分屏时"滑动方向（横/纵）是否决定上下/左右排列"（F2 映射限定）——查 OriginOS 多任务手势官方说明。
- 比对 vivo 2017.02.08 后同主题分屏专利（如有），看其权利要求是否描述"窗口间滑动互换"，以佐证交互手段差异。

## 总结一句话
vivo OriginOS/Funtouch 三指上滑分屏（F1）+ 双向互换应用（F4）命中，但互换由菜单/图标点击触发、未见窗口间滑动手势（F3 公开资料不足）、滑动方向映射限定（F2）亦无证据，落第 3 档。
