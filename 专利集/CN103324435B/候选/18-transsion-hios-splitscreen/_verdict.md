# 18-transsion-hios-splitscreen verdict

## 候选基本信息
- 名称：HiOS / XOS 分屏 / 组织：传音 Transsion / 类型：产品 / 初判命中 F#：F1, F2 / 专利公开日：2017.02.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 命中 | "Effortlessly multitask by sliding down with one finger to split your screen into two."（HiOS 13 Fold 单指下滑分屏） | https://www.facebook.com/TECNOMobile/videos/hios-13-fold-how-to-activate-split-screen-apps/531962109009426/ | [OR] 滑动信号任一分支即满足；TECNO 官方演示「单指下滑」=触摸屏滑动手势触发分屏。标准机另有 Recent Apps 按钮路径（手段不同，不影响本分支命中） |
| F2 | 命中 | "run two apps simultaneously — either side-by-side or one-above-the-other"；进入后屏幕被划分为上下两个窗口 | https://www.carlcare.com/gh/tips-detail/how-to-split-screen-on-tecno/ | [OR] 将当前显示区域划分为≥2 个并排窗口（上下/左右）确认；整数限定 N≥2 满足。横滑↔上下、纵滑↔左右的逐一方向映射未见图文确认，但 F2 只需「按手势划分为≥2 窗口」即满足 |
| F3 | 公开资料不足（未确定） | 公开图文/视频仅描述拖动中间分隔条调比例/退出，未见两个分屏窗口间的滑动/拖动跨窗口手势 | https://www.carlcare.com/gh/tips-detail/how-to-split-screen-on-tecno/ | 4 次 WebSearch 均无「窗口间滑动」描述；无针对该候选的正向否定→不剪枝，记为未确定 |
| F4 | 公开资料不足（未确定） | 任何公开来源均未描述「两个已分屏窗口内容双向互换/对调位置」；Carlcare 仅述调比例与退出 | https://www.carlcare.com/gh/tips-detail/how-to-split-screen-on-tecno/ | 本专利最具区分性特征（内容互换）无公开证据，亦无 verbatim「不支持/排除」否定→未确定，非第5档反据 |

## 已检查文档清单
- Carlcare 官方「How to split screen on TECNO phone」(2021-02-22)：进入分屏=Recent Apps+点分屏图标；上下/side-by-side 双窗口；拖分隔条调比例/退出，无互换 — https://www.carlcare.com/gh/tips-detail/how-to-split-screen-on-tecno/
- TECNO Mobile 官方「HiOS 13 Fold | How to Activate Split-screen Apps」(单指下滑分屏) — https://www.facebook.com/TECNOMobile/videos/hios-13-fold-how-to-activate-split-screen-apps/531962109009426/ ；YouTube 同视频 https://www.youtube.com/watch?v=6MuNu5Ns00U
- XOS (operating system) — Infinix（Transsion 子品牌）基于 Android — https://en.wikipedia.org/wiki/XOS_(operating_system)

## 最终判定
**第 4 档：命中<60%，无第5档反据（公开资料不足主导）**

判定依据（1-3 句）：F1（单指下滑触发分屏，TECNO 官方演示）+ F2（划分为≥2 个并排/上下窗口）字面命中，即 4 个特征中 2 个确认 = 50% < 60%；F3（窗口间跨窗滑动信号）与 F4（两窗口内容双向互换）这一最具区分性的特征对在所有公开图文/视频中均无任何描述，属公开资料不足（未确定），但**不存在针对 HiOS/XOS 的 verbatim「不支持互换/排除」正向否定事实**，故不满足第5档硬门槛（0/缺失命中≠已排除）。综合命中率 50% 且 F3/F4 未确定，落第 4 档。

## 升级路径（第3-4档填）
- 抓取传音 HiOS 14 / XOS 14 官方用户手册或 Camon 30 / Phantom V Fold 评测，核查是否存在「分屏窗口位置对调/swap apps」入口及其触发手势（拖动/长按拖拽/分隔条双击）。
- 检索传音 2017.02.08 后同主题专利（multi-window swap）作技术比对，确认其分屏内容互换的实现路径是否落入 F3+F4。
- 真机/录屏验证：HiOS 分屏下能否将上下两窗口内容对调（区别于仅在空窗口新开应用）。若证实存在「窗口间滑动→双向互换」，可升至第2-3档；若证实仅能替换单窗口、无双向互换，且有官方 verbatim 说明，则需重判是否落第5档(a)。

## 总结一句话
传音 HiOS/XOS 分屏的进入（单指下滑/Recent Apps 入口）与上下双窗口划分命中 F1/F2，但最具区分性的「两窗口内容互换」（F3+F4）无任何公开证据亦无反据，落第 4 档。
