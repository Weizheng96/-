# 07-dayu-paratus-vdpa sources（检索留痕）

## Phase 1 — react 粗筛 query 留痕
1. `大禹智芯 DaYu Paratus DPU virtio vDPA OVS 存储 卸载`
   - 命中：dayudpu.com 官网；腾讯云 Paratus 2.0 发布稿(2022-10-14)；极术社区《DPU和CPU互联的接口之争：Virtio还是SR-IOV？》；CSDN/知乎 vDPA 文章。
   - 信号：Paratus 2.0 支持 VirtIO、OVS 全卸载、存储客户端(Storage Initiator)全卸载、NVMe 模拟 → 与本专利 I/O 虚拟化领域相关，进入深抓。
2. `大禹智芯 Paratus 2.0 virtio 数据面 SR-IOV VF 直通 前端 后端 架构`
   - 命中：腾讯云发布稿、官网 product/paratus2、博客园 DPU 市场分析。
   - 信号：确认硬件架构 = ARM SoC + FPGA，基于 FPGA 的网络数据处理通路；但未披露 Host 内 FE/BE + VF 软件实例绑定细节。
3. `大禹智芯 vDPA virtio 控制面 数据面 VF passthrough 专利 OR patent`
   - 命中：均为他方专利(华为/Red Hat 等 virtio/passthrough 专利)与 arXiv 论文；**未检索到大禹智芯自有相关专利**。
   - 信号：无大禹智芯自有 FE/BE/VF 绑定架构专利可比对。

## Phase 2 — react 深抓 WebFetch 留痕
- https://www.dayudpu.com/product/paratus2 — 官方产品页。仅确认 ARM SoC + FPGA、基于 FPGA 的网络数据处理通路、HPRT™、端到端加密；**未披露** virtio/vDPA/SR-IOV VF 直通、FE/BE 实例、绑定空闲 VF 软件实例、DMA 数据通路等细节。
- https://cloud.tencent.com/developer/news/937365 — 腾讯云 Paratus 2.0 发布稿（发布日期 2022-10-14）。verbatim：「支持VirtIO来增强虚拟化环境下的适配性」「可以实现包括OVS全卸载、存储客户端（Storage Initiator）的全卸载及NVMe模拟等多种功能」；未详述实现机制，未提 Host 内 FE/BE+VF 软件实例绑定/DMA 通路。
- https://community.aijishu.com/a/1060000000228117 — 极术社区《DPU和CPU互联的接口之争：Virtio还是SR-IOV？》。verbatim：「硬件加速的VirtIO架构意味着后端（至少是数据路径）在硬件中实现，从而释放Hypervisor资源」「硬件vDPA将虚拟队列映射到硬件队列」。→ 证实 DPU/硬件 vDPA 模型中 virtio 后端数据面在 DPU 硬件内实现，而非 Host 内软件 BE 绑定空闲 VF 软件实例。

## 受限说明
- 官网 product/paratus2 页 WebFetch 可达但技术细节披露有限（宣传向），未触发 curl 兜底需求。
- 未检索到大禹智芯自有 FE/BE/VF 软件实例绑定混合直通架构的公开专利或白皮书；架构细节属"公开资料不足"。
