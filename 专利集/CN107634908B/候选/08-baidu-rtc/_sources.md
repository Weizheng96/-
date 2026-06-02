# 证据索引 — 08-baidu-rtc（检索留痕）

## Phase 1 — WebSearch（react 粗筛）
1. `百度智能云 RTC 弱网 NACK FEC 冗余 动态比例` → 命中 2 篇百度自有文档（cloud.baidu.com/article/294038、ai.baidu.com/forum/topic/show/991037）+ 同主题第三方。判定：相关，继续。
2. `百度 RTC FEC 冗余 网络状态 业务类型 QoS 自适应 抗弱网` → 百度自有 QoS 文档（cloud.baidu.com/article/3670952）+ 网易/融云同主题。判定：相关。
3. `百度 Baidu 专利 冗余数据包 数量 网络状态 业务类型 时延 FEC H04L1/1867` → 候选 metadata 关联专利 CN111314022A，经核为四川大学，非百度，剔除。

## Phase 2 — WebFetch（react 深抓）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2021-10-27 | 百度自有文档 | https://cloud.baidu.com/article/294038 | 《实时音视频抗弱网技术揭秘》。仅"根据实际丢包、延时改变 NACK+FEC 带宽分配比例"；未涉及三输入冗余量 / 业务类型识别 / 时延→总时间 / 调度方法 |
| 2 | 2025-09-19 | 百度自有文档 | https://cloud.baidu.com/article/3670952 | 《WebRTC QOS 技术深度实践指南》。ULPFEC/RED 生成冗余包；未涉及 F1/F2 三输入/F3/F4 |
| 3 | 2025-10-10 | 百度自有文档 | https://cloud.baidu.com/article/3833432 | 《WebRTC 产品智能优化实践》。"根据丢包类型动态切换策略"、场景分辨率切换；未涉及 F1/F3/F4，无冗余量计算输入变量 |
| 4 | 2020-06-19 | 专利（排除误关联） | https://patents.google.com/patent/CN111314022A/zh | 申请人=四川大学（非百度），申请 2020-02-12。与本候选无关，仅用于排除 metadata 误关联 |

## 工具受限注明
- https://ai.baidu.com/forum/topic/show/991037 —— WebFetch 返回 HTTP 503；curl UA 兜底仍返回 nginx 503（落盘 baidu-forum-991037.html 仅 190 字节，正文为 503 页面）。该 URL 正文未取得；标题《实时音频抗弱网技术揭秘》疑与 segmentfault.com/a/1190000040794703（2021）同源转载，未独立核验。
