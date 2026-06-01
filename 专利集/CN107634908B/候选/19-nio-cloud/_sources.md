# 证据索引 — 19-nio-cloud

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2026-05 | WebSearch | q="蔚来 NIO Cloud 车云 通信 协议 抗丢包 冗余" | 仅命中 TOX 协议栈（车内跨域总线，非车云上行），无 F# 可锚定 |
| 2 | 2026-05 | WebSearch | q="NIO OTA 升级 协议栈 冗余 FEC 业务类型" | 仅返回通用 OTA 双区冗余 / 断点续传知识，未涉 NIO 私有传输层 |
| 3 | 2026-05 | WebSearch | q='"NIO" OR "蔚来" car-to-cloud telemetry protocol redundancy packet loss adaptive' | 命中学术论文（MDPI / arXiv）但与 NIO 无关；无 NIO 私有实现公开材料 |
| 4 | 2026-05 | WebSearch | q="蔚来 NIO 车端 网关 telematics TBOX 数据上传 FEC 自适应冗余" | 仅命中通用 T-BOX 工作原理科普 + NIO CCC 中央计算平台官宣文，无 FEC / 自适应冗余技术描述 |
| 5 | 2026-05 | WebFetch | https://www.nio.cn/innovation | 确认 TOX 为"整车跨域融合"总线（车内），与"车-云上行"无关；未披露任何 FEC / 业务类型识别 / 冗余调度细节 |
| 6 | 2026-05 | WebFetch | https://www.nio.com/blog/nio-os-290-all-inclusive-and-effortless-upgrade | NIO OS 2.9.0 blog 仅面向用户功能介绍，无 OTA 传输层细节，无法判定是否实施 F1-F5 |
