# 17-tcl-splitscreen verdict

## 候选基本信息
- 名称：TCL 系统分屏 / 组织：TCL / 类型：产品 / 初判命中 F#：F1, F2 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 命中（等同） | "swipe up with 3 fingers on the screen to activate split mode"；"Swipe to corner to trigger float window/split screen" | https://support.tcl.com/common-questions-50-series/how-can-i-use-the-split-screen-function ; https://www.tcl.com/global/en/support-mobile/faq/17003 | 专利 F1=触摸屏横向/纵向滑动信号触发分屏；TCL 以"三指上滑/滑向边角"触摸屏滑动手势触发分屏——同手段（触摸屏滑动信号）、同功能（触发分屏）、同效果→等同命中。TCL 另提供 Recent Apps 菜单入口属非互斥替代手段，不构成反据。 |
| F2 | 命中（核心字面）+方向映射未确定 | 进入分屏后"select and drag the Divider icon in the middle of the screen up or down"，屏幕被分隔条划分为两个窗口 | https://support.tcl.com/common-questions-50-series/how-can-i-use-the-split-screen-function | 专利 F2 核心=当前显示区域划分为"至少两个显示窗口"(N≥2)——TCL 分屏确为两窗口，字面命中该核心。专利 F2 的"横向滑动→上下 / 纵向滑动→左右"方向映射限定，公开资料未记载由何决定→该限定分支公开资料不足（未确定），非反据。 |
| F3 | 公开资料不足（未确定） | （4 source 均无"窗口间滑动触摸信号"记载；仅记载分隔条拖动调整大小/全屏） | https://support.tcl.com/common-questions-50-series/how-can-i-use-the-split-screen-function | 专利 F3=获取两分屏窗口之间的滑动触摸信号。TCL 公开文档对"跨窗口滑动手势"沉默——非 verbatim 否定，按纪律落"未确定"，不据此判第5档。 |
| F4 | 公开资料不足（未确定） | （4 source 均无"两窗口内容双向互换/swap"记载） | https://www.tcl.com/global/en/support-mobile/faq/17003 | 专利 F4=依窗口间滑动把两窗口内容双向互换（[AND] 双向缺一不可）。TCL 公开文档仅有"分隔条拖动调整大小/拖到顶/底全屏"，对"内容互换"沉默——非正向否定，落"未确定"。 |

## 已检查文档清单
- TCL 50 系列官方支持页（分屏功能：三指上滑/滑向边角触发，分隔条调整大小，无互换记载） — https://support.tcl.com/common-questions-50-series/how-can-i-use-the-split-screen-function
- TCL 全球移动 FAQ 17003（Recent Apps 入口 + 三指上滑入口，无互换记载） — https://www.tcl.com/global/en/support-mobile/faq/17003
- TCL 全球移动 FAQ 7061 / 7362（分屏入口与分隔条调整，命中要点同上） — https://www.tcl.com/global/en/support-mobile/faq/7061
- AT&T TCL 30 Z 分屏教程（WebFetch 403 未取正文，已用官方页交叉印证） — https://www.att.com/device-support/article/wireless/KM1490545/TCL/TCL4188R

## 最终判定
**第 4 档：命中<60% 且无第5档反据（公开资料不足）**

判定依据（1-3 句）：F1 等同命中、F2 核心（≥2 窗口分屏）字面命中，但本专利最具区分性的特征 F3+F4（"以窗口间滑动手势把两个已分屏窗口内容双向互换"）在 TCL 全部公开文档中均无记载——属沉默/缺失而非 verbatim 正向否定，故落"未确定"而非第5档。4 个 F# 中确认命中 2 个（F1、F2 核心）= 50%<60%，且不存在针对该候选的反向事实（无"不支持互换"的正面否定、时间合规、同为触摸屏移动终端架构同层级），故落第 4 档，不可判第5档（0/沉默≠已排除）。

## 升级路径（第3-4档填）
- 取证 F3/F4 关键：核查 TCL 现行机型（基于 Android，多为类原生/AOSP 多窗口）是否提供"长按分隔条/双击分隔条/拖拽窗口互换"两个分屏窗口内容的交互——查 TCL 官方完整用户手册 PDF、机型评测视频、或在真机上实测分隔条双击/长按。若证实存在"窗口内容互换"手势→F3/F4 命中，可升至第 2/3 档；若证实 TCL 明确不提供该互换→才可据 F3/F4 正向否定考虑第5档。
- 取证 F2 方向映射：核查 TCL 分屏方向（上下/左右）是否随手势方向变化，以判定 F2 第二分支是否字面命中。

## 总结一句话
TCL 系统分屏 F1（三指上滑触发，等同）、F2 核心（≥2 窗口分屏）命中，但区分性特征 F3/F4（窗口间滑动互换内容）公开资料未记载、无正向反据，命中率 50%<60%，落第 4 档。
