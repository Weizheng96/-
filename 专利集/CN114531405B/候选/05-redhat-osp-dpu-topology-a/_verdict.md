# 候选：Red Hat OpenStack Platform (RHOSP) / OpenShift on DPU — Topology-A（默认配置）

## 候选标识
- candidate_slug: `05-redhat-osp-dpu-topology-a`
- 主体类型：A. vSwitch 软件方（商业发行版）+ E. SDN 控制器（OpenStack Neutron + OVN-K8s）
- 适用独立权：权 1, 11, 23, 36
- 命中场景：场景 2 / 3 / 5
- 拓扑变体：**topology-A** = RHOSP 17.1 + OVS hw-offload 默认双端口 Mellanox + Linux bond active-backup（vendor 实际推荐配置）

## §A 主流来源摘要

### §A.4 使用手册 / 技术文档（命中 — 真反向证据）

| # | 源 | URL | 关键引文 |
| --- | --- | --- | --- |
| 1 | RHOSP 17.1 — Configuring OVS TC-flower hardware offload (Ch. 8) | https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/config-ovs-hwol_rhosp-nfv | 唯一推荐的 hw-offload bond 例子使用 **`mode=active-backup miimon=100`**——非 LACP；"You can bond two ports of a Mellanox NIC by using Linux bond" → 是**单卡两端口** bond，非 N ≥ 2 张 NIC |
| 2 | RHOSP 16.2 — Network Interface Bonding (Ch. 12) | https://docs.redhat.com/en/documentation/red_hat_openstack_platform/16.2/html/advanced_overcloud_customization/assembly_network-interface-bonding | "**balance-tcp … is known to cause packet loss and should not be used in BondInterfaceOvsOptions**"；"The OVS/OVS-DPDK balance-tcp mode is **available as a technology preview only**" |
| 3 | OpenShift on DPU — DPU Operator | https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking_operators/dpu-operator | "labeling all compute nodes assuming **each node has an attached DPU**" → 1 DPU per host 模型 |
| 4 | Red Hat Developer — DPU-enabled networking with OpenShift and NVIDIA DPF (2025-03-20) | https://developers.redhat.com/articles/2025/03/20/dpu-enabled-networking-openshift-and-nvidia-dpf | "two physical servers, each equipped with **an** NVIDIA BlueField-3 DPU installed in a PCIe slot" — 单 DPU per host |

### §A.3 宣传材料

- Red Hat 2025-11-24 blog "Unifying multivendor DPUs in Red Hat OpenShift"：每节点装一个 DPU（不同节点用不同 vendor），**未涉及单节点多 DPU**
- Red Hat 2025-06-19 blog "Cloud-native enablement of DPUs"：0 命中"multi-DPU per server"

### §A.2 学术 / §A.5 标准 / §A.6 联合 / §A.7 上游归因

- §A.2 Red Hat 主导 OVS / OVN 上游 contribution，但 contribution 重点是 OVS-TC offload + OVN logical-flow，不涉及 N→1 跨 NIC 二层映射
- §A.5 不适用
- §A.6 Red Hat × NVIDIA / AMD-Pensando 联合 reference 全部描述单 DPU per host 拓扑
- §A.7 在 OVS / Linux netdev 上 @redhat.com 域贡献者大量，但未检索到"跨 NIC 第二层映射 + 同步流表卸载"feature 的 Red Hat 上游 patch
- §A.8-19：0 命中

## §C 子 agent 复核

由 1 个 general-purpose 子 agent（agent ID a449c6be92a424a26，2026-05-11）独立完成；主 agent 复核认可。

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 36 | **已排除（第 5 档）** | 等同三步法：active-backup 与 LACP 同步聚合在**同手段** 与 **同效果**上均不成立——active-backup 仅单 leg 转发，"steers flow to the active leg only"；反向证据 vs 限定语：引文 1 "active-backup miimon=100" 是 vendor 推荐配置（非 LACP）；引文 2 "balance-tcp ... should not be used" 属真反向证据 ("Y supports only Z (not X)" — Y=Red Hat, X=balance-tcp/LACP, Z=active-backup) | **已排除（topology-A 默认配置 — F2 真反向证据 + F4 公开资料 0 命中）** |

### F# 投票汇总（topology-A）

- F1：单 DPU per host + 单 NIC 两端口 → N=1 NIC，不命中
- F2：active-backup 而非 LACP → **真反向证据**
- F3：单层 bond，无 N→1 二层映射 → 不命中
- F4：active-backup → 流量只走 active leg；无"同步卸载 N 份相同" → 不命中

### 后置调整记录（按 7 条）

1. 等同三步法：F2 active-backup vs LACP——**同手段** 不成立（无 LACP 协商帧、无 hash-based load balance）；**同效果** 不成立（仅单 leg 转发 vs 多 leg 并行）→ 等同不通过
2. 反向证据 vs 限定语：引文 2 "balance-tcp should not be used" 是 Red Hat 主动建议**避开**——属真反向证据
3. 法律状态：Active，无降级
4. 现有技术 caveat：active-backup bonding 是 Linux kernel mainline 长期能力，但与本专利 F2/F4 不冲突
5. R-STANDARD 转移：不适用
6. §5.0 豁免：满足 (a) 真反向证据
7. Patent pledge：Red Hat OPN（Open Patent Non-Assertion Pledge，针对 Red Hat 自身专利）；Huawei 未对 RHOSP 做 patent pledge → 不构成调整

### 最终 verdict

**已排除（topology-A 默认配置）**：Red Hat 唯一公开推荐的 OVS hw-offload bond 配置使用 **active-backup**（非 LACP）；balance-tcp/LACP 被 Red Hat 明确建议**不使用**；OpenShift on DPU 是 1 DPU per host 模型——三处与 F1/F2/F4 在架构层面对立。

## 总结一句话

Red Hat 推荐 OVS hw-offload bond 用 active-backup（非 LACP），balance-tcp 被 Red Hat 主动建议不使用——F2 真反向证据，**落第 5 档已排除**。
