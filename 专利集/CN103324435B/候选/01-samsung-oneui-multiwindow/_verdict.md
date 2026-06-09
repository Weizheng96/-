# 01-samsung-oneui-multiwindow verdict

## 候选基本信息
- 名称：One UI 多窗口 / Multi Window（拖拽换位 + flip 对调）
- 组织：三星 Samsung
- 类型：产品
- 初判命中 F#：F1, F2, F3, F4
- 专利公开（授权）日：2017.02.08

## 检索粗筛
- query 1 `Samsung One UI multi window split screen swap apps flip top bottom panes` → 强命中（分隔条 two-arrows / 三点菜单 swap 换位；One UI 8 flip）
- query 2 `Samsung Galaxy split screen swipe gesture two fingers swipe up to split screen enter` → 强命中（两指底部上滑进入分屏，One UI 5.0=2022）
- query 3 `Samsung split screen drag app from one window to other window swap drag and drop multi window` → 命中（换位=点分隔条 two-arrows；跨窗口拖放仅限文本/图片内容传递，非窗口内容互换）
- 候选真实、已商用、本领域（安卓手机/平板系统 UI 分屏）、证据均晚于 2017.02.08 → 不剪枝，进入特征比对。

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 确认命中（字面） | "Place two fingers at the bottom of the screen, swipe up together, and you'll see your screen split in two." / "A two finger swipe from the bottom of the screen will [activate split screen]" | https://www.samsung.com/ph/support/mobile-devices/how-to-use-swipe-gestures-with-multi-window/ ; https://www.samsung.com/us/support/answer/ANS10002022/ | 两指触摸屏滑动手势触发分屏 = F1"分屏触摸信号(滑动信号)"字面命中（One UI 5.0/2022 起，晚于公开日） |
| F2 | 确认命中（等同） | "swipe up together, and you'll see your screen split in two" → 上下两个并排窗口；可拖第二 app 到下半屏 | https://www.samsung.com/ph/support/mobile-devices/how-to-use-swipe-gestures-with-multi-window/ ; https://www.samsung.com/us/support/answer/ANS10002022/ | 滑动信号→划分为上下排列的≥2个显示窗口，命中 F2 [OR] 的"上下窗口"分支；三星用竖直上滑得上下分屏，与权项"横向滑动→上下"方向映射不严格一致，按同手段(滑动)/同功能(分区)/同效果(≥2窗口)判等同 |
| F3 | 公开资料不足（未确定） | 官方换位触发为点按分隔条 two-arrows / 三点菜单 swap 图标："Tap the two arrows to swap the apps' positions" / "tap the three-dot menu on the split line between them, then tap the swap icon (two arrows)"；未检索到"第一窗口→第二窗口滑动手势触发互换"的官方描述 | https://www.samsung.com/us/support/answer/ANS10002022/ | F3 要求"第一显示窗口→第二显示窗口的滑动触摸信号"。三星换位由分隔条箭头点按(tap)触发，非跨窗口滑动信号——字面不命中；但无"该产品不支持跨窗口滑动/仅支持点按"的正向排他陈述，属手段不同+证据缺失，按纪律落"公开资料不足（未确定）"，非反据 |
| F4 | 确认命中（等同） | "Tap the two arrows to swap the apps' positions" — 双向互换（"both applications exchange their screen positions"） | https://www.samsung.com/us/support/answer/ANS10002022/ | F4 核心"双向互换两窗口显示内容"在结果层面命中：A↔B 位置对调，both exchange；惟其触发为点按（接 F3），故 F4 命中依附于 F3 的手段判定 |

## 已检查文档清单
- Samsung 官方支持页 ANS10002022（进入分屏方式 + 分隔条 two-arrows 双向换位）— https://www.samsung.com/us/support/answer/ANS10002022/
- Samsung PH 官方支持页（两指底部上滑进入分屏手势）— https://www.samsung.com/ph/support/mobile-devices/how-to-use-swipe-gestures-with-multi-window/
- SamMobile One UI 5.0 多任务滑动手势（功能首发时间=2022）— https://www.sammobile.com/news/one-ui-5-0-feature-focus-new-multitasking-swipe-gestures-labs/
- Droid Life One UI 8 split screen flip（2025.05.28）— https://www.droid-life.com/2025/05/28/samsung-upgrades-split-screen-in-one-ui-8-update/

## 最终判定
**第 3 档：确认命中≥60%（F1/F2/F4 命中，含等同），F3 公开资料不足且无正向反据**

五档定义（"命中"=三态中"确认命中"含字面/等同）：第1档 全部确认命中·字面；第2档 全部确认命中含≥1等同；第3档 确认命中≥60% 其余为"公开资料不足"且无正向反据；第4档 确认命中<60% 且无触发第5档的正向反据；第5档 已排除（仅当：(a)≥1条 F# 为"确认未命中（有正向反据）"，或(b)全部证据<专利公开日，或(c)架构层级不同）。

判定依据（基于上表 F# 分布）：4 个 F# 中 F1（字面）、F2（等同）、F4（等同，双向互换结果命中）确认命中=3/4=75%≥60%；唯一未确定的 F3（互换触发须为"跨窗口滑动触摸信号"）——三星官方记录的换位触发为分隔条 two-arrows 点按而非跨窗口滑动手势，字面读不上，且未取得"该产品不支持/排除跨窗口滑动换位"的正向排他事实（仅手段不同 + 证据缺失），按纪律落"公开资料不足（未确定）"，不构成正向反据，故不触发第5档。F4 的双向互换效果虽完整命中，但其实现手段(点按)与 F3 主张的滑动信号不同，是本案是否落第2/3档而非第5档的关键分界点：互换"效果"在、但"以窗口间滑动手势触发"这一最具区分性手段未被证实存在。综合落第3档。

## 升级路径（仅当落第 3-4 档时填）
- 重点补 F3：检索三星是否存在"从一个分屏窗口向另一个分屏窗口滑动/长按拖拽以互换两窗口内容"的手势（区别于点 two-arrows 与跨窗口拖放文本/图片）。可查：① One UI 各版本 release note / 用户手册 PDF 中"swap by drag"/"长按拖到另一窗口换位"措辞；② 三星 2017.02.08 之后申请的分屏换位同主题专利权利要求（Google Patents `Samsung split screen swap window drag gesture` after 2017），用其权项判断是否实现"滑动/拖拽换位"手段，可一步把 F3 定为命中或确认手段不同。
- 若证实存在跨窗口滑动/拖拽换位手势 → F3 命中 → 升第2档（全部命中含等同）。
- 若取得三星正向排他陈述"换位仅支持点按、不支持滑动" → F3 仍非反据（非互斥手段，权项只要求存在滑动信号；产品另有点按手段不否定其可同时具备滑动手段），需直接证据证明产品不具备该交互方式方可考虑第5档。

## 总结一句话
三星 One UI 分屏：两指滑动进分屏(F1字面)、上下分屏(F2等同)、分隔条 two-arrows 双向对调两 app(F4等同)均命中；唯 F3"跨窗口滑动手势触发互换"官方记录为点按而非滑动、手段不同且无排他反据→公开资料不足，候选落第 3 档（升档关键是补证三星是否有拖拽/滑动换位手势）。
