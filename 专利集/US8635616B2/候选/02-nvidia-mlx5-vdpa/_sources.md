# 02-nvidia-mlx5-vdpa sources / query 留痕

## Phase 1 — WebSearch (react 串行)
- query 1: `NVIDIA mlx5 vDPA BlueField virtio data path acceleration`
  → 命中 DPDK MLX5 vDPA 官方文档（多版本）+ NVIDIA DOCA "Virtio Acceleration through Hardware vDPA"。确认 mlx5 vDPA = ConnectX-6/7 + BlueField-2/3 的 vhost data path acceleration 驱动，支持 SR-IOV VF。强信号，不剪枝。
- query 2: `mlx5_vdpa hardware vDPA virtio control plane software data plane direct DMA guest memory VF`
  → 命中 DPDK mlx5 多版本文档。确认："this driver only deals with virtual memory addresses"；"vDPA driver needs to setup VF MSIX interrupts, each queue's interrupt vector is mapped to a callfd associated with a virtio ring"；VF in SR-IOV context。
- query 3: `vDPA architecture control plane software data plane hardware virtio ring guest memory DMA Red Hat kernel`
  → 命中 Red Hat 官方 vDPA 系列博客。架构层定性证据："the data plane goes directly from the NIC to the guest using the virtio ring layout"；"datapath complies with the virtio specification, but whose control path is vendor specific"；"The virtio data plane is mapped directly from the guest application to the VF in the physical NIC"。

## Phase 2 — WebFetch / curl 落盘
- DPDK vDPA Device Drivers PDF (Release 20.02.1, 2020-05-18)：curl 落盘 `dpdk-vdpa-2002.pdf`（doc.dpdk.org WebFetch 报 cert error，改用 fast.dpdk.org PDF）。pdfplumber 抽取 → `mlx5_text.txt`。含 MLX5 Design 章节 + IFCVF ops verbatim。
  - https://fast.dpdk.org/doc/pdf-guides-20.02/vdpadevs-20.02.pdf
- Red Hat 博客 "Achieving network wirespeed in an open standard manner: introducing vDPA"（2019-10-02）：WebFetch 成功，取架构层定性 verbatim。
  - https://www.redhat.com/en/blog/achieving-network-wirespeed-open-standard-manner-introducing-vdpa
- NVIDIA DOCA "Virtio Acceleration through Hardware vDPA"（DOCA v3.3.0）：WebFetch 成功但仅操作指引，无架构 verbatim，未采纳为 L1 证据。
  - https://docs.nvidia.com/doca/sdk/virtio-acceleration-through-hardware-vdpa/index.html

## 受限说明
- doc.dpdk.org（HTML 官方文档）WebFetch 报 "unknown certificate verification error"，curl 亦报 schannel TLS 握手失败；改用 fast.dpdk.org 的等价 PDF 版本（同一 DPDK 项目官方发布物）落盘解析，内容等价。
