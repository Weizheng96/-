# 证据索引 — 12-msft-teams

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| Q1 | Phase1 WebSearch | query | `Microsoft Teams Skype FEC forward error correction packet loss adaptive redundancy` | 泛 FEC 资料，确认自适应 FEC 机制存在 |
| Q2 | Phase1 WebSearch | query | `Microsoft Teams media FEC redundancy network condition adaptive bandwidth estimation engineering` | Teams 生产媒体栈用自适应 BWE + FEC，"adapt the amount of FEC to best fit the observed network loss rate"（方向契合 F2） |
| Q3 | Phase1 WebSearch | query | `assignee:Microsoft patent forward error correction redundancy packet loss adaptive real-time media traffic type` | US20150180785A1（实为 Imagination Technologies 受让）+ 2002–2009 老专利 |
| Q4 | Phase1 WebSearch | query | `Microsoft Skype Teams patent adaptive FEC redundancy amount traffic type loss rate delay scheduling real-time media` | "Skype adjusts its rates, FEC redundancy and video quality by varying packet loss rate, propagation delay and bandwidth" |
| F1 | Phase2 WebFetch | 专利 | https://patents.google.com/patent/US20150180785A1/en | 受让方 Imagination Technologies，非微软，排除 |
| F2 | Phase2 WebFetch | 论文(PDF) | https://arxiv.org/pdf/2409.19867 | Teams 生产 BWE 论文，仅带宽估计，无 FEC 冗余量/调度链 |
| F3 | Phase2 WebFetch | 研究提案 | https://wp.nyu.edu/minghao/rl-afec/ | NYU/Fortinet 提案（2022-06-14），非 Teams 生产 |
| S1 | 引用 | 论文(PDF) | https://arxiv.org/pdf/1310.1582 | FEC 随网络丢包率自适应一般机制（方向契合 F2） |
| S2 | 引用 | 博文 | https://tonyzhang95.github.io/2020/04/28/USF-AFEC/ | "Skype adjusts ... FEC redundancy ... by varying packet loss rate, propagation delay and bandwidth" |

## 工具受限
- Google Patents：WebFetch "unknown certificate verification error"；curl "schannel: failed to receive handshake (35)"。未能完成 `assignee:Microsoft` 过滤检索。
- 无成功落盘的 PDF/HTML（Google Patents TLS 受限；arxiv PDF 由 WebFetch 缓存于 tool-results 目录）。
