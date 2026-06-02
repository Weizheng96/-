# 证据索引 — 08-amd-pensando-vdpa（检索留痕）

## Phase 1 — react 粗筛 query
1. WebSearch: `AMD Pensando DPU virtio-net vDPA offload DSC Elba Giglio`
   → 命中 AMD 产品页、Linux kernel pds_vdpa 驱动文档、Elba/Giglio product brief、Red Hat vDPA 博客。有信号，进入 Phase 2。
2. WebSearch: `vDPA virtio datapath acceleration control plane vhost hardware ring DMA guest buffers architecture`
   → vDPA 通用架构：数据面 NIC↔guest 直通 virtio ring，控制面厂商私有。
3. WebSearch: `Pensando patent virtio offload SR-IOV virtual function DMA guest virtual machine datapath`
   → 未检索到 Pensando/AMD 自有 virtio 卸载专利；返回通用 SR-IOV/vDPA 资料（含 virtio 硬件卸载三种路线：full offload / vDPA / vDPA partitioning）。

## Phase 2 — react 深抓
- WebFetch: https://docs.kernel.org/networking/device_drivers/ethernet/amd/pds_vdpa.html
  → pds_vdpa 是 auxiliary bus 驱动，向 virtio 网络栈提供 vDPA 设备；依赖 pds_core 做 PF/VF PCI 处理；`echo N > sriov_numvfs` 创建 VF；启用 vDPA 服务后每个 VF 对应一个 auxiliary device；guest 侧 `modprobe virtio_vdpa`。
- WebFetch: https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework
  → 关键 verbatim：「the virtio data plane is mapped directly from the guest application to the VF in the physical NIC」；「the datapath is offloaded to the vDPA hardware」；doorbell 之外不允许直接寄存器映射。**guest virtio 前端直接对接硬件 VF 数据面，宿主机侧无"同类型半虚拟化 BE 转发数据"环节。**
- WebFetch（超时失败，改 curl 落盘）: pensando-elba-product-brief.pdf
  → curl 落盘成功。文本含「SR-IOV」「16 M hardware queues」「2K VNICs」「DMA commands / scatter-gather lists」「NVMe virtualization」「network virtualization」。确认 SR-IOV VF + 硬件队列 + DMA 硬件基底存在。

## 落盘文件
- pensando-elba-product-brief.pdf （AMD 官方，第二代 Elba DPU 产品简介）
- kernel-pds_vdpa.html （Linux kernel 官方 pds_vdpa 驱动文档）

| # | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- |
| 1 | 官方文档 | https://docs.kernel.org/networking/device_drivers/ethernet/amd/pds_vdpa.html | SR-IOV VF→aux device 一一对应 (F1/F2)；virtio 栈对接 (F4) |
| 2 | 官方博客 | https://www.redhat.com/en/blog/introduction-vdpa-kernel-framework | 数据面 guest↔VF 直通 (F8)，无 BE 转发 (F3/F7 分歧) |
| 3 | 官方产品简介 | pensando-elba-product-brief.pdf（本地） | SR-IOV + 16M 硬件队列 + DMA 硬件基底 (F1/F8) |
| 4 | 官方文档 | kernel-pds_vdpa.html（本地） | 同 #1 |
