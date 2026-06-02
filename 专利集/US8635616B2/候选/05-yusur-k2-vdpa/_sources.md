# 证据索引 — 05-yusur-k2-vdpa

## Phase 1 — react 粗筛（WebSearch，串行）
1. `中科驭数 YUSUR K2 DPU virtio vDPA 网络 存储 卸载`
   → 信号：K2-Pro KPU 架构融合网络/存储/安全/计算卸载；驭云 SDN 支持 PF/VF/SF/VFIO/VDPA；存储侧硬件模拟向 host 提供 nvme/virtio 块设备。命中方向，继续。
2. `中科驭数 DPU virtio 后端 数据面 卸载 DMA 队列 vDPA 数据通路`
   → 信号：virtio 卸载两种方案=全卸载 / vDPA；vDPA 解耦数据路径与控制路径，数据路径后端卸载到硬件、控制路径后端留在内核/DPDK；驭数轻量虚拟化方案 virtio-net/nvme 硬件卸载 + VF 直通透传给虚机。
3. `中科驭数 DPU 轻量虚拟化 virtio-net VF 直通 nvme 透传 虚机`
   → 信号：Host 侧只保留 Hypervisor + 部分内核，QEMU 作为 Device Emulation service 跑在 SoC；virtio-blk/virtio-net VF 直通；每虚机分配特殊 PCIe 设备，BAR 分 API CHANNEL + IOREQ RING BUFFER。
4. `中科驭数 专利 virtio 卸载 DPU 虚拟化 IO patents google` / `YUSUR ... assignee Google Patents`
   → 未检索到中科驭数自有的、与本专利"BE 绑定空闲 VF 软件实例 + 经 BE 导出 API 取 DMA 地址"机制可逐特征比对的专利；命中的是行业内其它主体（华为/通用 virtio）专利。

## Phase 2 — react 深抓（WebFetch / curl，串行）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2024-10-14 | WebFetch+curl 落盘 | https://blog.csdn.net/yusur/article/details/142918552 ；本地 csdn-yusur-lightvirt-142918552.html（154KB，L1） | 《基于DPU的轻量虚拟化解决方案》："驭数DPU卡支持nvme和virtio-net的硬件卸载，因此虚机的存储和网卡采用VF直通的方式透传给虚机"；"Host侧只保留Hypervisor和部分Linux内核功能，且不提供用户态控制面组件"；"QEMU作为Device Emulation service组件运行在SoC"；"每一个虚机都分配了一个特殊的PCIe设备，BAR空间划分成两部分：API CHANNEL...IOREQ RING BUFFER"。未展开 VF 直通的 DMA 收发通路/前后端实例/地址映射细节。 |
| 2 | 2022-05-10 | WebFetch | https://blog.csdn.net/yusur/article/details/124682791 | 《DPU应用场景系列（一）网络功能卸载》："采用SR-IOV替代虚拟交换机，VF直通到虚拟机（VM）内部"；"vhost-net作为virtio的backend"；"OVS-DPDK将从网卡收到的报文数据写入虚拟机（VM）的内存"。行业既有 SR-IOV/vhost/OVS-DPDK 综述，非驭数专有混合直通机制。 |
| 3 | — | WebFetch 失败 | https://zhuanlan.zhihu.com/p/669300731 | unknown certificate verification error，未取到。 |

## 时间窗
本专利 2014-01-21 授权。中科驭数成立于 2018，全部检索到材料（2022 / 2024）均晚于授权日，时间合规。

## 受限说明
国产 DPU 厂商对 virtio/vDPA 数据通路的硬件实现细节披露有限：公开材料确认"virtio-net/nvme 硬件卸载 + VF 直通""vDPA 数据/控制路径分离"，但**未公开**收包时 DMA 地址如何在 FE/BE/VF 软件实例间传递（是否经 BE 导出 API、是否写入 VF 设备 first storage unit、完成后如何通知）。相关 F#（F3/F4/F6/F7/F9）按"公开资料不足"判，不脑补。
