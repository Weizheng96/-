# 01-tech-google-webrtc verdict

## 候选基本信息
- 名称：WebRTC / libwebrtc（FlexFEC/ULPFEC）
- 组织：Google（及 WebRTC 社区）
- 类型：技术
- 初判命中 F#：F2, F4, F5
- 专利公开（授权）日：2021-06-08

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（业务类型由数据流特征自动识别） | 反向证据 | "未发现业务类型/media type自动识别机制。系统采用帧级区分…但这是编码层级特征，非业务层级"；Google 论文全文亦无 traffic-type 由包长度/数目/到达间隔/突发性识别的机制 | https://blog.csdn.net/qw225967/article/details/136457874 ; google-handling-packet-loss-webrtc.pdf (本地) | WebRTC FEC 不按"业务类型"差异化，且无任何由数据流特征推断业务类型的环节——这是 F1 的核心限定，两份来源（Google 一手论文 + 源码分析）一致表明该效果与机制均缺失，构成对 F1 的正向缺失证据 |
| F2（冗余包数量=网络状态+传输成功率+业务类型 三输入） | 公开资料不足（部分命中、缺必要输入） | "These network statistics include the available bandwidth, fractions of packets lost and the Round Trip Time (RTT)…The main function of MO…is to set the amount of FEC protection"；源码输入=fraction_lost+estimated_bitrate_bps+RTT+actual_framerate+分辨率 | google-handling-packet-loss-webrtc.pdf ; https://blog.csdn.net/qw225967/article/details/136457874 | 覆盖"网络状态变量(带宽/RTT)+传输成功率(丢包率取补)"两输入，但权 1 限定的第三必要输入"业务类型"缺失（F1 不成立连带 F2 三输入约束不满足）→ 不构成 F2 字面/等同命中 |
| F3（由时延要求得冗余传输总时间） | 公开资料不足 | 文章"未涉及时延要求到冗余包调度的链路设计"；论文仅有接收端附加播放时延 d_add=min(max(K–RTT/2–d_jitter,0),RTT) | https://blog.csdn.net/qw225967/article/details/136457874 ; google-handling-packet-loss-webrtc.pdf | d_add 是接收端 JitterBuffer 播放时延，非发送端"冗余数据包传输总时间"，对象与位置均不同→不命中 |
| F4（由网络状态+传输总时间+冗余数量得调度方法） | 公开资料不足 | 多帧 FEC 跨度 "λ ~ max(1, min(f·RTT, λo))"（依 RTT+帧率）；无"传输总时间→调度"环节 | google-handling-packet-loss-webrtc.pdf | 有多帧 FEC 跨度/排布参数，但不依据"冗余传输总时间"，缺 F3→F4 的总时间驱动调度链→不命中 |
| F5（按调度方法发送冗余包） | 字面命中 | "an FEC encoder is applied…(k,m)…m is the number of FEC packets in that protection group"；"FEC packets follow the source packets they protect" | google-handling-packet-loss-webrtc.pdf | WebRTC 确按保护组在源包后发送 FEC 冗余包；但此为通用 FEC 发送动作，单独命中 F5 不依赖 F1–F4 的判定路径 |

## 已检查文档清单
- Google "HANDLING PACKET LOSS IN WEBRTC"（Holmer/Shemer/Paniconi, ICIP 2013）— WebRTC FEC 由 Media Optimization 依带宽/丢包/RTT/帧率设定保护量；XOR(RFC5109) FEC；无业务类型识别 — https://research.google.com/pubs/archive/41611.pdf（本地 google-handling-packet-loss-webrtc.pdf）
- CSDN「WebRTC FEC逻辑分析」源码级解读 — FecControllerDefault.UpdateFecRates/ProtectionFactor 输入清单，明确无业务类型自动识别、无时延→调度链 — https://blog.csdn.net/qw225967/article/details/136457874
- WebSearch 旁证：getstream media-resilience、bloggeek FlexFEC/ULPFEC、RFC 8854（WebRTC FEC 自适应启停依网络状态）

## 最终判定
**第 4 档：公开资料不足（弱候选）**
五档定义：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且无反向证据；第4档=公开资料不足(弱候选)<60%F#命中；第5档=已排除（仅当(a)≥1条F#真反向证据/(b)全部证据<2021-06-08/(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选的正向事实（verbatim 否定或自有文档/专利写明用另一套手段）；"行业通用机制反推/公开资料未提及"不算反向证据→落第4档。**0命中≠已排除**。
判定依据（1-3句）：WebRTC FEC 确为"依网络状态自适应的主动冗余发送"，与专利同属实时传输抗丢包 FEC 领域，F5 字面命中、F2 命中两输入；但权 1 的灵魂限定"F1 业务类型由数据流特征自动识别 + F2 把业务类型作为第三必要输入 + F3/F4 时延要求→冗余传输总时间→调度三级链"在 WebRTC 中均缺失（Google 一手论文与源码分析双源印证），仅 1/5 字面命中，远低于 60%。F1 虽有正向缺失证据，但其余 F# 多为"公开资料不足/机制不同"而非逐条 verbatim 否定，按"0 命中≠已排除"与第5档硬门槛，不升至第5档，落第4档。

## 升级路径（仅当第3-4档时填）
- 抓取 webrtc.googlesource.com 现行 `modules/video_coding/fec_controller_default.cc` 与 `media_opt_util.cc` 源码，逐字核验是否存在任何 traffic-type / content-type 输入影响 FEC rate（若确为 verbatim 无→可考虑升至第5档反向证据）。
- 核查 WebRTC 是否对不同 media type（audio inband-FEC vs video FlexFEC）做差异化冗余——若仅为编解码层差异而非"由数据流特征推断业务类型"，仍不落 F1。
- 若关注的是基于 WebRTC 二次开发的厂商栈（各 RTC 厂商条目单独成行），其私有 FEC 改造可能补齐 F1/F3/F4，应在对应厂商候选中单独取证，不并入本开源库条目。

## 总结一句话
WebRTC/libwebrtc 的 FEC 是依带宽/丢包/RTT/帧率自适应的主动冗余，与专利同领域且 F5 命中，但缺失 F1 业务类型自动识别、F2 三输入约束与 F3/F4 时延→总时间→调度链（仅 1/5 字面命中），落第 4 档（公开资料不足-弱候选）。
