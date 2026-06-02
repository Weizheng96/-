# 10-zoom-meetings verdict

## 候选基本信息
- 名称：Zoom Meetings / 组织：Zoom（NASDAQ:ZM） / 类型：产品 / 初判命中 F#：F2, F4, F5 / 专利公开（授权）日：2021-06-08

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（业务类型由数据流特征识别） | 资料不足 | Zoom 区分 "0x0f AUDIO / 0x10 VIDEO"（audio/video/data 三 UDP 流），但未见"由缓存包长度/数目、到达间隔、数据突发性等数据流特征变量**自动推断**业务类型"的披露 | https://research.spec.org/icpe_proceedings/2023/proceedings/p221.pdf | 媒体类型区分存在，但业务类型识别机制（特征变量→类型）未公开；无反向证据 |
| F2（冗余包数量自适应计算·三输入） | 资料不足 | "failure recovery mechanisms, including Forward Error Correction (FEC)…"；"adaptively adapt its video bitrate to different network conditions"；"reactive quality-of-service layer that adapts to real-time network and device conditions"，监控 "bandwidth, packet loss, latency, and jitter" | https://research.spec.org/icpe_proceedings/2023/proceedings/p221.pdf · https://library.zoom.com/admin-corner/architecture-and-design/zoom-architected-for-reliability | 确认 Zoom 用 FEC 且按网络状态自适应；但冗余包**数量**是否同时依「网络状态+传输成功率+业务类型」三输入计算，未公开，无法核验 |
| F3（冗余传输总时间·由时延要求得出） | 资料不足 | 未找到 | — | 闭源；工程博客与学术分析均未披露"时延要求→冗余传输总时间"环节 |
| F4（冗余调度方法生成） | 资料不足 | 未找到 | — | 未披露"网络状态+传输总时间+冗余数量→调度方法"三入一出生成逻辑 |
| F5（按调度方法发送冗余包） | 资料不足 | Zoom 确实发送 FEC 冗余/恢复包（"Forward Error Correction (FEC)"） | https://research.spec.org/icpe_proceedings/2023/proceedings/p221.pdf | 发送冗余包属实，但是否"按 F4 调度方法"发送依赖 F4，F4 未证实 |

## 已检查文档清单
- Zoom Technical Library —「Zoom: Architected for Reliability」（约 2025-11）：reactive QoS 监控 bandwidth/packet loss/latency/jitter，adaptive bitrate + packet-loss mitigation，~45% 丢包时 audio 优先 video — https://library.zoom.com/admin-corner/architecture-and-design/zoom-architected-for-reliability
- ICPE 2023 — Packet-Level Analysis of Zoom Performance Anomalies（同行评审，2023）：确认 Zoom 用 FEC + application-layer retransmission + 按网络状态自适应视频码率 + 区分 audio/video/data 媒体流 — https://research.spec.org/icpe_proceedings/2023/proceedings/p221.pdf
- US20230262209A1：经核验 assignee = Agora Lab 非 Zoom，与本候选无关，排除 — https://patents.google.com/patent/US20230262209A1/en

## 最终判定
**第 4 档：资料不足（弱）**

判定依据（1-3句）：公开来源（ICPE 2023 同行评审 + Zoom 官方技术库，均晚于 2021-06-08）确证 Zoom Meetings 使用 FEC 主动冗余、按网络状态（bandwidth/packet loss/latency/jitter）自适应、并区分 audio/video/data 媒体类型——与权 1 大方向一致；但本专利的判定核心特征（F2 冗余包数量同时依「网络状态+传输成功率+业务类型」三输入、F1 业务类型由数据流特征变量自动推断、F3/F4「时延要求→冗余传输总时间→调度方法」三级链）均为算法级内部实现，Zoom 闭源且无任何公开来源披露，无法核验。无任何反向证据（无来源称 Zoom"不做"上述任一步骤），故不入第 5 档；但有非反向证据支撑的特征明显 <60%（仅 F2/F5 有部分泛化级证据，F1/F3/F4 全为"未找到"），故落第 4 档而非第 3 档。

## 升级路径（仅3-4档）
- 检索 Zoom 自有专利（USPTO/Google Patents `assignee:"Zoom Video Communications" + (FEC OR "forward error correction" OR redundan*)`，2021-06-08 后），权利要求全文最可能一步定档 F2/F4。
- 检索 Zoom 工程博客 / RTC 技术分享（如 InfoQ、Zoom Developer Blog、学术逆向分析）是否披露冗余比例计算输入变量与冗余包发送调度时序。
- 抓取 Zoom 媒体流逆向分析论文（除 ICPE 2023 外）核验是否有"业务类型自动识别"与"冗余调度方法"的实测证据。

## 总结一句话
Zoom Meetings 确用 FEC 主动冗余 + 网络自适应 + 媒体类型区分（公开来源证实），但 F1/F2/F3/F4 的三输入冗余计算与时延→调度三级链均为闭源未披露、无法核验，无反向证据，落第 4 档（资料不足-弱）。
