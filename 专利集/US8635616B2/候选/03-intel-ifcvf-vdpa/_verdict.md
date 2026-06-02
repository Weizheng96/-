# 03-intel-ifcvf-vdpa verdict

## 候选基本信息
- 名称：Intel IFCVF（FPGA 100G VF）vDPA 驱动（DPDK net/ifc PMD + in-kernel ifcvf 参考实现） / Intel IPU
- 组织：Intel
- 类型：产品
- 初判命中 F#：F1,F2,F5,F7,F8
- 专利公开（授权）日：2014-01-21（优先权日 2011-12-31）
- 候选首次公开日：2018-03-31（DPDK ifcvf vdpa 驱动首版 patch），晚于专利授权 → 时间窗合规，可作侵权证据。

> 架构对应关系（判定基准）：本专利的"BE（半虚拟化后端，经导出 API 对外提供 DMA 地址）"在 DPDK IFCVF 中由 **DPDK vhost library（`rte_vhost_*` API）** 充当；"VF 软件实例"由 **per-VF 的 ifcvf PMD/internal 驱动实例** 充当；"FE（前端）"为 **Guest VM 内的 virtio-net 前端驱动**。整体即"控制/兼容面走 virtio 半虚拟化前后端、数据面走硬件 VF 直接 DMA"的混合直通通路——与本专利混合架构同机制。术语不同（virtio/vhost vs FE/BE）属表述差异，非反向信号。

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（VF 从 I/O 设备虚拟化而来） | 命中（字面） | "the Intel FPGA 100G VF (IFCVF)"；"Different VF devices serve different virtio frontends which are in different VMs" | http://patchwork.dpdk.org/project/dpdk/patch/20180331022929.42172-4-xiao.w.wang@intel.com/ | IFCVF 即 Intel FPGA 100G 网卡的 SR-IOV VF，从物理 I/O 设备虚拟出多个 VF，每个 VF 服务一个 VM 的 virtio 前端。 |
| F2（VF 软件实例与 VF 设备一一对应） | 命中（等同） | "each VF needs to have its own DMA address translation service. During the driver probe a new container is created"；源码：每个 VF 由独立 `struct ifcvf_internal`/`ifcvf_hw` 实例管理（probe 时一对一创建） | 同上 / dpdk-ifcvf-patch.mbox L60-64, L1015-1033 | 每个 VF 设备探测时创建独立驱动实例与独立 VFIO container，VF 设备↔驱动实例一对一。"一一对应"未逐字，结构等同。 |
| F3（Host 有同类型 I/O 虚拟设备的 BE） | 命中（等同） | "it works as a HW vhost backend which can send/receive packets to/from virtio directly by DMA" | 同上 mbox L56-58 | "HW vhost backend" 逐字即半虚拟化后端 BE；设备类型为 virtio-net，与底层网卡 I/O 同类（网络设备）。BE 由 DPDK vhost lib + ifcvf 驱动共同充当。 |
| F4（VM 有该 I/O 虚拟设备的 FE） | 命中（字面） | "VF devices serve different virtio frontends which are in different VMs"；"VFIO interrupt setup to route HW interrupt to virtio driver" | 同上 mbox L60-61, L70-71 | Guest 内 virtio-net 前端即 FE，verbatim 出现 "virtio frontends ... in different VMs"。 |
| F5（BE 绑定一个空闲 VF 软件实例）★关键★ | 命中（等同） | "Enable VF data path with virtio information provided by vhost lib"；`vdpa_ifcvf_start()` 把 vhost lib 协商出的 vring/特性配置到具体 VF 硬件 | 同上 mbox L68-73, L1020-1035 | vDPA 框架把一个 vhost(BE)实例绑定到一个具体 VF 驱动实例，由该 VF 承载数据面。"绑定"机制命中；"idle/空闲" 未逐字（VF 须为未被占用方可分配，功能上等价），故记等同。 |
| F6（FE 预分配 DMA 缓存） | 命中（等同） | virtio 前端在 Guest 内分配 vring 描述符/缓冲区，经 vhost 协议把内存区域上报；"program DMA remapping table with the VM's memory region information" | 同上 mbox L62-64 | 缓存由 Guest virtio 前端分配（virtio 标准语义），Host 侧据 VM memory region 建 DMA 映射。前端预分配 DMA 缓存机制等同。 |
| F7（绑定 BE 的 VF 软件实例经 BE 导出 API 取地址写入 VF 设备存储单元） | 命中（等同，源码级） | `rte_vhost_get_vhost_vring(vid,i,&vq); hw->vring[i].desc=qva_to_gpa(...vq.desc); .avail=...; .used=...;` 随后 `io_write64_twopart(hw->vring[i].desc,&cfg->queue_desc_lo...)` / `.avail→queue_avail_lo` / `.used→queue_used_lo` 写入 VF 硬件 PCI 配置 | dpdk-ifcvf-patch.mbox L1024-1032, L404-415 | vhost lib 的 `rte_vhost_get_vhost_vring` = BE 的导出 API；VF 驱动经该 API 取得 DMA 缓存（vring）地址，写入 VF 设备的队列寄存器（first storage unit=接收队列）。逐条对应 F7，仅术语不同。 |
| F8（VF 收到数据时取地址发起 DMA 写） | 命中（字面） | "it works as a HW vhost backend which can send/receive packets to/from virtio directly by DMA"；"IOMMU programming to enable VF DMA to VM's memory" | 同上 mbox L56-58, L69-70 | VF 硬件以写入的 vring 地址为目标，直接 DMA 收发包到 VM 内存（数据面直通）。F8 字面命中。 |
| F9（VF 通知 VF 软件实例 → 触发 FE 收数据） | 命中（等同） | "VFIO interrupt setup to route HW interrupt to virtio driver"；"create notify relay thread to translate virtio driver's kick to a MMIO write onto HW" | 同上 mbox L70-73 | VF 完成 DMA 后经硬件中断（VFIO 路由到 virtio 前端）通知，前端据此收数据；notify relay 处理反向 kick。通知→触发前端收数据机制等同。 |

命中统计：F1/F4/F8 字面；F2/F3/F5/F6/F7/F9 等同（机制一致、术语不同）。9/9 全命中，含 ≥1 等同。

## 已检查文档清单
- 原始 patch "net/ifc: add ifcvf vdpa driver"（2018-03-31，Xiao Wang/Rosen Xu @ Intel，Reviewed-by Maxime Coquelin @ Red Hat），含完整 commit message 与驱动源码（ifcvf.c / ifcvf_vdpa.c），逐字对应 F1–F9 — http://patchwork.dpdk.org/project/dpdk/patch/20180331022929.42172-4-xiao.w.wang@intel.com/ （落盘 dpdk-ifcvf-patch.mbox，41552 字节）
- DPDK 官方 IFCVF vDPA 驱动文档（guides/vdpadevs/ifc.html，存在 19.02~25.11 各版本，内容与 patch commit message 一致） — https://doc.dpdk.org/guides/vdpadevs/ifc.html

## 最终判定
**第 2 档：全命中含 ≥1 等同**

判定依据：IFCVF vDPA 驱动是与本专利完全同构的"混合直通 I/O 虚拟化"实现——virtio 半虚拟化前后端（FE=Guest virtio 前端，BE=DPDK vhost lib + ifcvf 驱动作为 "HW vhost backend"）+ 硬件 VF 直接 DMA 数据面。F1/F4/F8 由 commit message verbatim 字面命中（IFCVF=I/O 设备的 VF；virtio frontends in VMs；VF DMA 直接收发到 VM 内存）。F7 由驱动源码逐条命中：`rte_vhost_get_vhost_vring`（BE 导出 API）取 vring 地址 → `qva_to_gpa` → `io_write64_twopart(...queue_desc/avail/used_lo)` 写入 VF 设备队列寄存器，精确对应"VF 软件实例经 BE 导出 API 取 DMA 地址写入 VF 设备 first storage unit"。F2/F3/F5/F6/F9 机制等同（术语为 virtio/vhost/VFIO，与专利 FE/BE/VF 一一映射，无任何反向证据）。唯一非字面点是 F5 的 "idle/空闲" 修饰词与 F2 的 "一一对应" 措辞未逐字出现，但 vDPA probe 阶段一个 VF 绑定一个 vhost 实例、占用即不可再分配，功能上等价 → 记等同。无任何"explicitly excludes / 不支持"类反向语，未达第 1 档（全字面）但全 9 项命中 → 第 2 档。

## 升级路径（仅 3-4 档）
（本候选落第 2 档，无需升级路径。）

## 总结一句话
Intel IFCVF vDPA 驱动以 "HW vhost backend + VF 直接 DMA" 实现与本专利同构的混合直通 I/O 虚拟化，commit message 与驱动源码逐条对应 F1–F9（F1/F4/F8 字面，余等同），无反向证据，落第 2 档。
