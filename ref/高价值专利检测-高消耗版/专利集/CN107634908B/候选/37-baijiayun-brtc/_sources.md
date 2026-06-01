# 证据索引 — 37-baijiayun-brtc

## Phase 1 粗筛（WebSearch）

| # | Query | 命中要点 |
| --- | --- | --- |
| q1 | 百家云 BRTC 教育 RTC FEC 抗丢包 冗余 | docs.baijiayun.com/rtc/ 明示"智能网络状况探测、码率动态调整、智能 FEC、PLC 算法 / 抗 800ms 抖动 / 30% 丢包"。命中 F5 信号；F1-F4 不明。 |
| q2 | Baijiayun BRTC adaptive redundancy FEC education streaming | 英文官网（baijiayun.com/en/brtc）声明 "Recovering packet loss through redundant packet encoding algorithm" + "up to 70% packet loss"（视频）/ "80%"（音频）。F5 命中；F1-F4 不明。 |
| q3 | 百家云 BRTC 业务类型 自适应 网络状态 调度 教育 直播 | 多源（云巴巴 / CSDN / docs）反复印证"网络自适应 + 智能 FEC"宣传语；"业务场景"包括一对一/小班/大班/双师/会议/连麦，但**未发现业务类型→冗余量映射**的描述。 |

## Phase 2 深抓（WebFetch）

| # | URL | 命中要点 |
| --- | --- | --- |
| 1 | https://docs.baijiayun.com/brtc/ | 仅复述 "智能网络状况探测，码率动态调整，智能 FEC、PLC 算法" + "抗 800ms 抖动 / 30% 丢包"。F1-F4 技术细节未公开。 |
| 2 | https://docs.baijiayun.com/rtc/ | 同上；技术细节链接（音视频引擎 / 弱网对抗 / SDK 架构）未暴露深层文档。 |
| 3 | https://blog.csdn.net/u012368971/article/details/135723763 (2024-01-21) | 解决方案概览，无 FEC / 业务类型 / 调度算法细节。 |
| 4 | https://blog.csdn.net/epubcn/article/details/141853774 (2024-09-03) | 强调"自主研发音视频引擎 + 网络自适应"四特性宣传语；五项技术细节（F1-F4 + 调度）**全部未披露**。 |
| 5 | https://www.baijiayun.com/en/brtc | 英文产品页：redundant packet encoding 抗丢包；jitter buffer；端到端 68ms 低延迟；但无业务类型分类描述，无调度算法描述。 |

## 时间窗

百家云 BRTC 至少持续运营至 2024-Q3（CSDN 2024-09 描述 HarmonyOS NEXT 适配），晚于专利公开日 2021-06-08 — **时间窗合规**。
