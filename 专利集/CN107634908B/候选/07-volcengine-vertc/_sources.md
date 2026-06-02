# 证据索引 — 07-volcengine-vertc

## 时间窗基准
- 专利公开（授权）日：2021-06-08，仅 2021-06-08 之后公开材料计入。

## Phase 1 — WebSearch 粗筛（react 串行）
1. `火山引擎 veRTC 弱网 FEC 冗余 抗丢包 自适应` → 通用 WebRTC FEC 原理为主，无 veRTC 专属细节（相关但泛化）。
2. `火山引擎 RTC FEC 冗余 网络状态 业务类型 自适应 QoS 弱网` → 强信号：veRTC 有"弱网冗余传输"模式；按丢包率动态调冗余度（<2%降、>5%升至20-30%）；按场景(1v1/多人/直播)差异化 QoS。
3. `assignee:Bytedance FEC redundancy adaptive transmission H04L1/1867 service type network state patent` → 均第三方(Intel等) adaptive FEC 专利，未检索到字节自有同主题专利。
4. `字节跳动 火山引擎 RTC FEC 冗余度 丢包率 业务类型 调度 弱网 InfoQ` → InfoQ《火山引擎 RTC 在互娱场景下的最佳实践》（字节跳动技术团队，2021-07）等。
5. `字节跳动 Bytedance patent FEC redundancy adaptive 冗余 业务类型 发送 google patents` → 未检索到字节自有 FEC 冗余/业务类型自适应专利。

## Phase 2 — WebFetch 深抓（react 串行）
| # | 时间 | 类型 | URL | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-05-31 | 技术博客 | https://blog.csdn.net/ByteDanceTech/article/details/130979702 | 《多链路传输…探索和实践》仅披露"弱网冗余传输=检测弱网开启双链路"多链路架构；FEC 冗余量算法/三输入/调度链在付费墙内，未见。 |
| 2 | — | 开发者社区 | https://developer.volcengine.com/articles/7241139154191384631 | 《从 QoS 到 QoE》QoS/QoE 指标体系与诊断，属监测层；无冗余量计算/时延-调度链；仅提"不同场景容忍度不同"。 |
| 3 | 2021-07 | InfoQ | https://www.infoq.cn/article/lsse5opgclmmimeasxol | 《互娱场景最佳实践》服务端选流/智能合流/云渲染架构；无 F1/F2/F3/F4 级别披露。 |

## 小结
veRTC 确有自适应 FEC 冗余 + 弱网冗余传输 + 场景差异化 QoS（域强相关，时间合规）。但权 1 三输入冗余量算法（F2）、数据流特征自动识别业务类型（F1）、时延→传输总时间→调度三级链（F3/F4）公开材料均未达可逐字比对级别，多为架构/QoE 层。属资料不足，非反向。
