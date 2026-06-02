# 01-opensource-vdpa-stack verdict

## 候选基本信息
- 名称：开源 vDPA 栈（Linux kernel `drivers/vdpa` + `vhost-vdpa` + QEMU virtio-net/vhost-vdpa + DPDK `rte_vdpa`）
- 组织：Linux/QEMU/DPDK 社区（Red Hat 主导）
- 类型：技术
- 初判命中 F#：F1,F2,F3,F4,F5,F6,F7,F8,F9
- 专利公开（授权）日：2014-01-21

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（VF 从 I/O 设备虚拟化而来） | 字面命中 | "standardize the NIC SRIOV data plane using the virtio ring layout"；vDPA "could be implemented through ... a physical function (PF), a virtual function (VF) or other vendor specific slices" | https://www.redhat.com/en/blog/achieving-network-wirespeed-open-standard-manner-introducing-vdpa ; https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework | vDPA 栈以 SR-IOV NIC 为典型底层设备，每个 vDPA 设备即一个硬件 VF（亦支持 PF/slice，但 VF 形态是主流部署，与 F1 同） |
| F2（VF 软件实例与 VF 设备一一对应） | 等同命中 | "Each NIC vendor can now continue using its own driver (with a small vDPA add-on) and a generic vDPA driver is added to the kernel" | https://www.redhat.com/en/blog/achieving-network-wirespeed-open-standard-manner-introducing-vdpa | 每个硬件 VF 由一个 vendor vDPA 驱动实例 + 一个 generic vDPA device 对象表示，主机侧软件实例与硬件 VF 一一对应（同手段/同功能/同效果） |
| F3（Host 有同类型 I/O 虚拟设备后端 BE） | 字面命中 | "Usually we have the virtio device on the host and virtio driver on the guest"；"vhost-vdpa device could be used as a network backend for VMs with the help of QEMU" | https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework ; https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers | vhost-vDPA backend 即 Host 侧半虚拟化后端，设备类型为 virtio-net，与底层 NIC 同类（网络 I/O 设备） |
| F4（VM 有该 I/O 虚拟设备前端 FE） | 字面命中 | "how the vDPA device is used by the guest kernel virtio-net driver ... QEMU to present a virtio device to the guest"；"a single standard virtio driver in the guest" | https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers ; https://www.redhat.com/en/blog/achieving-network-wirespeed-open-standard-manner-introducing-vdpa | Guest 内标准 virtio-net 驱动即前端 FE，与后端同为 virtio-net 类型 |
| F5（BE 绑定一个空闲 VF 软件实例）★关键★ | 等同命中 | "When a vDPA device is probed by the vhost-vDPA bus driver, a char device (/dev/vhost-vdpa-X) will be created for userspace drivers"；"The key responsibility of the vhost-vDPA bus driver is to perform mediation between the vhost uAPIs and vDPA bus operations." | https://www.redhat.com/en/blog/vdpa-kernel-framework-part-2-vdpa-bus-drivers-kernel-subsystem-interactions | vhost-vDPA bus driver 把一个 vDPA 设备（= 一个 VF 软件实例）绑定到 vhost 后端通路。该 VF 被 vDPA 独占、不参与 Host 自身网络栈（处于"空闲/专用"态），公开资料未逐字用 "idle" 一词→等同命中（同手段：后端绑定一个专用 VF 软件实例；同功能/同效果） |
| F6（FE 预分配 DMA 缓存） | 等同命中 | "the data plane goes directly from the NIC to the guest using the virtio ring layout"；"the buffer pointed in the virtqueue" | https://www.redhat.com/en/blog/achieving-network-wirespeed-open-standard-manner-introducing-vdpa ; https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers | Guest virtio-net 驱动按 virtio 规范在 virtqueue 中预挂接收缓存（DMA 目标 buffer），属标准 virtio FE 行为；公开博客未逐字描述"预分配"步骤但 virtqueue buffer 即此机制→等同命中 |
| F7（绑定 BE 的 VF 软件实例经 BE 导出 API 取地址并写入 VF 设备 first storage unit） | 等同命中 | "The vhost-vDPA backend will listen to the mappings of GPA->VA maintained by QEMU memory core, and update them to the vhost-vDPA device."；"The userspace vhost drivers should inform the memory mapping between IOVA ... and VA" | https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers ; https://www.redhat.com/en/blog/vdpa-kernel-framework-part-2-vdpa-bus-drivers-kernel-subsystem-interactions | 后端（vhost-vDPA + IOTLB/vhost uAPI）即 BE 的"导出 API"；地址映射经此接口取得并下发（update）到 vDPA 设备的 virtqueue 配置（first storage unit = 接收队列）。中间变量省略/路径同效→等同命中 |
| F8（VF 设备收到数据取地址发起 DMA 写） | 字面命中 | "The vDPA device (vDPA VF) uses GPA as IOVA, and the platform IOMMU will validate and translate GPA->PA for the DMA to the buffer pointed in the virtqueue."；"The vDPA device can DMA to or from guest memory directly." | https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers | VF 硬件以 virtqueue 中的 guest 缓存地址为目标直接 DMA 写入 guest 内存（数据面直通），与独权 1 及从属权 GPA+IOMMU 路径一致 |
| F9（VF 设备通知 VF 软件实例 → 触发 FE 收数据） | 字面命中 | "vDPA framework will also relay the interrupts from vDPA hardware to the userspace vhost drivers and kernel virtio drivers."；"vhost-vDPA driver simply writes to irqfd which is polled by KVM. KVM will ... inject virtual interrupt to the guest." | https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework ; https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers | DMA 完成后 VF 中断经 vDPA 框架/irqfd→KVM 注入 guest，触发 guest virtio-net 前端收数据 |

## 已检查文档清单
- Red Hat《Introduction to vDPA kernel framework》(2020-08-12) — vDPA 定义（datapath 合 virtio 规范、control path vendor 私有）、host virtio device + guest virtio driver、中断中继到 virtio driver、VF/PF 实现 — https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework
- Red Hat《Achieving network wirespeed ... introducing vDPA》(2019-10-02) — SR-IOV 数据面用 virtio ring 标准化、generic vDPA 驱动桥接 vendor 控制面到 virtio 控制面、数据面 NIC→guest 直通、guest 单一标准 virtio 驱动 — https://www.redhat.com/en/blog/achieving-network-wirespeed-open-standard-manner-introducing-vdpa
- Red Hat《vDPA kernel framework part 2》(2020-08-27) — vhost-vDPA bus driver probe→char dev、vhost uAPI↔vDPA bus 中介、IOVA↔VA 映射、eventfd 中继 kick/interrupt — https://www.redhat.com/en/blog/vdpa-kernel-framework-part-2-vdpa-bus-drivers-kernel-subsystem-interactions
- Red Hat《vDPA kernel framework part 3》(2020-09-03) — QEMU+vhost-vdpa 作 VM 网络后端、QEMU 中介 emulated virtio↔vhost-vDPA、vDPA VF 用 GPA 作 IOVA + IOMMU 翻译 DMA 到 virtqueue buffer、后端监听 GPA→VA 映射并下发设备、irqfd→KVM→注入 guest 中断 — https://www.redhat.com/en/blog/vdpa-kernel-framework-part-3-usage-vms-and-containers

## 最终判定

**第 2 档：确认侵权（中）**

五档定义：
  - 第 1 档：确认侵权（高）— F1-Fk 全部字面命中
  - 第 2 档：确认侵权（中）— F1-Fk 全部命中，含 ≥1 等同命中
  - 第 3 档：公开资料不足（强候选）— ≥60% F# 命中，剩余公开资料不足且无反向证据
  - 第 4 档：公开资料不足（弱候选）— <60% F# 命中
  - 第 5 档：已排除 — 仅当：(a) ≥1 条 F# 有真反向证据，或 (b) 全部证据 < 专利公开日（现有技术），或 (c) 架构层级不同

判定依据（1-3 句话，基于上表 F# 命中分布）：
F1–F9 全部命中（F1/F3/F4/F8/F9 字面命中，F2/F5/F6/F7 等同命中），整套 vDPA 栈完整再现了本专利"FE/BE 半虚拟化设备模型（控制面/兼容性）+ VF 硬件 DMA 直通（数据面）+ 后端绑定一个专用 VF 软件实例桥接两层"的混合直通架构，且接收通路（FE 预挂 buffer → 经后端取址下发 VF → VF 直接 DMA 写 guest 缓存 → 中断经 VF 软件实例触发 FE 收数据）逐步对应权 1。F5（"idle"字样）、F2/F6/F7（中间步骤/接口措辞）公开资料未逐字复现但机制同手段/同功能/同效果，故含等同命中，落第 2 档而非第 1 档。所有证据材料发布于 2019–2020，晚于 2014 授权日，属专利公开后材料，可作侵权证据；未发现任何针对本候选的反向证据。

## 升级路径（仅当落第 3-4 档时填）
（不适用——已落第 2 档。若需升至第 1 档：从 Linux 内核 `drivers/vhost/vdpa.c`、`drivers/vdpa/vdpa.c` 源码逐字核验 F5"专用/空闲 VF 实例绑定"与 F7"经后端接口取地址写入接收队列"的实现代码，将等同命中升级为字面命中。）

## 总结一句话
开源 vDPA 栈以 virtio FE/BE 半虚拟化模型 + vendor VF 直接 DMA 直通 + vhost-vDPA 后端绑定专用 VF 软件实例，完整再现 US8635616B2 混合直通架构 F1–F9，含数处等同命中，落第 2 档（确认侵权-中），证据均晚于 2014 授权日。
