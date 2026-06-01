# 证据索引 — 17-baidu-apollo

## Phase 1 WebSearch 留痕（4/4 query 用完，触发早判定）

### q1: `Baidu Apollo V2X 云控 通信 抗丢包 冗余`
命中（节选）：
- https://jiaotong.baidu.com/v2x/ — 百度地图智慧交通 V2X 解决方案
- https://zhuanlan.zhihu.com/p/633494046 — 百度 Apollo 车路协同自动驾驶探索与实践（提 50ms 空口 / 200ms 端到端 / 轨迹预测模型补偿丢包，**应用层补偿，非 packet-level FEC**）
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10856888/ — V2I 协作感知论文（背景参考）
- https://arxiv.org/pdf/2304.11821 — Interruption-Aware Cooperative Perception V2X（学术，非 Apollo 实现）

要点：Apollo V2X 公开资料中丢包应对 = 轨迹预测补偿（接收端推断），非主动发送冗余包。

### q2: `Apollo CyberRT messaging 弱网 FEC redundancy`
命中（节选）：
- https://github.com/ApolloAuto/apollo/blob/master/docs/04_CyberRT/CyberRT_FAQs.md
- https://github.com/ApolloAuto/apollo/blob/master/cyber/doxy-docs/source/CyberRT_FAQs.md
- https://apolloauto.github.io/apollo/04_CyberRT/CyberRT_FAQs.html
- https://cyber-rt.readthedocs.io/en/latest/CyberRT_FAQs.html

要点：CyberRT 默认进程内 INTRA / 跨进程 SHM / 跨主机 RTPS（UDP multicast）；FAQ 未提 FEC / 业务类型自适应 / 主动冗余。
注：ClassicOldSong/Apollo 是另一个同名游戏 streaming 项目（非自动驾驶 Apollo），其 FEC issue 与本候选无关。

### q3: `site:github.com ApolloAuto FEC redundancy packet`
命中（节选）：
- https://github.com/apolloauto/apollo — Apollo 仓库主页
- https://github.com/ApolloAuto/apollo/blob/master/modules/bridge/README.md
- https://github.com/apolloauto — Apollo Auto 组织页

要点：ApolloAuto/apollo 内未见 FEC / redundancy 关键词直接命中页。bridge README 描述为 UDP 单发 + 接收 + 解析。

### q4: `ApolloAuto apollo bridge UDP "service_type" OR "redundancy" OR "FEC" packet loss`
命中（节选）：
- https://github.com/ApolloAuto/apollo/blob/master/modules/bridge/README.md
- https://github.com/ApolloAuto/apollo/blob/master/modules/bridge/udp_bridge_multi_receiver_component.cc
- https://daobook.github.io/apollo/docs/specs/bridge_header_protocol.html
- https://daobook.github.io/apollo/modules/bridge/README.html
- https://github.com/ApolloAuto/apollo/issues/9650
- https://github.com/ApolloAuto/apollo/issues/10816
- https://github.com/ApolloAuto/apollo/issues/5375
- https://github.com/ApolloAuto/apollo/issues/13276
- https://github.com/ApolloAuto/apollo/issues/14334

要点：bridge = UDP sender + receiver，按 65535 B 分片后逐 frame 发送 + 接收端重组反序列化；**无 redundancy / FEC / 冗余包 / 业务类型自适应字段**。Issue 列表围绕 topic 转发 / 解析 bug，未见 FEC 议题。

## Phase 2 WebFetch
**未进入**——Phase 1 4 次 query 已得出"公开层 F1-F5 0 命中"明确结论；继续 Fetch 无新增证据空间（Apollo 云控 / V2X 服务器端闭源，Web 不可达）。节约 token budget。

## 证据时间窗
- 所有命中页内容均在 Apollo 长期迭代项目内，覆盖 2021-06-08（专利公开日）前后，**时间窗合规**，可用于判定。
