# 11-sony-xperia-multiwindow verdict

## 候选基本信息
- 名称：Xperia 多窗口 / 多任务分屏 / 组织：索尼 Sony / 类型：产品 / 初判命中 F#：F1, F2 / 专利公开日：2017.02.08

## 检索粗筛
- WebSearch 1：`Sony Xperia split screen multi-window how to enter swipe gesture` → 命中 Sony 官方 helpguide 多代机型分屏页；进入分屏=Overview 键 / Side sense 菜单。
- WebSearch 2：`Sony Xperia split screen swap windows switch top bottom apps positions multi-window` → 同批官方页；分屏方向由设备方向决定，"Multi-window switch"=换窗口里的 app，无 swap。
- 粗筛通过（真实在售产品，进入 Phase 2 深抓 verbatim）。

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 公开资料不足 | "Tap (Overview button) in the navigation bar" → "[Multi-window switch]"；备选 "flicking up the Side sense bar, and then tapping [Multi-window] or swiping left on the screen." | helpguide.sony.net/.../xperia-1m6/.../split_screen_mode.html | 进入分屏由 Overview 键/Side sense 菜单点击触发，非"沿触摸屏横向/纵向滑动手势分屏"。属不同交互手段达成"进入分屏"同一效果，单看 F1 为等同信号；但 F2 方向映射被正向否证（见下），故整体不构成 F1+F2 的滑动触发链。 |
| F2 | 未命中（正向反据） | "A window in the Split-screen mode is split vertically in the portrait orientation and horizontally in the landscape orientation." | helpguide.sony.net/.../xperia-1m6/.../split_screen_mode.html | 分屏方向由**设备方向**（竖屏/横屏）决定，明确不由"横向/纵向滑动信号"决定。专利 F2 核心"根据横向滑动→上下、纵向滑动→左右"在 Xperia 上不成立——无滑动信号驱动分屏方向。正向反据。 |
| F3 | 未命中（正向反据） | 官方分屏页仅有 "drag the bar on the partition line"（拖分隔条调整大小/退出）与 "Swipe left or right to select the desired apps"（在 Multi-window switch 里选 app），无"第一窗口至第二窗口的跨窗口滑动以触发互换"指令 | helpguide.sony.net/.../xperia-1m6/.../split_screen_mode.html | 不存在"两个已分屏窗口之间的滑动以互换内容"的跨窗口手势。 |
| F4 | 未命中（正向反据） | "Multi-window switch ... Swipe left or right to select the desired apps, and then tap [Done]"（换某一窗口里显示哪个 app）；Xperia 1 II："Split-screen button – Select a recently used application for the lower window" | helpguide.sony.net/.../xperia-1m6/.../split_screen_mode.html ; helpguide.sony.net/.../xperia-1m2/.../TP0003101962.html | Xperia 的 "Multi-window switch" 是**替换**某个窗口里的应用（选 app），不是把两个窗口内容**双向互换**。跨 2020(1 II)~2024(1 VI) 多代官方文档均无 swap/exchange 功能。专利最具区分性特征（F4 双向互换）正向缺失。 |

## 已检查文档清单
- Sony Xperia 1 VI 官方 Help Guide — Split-screen mode (Multi-window switch)，2024 机型 — https://helpguide.sony.net/mobile/xperia-1m6/v1/en/contents/split_screen_mode.html
- Sony Xperia 1 II 官方 Help Guide — Using the Split-screen mode，2020 机型（历史交叉印证） — https://helpguide.sony.net/mobile/xperia-1m2/v1/en/contents/TP0003101962.html

## 最终判定
**第5档：已排除**

判定依据（1-3 句）：Sony Xperia 分屏方向由**设备方向**决定（竖屏上下/横屏左右），官方文档明确否证 F2 的"滑动方向→分屏方向"映射；其 "Multi-window switch" 仅是**替换**某窗口里的应用，跨 2020~2024 多代官方 Help Guide 均无"两个分屏窗口内容双向互换（swap）"功能，F4（本专利最具区分性特征）有正向缺失反据。命中硬门槛(a)：≥1 个 F#（F2、F4）确认未命中且有针对该候选的正向反向事实，非推断非缺失。

## 升级路径（第3-4档填）
- （不适用，已落第5档；如未来某代 Xperia/Android 引入"分屏窗口内容互换/swap"或"滑动方向决定分屏方向"特性，需重新核查并升级。）

## 总结一句话
Sony Xperia 分屏方向由设备朝向决定且无"两分屏窗口内容互换"功能，F2/F4 有官方正向反据，落第5档（已排除）。
