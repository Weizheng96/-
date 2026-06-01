# 证据索引 — 12-alibaba-cipu-moc

## Phase 1 WebSearch（粗筛留痕）
1. `阿里云 神龙 MoC 卡 CIPU 虚拟交换机 流表卸载 网络` → 命中（CIPU/MoC 承担 VPC 网络硬件卸载，单卡叙事）
2. `阿里云 CIPU 多网卡 链路聚合 LACP 流表 高可靠 卸载` → 命中均为通用 LACP 教程 + CIPU 七千字 PDF；CIPU「双上联」≠ 主机内多网卡聚合
3. `Alibaba CIPU vSwitch flow table offload multiple NIC dual uplink high availability` → 命中 SIGCOMM '24 Triton 论文、theregister、AVS 资料

## Phase 2 WebFetch（深抓证据）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2024-06-29 | 学术论文 | https://cs.stanford.edu/~keithw/sigcomm2024/sigcomm24-final113-acmpaginated.pdf （Triton: Apsara vSwitch 硬件卸载） | 最权威技术来源；无 LACP / 多网卡聚合 / 跨网卡流表同步 → F2/F3/F5 未命中 |
| 2 | 2023-08-31 | 厂商架构 PDF | https://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/file-manage-files/zh-CN/20230831/xxzd/七千字详解阿里云CIPU技术架构.pdf | 扫描图片型 PDF，WebFetch 无法抽取正文（受限，盲区） |
| 3 | 2022-06-15 | 技术媒体 | https://www.infoq.cn/article/kjno59x5hifczzfoahrw | 仅单芯片加速指标（200G/4000万PPS），无多网卡/流表冗余 |
| 4 | 2022-06-29 | 技术博客 | https://blog.csdn.net/Jmilk/article/details/125518158 | 网络卸载为单卡机制，无多网卡/LACP/流表同步 |
| 5 | — | 厂商文档 | https://www.alibabacloud.com/help/en/vpc/product-overview/service-architecture | VPC 高可靠=分布式 vSwitch + 跨 AZ failover + 链路冗余，机制不同 |

## 受限说明
- CIPU 七千字 PDF 为图片型，WebFetch 抽取失败，存在盲区。
- 云厂商网卡级实现细节公开度低，无权威实现文档披露主机内 N≥2 网卡 bond + 流表卸载拓扑。

## 落档
第 4 档（公开证据不足，<60%；非已排除——无确凿反证、来源非全部早于 2023-06-06）
