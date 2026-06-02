# 证据索引 — 10-zoom-meetings

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| P1 | 2026-06 | WebSearch | `Zoom video FEC forward error correction packet loss adaptive redundancy` | 命中泛化 FEC 资料，无 Zoom 专属；相关但需缩窄 |
| P2 | 2026-06 | WebSearch | `Zoom Meetings FEC redundancy network condition packet loss engineering blog media transport` | **有信号**：Zoom Technical Library + ICPE 2023；Zoom 有 reactive QoS + FEC + 自适应码率 |
| P3 | 2026-06 | WebSearch | `Zoom Video Communications patent forward error correction redundant packets adaptive bitrate scheduling` | 均为他方/历史 FEC 专利，无 Zoom 自有同主题专利 |
| P4 | 2026-06 | WebSearch | `assignee Zoom Video Communications patent FEC redundancy packet loss real-time media US patent grant 2022 2023` | 无匹配三输入冗余机制的 Zoom 专利；20230262209 实为 Agora Lab |
| D1 | ~2025-11 | WebFetch | https://library.zoom.com/admin-corner/architecture-and-design/zoom-architected-for-reliability | reactive QoS 监控 bandwidth/packet loss/latency/jitter；adaptive bitrate + packet-loss mitigation；~45% 丢包时 audio 优先 video。**未披露三输入冗余计算 / F1 业务类型识别 / F3-F4 调度链** |
| D2 | 2023 | PDF(pdfplumber) | https://research.spec.org/icpe_proceedings/2023/proceedings/p221.pdf | verbatim："failure recovery mechanisms, including Forward Error Correction (FEC), application-layer retransmission"；"adaptively adapt its video bitrate to different network conditions"；媒体流 0x0f AUDIO/0x10 VIDEO 区分。**确认 FEC+网络自适应+媒体类型区分；未披露冗余包数量内部公式** |
| X1 | 2023-08 | WebFetch | https://patents.google.com/patent/US20230262209A1/en | 经核验 assignee=Agora Lab 非 Zoom，与本候选无关，排除 |

## 工具受限说明
- ICPE 2023 PDF 经 WebFetch 返回二进制无法解析，改用 pdfplumber 本地抽取（成功）。
- Justia patent 页面 HTTP 403；改用 Google Patents 镜像。
- WebSearch 为 US-only；Zoom FEC 内部实现属闭源/专有，工程博客未披露算法级细节。
