# 09-marvell-octeon-vdpa 检索留痕 (_sources.md)

## Phase 1 — react 粗筛 query
1. `Marvell OCTEON 10 DPU virtio-net hardware offload vDPA`
   → 命中 Linux 内核 vDPA 驱动 patch 系列（v1–v6）+ Marvell DPU 产品页。强信号：vDPA = "virtio 控制面 + 数据面卸载到硬件" 的混合架构，与本专利混合直通概念同向。
2. `octeon_ep_vdpa driver kernel virtqueue DMA address dataplane offload control plane vringh`
   → Red Hat vDPA 框架系列博客 + 驱动两层架构（Octep HW Layer / Octep Main Layer）。
3. `Marvell OCTEON DPU virtio offload patent SR-IOV VF guest memory DMA virtualization`
   → 确认 OCTEON 为 SR-IOV 设备、PF/VF 支持；未发现 Marvell 自有对应专利（仅检出他方 US9898430，主题为 SR-IOV dirty-page tracking，非本专利结构）。

## Phase 2 — react 深抓（WebFetch）
- v6 patch（2024-06-14）：核验 SR-IOV VF、是否存在 FE/BE 半虚拟化层绑定空闲 VF、DMA 通路。
- v2 patch：核验 commit cover letter + `octep_set_vq_address(desc_area, driver_area, device_area)` 地址编程方式。
- Red Hat vDPA part 3：核验 vDPA 数据面工作方式（guest 标准 virtio-net 驱动；vhost-vDPA 控制面 + 硬件直 DMA guest 内存；IOMMU GPA→PA 映射）。

## 已检查文档清单
- [PATCH v6] virtio: vdpa: vDPA driver for Marvell OCTEON DPU devices（2024-06-14）— https://www.mail-archive.com/virtualization@lists.linux.dev/msg00654.html
- [PATCH v2] 同上 — https://www.mail-archive.com/virtualization@lists.linux.dev/msg00533.html
- Marvell Data Processing Units (DPU) 产品页 — https://www.marvell.com/products/data-processing-units.html
- vDPA kernel framework part 3: usage for VMs and containers (Red Hat) — https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers
- vDPA kernel framework part 2 (Red Hat) — https://www.redhat.com/en/blog/vdpa-kernel-framework-part-2-vdpa-bus-drivers-kernel-subsystem-interactions

## 备注
- 时间窗：vDPA 驱动 2024-06 上游，远晚于 2014-01-21 授权，时间合规。
- 受限说明：内核 patch 仅公开"控制面 over vDPA bus"+ 队列地址编程函数；硬件 DMA 内部细节（是否经"空闲 VF 软件实例 + BE 导出 API"两段式）未在公开 patch 中描述，按"公开资料不足"处理 F7/F9，不脑补。
- WebFetch 全部成功，无需 curl 兜底。
