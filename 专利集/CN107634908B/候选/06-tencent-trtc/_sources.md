# 证据索引 — 06-tencent-trtc

## Phase 1 — react 粗筛 WebSearch
1. `腾讯云 TRTC 弱网 FEC 冗余 抗丢包 自适应`
   - 命中：TRTC 实测抗丢包率>80%、抗抖动>1000ms；《基于内容关键性的高效 FEC 抗丢包算法》（发送端根据网络状况反馈结果配置 FEC 冗余率）；智能网络适应算法动态调整传输方式。→ 强相关，不剪枝。
2. `TRTC FEC 冗余率 网络状态 业务类型 QoS 自适应 调度`
   - 命中多为通用 WebRTC/QoS 文章（网易云信、metaRTC、知乎 WebRTC Qos）；提到自适应冗余率 + ARQ/FEC 协调调度器，但非 TRTC 专属披露。

## Phase 2 — react 深抓 WebFetch
- WebFetch https://cloud.tencent.cn/developer/article/1020364 （腾讯云开发者社区《基于内容关键性的高效 FEC 抗网络丢包算法》）
  - 摘录："发送端根据网络状况反馈结果配置的FEC冗余率"；"对关键参数进行FEC编码"，按内容关键性级别自适应取得带宽与质量平衡（节省 55-100% 带宽）。
  - 仅确认按网络状况反馈配置冗余率（部分对应 F2 的"网络状态"输入）；未披露"传输成功率+业务类型"双输入、未披露 F1 业务类型自动识别、未披露 F3 时延→传输总时间、未披露 F4 调度方法生成。
- WebSearch `assignee Tencent patent FEC 冗余 网络状态 业务类型 时延 调度 H04L1/1867`
  - 未检索到腾讯自有"三输入冗余 + 时延调度链"同主题专利；返回均为第三方无关专利。
- WebFetch https://cloud.tencent.com/developer/news/840659 （腾讯云开发者社区《音视频学习--弱网对抗技术相关实践》）
  - 摘录："在发送端，针对媒体包增加一定冗余 FEC 包"；"针对不同的网络条件，依据丢包率、RTT 等相关参数"调整。
  - 仅确认 FEC + 按丢包率/RTT（网络状态）整体调整；未披露 F1/F3/F4 及 F2 的传输成功率+业务类型输入。

## 工具受限注明
- 知乎 https://zhuanlan.zhihu.com/p/1910993857153331687 (《理解并解决高丢包率…》) WebFetch 403；curl UA 兜底仅返回 694B 反爬壳（非 SPA，提取脚本无效），未取得正文。落盘文件已删除。
