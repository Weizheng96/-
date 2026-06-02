# 04-napatech-link-virt sources

## Phase 1 — react 粗筛 query 留痕
1. `Napatech Link-Virtualization virtio-net virtio-blk hardware offload vDPA SmartNIC`
   - 命中：napatech.com datasheet/产品页多条；确认"exposing 16 virtio-net and 16 virtio-blk to the host with full tenant isolation"、"implements the standard vDPA kernel framework"、"NT50B01 features fully accelerated VirtIO 1.1 with vDPA"。**强信号，继续深抓。**
2. `Napatech Link-Virtualization vDPA virtio datapath SR-IOV VF passthrough live migration architecture`
   - 命中：确认"VirtIO (as opposed to SR-IOV) enables Live Migration"、"vDPA kernel framework ... retaining the high performance and low latency of SR-IOV"、"bare-metal offload SmartNIC ... exposing 16 virtio-net and 16 virtio-blk"。
3. `vDPA vhost-vdpa architecture virtio control plane vendor datapath VF DMA descriptor ring guest driver kernel framework explained`
   - 命中：Red Hat / QEMU / vDPA-dev 权威文档。确认 vDPA = "datapath which complies with the virtio specifications with a vendor specific control path"；"vDPA device can DMA to or from guest memory directly"；"implemented through PCI as a PF, a VF or ... SF"。用于核验 F1/F5/F8 机制。
4. `Napatech Link-Virtualization press release virtio vDPA SmartNIC bare metal virtio-blk announcement date`
   - 命中：Napatech press release（2022-07-05）"hardware-offloaded implementation of the Virtio 1.1 ... framework for Linux"、"guest VMs do not require a custom or proprietary driver"。提供有日期的公开材料（晚于 2014 授权）。

## Phase 2 — react 深抓（WebFetch + curl 落盘）
- WebFetch: napatech.com Link-Virtualization datasheet —— 产品级事实（16 virtio-net/blk、vDPA、VirtIO 1.1、live migration、tenant isolation）；copyright © 2026。
- WebFetch: napatech.com press release —— 2022-07-05；hardware-offloaded Virtio 1.1、guest VMs 不需私有驱动、vDPA、offload host CPU→SmartNIC。
- WebFetch: Red Hat "Introduction to vDPA kernel framework"（2020-08-12）—— "datapath complies with the virtio specification, but ... control path is vendor specific"；"could be a PF, a VF or ... SF"；"datapath ... mapped directly from the guest application to the VF in the physical NIC"；"translation between the NIC vendor control plane and the virtio control plane interface for a VM"。
- WebFetch: Red Hat "vDPA kernel framework part 1"（2020-08-17）—— vDPA device driver 经 vendor-specific method 通信；"DMA mapping operations - ... enabling the vDPA devices to set their own DMA mapping"。
- WebSearch 汇总（QEMU vhost-vdpa 文档）—— "the vDPA device can DMA to or from guest memory directly, enabling native speed of the hardware"。

## L1 证据落盘（curl）
- `napatech-link-virt-datasheet.html`（189KB）—— Grep 已核验含 "16 virtio-net" / "virtio-blk" / "tenant isolation" / "vDPA"。
- `napatech-press-release-2022.html`（186KB）—— Grep 已核验含 "hardware-offloaded" / "proprietary driver" / "vDPA"。

## 引用 URL
- https://www.napatech.com/support/resources/data-sheets/link-virtualization-software-for-napatech/
- https://www.napatech.com/media/press-releases/napatech-accelerates-infrastructure-services-processing-for-data-center-applications/ （2022-07-05）
- https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework （2020-08-12）
- https://www.redhat.com/en/blog/vdpa-kernel-framework-part-1-vdpa-bus-abstracting-hardware （2020-08-17）
- https://www.qemu.org/docs/master/interop/vhost-vdpa.html
- https://www.napatech.com/support/resources/data-sheets/link-nt50b01-smartnic/ （NT50B01：VirtIO 1.1 + vDPA + Xilinx Kintex UltraScale+ FPGA）

## 备注
- 时间窗：所有 Napatech / vDPA 公开材料均为 2020 年及以后，晚于本专利 2014-01-21 授权，可作侵权证据。
- Napatech FPGA 固件细节闭源，F7/F9 的"导出 API 取地址写 first storage unit"与"VF 通知 VF 软件实例触发 FE"等内部步骤无 Napatech 自有 verbatim；以 vDPA 标准框架机制 + virtio 规范推定，列为"机制等同/资料不足"。
