# 05-yusur-k2-vdpa verdict

## 候选基本信息
- 名称：YUSUR K2 / K2-Pro DPU（virtio/vDPA 卸载，KPU 架构） / 组织：中科驭数 YUSUR（北京中科驭数科技） / 类型：产品 / 初判命中 F#：F1,F2,F5,F8 / 专利公开（授权）日：2014-01-21

> 注：本专利侵权特征清单实际编号为 F1–F9（F1–F5=混合直通架构前提；F6–F9=接收数据通路四步）。下表按权威文档 F1–F9 全列；初判 metadata 的 "F8" 对应"硬件 DMA 直通"语义，落在本表 F8。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（VF 从 I/O 设备虚拟化而来 / SR-IOV） | 命中（字面） | "采用SR-IOV替代虚拟交换机，VF直通到虚拟机（VM）内部"；"驭云SDN...支持的网卡如PF/VF/SF/VFIO/VDPA" | blog.csdn.net/yusur/article/details/124682791 ; yusur.tech/dpu/K2-Pro | 驭数 DPU 明确做 SR-IOV，从物理 I/O 设备虚拟出 VF。 |
| F2（VF 软件实例与 VF 设备一一对应） | 等同/可推定命中 | "支持的网卡如PF/VF...通过device-plugin发布给Kubernetes进行统一的管理和调度" | 同上 | 凡 SR-IOV VF 直通方案，Host 侧必有与各 VF 一一对应的 VF 驱动/管理实例；属本领域标配，等同命中。但驭数未逐字描述"一一对应"。 |
| F3（Host 有同类型 I/O 虚拟设备后端实例 BE） | 公开资料不足 | "vhost-net作为virtio的backend"（行业综述）；驭数轻量虚拟化"QEMU作为Device Emulation service组件运行在SoC" | 124682791 ; 142918552 | 驭数自有方案把后端模拟移到 SoC 上的 QEMU，且 virtio-net/nvme 走 VF 直通——是否存在专利所述"与底层 I/O 设备同类型的 BE 半虚拟化后端"且参与数据面，公开材料未明确，不脑补。 |
| F4（VM 有 I/O 虚拟设备前端实例 FE） | 命中（字面，但语境存疑） | "虚拟化通常使用virtio-blk，virtio-net为虚机提供磁盘和网卡设备" | 142918552 | Guest 内有 virtio 前端驱动属事实。但在驭数"VF 直通透传"模式下，VM 内可能直接是 VF 驱动而非 virtio FE，二者并存与否未披露。 |
| F5（BE 绑定一个空闲 idle VF 软件实例）★关键★ | 公开资料不足（未见此桥接动作） | 无对应 verbatim；驭数描述为"virtio-net硬件卸载 + VF直通透传"与"vDPA：数据路径后端卸载到硬件、控制路径后端留在内核/DPDK" | 142918552 ; 124682791 | 本专利最核心限定=BE 绑定一个**空闲** VF 软件实例以桥接控制面与数据面。驭数公开材料只说 VF 直通 / vDPA 数据控制面分离，**未披露**"BE 绑定空闲 VF 软件实例"这一具体桥接机制。无正向证据。 |
| F6（FE 预分配 DMA 缓存） | 公开资料不足 | 无 | — | 收包通路 DMA 缓存预分配主体未披露。 |
| F7（VF 软件实例经 BE 导出 API 取 DMA 地址并写入 VF 设备 first storage unit/接收队列） | 公开资料不足 | 无（驭数 host-VM 通信用 "API CHANNEL + IOREQ RING BUFFER" over PCIe BAR，非"BE 导出 API"语义） | 142918552 | 驭数的跨侧通信原语是 PCIe BAR 上的 API CHANNEL/IOREQ RING BUFFER，与专利"经 BE exporting API 取地址写入 VF first storage unit"不是同一描述；细节不足，不认定命中也无反向证据。 |
| F8（VF 设备收到数据时取地址发起硬件 DMA 写） | 部分命中（硬件 DMA 直通事实成立，但具体取址链路不足） | "OVS-DPDK将从网卡收到的报文数据写入虚拟机（VM）的内存"（行业综述）；驭数"virtio-net/nvme 硬件卸载 + VF 直通...提供高性能的存储和网络" | 124682791 ; 142918552 | DPU 硬件 VF 直接 DMA 收发报文到 VM 内存是 VF 直通方案固有事实，方向命中；但"从 first storage unit 选地址作为目标地址"这一专利特定步骤未单独披露。 |
| F9（DMA 完成后 VF 设备通知 VF 软件实例 → 触发 FE 收数据） | 公开资料不足 | 无（驭数有"SoC 和 Host 间双向中断机制"，但非专利所述"VF 设备→VF 软件实例→FE"链路） | 142918552 | 通知/中断机制存在，但与专利特定三级通知链不可逐字对应。 |

命中小结：F1 字面命中、F2/F8 等同或方向命中、F4 字面但语境存疑；**F3/F5/F6/F7/F9（含最关键的 F5 桥接动作）均公开资料不足，且无任何反向证据**。即专利"混合直通"的两层（FE/BE 半虚拟化 + VF 硬件 DMA）在驭数确各有踪迹，但把两层桥接的核心限定（F5 "BE 绑定空闲 VF 软件实例" + F7 "经 BE 导出 API 取地址写 VF first storage unit"）在公开材料中无法证实也无法证伪。

## 已检查文档清单
- 《基于DPU的轻量虚拟化解决方案》（2024-10-14，CSDN 驭数官方号；已 curl 落盘 csdn-yusur-lightvirt-142918552.html）— https://blog.csdn.net/yusur/article/details/142918552
- 《DPU应用场景系列（一）网络功能卸载》（2022-05-10，CSDN 驭数官方号）— https://blog.csdn.net/yusur/article/details/124682791
- K2-Pro 产品页（KPU 架构，网络/存储/安全/计算卸载）— https://www.yusur.tech/dpu/K2-Pro
- 驭云 SDN 解决方案（PF/VF/SF/VFIO/VDPA 经 device-plugin 发布给 K8s）— https://www.yusur.tech/solution/DPU
- WebSearch 摘要（virtio 全卸载 vs vDPA：vDPA 解耦数据/控制路径，数据路径后端卸载到硬件）
- 《DPU 与 CPU 互联接口 Virtio 还是 SR-IOV》知乎 — https://zhuanlan.zhihu.com/p/669300731（证书错误未取到）

## 最终判定
**第 3 档：≥60% 命中且其余资料不足、无反向证据**

判定依据：
1. 时间窗合规：驭数成立 2018，材料 2022/2024，均晚于专利 2014-01-21 授权日。
2. 架构层一致：驭数 DPU 走的正是本专利所属"虚拟化 I/O 数据面硬件卸载（SR-IOV VF + virtio/vDPA）"抽象层，非不同架构层，**不构成第 5 档(c)排除**。
3. F1 字面命中、F2/F8 等同或方向命中、F4 字面命中（语境存疑），架构前提层已可见 SR-IOV VF + virtio 前后端两层共存的迹象——粗略覆盖度在 ~50–60% 区间且方向高度吻合。
4. **但全案最关键的 F5（BE 绑定空闲 VF 软件实例桥接）与配套的 F6/F7/F9 收包通路细节，公开材料完全未披露**——国产 DPU 厂商对 virtio/vDPA 数据通路硬件实现细节披露有限，属"公开资料不足"，**不是反向证据**（未见任何"驭数不采用此机制 / excludes / 不支持"的明示）。
5. 因此既不能升到第 2 档（缺关键 F5/F7 的正向证据），也不能降到第 5 档已排除（无 (a) 真反向 / (b) 时间不合规 / (c) 架构不同 任一硬条件）。资料不足 + 方向吻合 + 无反向 → 严格落第 3 档。

## 升级路径（仅 3-4 档）
- 取得驭数 DPU virtio-net/vDPA **数据面后端**的技术白皮书 / 架构详解 / SDK 文档，核实收包时 DMA 地址是否经"后端导出接口"传递、是否存在"后端绑定空闲 VF 实例"桥接动作（验证 F5/F7）。
- 检索中科驭数（assignee：北京中科驭数科技有限公司）2018 年后自有专利（Google Patents / 国家知识产权局），找其 virtio/vDPA 卸载专利逐特征比对 F5/F6/F7/F9，看是否落入或回避本专利。
- 抓取驭数 vDPA 驱动 / virtio backend 的开源代码或 device-plugin 实现（若有 GitHub 公开仓库），看 VF 软件实例与 BE 的绑定关系及收包 DMA 地址来源。
- 突破 zhuanlan.zhihu.com/p/669300731（virtio vs SR-IOV）证书问题（curl 兜底），获取其对驭数数据通路的描述。

## 总结一句话
中科驭数 K2/K2-Pro DPU 确在做 SR-IOV VF + virtio/vDPA 的虚拟化 I/O 硬件卸载（架构层吻合、F1 命中、F2/F4/F8 等同或方向命中、时间合规），但本专利最核心的"BE 绑定空闲 VF 软件实例 + 经 BE 导出 API 取 DMA 地址写 VF 接收队列"桥接机制（F5/F7）公开资料不足、亦无反向证据，故落第 3 档。

---
*免责声明：本文件为侵权线索与证据链梳理，不构成"已构成侵权"的法律结论；最终侵权认定须经权利要求逐项比对与专业法律意见。*
