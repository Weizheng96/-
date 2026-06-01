# 证据索引 — 25-valve-sdr

候选：Steam Datagram Relay (SDR) — Valve
专利公开日：2021-06-08

## Phase 1 WebSearch query 留痕

| # | query | 命中关键页 | 关键发现 |
| --- | --- | --- | --- |
| q1 | `Valve Steam Datagram Relay FEC redundancy game streaming` | Steamworks doc / Valve Dev Wiki / GameIndustry blog / GameNetworkingSockets repo | 所有命中页面无 FEC / 主动冗余的描述 |
| q2 | `site:github.com ValveSoftware GameNetworkingSockets FEC redundancy` | GitHub repo / SNP 源码 / README | `steamnetworkingsockets_snp.cpp` 中检索到注释 `"If senders do retransmit unreliable segments (perhaps FEC?) then they need to retransmit the exact same segments."` —— FEC 仅以 "perhaps"/未来设想形态出现在注释里，**非已实现产品代码** |
| q3 | `Valve SDR Steam Datagram packet loss adaptive redundant lane` | 同 q1 + rtldg 的 SDR FAQ gist | 均无 adaptive redundancy / 业务类型自适应 / 时延驱动冗余调度的描述 |
| q4 | `"GameNetworkingSockets" "FEC" code OR comment OR feature` | repo 主页 + 多个二级镜像 / 第三方 blog | 搜索引擎层无 FEC 实装的代码 / 文档 hit |

## Phase 2 WebFetch URL 留痕

| # | URL | 状态 | 关键摘录 |
| --- | --- | --- | --- |
| W1 | https://partner.steamgames.com/doc/features/multiplayer/steamdatagramrelay | 200 | Steamworks 官方 SDR 文档；**无 FEC / 冗余 / 主动重传任何提及**；仅讲 relay 路由 + DDoS 防护 + 加密 |
| W2 | https://github.com/ValveSoftware/GameNetworkingSockets/blob/master/src/steamnetworkingsockets/clientlib/steamnetworkingsockets_snp.cpp | 200 | SNP 实现（4784 行）；前 1000 行内**无 FEC / 冗余 / 业务类型自适应**；仅 reliable/unreliable 消息分片 + ack/nack 序列化 + token-bucket 限速 + 优先级 lane 排队 + 包解码 |
| W3 | https://raw.githubusercontent.com/ValveSoftware/GameNetworkingSockets/master/README.md | 200 | repo README；**无 FEC / 主动冗余 / 业务类型自适应**；明确描述为 "reliable & unreliable messages over UDP" + ack vector 机制 |
| W4 | https://github.com/ValveSoftware/GameNetworkingSockets/blob/master/README_P2P.md | 200 | **无 FEC / 冗余 / 业务类型自适应**；仅讲 P2P / NAT 穿透 / STUN/TURN |
| W5 | https://gist.github.com/rtldg/9e6ea7aa9b37388c119d31043b7f5189 | 200 | 民间 SDR FAQ 整理；**无 FEC / 冗余**描述 |
| W6 | https://gameindustry.eu/blog/steam-datagram-relay/ | 200 | 第三方 SDR 介绍 blog；**无 FEC / 冗余 / 主动重传** |
| W7 | https://developer.valvesoftware.com/wiki/Steam_Datagram_Relay | 403 (Anubis JS challenge) / WebFetch 403 | 直接抓取被反爬阻断；但 WebSearch snippet 与 Steamworks doc 一致 |

## 工具受限明示

- `gh` CLI 不可用（command not found） —— GitHub Code Search via WebFetch 被登录墙拦截（"sign in to access code search"），故未能跨整个 repo 完整 grep FEC
- Valve Developer Wiki 直接 curl 被 Anubis JS challenge 阻断（5xx-like 行为）；fallback 只能依赖 WebSearch snippet
- 综合 Steamworks 官方 + GameNetworkingSockets 开源 README + SNP 源码片段 + README_P2P + 第三方 FAQ 五个独立来源，FEC / 主动冗余 / 业务类型自适应在 Valve SDR 公开层面**一致缺失**
