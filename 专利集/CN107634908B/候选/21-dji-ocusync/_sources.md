# 21-dji-ocusync 检索留痕

## Phase 1 WebSearch（4 次）

### q1: `DJI OcuSync 4 adaptive FEC packet loss redundancy`
返回主要链接：
- https://www.digidow.eu/publications/2021-christof-masterthesis/Christof_2021_MasterThesis_DJIProtocolReverseEngineering.pdf — DJI Wi-Fi 协议逆向工程（硕士论文，2021）
- https://everse.in/blogs/ocusync-in-dji-drones-how-do-they-work-perfectly
- https://store.dji.bg/en/blog/what-is-dji-ocusync-and-how-does-it-work
- https://medium.com/@dronesnuture/dji-ocusync-2-0-what-we-need-to-know-about-this-great-fpv-transmission-system-c34d87e4e81f
- https://forum.dji.com/thread-250137-1-1.html — DJI 官方论坛 OcuSync 2.0 讨论
- https://www.ietf.org/archive/id/draft-dmoskvitin-quic-adaptive-fec-00.html — 与 DJI 无关，是 QUIC 自适应 FEC 草案
- https://dl.acm.org/doi/pdf/10.1145/1374296.1374318 — 802.11 burst loss FEC，与 DJI 无关

判定：通用 FEC 文献 + OcuSync 概览，未见 DJI 应用层 FEC 资料。

### q2: `DJI OcuSync OFDM coding scheme adaptive physical layer`
返回主要链接：
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12567810/ — TranSIC-Net: DJI DroneID OFDM 解调（physical layer 研究）
- https://www.digidow.eu/publications/2021-christof-masterthesis/Christof_2021_MasterThesis_DJIProtocolReverseEngineering.pdf
- https://mavicpilots.com/threads/very-interesting-ocusync.109873/

判定：所有相关 hit 都聚焦 OFDM 物理层 / DroneID 信令，未见 packet-level FEC。

### q3: `DJI OcuSync 4 white paper transport layer packet level redundancy business type`
返回主要链接：
- https://stockrc.com/pdfdoc/DJI%20Security%20White%20Paper.pdf — DJI 官方安全白皮书
- https://dronedj.com/2025/06/24/dji-drone-security-paper-2025/ — 2025 DJI 安全白皮书报道
- https://www.worldmilitaryfans.com/archives/2702
- https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f217_paper.pdf — NDSS 2023 DroneID 论文
- https://www.researchgate.net/publication/392535837_IDENTIFYING_AND_ANALYZING_DJI_DRONE_SIGNALS

判定：DJI 公开材料未涉及 transport layer packet-level redundancy。

### q4: `"OcuSync" "FEC" packet redundancy control video stream`
返回主要链接：
- https://www.haivision.com/blog/broadcast-video/low-latency-video-packet-loss-arq-fec/
- https://pion.ly/blog/fec-with-pion/
- https://www.mdpi.com/2079-9292/14/3/563
- https://medium.com/@dronesnuture/dji-ocusync-2-0-what-we-need-to-know-about-this-great-fpv-transmission-system-c34d87e4e81f

判定：通用视频 FEC 文献占主体，OcuSync 相关 hit 仍未涉及 packet-level FEC。

## Phase 2 WebFetch（2 次 + 1 次 curl 兜底）

### F2.1 WebFetch — DigiDow 硕士论文（DJI Wi-Fi 协议逆向工程，2021）
URL: https://www.digidow.eu/publications/2021-christof-masterthesis/Christof_2021_MasterThesis_DJIProtocolReverseEngineering.pdf
结论：论文聚焦 DJI Wi-Fi 协议逆向、payload 加密、Wireshark 协议解析、MitM 攻击。**完全未涉及** FEC / 冗余策略 / 包恢复 / 业务类型区分 / 时延感知调度 / OFDM 物理层信道编码 / 传输层可靠性机制。

### F2.2 WebFetch — DJI OcuSync 综述博客
URL: https://store.dji.bg/en/blog/what-is-dji-ocusync-and-how-does-it-work
结论：仅描述 OcuSync 操作特征：
- 2.4 GHz / 5.8 GHz 双频段切换
- 在 20MHz / 10MHz / 1.4MHz 三种信道模式间自适应选择（基于本地干扰扫描）
- 测量延时：命令 5ms，视频数据 10ms，端到端视频 130ms
**无任何关于 FEC / 包冗余 / ARQ / 业务类型差分 / 时延感知调度 / OSI 层级机制**的描述。

### F2.3 curl 兜底 — DJI 官方安全白皮书
URL: https://stockrc.com/pdfdoc/DJI%20Security%20White%20Paper.pdf
HTTP 403 Forbidden（两次：WebFetch + curl 均 403）。无法获取。

## 工具限制
- Phase 2 curl 兜底失败一次（DJI Security White Paper 403）。其余源充分。
- DJI 闭源产品，官方未公开 OcuSync 物理层以上的协议栈细节；逆向工程论文（DigiDow 2021）也未提及 packet-level FEC。
