# 证据索引 — 01-opensource-vdpa-stack

## 候选
开源 vDPA 栈（Linux kernel `drivers/vdpa` + `vhost-vdpa` + QEMU virtio-net/vhost-vdpa + DPDK `rte_vdpa`），Red Hat 主导，2020 合入内核主线。

## Phase 1 — react 粗筛 query
- query 1: `Red Hat vDPA vhost-vdpa architecture virtio control plane datapath passthrough`
  → 命中且高度相关。Red Hat 官方系列博客，核心句："A 'vDPA device' means a type of device whose datapath complies with the virtio specification, but whose control path is vendor specific."；"The vDPA device can DMA to or from guest memory directly."
- query 2: `vhost-vdpa kernel framework DMA guest memory IOTLB virtqueue address QEMU virtio-net device`
  → 命中且高度相关。vhost-vDPA IOTLB / GPA→VA→PA 地址映射、virtqueue kick/call eventfd 通知机制。

粗筛结论：信号强，未触发任何早剪枝条件，进入 Phase 2 深抓。

## Phase 2 — WebFetch（react 串行）
| # | 时间 | 类型 | URL | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2020-08-12 | Red Hat 官方博客 | https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework | "datapath complies with the virtio specification, but whose control path is vendor specific"；"virtio device on the host and virtio driver on the guest"；中继 interrupt 到 virtio driver；VF/PF 实现 |
| 2 | 2019-10-02 | Red Hat 官方博客 | https://www.redhat.com/en/blog/achieving-network-wirespeed-open-standard-manner-introducing-vdpa | "standardize the NIC SRIOV data plane using the virtio ring layout"；"generic vDPA driver ... translate the vendor NIC driver/control-plane to the virtio control plane"；"data plane goes directly from the NIC to the guest" |
| 3 | 2020-08-27 | Red Hat 官方博客 | https://www.redhat.com/en/blog/vdpa-kernel-framework-part-2-vdpa-bus-drivers-kernel-subsystem-interactions | vhost-vDPA bus driver probe vDPA device → 创建 char dev；"mediation between the vhost uAPIs and vDPA bus operations"；IOVA↔VA 映射；eventfd 中继 kick/interrupt |
| 4 | 2020-09-03 | Red Hat 官方博客 | https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers | "vhost-vdpa device could be used as a network backend for VMs with the help of QEMU"；QEMU 中介 emulated virtio device↔vhost-vDPA；"vDPA VF uses GPA as IOVA, ... IOMMU will ... translate GPA->PA for the DMA to the buffer pointed in the virtqueue"；"vhost-vDPA backend will listen to the mappings of GPA->VA ... and update them to the vhost-vDPA device"；irqfd→KVM→inject interrupt to guest |

## 时间窗
本专利授权日 2014-01-21。vDPA 框架 2020-03 合入 Linux 内核主线，相关博客 2019-2020 发布——全部晚于专利公开日，属专利公开后材料，可作侵权证据（非现有技术）。

## 工具能力说明
全部来源为 Red Hat 官方公开博客 + 内核/QEMU 公开文档，无付费/登录墙。未遇 WebFetch 失败，无需 curl 兜底。
