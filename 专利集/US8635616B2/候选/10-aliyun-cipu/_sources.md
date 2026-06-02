# 证据索引 — 10-aliyun-cipu

## Phase 1 — react 粗筛 query（串行）
1. `阿里云 CIPU 神龙 X-Dragon virtio DPU 虚拟化 IO 卸载` — 强信号：神龙/CIPU 把网络/存储虚拟化从 CPU 卸载到自研 MOC 卡/X-Dragon 芯片；基于 virtio-net/virtio-blk/NVMe 标准 IO 设备模型；通过 VT-d 做 IO 硬件设备虚拟化。命中方向 F1/F3/F4。
2. `神龙架构 virtio 前端 后端 VF 直通 DMA passthrough 数据面 控制面` — 命中 vDPA 概念（控制面软件 + 数据面 DMA/VF 直通），与本专利"混合直通"同域。
3. `阿里云 神龙 CIPU virtio 硬件卸载 vDPA datapath offload guest 前端驱动 数据面直通` — 确认 VirtIO Offload：控制面驱动传递、数据面虚拟机↔网卡直通。
4. `Alibaba virtualization IO offload patent virtio front-end back-end VF DMA passthrough computing node` — 命中 alibabacloud.com 官方博客：VirtIO-blk frontend driver 在 ECS 实例内 + Kunpeng backend driver 在 MoC NIC。

## Phase 2 — react 深抓 / 落盘
- 千字详解阿里云 CIPU 技术架构（官方 PDF，2022 发布）— https://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/file-manage-files/zh-CN/20230831/xxzd/CIPU技术架构.pdf
  → 本地落盘 `cipu-tech-arch.pdf`（已 pdfplumber 抽取正文，见 _verdict.md 证据）
- 神龙(X-Dragon)：一种新型的软硬融合虚拟化技术 / 张献涛 OS2ATC2018 PPT — https://soft.cs.tsinghua.edu.cn/os2atc2018/ppt/v2.pdf
  → 本地落盘 `os2atc2018-xdragon-zhangxiantao.pdf`（幻灯片为图片+内嵌字体，pdfplumber 仅前 7 页可读，正文多为乱码；页 7 架构图文字可辨：典型虚拟化软件架构 = virtio FE/BE + 虚拟化硬件平台 VT-x/VT-d/SR-IOV）
- 阿里云第六代 ECS 介绍（alibabacloud.com 官方博客，2020-01-08）— https://www.alibabacloud.com/blog/introducing-the-sixth-generation-of-alibaba-clouds-elastic-compute-service_595716
- 阿里云弹性裸金属服务器-神龙架构（X-Dragon）揭秘（developer.aliyun.com，2018-05-19）— https://developer.aliyun.com/article/594276 （部分 SPA，正文可读片段有限）
- 看阿里云 CIPU 的 10 大能力（CSDN，引官方口径，2022）— https://blog.csdn.net/Jmilk/article/details/125518158
- Virtio without the "virt"（LWN.net, 2019-11-26）— https://lwn.net/Articles/805662/ （评论确认 Alibaba Cloud 提供 full Virtio offload NIC；正文未抓到）

## 受限说明
- 神龙/CIPU 数据通路微观实现（VF 软件实例绑定、DMA 缓存预分配交互、收/发队列写入、DMA 写完成通知 FE 的精确时序）属闭源，公开资料仅披露到"virtio FE 在 Guest + 后端在 MoC NIC 硬件 + VT-d/IOMMU/SR-IOV 硬件 IO 虚拟化 + DMA 直通"架构层，未到权 1 字面动作粒度。按"公开资料不足"判，不脑补。
- 未检索到阿里巴巴 2014 后与本专利接收通路逐步对应的自有公开专利可供逐句比对。
