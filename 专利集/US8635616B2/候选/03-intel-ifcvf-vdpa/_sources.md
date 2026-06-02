# 证据索引 — 03-intel-ifcvf-vdpa

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2018-03-31（首版引入；文档持续到 25.11） | 官方文档/源码 patch | http://patchwork.dpdk.org/project/dpdk/patch/20180331022929.42172-4-xiao.w.wang@intel.com/ ；落盘 dpdk-ifcvf-patch.mbox | commit message + 驱动源码逐字对应 F1/F2/F3/F4-等价/F5/F7/F8/F9 |
| 2 | 各版本 19.02~25.11 | 官方文档 | https://doc.dpdk.org/guides/vdpadevs/ifc.html | "HW vhost backend"/"virtio ring compatible"/"VF DMA to VM's memory"/"notify relay thread" verbatim |

## Phase 1 — react 粗筛 query 留痕
1. `Intel IFCVF vDPA driver virtio ring HW vhost backend DMA`
   - 命中：DPDK 官方 IFCVF vDPA 驱动文档（多版本 19.02→25.11）+ 原始 patchwork patch。
   - 信号：极强。文档原文直述 "IFCVF's datapath is virtio ring compatible, it works as a HW vhost backend which can send/receive packets to/from virtio directly by DMA"，逐字对应 F3（HW vhost backend = BE）+ F8（VF 直接 DMA）。无需继续粗筛，直接进 Phase 2。

## Phase 2 — react 深抓
- WebFetch `doc.dpdk.org/guides/vdpadevs/ifc.html` → 成功（小模型摘出 verbatim），但本机 curl 落盘 doc.dpdk.org 失败（schannel TLS handshake，多次重试含 --tlsv1.2 均 exit 35）。改以 patchwork mbox 作为 L1 落盘证据（同源 commit message 逐字一致，且含完整驱动源码）。
- WebFetch `patchwork.dpdk.org/.../20180331022929.42172-4-xiao.w.wang@intel.com/` → 成功，取得提交日期 2018-03-31、作者 Xiao Wang / Rosen Xu（Intel）、commit message verbatim。
- curl `http://patchwork.dpdk.org/.../mbox/` → 成功落盘 `dpdk-ifcvf-patch.mbox`（41552 字节，含完整 commit message + 驱动源码 `ifcvf.c` / `ifcvf_vdpa.c`）。
- Grep mbox 核验源码级证据：
  - L55-64：commit message verbatim（HW vhost backend / virtio ring compatible / per-VF DMA address translation / DMA remapping table with VM memory region）。
  - L66-73：`ifcvf_dev_config` ops verbatim（IOMMU programming to enable VF DMA to VM's memory / VFIO interrupt route HW interrupt to virtio driver / notify relay thread translate virtio driver's kick to MMIO write / HW queues configuration）。
  - L404-415：`io_write64_twopart(hw->vring[i].desc/avail/used, &cfg->queue_desc/avail/used_lo...)` —— 把 vring 队列地址写入 VF 硬件 PCI 配置寄存器（=写入 VF 设备的存储单元/队列）。
  - L1024-1032 `vdpa_ifcvf_start()`：`rte_vhost_get_vhost_vring(vid,i,&vq)` 从 vhost lib（BE）取 desc/avail/used → `qva_to_gpa()` 转 GPA → 存 `hw->vring[i]`，随后 `ifcvf_start_hw` 写入硬件。这就是 F7（绑定 BE 的 VF 软件实例经 BE 导出 API 取 DMA 地址写入 VF 设备队列）。

## 已检查文档清单
- DPDK 官方 IFCVF vDPA 驱动文档（guides/vdpadevs/ifc.html，存在 19.02~25.11 各版本） — https://doc.dpdk.org/guides/vdpadevs/ifc.html
- 原始 patch "net/ifc: add ifcvf vdpa driver"（2018-03-31，Xiao Wang/Rosen Xu @ Intel，Reviewed-by Maxime Coquelin @ Red Hat） — http://patchwork.dpdk.org/project/dpdk/patch/20180331022929.42172-4-xiao.w.wang@intel.com/
- 落盘 mbox（含完整 commit message + 驱动源码） — dpdk-ifcvf-patch.mbox

## 受限说明
- doc.dpdk.org 在本机 curl 全程 schannel TLS handshake 失败（exit 35，含 --tlsv1.2 重试）。已用同源 patchwork mbox 落盘作为 L1 证据替代；WebFetch 该 doc 成功，verbatim 与 mbox 完全一致，结论不受影响。
