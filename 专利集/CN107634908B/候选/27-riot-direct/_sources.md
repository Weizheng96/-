# 27-riot-direct sources / query 留痕

## Phase 1 — WebSearch（4 次）
1. `Riot Direct backbone game network FEC packet loss`
   - 命中：Riot tech blog "Fixing the Internet for Real Time Applications" Part I/II/III；Valorant 玩家排错指南；BT Community 抱怨贴。无任何 FEC / 冗余包描述。
2. `Riot Games engineering blog adaptive packet redundancy`
   - 命中：均为非 Riot 来源；专利来自 USPTO（无 Riot 关联）。Riot 自家工程博客无 "adaptive redundancy" 命中。
3. `Valorant netcode FEC forward error correction redundant packet`
   - 命中：Riot 官方 "Peeking into VALORANT's Netcode"；esports.net 二手分析；F5 通用 FEC 文档（与 Riot 无关）。无 Riot 实现 FEC 的证据。
4. `"Riot Direct" OR "Riot Games" packet duplication redundant transmission low latency`
   - 命中：仅 Riot tech blog 三部曲 + 玩家排错；无 packet duplication / redundant transmission 描述。

## Phase 2 — WebFetch（4 次，含跳转重试）
| # | 时间 | 类型 | URL | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | ~2014-2016 | Riot 官方博客 | https://www.riotgames.com/en/news/fixing-internet-real-time-applications-part-i | 仅描述问题（互联网非为实时应用而建；UDP 丢包是路由器拥塞减负策略）；未提 FEC / 冗余 |
| 2 | ~2014-2016 | Riot 官方博客 | https://www.riotgames.com/en/news/fixing-internet-real-time-applications-part-ii | Riot Direct 核心 = 少跳数 backbone + BGP Communities/MED + ISP peering + 暗光纤；**显式无 FEC / 冗余包** |
| 3 | ~2014-2016 | Riot 官方博客 | https://www.riotgames.com/en/news/fixing-internet-real-time-applications-part-iii | Anycast + 自定义路由协议 + Gateway 引流；track latency/loss/jitter 仅作监测指标 |
| 4 | 2020 | Riot 官方博客 | https://www.riotgames.com/en/news/peeking-valorants-netcode | Valorant 用 **client prediction + server reconciliation** 应对丢包；服务端在缺包时 guess last-known input，**非 FEC** |

## 检索工具受限明示
WebFetch 对 technology.riotgames.com 发生 301 跳转到 riotgames.com/en，已重试成功。所有命中 URL 均为官方 Riot 来源；未触发抓取失败需 curl 兜底的情形。
