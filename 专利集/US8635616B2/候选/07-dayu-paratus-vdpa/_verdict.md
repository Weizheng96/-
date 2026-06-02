# 07-dayu-paratus-vdpa verdict

## 候选基本信息
- 名称：大禹智芯 Paratus 2.0 DPU
- 组织：DaYu 大禹智芯
- 类型：产品
- 初判命中 F#：F1,F2,F5,F8
- 专利公开（授权）日：2014-01-21

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（VF 从 I/O 设备虚拟化而来 / SR-IOV） | 资料不足 | 「支持VirtIO来增强虚拟化环境下的适配性」「OVS全卸载…NVMe模拟」 | cloud.tencent.com/developer/news/937365 | 公开材料强调 virtio 设备模拟与 DPU 卸载，未明确披露在 Host 硬件层做 SR-IOV 虚拟出 VF 设备并由本专利方式使用；DPU 卡多以 virtio/NVMe 设备形态呈现，非本专利"Host I/O 设备 SR-IOV 出 VF"前提。 |
| F2（VF 软件实例与 VF 设备一一对应） | 未命中/资料不足 | （无相关披露） | — | 无任何关于 Host 内"VF 软件实例与 VF 设备一一对应"的公开描述。 |
| F3（Host 有同类型 I/O 虚拟设备的后端实例 BE） | 不匹配 | 「硬件加速的VirtIO架构意味着后端（至少是数据路径）在硬件中实现」 | community.aijishu.com/a/1060000000228117 | DPU/硬件 vDPA 模型中 virtio 后端在 DPU 硬件内实现，而非本专利要求的"Host 内 BE 软件实例"。架构层不同。 |
| F4（VM 有 I/O 虚拟设备的前端实例 FE） | 部分相关 | 「支持VirtIO来增强虚拟化环境下的适配性」 | cloud.tencent.com/developer/news/937365 | Guest 内有 virtio-net/virtio 前端驱动属 virtio 通用形态，与 F4 抽象一致；但 F4 单独命中不足以构成本专利混合架构。 |
| F5（BE 绑定一个空闲 VF 软件实例）★关键限定★ | 未命中/资料不足 | （无相关披露） | — | 本专利最关键桥接动作。公开材料完全未披露"Host 内 BE 绑定空闲 VF 软件实例"机制；DPU 数据面卸载发生在 DPU 硅片内，非 Host 软件绑定。关键限定缺失。 |
| F6（FE 预分配 DMA 缓存） | 资料不足 | （无相关披露） | — | 无 DMA 数据通路细节披露。 |
| F7（VF 软件实例经 BE 导出 API 取地址写入 VF 设备 first storage unit） | 资料不足 | （无相关披露） | — | 无"BE 导出 API"/first storage unit 相关披露；此为本专利 FE/BE/VF 解耦的特征接口。 |
| F8（VF 设备收数据时取地址发起 DMA 写请求） | 部分相关/资料不足 | 「硬件vDPA将虚拟队列映射到硬件队列」 | community.aijishu.com/a/1060000000228117 | 硬件 vDPA 把虚拟队列映射到硬件队列、数据面直达硬件，与"数据面直通硬件"抽象相近；但实现主体在 DPU 硬件而非本专利 Host 内"VF 设备→VF 软件实例"路径，且无 verbatim 证据描述 DMA 写目标地址来自 FE 预分配缓存。 |
| F9（VF 设备通知 VF 软件实例 → 触发 FE 收数据） | 未命中/资料不足 | （无相关披露） | — | 无"VF 设备通知 Host 内 VF 软件实例再触发 FE"的接收通路披露。 |

## 已检查文档清单
- 大禹智芯官方 Paratus 2.0 产品页（ARM SoC + FPGA、基于 FPGA 网络数据处理通路、HPRT™、端到端加密；无 FE/BE/VF 绑定与 DMA 细节）— https://www.dayudpu.com/product/paratus2
- 腾讯云 Paratus 2.0 发布稿（2022-10-14；支持 VirtIO、OVS 全卸载、存储客户端全卸载、NVMe 模拟）— https://cloud.tencent.com/developer/news/937365
- 极术社区《DPU和CPU互联的接口之争：Virtio还是SR-IOV？》（硬件 vDPA：后端数据面在硬件中实现，虚拟队列映射到硬件队列）— https://community.aijishu.com/a/1060000000228117
- WebSearch 检索大禹智芯自有 virtio/passthrough 专利：未检索到公开来源（命中均为他方专利/论文）

## 最终判定
**第 4 档：部分命中（<60%）**

判定依据：
- 时间合规：Paratus 2.0 发布于 2022-10-14，晚于专利授权日 2014-01-21，落入时间窗。
- 领域相关：属 I/O 虚拟化（virtio + DPU 数据面卸载），与本专利同领域，不构成"架构层完全无关"的早剪枝条件。
- 但本专利的判定核心是 **F5（BE 绑定空闲 VF 软件实例）** 这一把"Host 内半虚拟化 FE/BE 控制面"与"VF 硬件直通数据面"桥接起来的特定 **Host 内软件机制**，并配套 F3（Host 内 BE）、F7（BE 导出 API + VF 设备 first storage unit）、F9（VF 设备→VF 软件实例→FE 接收通路）。这些是本专利区别于纯 SR-IOV 直通 / 纯 virtio 软件后端的关键限定。
- 公开材料显示 Paratus 2.0 是 **DPU 卡（ARM SoC + FPGA）** 形态：virtio 后端 / 数据面卸载在 **DPU 硬件内** 实现（"后端…在硬件中实现"、"硬件 vDPA 将虚拟队列映射到硬件队列"），而非本专利要求的 Host 内"BE 软件实例绑定空闲 VF 软件实例 + 经 BE 导出 API 取 DMA 地址写入 VF 设备"。F3/F5/F7/F9 在架构主体上与本专利不一致，且无公开证据。
- 仅 F4（Guest virtio 前端）抽象相符、F1/F8 部分相近但缺关键 verbatim；核心限定 F2/F3/F5/F6/F7/F9 均未命中或资料不足 → 命中率明显 <60%。
- 未达第 5 档：本候选与专利同属 I/O 虚拟化领域，存在 virtio/数据面直通的概念交集，**不满足"架构层完全不同"的硬门槛**（DPU 硬件 vDPA 与本专利 host 软件混合直通是相邻而非无关方案），亦无针对该候选的正向反向证据明确排除；属"资料不足 + 关键限定不匹配"，落第 4 档而非第 5 档。

## 升级路径（仅 3-4 档）
- 获取大禹智芯 Paratus 2.0 的技术白皮书 / SDK 文档 / vDPA 驱动实现，核验其是否在 Host 内（而非纯 DPU 硅片）维护"BE 软件实例 + 与 VF 设备一一对应的 VF 软件实例 + BE 绑定空闲 VF 软件实例"的混合直通栈。
- 检索大禹智芯自有专利 / 公开技术演讲，确认其数据面是否走"VF 设备 DMA 写入 Guest FE 预分配缓存 + 经 Host 内 VF 软件实例触发 FE 接收"（F6–F9 接收通路）；若证实落入 Host 内此结构，可上调至第 3 档并进一步逐特征比对 F5/F7。
- 核验 OVS 全卸载 / NVMe 模拟的具体数据通路是否复用上述 host-side FE/BE/VF 绑定机制，区分"DPU 内置 virtio 后端"与"专利的 host 内 BE 绑定空闲 VF 软件实例"。

## 总结一句话
Paratus 2.0 为 2022 年发布的国产 DPU（ARM SoC+FPGA），支持 virtio 与 OVS/存储/NVMe 数据面卸载，与本专利同属 I/O 虚拟化领域，但其 virtio 后端/数据面卸载在 DPU 硬件内实现，缺本专利"Host 内 BE 绑定空闲 VF 软件实例"等关键限定的公开证据，落第 4 档。
