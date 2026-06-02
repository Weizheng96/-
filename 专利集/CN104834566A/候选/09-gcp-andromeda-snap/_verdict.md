# 09-gcp-andromeda-snap verdict

## 候选基本信息
- 名称：Google Andromeda 虚拟网络 / Snap 用户态网络栈
- 组织：Google Cloud
- 类型：产品
- 初判命中 F#：F1,F2,F3
- 专利公开日：2015-08-12（Snap 公开材料 SOSP 2019，**晚于公开日 → 时间合规**）

## 检索粗筛留痕
- Q1 WebSearch：`Google Snap userspace networking engine CPU core scaling dynamic NSDI` → 命中 Snap SOSP 2019：dynamic scaling of CPU resources、pluggable engine、kernel/userspace CPU scheduler co-design。
- Q2 WebSearch：`Snap engine load balancing dynamic scaling compacting cores spreading engines reassign Pony Express` → 命中 Spreading / Compacting 两调度模式，"periodic polling of engine queuing delays to detect load imbalance"。
- 粗筛结论：强信号，进入 Phase 2 深抓。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测转发线程/引擎状态） | 等同 | "it relies on periodic polling of engine queueing delays to detect load imbalance"；"The algorithm estimates the queueing load of engines by directly accessing concurrently-updated shared variables in memory" | snap-sosp2019.pdf (SOSP'19) | Snap 周期性轮询/估计各 engine 排队时延=负载状态。专利对象是 vSwitch"转发处理线程"，Snap 对象是"engine（用户态网络栈数据面单元）"——抽象层不同，故记等同 |
| F2（满足预设触发条件） | 等同 | "the CPU-bottlenecked queueing delay of all engines … stays below some configured latency SLO. Then … a rebalancing function periodically performs one of several actions. One action is to respond to queue build-up by scaling out an engine … Another action is to detect excess capacity and migrate back an engine that has sufficiently low load" | snap-sosp2019.pdf | configured latency SLO / queue build-up / excess capacity = 预设调整触发条件；对应权 3/11"负载均衡度/资源额度"择一 |
| F3（调整线程所服务的交换端口） | 公开资料不足（部分等同信号） | "scaling out an engine to another thread (awoken if necessary)"；"migrate back an engine"；"engine compaction and engine swaps to effectively bin-pack work" | snap-sosp2019.pdf | Snap 迁移的是**整个 engine 在 thread/core 间**（engine↔core 映射），专利 F3 是**调整某转发线程所服务的"交换端口"**（port↔thread 映射）。是否同一抽象层无法从公开论文确证——见判定依据 |
| F4（K 正整数 / 多核） | 等同 | "supports real-time scheduling with dynamic scaling of CPU resources"；"collapses work onto as few cores as possible"；"scales to many more cores" | snap-sosp2019.pdf | 多核动态伸缩，K≥1 满足 |

## 已检查文档清单
- Snap: a Microkernel Approach to Host Networking (SOSP 2019) — https://courses.grainger.illinois.edu/cs598hpn/fa2020/papers/snap.pdf（本地 snap-sosp2019.pdf）
- the morning paper: Snap networking 摘要 — https://blog.acolyer.org/2019/11/11/snap-networking/
- Google Research 论文页 — https://research.google/pubs/snap-a-microkernel-approach-to-host-networking/

## 最终判定
**第 3 档：≥60% F 命中且无反向证据**

判定依据（1-3句）：Snap 论文明确披露"周期性检测各 engine 排队负载（F1）→ 队列堆积 / SLO 越界等条件触发（F2）→ 重平衡函数把 engine 在线程/CPU 核间 scale-out / migrate / compaction / swap（F3 同手段同功能同效果信号）→ 多核动态伸缩（F4）"，整体机制与权 1"检测线程状态→满足触发条件→运行时重分配"高度同构，且无任何反向证据（论文为正向披露动态迁移）。关键差异在 F3 的抽象层与重分配对象：专利核心是"转发线程↔交换端口（port/rxq）映射"再分配，Snap 是"engine↔CPU 核/线程"再分配——Snap 调度的是承载数据包处理的 engine 整体迁核，而非"某线程改服务哪个端口"；二者可能构成等同（同为按负载在多核间动态重分配数据包处理工作），也可能因映射对象不同被认定为不同手段。公开论文未细化到"端口/队列↔线程"粒度，故 F3 记"公开资料不足"，整体落第 3 档而非第 2 档。

## 升级路径（第3-4档填）
- 取证 Snap engine 是否随负载重映射其服务的 NIC steering/queue（端口侧）：论文提及"utilizing NIC steering functionality as needed"——需抓取 Snap 后续材料确认是否做"端口/队列↔engine"层级再分配（而非仅 engine↔core），若确证可升至第 2 档。
- 抓取 Andromeda（NSDI 2018, "Andromeda: Performance, Isolation, and Velocity at Scale in Cloud Network Virtualization"）核实其 vSwitch/数据面是否有 per-port/per-flow→转发线程的运行时再分配——Andromeda 才是直接对标"vSwitch 多核转发"的产品层。
- 字面命中需 Google 内部实现细节（端口队列↔转发线程映射的动态调整），公开渠道难得。

## 总结一句话
Snap 周期性检测 engine 排队负载并在多核间动态 scale-out/migrate/compaction 数据包处理引擎，机制与本专利"检测线程状态→触发→重分配"高度同构且时间合规，但重分配对象是 engine↔CPU 核而非专利的端口↔转发线程，抽象层差异令 F3 仅达等同信号，落第 3 档。
