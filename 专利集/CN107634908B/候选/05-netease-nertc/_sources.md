# 证据索引 — 05-netease-nertc

## Phase 1 — react 粗筛（WebSearch）
1. `网易云信 NeRTC 弱网 FEC 冗余 抗丢包 自适应` → 强相关。命中多篇网易云信官方技术博客（QoS综述 / 弱网对抗 / QoS策略），披露 FEC + RED + NACK/RTX 自适应抗丢包。
2. `网易云信 FEC 冗余 网络状态 业务类型 QoS NACK 自适应 码率` → 强相关。检索摘要直接给出 FEC 冗余率公式 `TL = a*XL + b*BL`（a 增益系数自适应、BL 观测器基本丢包率），及"ARQ 成功率 + FEC 兜底"、网络状态观测器（丢包/抖动/时延/拥塞）。未早剪枝。

## Phase 2 — react 深抓
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-04-21 | 官方博客 | https://blog.csdn.net/netease_im/article/details/130287054 《网易云信 RTC 音频 QoS 综述》 | FEC 冗余度=贝叶斯(丢包率,rtt,分组长度)；GCC 把带宽分配到 编码/RED/FEC/RTX 码率；NACK/RTX。post-grant 窗口仍在用。 |
| 2 | （同综述） | 官方博客镜像 | http://www.52im.net/blog-8045-2703.html → WebFetch cert error；**curl UA 兜底落盘** `52im-qos-8045-2703.html`(GBK,27KB) | 同《音频 QoS 综述》全文，确认 FEC 贝叶斯冗余、GCC 码率分配、NACK/RTX、RED 机制。 |
| 3 | 2020-07-13 | 官方博客 | https://zhuanlan.zhihu.com/p/136710986（403）；同文 cnblogs https://www.cnblogs.com/wangyiyunxin/p/13295032.html → curl 落盘 `cnblogs-qos-13295032.html`(UTF-8,40KB) | **最完整机制**：FEC 冗余参考丢包率 `TL=a·XL+b·BL`，`XL=L^(C+1)`，`C=(D−R)/I`（D=最大端到端Delay、R=rtt、I=最小NACK间隔）；网络状态观测器；ARQ先行+FEC兜底；调度器协同ARQ/FEC；发送队列优先级（重传>音频>视频>Padding）。**发布于专利公开日 2021-06-08 之前**——仅作机制理解，证据加权以 2023 综述为准。 |

## Google Patents / 旁证
- WebSearch `assignee:网易 FEC 冗余 数据包 网络状态 传输方法` → Justia 列 Netease(Hangzhou) 专利集；CN112860383A（网易杭州，2021-03-12）。未逐篇深抓（产品博客已足够定档）。

## 落盘文件
- 52im-qos-8045-2703.html（GBK,27KB）
- cnblogs-qos-13295032.html（UTF-8,40KB）
- _extract.txt / _extract2.txt（提取正文，供合议引用）
