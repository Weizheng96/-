# 12-amazon-fireos-splitscreen verdict

## 候选基本信息
- 名称：Fire OS 分屏视图 Split View / 组织：亚马逊 Amazon / 类型：产品 / 初判命中 F#：F1, F2 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（分屏由触摸屏滑动手势触发） | 未命中 | "you can only initiate the multiwindow mode through the task-switching button, which is on the right of the Home button in the navigation bar" | https://kindlefireforkid.com/use-split-screen/ | 分屏由 task-switcher/Recents 按钮 → 菜单 "Split Screen" 触发，非"沿触摸屏横向/纵向滑动信号"。属"通过菜单/多任务卡片按钮进入分屏、无滑动手势"——SKILL 已注此情形需个案判等同；这里有明确正向反证据指向"仅能经按钮进入" |
| F2（按滑动方向把显示区域划分为≥2窗口） | 未命中 | "the first app always occupies the left (in landscape orientation) or top (in portrait orientation) of the screen"；"You can now select an app to show on the right half" | https://kindlefireforkid.com/use-split-screen/ ; https://www.lovemyfire.com/how-to-use-split-screen-on-fire-tablet.html | 分屏方向由设备朝向（横屏→左右、竖屏→上下）决定，且第二窗口内容由用户手动选取——非"横向滑动→上下/纵向滑动→左右"的滑动方向映射，无 F2 的方向映射机制 |
| F3（获取两个窗口之间的滑动触摸信号以互换） | 未命中（公开资料证为反向） | "Fire HD 10 and Fire HD 10 Plus do not allow you to switch the app slots." | https://kindlefireforkid.com/use-split-screen/ | 不存在"窗口间滑动以互换内容"交互；拖中央分隔条仅用于 resize 或退出分屏（拖到边缘则关闭一个 app，另一占满全屏），非两窗口互换 |
| F4（依滑动信号双向互换两窗口显示内容） | 未命中（公开资料证为反向） | "do not allow you to switch the app slots"；官方仅 "drag and drop files and objects between windows" | https://kindlefireforkid.com/use-split-screen/ ; https://developer.amazon.com/apps-and-games/blogs/2021/04/new-fire-hd-10-tablets | 明确"不允许互换 app 槽位"；官方仅描述窗口间拖放文件/对象，无"两窗口应用内容双向对调（A→B 且 B→A）"，缺本专利最具区分性的互换特征 |

## 已检查文档清单
- lovemyfire.com 分屏教程（2021）：进入分屏 = task switcher 菜单 → "Split Screen" — https://www.lovemyfire.com/how-to-use-split-screen-on-fire-tablet.html
- developer.amazon.com 官方博客（2021-04-27，Fire OS 7）：side-by-side + 窗口间 drag-and-drop 文件 — https://developer.amazon.com/apps-and-games/blogs/2021/04/new-fire-hd-10-tablets
- kindlefireforkid.com 分屏完整指南（2021，curl 兜底落盘）：仅 task-switching 按钮进入；首 app 固定左/上；不允许互换 app 槽位 — https://kindlefireforkid.com/use-split-screen/

## 最终判定
**第5档：已排除**

判定依据（1-3 句）：Fire OS（Fire 平板，Fire OS 7，2021，时间合规）分屏仅能经 task-switcher/Recents 按钮 → 菜单 "Split Screen" 进入（非滑动手势，反 F1），分屏方向由设备朝向决定且第二窗口由用户手动选取（非滑动方向映射，反 F2）。最关键的本专利区分性特征——"以窗口间滑动手势双向互换两个分屏窗口内容"——有针对该候选的正向 verbatim 反证据："do not allow you to switch the app slots"（不允许互换 app 槽位），且拖分隔条仅用于 resize/退出而非互换（反 F3、F4）。满足第5档硬门槛 (a)：≥1 个 F#（实为 F3、F4）确认未命中且有正向事实反证据。

## 升级路径（第3-4档填）
- （不适用，已落第5档）

## 总结一句话
亚马逊 Fire OS Split View 分屏仅经 task-switcher 菜单触发、方向由屏幕朝向决定、且官方文档明确"不允许互换 app 槽位"无窗口间滑动互换交互，与本专利 F1/F2/F3/F4 均不符且 F3/F4 有正向反证据，落第5档（已排除）。
