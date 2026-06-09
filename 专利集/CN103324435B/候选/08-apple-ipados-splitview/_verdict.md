# 08-apple-ipados-splitview verdict

## 候选基本信息
- 名称：iPadOS Split View / Slide Over / Stage Manager / 组织：苹果 Apple / 类型：产品 / 初判命中 F#：F1, F2, F3 / 专利公开日：2017.02.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 未确定（等同存疑·偏否） | 「drag another app from the Dock, App Library, or Spotlight to the left or right edge of the screen」；另「quickly swipe a window to the left or right side ... then quickly swipe another window to the other side」 | https://support.apple.com/en-us/125309 | 专利 F1 要求"沿触摸屏横向/纵向滑动信号→划分当前显示区域"。iPad 主流靠 Dock 拖图标/三点菜单进入分屏；iPadOS 26 的"swipe window to a side"语义是把整窗口推到一侧（左右），非"横/纵滑动方向决定上下/左右"映射。手段实质不同，但同为触屏平板分屏（同抽象层，非架构层级不同）。无 verbatim 正向拒绝→未确定，公开资料不足以判等同 |
| F2 | 未确定（部分·结果形态存在但映射缺失） | iPad Split View「仅支持左右并排，不支持上下（top/bottom）分屏」；「Split View divides the iPad's screen in the middle, with each app taking up one half」 | https://support.apple.com/en-us/125309 ; https://www.idownloadblog.com/2023/01/16/how-to-use-split-view-ipad/ | 专利 F2 为 [OR]：横向滑动→上下 或 纵向滑动→左右。iPad 仅有"左右并排"这一结果形态，但并非由"纵向滑动信号"触发产生；"横向滑动→上下分屏"分支在 iPad 完全不存在。结果形态部分对应、触发方向映射缺失→未确定 |
| F3 | 命中（等同） | 「touch the three-dotted menu at the top of either app and drag it left or right to switch your Split View arrangement」 | https://www.idownloadblog.com/2023/01/16/how-to-use-split-view-ipad/ | 长按某窗口顶部把手、拖过中间分隔条到另一侧 = 第一窗口至第二窗口的跨窗口滑动/拖动触摸信号。手段（长按拖动）与专利"滑动触摸信号"功能/效果相同→等同命中 |
| F4 | 命中（字面到等同） | 「drag it left or right to switch your Split View arrangement」；第三方："the apps will trade places" | https://www.idownloadblog.com/2023/01/16/how-to-use-split-view-ipad/ | 互换后两 App 左右位置对调=第一窗口内容到第二、第二窗口内容到第一，双向互换（[AND] 满足），非"在空窗口新开应用"的替换→命中 |

## 已检查文档清单
- Apple 官方 Support「Multitask on iPad with iPadOS 26」（进入方式、左右排布）— https://support.apple.com/en-us/125309
- iDownloadBlog「How to use Split View on iPad」（互换手势 verbatim、左右各半）— https://www.idownloadblog.com/2023/01/16/how-to-use-split-view-ipad/
- WebSearch 摘要：三点菜单/ Dock 拖入进入；仅左右并排不支持上下 — 见 _sources.md Phase 1

## 最终判定
**第 4 档：命中不足 60%，无第 5 档反据（部分技术特征对应，核心触发/方向映射存疑）**

判定依据（1-3 句）：F3（窗口间拖动信号）、F4（两窗口内容双向互换）明确命中（含等同），是本专利最具区分性的"内容互换"特征——iPad 确具备"两已分屏窗口整体互换左右位置"交互。但 F1（分屏触发手段：iPad 靠 Dock 拖/三点菜单，非沿屏横/纵滑动信号）与 F2（方向映射：iPad 仅左右、无"横向滑动→上下"分支，且左右排布非由纵向滑动触发）与专利限定实质不符且公开资料不足以判等同。明确命中约 2/4（<60%），且无任何第 5 档硬反据（时间合规、同为触屏分屏属同抽象层非架构层级不同、无针对该候选的 verbatim 正向拒绝），故落第 4 档。

## 升级路径（第3-4档填）
- 取证 iPad 是否存在"以触摸屏滑动手势（而非 Dock 拖图标/菜单）直接触发分屏"的官方交互：若 iPadOS 26"swipe a window to a side"被认定为"沿触摸屏横向滑动→进入左右分屏"，则 F1 可向等同命中升级。
- 取证 iPad 是否存在任何"纵向/横向滑动方向决定上下 vs 左右排布"的映射（含分屏过程动画/手势方向判定逻辑），以评估 F2 是否等同。
- 比对苹果 2017.02.08 后同主题专利/技术文档中对"swap/对调分屏窗口"的描述，强化 F3+F4 字面命中并固化时间合规。

## 总结一句话
iPad Split View 具备"两分屏窗口整体互换左右位置"的核心区分特征（F3/F4 命中），但分屏触发靠 Dock 拖/三点菜单而非沿屏横/纵滑动、且仅左右无上下映射（F1/F2 等同存疑、公开资料不足），明确命中约半数无第5档反据，落第 4 档。
