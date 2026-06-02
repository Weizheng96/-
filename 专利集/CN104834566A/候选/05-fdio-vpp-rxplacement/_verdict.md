# 05-fdio-vpp-rxplacement verdict

## 候选基本信息
- 名称：FD.io VPP（worker 线程 + `rx-placement`） / 组织：FD.io / Linux Foundation（思科发起） / 类型：产品 / 初判命中 F#：F1,F3,F4 / 专利公开日：2015-08-12

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测转发线程状态属性） | 公开资料不足 | 未找到"VPP 持续检测各 worker 线程负载状态属性并据此驱动端口重分配"的正向证据。`show interface rx-placement` 仅显示当前 queue↔thread 映射快照（静态查看），非以"触发再分配"为目的的状态检测 | https://s3-docs.fd.io/vpp/23.10/developer/corearchitecture/multi_thread.html | VPP 提供监控/统计，但未把"检测线程状态属性"与"自动调整端口"形成专利所述闭环 |
| F2（满足预设触发条件自动调整） | 反向 | "On startup, the VPP platform assigns interfaces (or interface, queue pairs if RSS is used) to different worker threads in round robin fashion." + `set interface rx-placement <interface> [queue <n>] [worker <n> \| main]` "This command is used to assign a given interface, and optionally a given queue, to a different thread." 官方文档明确无 automatic load-based rebalancing | https://s3-docs.fd.io/vpp/23.10/developer/corearchitecture/multi_thread.html ; https://s3-docs.fd.io/vpp/23.10/cli-reference/clis/clicmd_src_vnet.html | 启动时 round-robin 固定 + 之后仅靠管理员手动 CLI 改放置；无"检测到满足预设调整触发条件"的自动触发器 |
| F3（调整至少 1 个线程所服务的交换端口） | 等同（但仅手动触发） | `set interface placement TenGigabitEthernet2/0/1 queue 1 thread 1` — 把某 queue 从一个 thread 改派到另一 thread | https://s3-docs.fd.io/vpp/23.10/developer/corearchitecture/multi_thread.html | rxq↔worker 重映射动作本身存在且等同于"调整线程所服务的端口"，但由管理员手动发起，非自动。注意 VPP "worker handoff" 是按包 hash 流量交接，非 rxq↔thread 重放置，不等同 F3 |
| F4（K 为正整数，多线程多端口） | 字面 | "each worker has a dedicated RxQ on each interface tested"；多 worker 线程绑核（PMD per-core），K 个 worker 对应 K 个 CPU | https://csit.fd.io/cdocs/methodology/overview/per_thread_resources/ | 多核 worker + 每 worker 专属 RxQ，满足 K 为正整数、线程↔CPU 一一对应的多核形态 |

## 已检查文档清单
- VPP 23.10 Multi-threading 官方文档（启动 round-robin、手动 `set interface placement`、无自动 rebalance）— https://s3-docs.fd.io/vpp/23.10/developer/corearchitecture/multi_thread.html
- VPP `set interface rx-placement` CLI 参考（纯手动 operator 命令）— https://s3-docs.fd.io/vpp/23.10/cli-reference/clis/clicmd_src_vnet.html
- CSIT Per Thread Resources（每 worker 专属 RxQ、多核绑核）— https://csit.fd.io/cdocs/methodology/overview/per_thread_resources/
- vpp-dev 邮件列表 TX Queue Placement（静态映射、当时无 dynamic rebalancing）— https://lists.fd.io/g/vpp-dev/topic/tx_queue_placement/82088483
- VPP-1734 Worker handoff Queue congestion（handoff = 按包 hash 流量交接，非 rxq 重放置）— https://jira.fd.io/browse/VPP-1734
- VPP Multi-thread wiki（WebFetch 403 / curl 取回 JS 壳；内容由官方文档覆盖）— https://wiki.fd.io/view/VPP/Using_VPP_In_A_Multi-thread_Model

## 最终判定
**第 4 档：部分命中（<60% 或缺关键特征）**

判定依据（1-3句）：本专利发明核心是"检测转发线程状态属性 → 满足预设触发条件 → 自动调整线程所服务的端口"这一**自动闭环**（F1+F2+F3 联动），其中 F2 的"自动按负载触发"是与背景技术"固定绑定"对立的判定关键。VPP 虽具备 worker 线程绑核（F4 字面）与 rxq↔thread 重映射能力（F3 等同动作），但官方文档明确：放置在启动时 round-robin 固定、之后只能由管理员**手动** `set interface rx-placement` 改派，**无任何自动按负载触发的重分配机制**（F2 反向），F1 的"为触发再分配而检测线程状态"亦无正向证据。缺失发明核心的自动触发链条，仅落第 4 档。

## 升级路径（第3-4档填）
- 检索 VPP 是否有第三方插件 / 厂商发行版（如 vendor NFVI / DPU 卸载 vSwitch）在 VPP 之上叠加"按 worker 负载自动 rebalance rxq"的控制器组件；若存在闭环自动触发，该叠加组件可升至第 2-3 档（VPP 本体仍为第 4 档）。
- 核验后续 VPP 版本（>23.10）是否落地了 2021 邮件列表提到的"计划中的 dynamic rebalancing"；若已实现自动触发，则 F2 由反向转为命中，整体可升档。

## 总结一句话
VPP 具备 worker 绑核与手动 rxq↔thread 重放置，但启动后只能管理员手动改派、无自动按负载触发的重分配机制（F2 反向），缺发明核心自动闭环，落第 4 档。
