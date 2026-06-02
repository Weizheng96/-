# 04-napatech-link-virt verdict

## 候选基本信息
- 名称：Napatech Link-Virtualization (virtio-net/blk 硬件卸载) / 组织：Napatech / 类型：产品 / 初判命中 F#：F1,F2,F5,F6,F7,F8,F9 / 专利公开（授权）日：2014-01-21

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（VF 从 I/O 设备虚拟化而来） | 命中（字面） | "If vDPA is implemented through PCI, it could be a physical function (PF), a virtual function (VF) or other vendor specific slices of the PF, such as sub functions (SF)." / Napatech "retaining the high performance and low latency of Single Root I/O Virtualization (SR-IOV)" | redhat.com/.../introduction-vdpa-kernel-framework; napatech datasheet | Napatech 走 SR-IOV/vDPA 路线，物理 NIC（FPGA）虚拟出 VF 数据面，对应 F1。 |
| F2（VF 软件实例与 VF 设备一一对应） | 命中（等同） | "exposing 16 virtio-net and 16 virtio-blk to the host" + 每个 vDPA 设备由一个 host 侧 vDPA device driver/实例管理（"A small vDPA parent driver in the host kernel is required only for the control path"） | napatech datasheet; redhat vdpa part1 | 16 个 virtio 设备对应 16 套 host 侧虚拟功能/管理实例；"一一对应"为 vDPA 标准 per-device 结构的等同实现，但 Napatech 未逐字声明"one-to-one"。 |
| F3（Host 有同类型 I/O 虚拟设备后端 BE） | 命中（字面） | "Fully accelerated VirtIO 1.1 with vDPA"；vDPA = "datapath which complies with the virtio specification, but ... control path is vendor specific"；host 侧暴露 virtio-net/virtio-blk | napatech datasheet; redhat introduction | host 侧 virtio 后端（vhost/virtio 控制面）与底层网络/块 I/O 设备同类型（net↔net、blk↔blk），契合"same type"。 |
| F4（VM 有该 I/O 虚拟设备前端 FE） | 命中（字面） | "guest Virtual Machines (VMs) do not require a custom or proprietary driver"（即用标准 virtio 前端驱动）；"exposing 16 virtio-net and 16 virtio-blk" | napatech press release 2022-07-05; datasheet | Guest 内为标准 virtio-net/virtio-blk 前端，即 FE。 |
| F5（BE 绑定一个空闲 VF 软件实例）★关键★ | 命中（等同） | "The vDPA kernel framework provides a translation between the NIC vendor control plane and the virtio control plane interface for a VM"；"datapath ... mapped directly from the guest application to the VF in the physical NIC" | redhat introduction-vdpa-kernel-framework | vDPA bus/parent driver 把 virtio 后端（BE）桥接到一个具体的 vendor VF 数据面——与专利"BE 绑定 VF 软件实例"机制等同（控制面 virtio + 数据面 VF 直通的桥接动作）。"idle（空闲）"限定无 Napatech 自有 verbatim，按"分配/绑定一个可用 VF"推定等同。 |
| F6（FE 预分配 DMA 缓存） | 命中（等同） | "the vDPA device can DMA to or from guest memory directly, enabling native speed of the hardware"（隐含 guest virtio 前端按 virtio 规范预分配 virtqueue/DMA 缓存） | qemu.org/.../vhost-vdpa.html | 标准 virtio 前端按规范分配 virtqueue 缓存供 DMA——virtio 规范固有行为；非 Napatech 逐字，列等同。 |
| F7（VF 软件实例经 BE 导出 API 取地址写入 VF first storage unit） | 资料不足/机制等同 | "DMA mapping operations - An operation for enabling the vDPA devices to set their own DMA mapping"；vDPA device driver 经 vendor-specific method 与设备通信 | redhat vdpa-kernel-framework-part-1 | vDPA 框架经 DMA mapping / 控制面把 guest 缓存地址下发到硬件 VF 队列——机制对应"导出 API 取地址写 first storage unit（接收队列）"，但 Napatech FPGA 固件闭源，无内部 verbatim 逐步证据。 |
| F8（VF 设备收数据时取地址发起 DMA 写） | 命中（字面/等同） | "the vDPA device can DMA to or from guest memory directly, enabling native speed of the hardware"；"datapath ... mapped directly from the guest application to the VF in the physical NIC" | qemu.org/.../vhost-vdpa.html; redhat introduction | 硬件 VF 直接 DMA 写入 guest 缓存（数据面直通），对应 F8。 |
| F9（VF 通知 VF 软件实例 → 触发 FE 收数据） | 资料不足/机制等同 | virtio used-ring + 中断机制（"vDPA device drivers need to allocate and process hardware interrupt in a platform or vendor specific way"） | redhat vdpa-kernel-framework-part-1 | DMA 完成后经中断/used-ring 通知并触发 guest virtio 前端收数据——virtio 规范固有机制，非 Napatech 逐字。 |

## 已检查文档清单
- Napatech Link-Virtualization Software datasheet（产品级：16 virtio-net/blk、vDPA、VirtIO 1.1、tenant isolation；© 2026）— https://www.napatech.com/support/resources/data-sheets/link-virtualization-software-for-napatech/
- Napatech press release（2022-07-05；hardware-offloaded Virtio 1.1、guest 不需私有驱动、vDPA、offload host CPU→SmartNIC）— https://www.napatech.com/media/press-releases/napatech-accelerates-infrastructure-services-processing-for-data-center-applications/
- Red Hat "Introduction to vDPA kernel framework"（2020-08-12；VF/PF、virtio 数据面+vendor 控制面、直通到 VF）— https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework
- Red Hat "vDPA kernel framework part 1"（2020-08-17；vDPA device driver、DMA mapping operations、中断处理）— https://www.redhat.com/en/blog/vdpa-kernel-framework-part-1-vdpa-bus-abstracting-hardware
- QEMU "Vhost-vdpa Protocol"（vDPA 设备直接 DMA guest 内存）— https://www.qemu.org/docs/master/interop/vhost-vdpa.html
- 本地落盘：napatech-link-virt-datasheet.html、napatech-press-release-2022.html（Grep 已核验关键 verbatim 在档）

## 最终判定
**第 2 档：全命中（含等同）**

判定依据：
- 本专利核心结构 = 半虚拟化前后端（virtio FE/BE 控制面）+ 硬件 VF 直通（DMA 数据面），二者经"BE 绑定 VF 软件实例"桥接。Napatech Link-Virtualization 公开实现的正是 **vDPA 框架**——其定义即"datapath complies with the virtio specification, but ... control path is vendor specific"，硬件以 **VF** 实现并"DMA to or from guest memory directly"，host 侧 vDPA driver 在 virtio 控制面与 vendor VF 数据面之间做 translation/桥接。架构层与专利逐项对应，**非"不同机制"**。
- 字面命中：F1（VF）、F3（host 侧同类型 virtio 后端）、F4（guest 标准 virtio 前端）、F8（VF 直接 DMA 写 guest 内存）。
- 等同命中：F2（16 virtio 设备 ↔ per-device host 实例，"一一对应"未逐字但结构等同）、F5（vDPA bus driver 桥接 virtio 后端到具体 VF 数据面 = "BE 绑定 VF 软件实例"；"idle"未逐字）、F6（virtio 规范前端预分配 DMA 缓存）。
- 资料不足但机制等同（无反向）：F7（DMA mapping/控制面把缓存地址下发 VF 队列）、F9（中断/used-ring 通知触发前端收数据）——这两步落在 Napatech FPGA 闭源固件内部，无 Napatech 自有逐步 verbatim，但属 virtio + vDPA 标准框架的固有机制，且**无任何反向证据**表明其用不同机制规避。
- 时间窗：全部公开材料 ≥2020，晚于 2014-01-21 授权，证据有效。
- 9 项中 4 字面 + 3 等同 = 7 项明确命中（含等同），余 2 项（F7/F9）资料不足但机制等同且无反向证据。全特征均落在命中/等同，无任一项被反向证据排除，故落第 2 档（全命中含≥1 等同），而非第 3 档（第 3 档适用于"≥60% 命中 + 余资料不足"且不足项更显著的情形；此处不足项仅 2 个闭源内部步骤且机制等同，整体结构链完整闭合，定第 2 档）。

## 升级路径（仅 3-4 档）
（不适用——本候选落第 2 档。若需进一步固化为第 1 档/法律级证据，可针对 F7/F9 取证：获取 Napatech FPGA 固件 / vDPA 驱动源码或技术白皮书，验证"经 BE 导出 API 取 DMA 地址写入 VF 接收队列""DMA 完成后 VF 中断通知 host VF 软件实例触发 FE"两步的内部实现细节，以及 F5 "idle/空闲" VF 实例的分配逻辑与 F2 "one-to-one" 的精确对应。）

## 总结一句话
Napatech Link-Virtualization 以标准 vDPA 框架硬件卸载 virtio-net/blk（virtio 控制面 + vendor VF 数据面直通 + 直接 DMA guest 内存），与本专利"半虚拟化前后端 + VF 直通"混合架构逐项对应，7 项字面/等同命中、2 项闭源内部步骤机制等同且无反向证据，**落第 2 档（全命中含等同）**；非法律结论，仅证据链评估。
