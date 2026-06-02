# 06-yunsilicon-vdpa verdict

## 候选基本信息
- 名称：云豹智能 metalDPU / Xinghe DPU（轻量虚拟化 / vDPA 方案）
- 组织：Yunsilicon 云豹智能
- 类型：产品
- 初判命中 F#：F1,F2,F5,F8
- 专利公开（授权）日：2014-01-21

## 检索粗筛
- query1 `云豹智能 Yunsilicon DPU virtio vDPA 轻量虚拟化 卸载` → 有信号：virtio 后端在 DPU 上硬化、基于 vDPA 热迁移。
- query2 `云豹智能 DPU virtio 后端 硬化 vDPA 热迁移 数据面 控制面 架构` → 有信号：用户态 vDPA 框架、数据面硬件加速+控制面软件分离。
- query3 `云豹智能 专利 virtio DPU 数据面 卸载 SR-IOV VF 虚拟机` → 无云豹自有专利文本，命中「Virtio vs SR-IOV」产业文。
- 结论：有信号，进入深抓（非早剪枝）。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（VF 设备从 I/O 设备虚拟化而来 / SR-IOV） | 部分相关 | 「SR-IOV exposes multiple virtual devices to higher-level software... VMs direct hardware access」；云豹「支持 PF/VF 热插拔」 | community.aijishu.com/a/1060000000228117 | 云豹支持 SR-IOV/VF，但其 virtio 卸载主线是 vDPA，公开材料未确认 vDPA 数据面建立在"VF 设备"之上 |
| F2（VF 软件实例与 VF 设备一一对应） | 未证实 | —（vDPA 公开描述为"虚拟队列映射到硬件队列"，未出现 Host 侧"VF 软件实例一一对应"概念） | cnblogs 16890840 | 公开资料不足，无正向证据 |
| F3（Host 有同类型 I/O 虚拟设备后端 BE） | 部分相关 | 「virtio 后端在 DPU 上做硬化」 | csdn 124996167 | 后端被硬化到 DPU 上，而非本专利"Host 内软件 BE"形态；类型一致性未明 |
| F4（VM 有该 I/O 虚拟设备前端 FE） | 命中（通用 virtio） | 「guest 和 QEMU 继续使用标准 virtio 协议」 | cnblogs 16890840 | Guest 内标准 virtio 前端，符合 F4，但属 virtio 通用特征 |
| F5（BE 绑定一个空闲 VF 软件实例）★关键★ | 不满足（架构无此结构） | 「数据通信过程由硬件设备（智能网卡）完成，虚拟机与网卡之间直通」「vDPA 把虚拟队列映射到硬件队列」 | cnblogs 16890840 / aijishu 228117 | vDPA 数据面 Guest ring 直接由硬件服务，无"Host 内 BE 绑定空闲 VF 软件实例"中转结构——本专利最关键桥接限定未体现 |
| F6（FE 预分配 DMA 缓存） | 未证实 | —（virtio 前端通用会分配队列缓存，但云豹未公开 DMA 缓存预分配细节） | — | 公开资料不足 |
| F7（VF 软件实例经 BE 导出 API 取地址写入 VF first storage unit）★关键★ | 不满足/未证实 | 「(虚拟队列)传递到硬件中，硬件会通过这些信息配置好数据平面」 | cnblogs 16890840 | vDPA 由硬件依据控制面配置数据平面，公开材料中无"VF 软件实例经 BE 导出 API 取 DMA 地址再写入 VF 设备"这一中转步骤 |
| F8（VF 设备收数据时取地址发起 DMA 写） | 部分相关 | 「数据通信...由硬件设备完成，虚拟机与网卡之间直通」 | cnblogs 16890840 | 硬件直接 DMA 收发与 F8 方向一致，但缺"从 first storage unit 取本专利方式下发的地址"这一前序，不构成完整命中 |
| F9（VF 设备通知 VF 软件实例 → 触发 FE 收数据） | 未证实 | — | — | 公开资料不足；vDPA 数据面通知路径未公开为"经 Host VF 软件实例触发 FE" |

## 已检查文档清单
- 龙蜥 virtio+DPU 实践 Q&A（含云豹 virtio 后端硬化/vDPA 热迁移表述）— https://blog.csdn.net/weixin_60347558/article/details/124996167
- vDPA = virtio 半硬件虚拟化（数据面硬件直通、控制面软件、无 SR-IOV VF 中转后端）— https://www.cnblogs.com/kevin-jun-2022/p/16890840.html （落盘 cnblogs-vdpa-16890840.html）
- DPU 与 CPU 互联接口之争：Virtio 还是 SR-IOV（两路线区别+性能对比）— https://community.aijishu.com/a/1060000000228117 （落盘 aijishu-virtio-vs-sriov-228117.html）
- 龙蜥 virtio 趋势+云豹解读 — https://xie.infoq.cn/article/b420dbaeb67a60d3beaa133b8 （正文抓取为空，无可用文本）

## 最终判定
**第 4 档：命中比例 < 60%**

判定依据：
- 云豹智能公开披露的 virtio 卸载主线是 **vDPA（vhost Data Path Acceleration）**——virtio 后端硬化在 DPU 上、数据面由硬件直接服务 Guest virtio 队列（虚拟队列映射到硬件队列）、控制面在软件，并据此实现热迁移。这是一种与本专利**不同的架构路线**。
- 本专利权 1/权 13 的核心结构限定是"**半虚拟化 FE/BE + SR-IOV VF 直通的混合架构**，由『BE 绑定一个空闲 VF 软件实例』桥接，并由该 Host 内 VF 软件实例经 BE 导出 API 取 DMA 地址、写入对应 VF 设备的存储单元"（F5/F7，及配套 F2/F8/F9）。在 vDPA 公开模型中，Guest virtio ring 直接由硬件队列服务，**不存在** Host 侧"BE 绑定空闲 VF 软件实例 + VF 软件实例经导出 API 中转 DMA 地址"这一桥接层——F5、F7 这两条最关键限定缺乏对应结构（属针对该候选的正向事实，非"未提及"）。
- 但本案不判第 5 档（已排除）：(a) F5/F7 缺失是基于"vDPA 公开架构描述"的正向推断，而非云豹官方明确声明"不实现该结构"的反向证据；(b) 云豹同时支持 SR-IOV / PF-VF 热插拔，且未公开 vDPA 数据面 DMA 地址下发的内部实现细节，F2/F6/F9 等多条属"公开资料不足"；(c) 全部证据均 ≥2014，时间窗合规，不满足第 5 档三条硬门槛中任一条（无真反向声明、证据非全部 <2014、且仍属同一 I/O 虚拟化抽象层）。
- 综合：仅 F4 较确定命中（且属 virtio 通用特征），F1/F3/F8 部分相关但不完整，F5/F7 两条核心限定不满足，F2/F6/F9 资料不足。可确认命中显著 < 60% → 第 4 档。

## 升级路径（3-4 档）
- 获取云豹智能 2014 年后自有专利或技术白皮书，逐字核实其 DPU 上 virtio 数据面 DMA 地址建立路径：若内部仍保留"Host 侧软件实体绑定一个 VF 资源、经后端导出接口取 GPA/HPA 并下发到硬件接收/发送队列"的等同结构，则 F5/F7 可能由"不满足"上修为"等同命中"，整体或升至第 3 档。
- 核实其某些产品形态是否在 SR-IOV VF 直通之上叠加半虚拟化 FE/BE（即非纯 vDPA 而是混合直通）。若存在该形态，则 F1/F2/F5 同时坐实，可触发更高档复核。
- 抓取云豹热迁移技术细节：本专利 FE/BE 软件层正是为兼容性/热迁移而设；若其热迁移实现依赖 Host 侧 VF 软件实例与 BE 的解耦接口，可佐证 F7/F9。

## 总结一句话
云豹智能 virtio 卸载走 vDPA 路线（数据面硬件直通、无"BE 绑定空闲 VF 软件实例"中转层），核心限定 F5/F7 缺乏对应结构、其余多条公开资料不足，落第 4 档。
