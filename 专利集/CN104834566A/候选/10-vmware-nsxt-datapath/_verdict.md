# 10-vmware-nsxt-datapath verdict

## 候选基本信息
- 名称：VMware NSX-T / vSphere DPDK datapath（Edge / EDP）
- 组织：VMware (Broadcom)
- 类型：产品
- 初判命中 F#：F1,F2,F3
- 专利公开日：2015-08-12

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测转发线程状态属性） | 等同 | "The method collects utilization data from at least the cores allocated to the set of data message processing processes." | https://patents.google.com/patent/US11599395B2/en | VMware 自有专利：检测 datapath 数据消息处理核（=转发线程）的利用率，对应"检测 K 个转发处理线程的状态属性"。产品文档侧 EDP/ENS 为 DPDK poll-mode 多核转发面 |
| F2（满足预设调整触发条件） | 等同 | "Based on the received utilization data, the method determines that one of the sets of cores is being underutilized (e.g., less than 50% aggregate utilization)." | https://patents.google.com/patent/US11599395B2/en | 利用率与预设阈值（<50%）比较作为触发判据，对应"状态属性满足预设调整触发条件"（权 3/11 的"负载均衡度低于预设"择一子类型） |
| F3（调整线程所服务的交换端口） | 等同 | "updates a load balancing operation to distribute data messages among a set of queues associated with the cores allocated to the set of data message processing processes in the identified new allocation and reallocates the cores based on the identified new allocation" | https://patents.google.com/patent/US11599395B2/en | 运行时重分配核 + 把数据消息在与核关联的队列间重分发 = 调整转发线程↔队列/端口映射（动态再分配，非运行前固定绑定） |
| F4（K 为正整数，多线程多核） | 等同 | "A method for updating a core allocation among a plurality of threads of a gateway datapath that executes on a gateway computing device comprising a plurality of cores" | https://patents.google.com/patent/US11599395B2/en | 多核多线程 gateway datapath，对应 K≥1 整数、线程绑核（PMD per-core）形态 |

## 已检查文档清单
- VMware 博客《Accelerated Data Plane Performance Using EDP in NUMA Architecture》（2018-10-30）— 仅初始 NUMA 对齐，未公开按负载运行时再分配 — https://blogs.vmware.com/networkvirtualization/2018/10/accelerated-data-plane-performance-using-enhanced-data-path-in-numa-architecture.html/
- Broadcom TechDocs《Enhanced Data Path》（NSX 4.0，更新 2026-01-21）— Load Balanced Source teaming + NUMA aware，未明示 CPU 负载触发的动态队列再分配 — https://techdocs.broadcom.com/us/en/vmware-cis/nsx/vmware-nsx/4-0/installation-guide/transport-zones-and-transport-nodes/enhanced-datapath-1.html
- NVIDIA Docs《Enhanced Network Stack (ENS)》（2023-08-31）— 逻辑核/NUMA 于初始 N-VDS 配置时选定（静态） — https://docs.nvidia.com/networking/display/VMwareUMv417711/Enhanced+Network+Stack+(ENS)
- **VMware 专利 US11599395B2《Dynamic Core Allocation》**（assignee VMware LLC；申请 2020-02-19；授权 2023-03-07）— F1-F4 完整链路实现证据 — https://patents.google.com/patent/US11599395B2/en
- 旁证 US9571426B2《Traffic and load aware dynamic queue management》（503 未抓取，仅搜索摘要） — https://patents.google.com/patent/US9571426B2/en

## 最终判定

**第 2 档：全命中（含等同）**

判定依据（1-3句）：VMware 公开产品文档（EDP/ENS）止步于"DPDK 多核 poll-mode 转发面 + NUMA 亲和性 + 初始核分配（含 on demand）"，单凭产品文档对 F2/F3 的"按负载自动触发的运行时再分配"为公开资料不足；但 VMware 自有专利 US11599395B2 明确公开了"检测核利用率（F1）→ 阈值条件 underutilized（F2）→ 运行时重分配核并在队列间重分发数据消息（F3）→ 多核多线程（F4）"的完整链路，与本专利发明核心实质等同，且实现/公开时间（2020 申请 / 2023 授权）均晚于专利公开日 2015-08-12。各 F# 均为等同（非逐字），故落第 2 档。未发现任何反向证据（无"不支持/手动 only"明示拒绝）。

## 升级路径（第3-4档填）
（本档为第 2 档，无需升级；如需固化为第 1 档字面命中，可补取 VMware 产品文档/源码中将 US11599395 动态核分配特性默认启用于 NSX Edge EDP 出货版本的直接证据，将"实现路径专利"升级为"出货产品逐字特征"。）

## 总结一句话
VMware NSX-T/EDP DPDK 转发面公开文档不足以单独定字面，但其自有专利 US11599395B2 完整公开"检测核负载→阈值触发→运行时重分配核与队列"链路，与本专利核心等同且晚于公开日，落第 2 档（全命中含等同）。
