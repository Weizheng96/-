# 41-google-stadia verdict

## 候选基本信息

- 候选名称：Google Stadia（云游戏平台）
- 组织：Google
- 类型：产品
- 专利公开日：**2021-06-08**
- 产品时间窗：Stadia 于 2019-11 上线、**2023-01-18 正式下线**；2021-06-08 ~ 2023-01-18 约 19 个月在专利时间窗内**仍在运营**，故时间合规。
- 公开度（实测）：中。Google 自身未发布 Stadia 流媒体协议技术白皮书；公开材料以**第三方学术抓包逆向分析论文**为主（Carrascosa & Bellalta 2020；Di Domenico et al. 2021；Manzano et al. 2014/2021 cloud-gaming 系列）。Google 仅在 Stadia 一般性技术博客中提及"实时自适应流"与"基于 WebRTC"，未披露 FEC / 冗余调度细节。
- 命中 F#（初判）：F2, F3, F4, F5
- 命中 F#（实测）：见下表，**初判与实测显著不一致**。

## F# 命中表（权 1，F1-F5）

| F#  | 限定（摘要） | Stadia 实际行为（来自 Carrascosa & Bellalta 2020 / Di Domenico et al. 2021） | 命中 |
|-----|--------------|------------------------------------------------------------------------------|------|
| F1  | 由发送端**自动**根据数据流特征变量（缓存长度数目 / 在网长度数目 / 到达间隔 / 突发性 至少 1 项）识别**业务类型** | Carrascosa & Bellalta：观察到"different games have different traffic characteristics such as the packet size, inter-packet times, and load"，但**未发现 Stadia 自身用这些统计去识别业务类型并据此差异化处理**。Stadia 自适应链路是 Google Congestion Control（GCC）双控制器（delay-based + loss-based），输入是**帧延迟与丢包率**，**不输入业务类型/数据流特征变量**。 | **否** |
| F2  | 根据**网络状态 + 传输成功率 + 业务类型**三元组联合得到冗余包数量 | GCC 输出的是**目标 bitrate**（取 delay-based 与 loss-based 的最小值），调节的是编码器码率与分辨率（"frame-by-frame bitrate adaptation"），而**不是"冗余包数量"**。Carrascosa & Bellalta 全文未涉及 FEC。Di Domenico et al.（cloud gaming 网络分析，含 Stadia/GeForce Now/PSNow）明确指出 Stadia 的冗余通道是**视频重传（RTX）**："a third flow used for video retransmission … is almost inactive [normally] but becomes suddenly active, carrying large packets containing video content [on loss]"——这是 **reactive RTX**，不是 proactive 冗余包数量计算。 | **否** |
| F3  | 由**时延要求**得到冗余包**传输总时间** | 公开材料未发现 Stadia 有"冗余包传输总时间"这一概念。GCC 的延时反馈用于调 bitrate，不是用于划定冗余调度窗口。 | **否** |
| F4  | 根据**网络状态 + 总时间 + 冗余包数量**联合选**调度方法**（权 2 / 权 9：随机度 / 最短 / 最长 / 均匀 至少一种） | Di Domenico et al. 直接结论："Stadia maintains constant bitrate per resolution tier, suggesting **static rather than dynamic redundancy scheduling**"。Stadia 没有动态选调度方法这一行为。 | **否** |
| F5  | 按调度方法**发送冗余包**（主动 FEC / packet-level 冗余，非 ARQ / 重传） | Stadia 的丢包恢复机制实测为**视频 RTX 重传流**，属于 reactive 重传（"co-occurs with packet losses"），按专利 F5 的"主动冗余 vs 重传 / ARQ"区分条款，**纯 RTX 重传不构成 F5 命中**。同期对 PSNow 的分析中作者**猜测**其可能有 FEC（"channel 12 … used for video retransmission or some form of forwarding error correction (FEC)"），对 Stadia **未做此猜测**——只描述为 retransmission。 | **否** |

**F# 命中数：0 / 5。**

## 已检查文档清单

| 序号 | 来源 | 类型 | 关键结论 |
|------|------|------|----------|
| D1 | Carrascosa, Bellalta. *Cloud-gaming: Analysis of Google Stadia traffic*. arXiv:2009.09786 / Computer Networks 2022. | 学术论文（抓包逆向） | Stadia 用 WebRTC，UDP 上承载 RTP（音视频）/ RTCP（反馈）/ DTLS（应用数据）/ STUN（保活）。自适应通过 GCC 双控制器，**未提 FEC**。 |
| D2 | Di Domenico et al. *A Network Analysis on Cloud Gaming: Stadia, GeForce Now and PSNow*. arXiv:2012.06774 / MDPI Network 2021. | 学术论文（多平台对比） | Stadia 第三 UDP 流为**视频 RTX 重传**（reactive，丢包时才激活），**不是主动 FEC**；resolution tier 内 bitrate 恒定，"static rather than dynamic redundancy scheduling"。 |
| D3 | IEEE Spectrum: *How YouTube Paved the Way for Google's Stadia Cloud Gaming Service*. | 行业报导 | 描述 GCC、BBR、frame-by-frame bitrate adaptation；未提 FEC 或业务类型驱动。 |
| D4 | Manzano et al. / IEEE *A First Look at the Network Turbulence for Google Stadia Cloud-based Game Streaming*. | 学术论文 | 与 D1 互证 Stadia 的 GCC + RTX 模型。 |

WebFetch 受限说明：MDPI（403）、inria HAL（bot 挑战页）、arxiv PDF 二进制直取失败。已通过 ar5iv HTML 镜像（D1/D2）拿到核心结论，curl 兜底于 MDPI 与 HAL 仍被 edge / Anubis 拦截——明示工具受限，未伪造引文。

## 最终判定

**第 5 档：已排除**（**0 命中 ≠ 已排除** —— 本结论不是因为"0 命中"而下，而是因为**有真反向证据**：D2 论文实证 Stadia 的冗余通道是 RTX 重传而非主动 FEC，且 GCC 自适应输入不含业务类型 / 数据流特征变量，bitrate 在每个分辨率档内恒定无动态冗余调度，这与权 1 的 F1 / F2 / F4 / F5 的核心限定**正面冲突**。）

理由小结：
- **F1 反向**：Stadia 的自适应输入是帧延迟 + 丢包率，**不**用缓存长度数目 / 在网包统计 / 到达间隔 / 突发性来识别"业务类型"，且 Stadia 流媒体协议本身**不做业务类型区分**（同一 GCC 处理所有游戏）。
- **F5 反向**：Stadia 是 reactive RTX 重传机制，不是 proactive packet-level 冗余 / FEC——按权 1 解释（"'主动冗余' vs '重传 / ARQ' 区别"），纯 RTX **不构成 F5 命中**。
- **F4 反向**：Stadia bitrate per resolution tier 恒定 + 无 FEC 概念，自然无"动态选调度方法"。
- 5 个独立特征中 0 个命中、且至少 3 个有正面反向证据 → 落第 5 档。

## 升级路径（3-4 档时；本档为第 5 档，仅作合规留痕）

不适用。若日后 Google 复活 Stadia 后继产品（Immersive Stream for Games 等）且公布或被逆向出业务类型自适应 / packet-level FEC / 冗余调度方法，需重新评估，但目前 Immersive Stream 已不在本候选范围。

## 总结一句话

实测 Stadia 用 WebRTC + GCC 做整体码率自适应、用 RTX 流做反应式视频重传，**既不主动发 FEC 冗余包也不按业务类型差异化处理**，与 CN107634908B 权 1 的 F1 / F2 / F4 / F5 核心限定正面冲突，落第 5 档（已排除）。

---

**免责声明**：本报告仅基于公开抓包逆向分析与行业报导给出技术档位判定，不构成对 Google / Alphabet 的"已构成侵权"法律结论。最终是否构成侵权需由专利权人结合产品源码、专利全部权利要求与司法解释、等同原则等综合判定。
