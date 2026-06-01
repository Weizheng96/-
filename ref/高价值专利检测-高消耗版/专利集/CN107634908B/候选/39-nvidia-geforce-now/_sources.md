# 证据索引 — 39-nvidia-geforce-now

## Phase 1 粗筛 queries
- q1: `NVIDIA GeForce NOW adaptive FEC packet loss streaming` — 6 命中（均为社区 forum / 网游用户 troubleshooting / NVIDIA 帮助页讨论 L4S；**未出现 NVIDIA 官方 FEC 描述**）
- q2: `GeForce NOW streaming protocol network resilience redundancy` — 8 命中（核心命中：arXiv 2012.06774 网络分析论文；NVIDIA L4S 帮助页）
- q3: `site:research.nvidia.com cloud gaming FEC forward error correction` — 0 NVIDIA Research 命中（无相关论文）

## Phase 2 深抓
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2020-12 | 学术论文（arXiv） | https://arxiv.org/pdf/2012.06774 ; https://ar5iv.labs.arxiv.org/html/2012.06774 | Di Domenico et al. "A Network Analysis on Cloud Gaming"。§4.1 GeForce NOW 协议剖析：TLS+TCP 建会话 + 客户端开多个 UDP 通道（不走 ICE/STUN/TURN）；§4.3 端口分流多媒体（视频 49005、音频 49003），命令独立 UDP；**"we do not observe the presence of the RTCP protocol"**；**未观察到 FEC / ARQ retransmission**；§4.4 网络韧性靠码率自适应（≤5% 丢包不降分辨率）。 |
| 2 | 2024+ | 官方帮助页（NVIDIA support）| https://nvidia.custhelp.com/app/answers/detail/a_id/5522/ （curl 403 / WebFetch 403，但 WebSearch 摘要可读） | L4S 设置说明：ECN-Capable Transport（ECT）标记 → 网络路径上 L4S 设备 remark CE → 客户端反馈 → 服务端**调整码率（adjust streaming rate / encoding bitrate）**。机制是**congestion control / rate adaptation**，不是 FEC redundancy。 |
| 3 | 2024 | NVIDIA-published L4S 合规文档 | https://l4steam.github.io/PragueReqs/GeforceNow_L4S_requirements_Compliance_and_Objections.pdf | IETF L4S 框架的合规清单（NVIDIA 提交）。整篇围绕 ECN-based congestion control 展开；**未提 FEC、未提 redundant packets、未提 ARQ**。 |
| 4 | 2025 | 第三方营销博客（低权重） | https://www.tesmart.com/blogs/news/what-is-forward-error-correction-how-does-it-improve-gaming-experience | 一句话宣称 "Both NVIDIA's GeForce NOW and AMD's cloud gaming platforms use FEC"。**无引用、无 NVIDIA 一手来源链接、无技术细节**；与 arXiv 实测论文（无 FEC 观察）冲突。**权重不足，仅备查。** |
| 5 | 本地（curl 抓取） | 本地 HTML | 候选/39-nvidia-geforce-now/nvidia-l4s.html, nvidia-reduce-lag.html | NVIDIA custhelp 域名启用 Akamai IP 信誉拦截 → curl 返回 Oracle/Akamai "Access Denied" 兜底页（1127 字节）。无法直读原文。WebSearch 摘要为唯一可用证据。 |

## 工具受限记录
- WebFetch nvidia.custhelp.com 全部 403
- curl 同域返回 Akamai "Access Denied"
- 官方 L4S 合规 PDF 已抓取（135KB）但 WebFetch 摘要器**未读取到 GeForce NOW 实现细节**——文档主要引用 IETF §4.3 通用 L4S 信令机制
- arXiv 论文 PDF 已抓取（494KB），主 PDF 摘要器报"未提取到具体 GFN 协议细节"，但 ar5iv HTML 镜像摘要给出了 §4.1/4.3/4.4 的具体内容
