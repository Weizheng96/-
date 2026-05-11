# 候选：VMware vSphere 8 + Distributed Services Engine (DSE) + NSX-T

## 候选标识
- candidate_slug: `07-vmware-vsphere8-dse`
- 主体类型：A. vSwitch 软件方（vDS）+ E. SDN 控制器（NSX-T）
- 适用独立权：权 1, 11, 23, 33, 36
- 命中场景：场景 1 / 3 / 4 / 5

## §A 主流来源摘要（19 类源 — 关键证据）

### §A.4 使用手册 / 技术文档（命中 — 反向证据）

| # | 源 | URL | 关键引文 |
| --- | --- | --- | --- |
| 1 | Broadcom TechDocs — vSphere 8 DSE Install / Network Offloads | https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/introducing-vmware-vsphere-distributed-services-engine-and-networking-acceleration-by-using-dpus-install.html | **HA mode**: "If dual DPUs are connected to the same network switch at the same time, **only one of them processes data packets**. The other DPU is on stand-by mode. However, shadow switches and ports are created on the stand-by DPU." → 仅 active/standby，非 N 张并行 |
| 2 | Broadcom TechDocs — Network Offloads Compatibility | https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/basic-networking-with-vnetwork-distributed-switches/network-offloads-capability.html | **Non-HA mode**: "each DPU is allowed to be consumed by a separate offloaded vDS. This mode allows both the DPUs to be consumed for active networking datapath offload" → 两 DPU 服务**不同 vDS、不同 VM、不同流量**；非"同一精确流表 N 份相同副本" |
| 3 | VCF Blog — Dual DPU Support in VCF 5.2 | https://blogs.vmware.com/cloud-foundation/2024/07/26/announcing-dual-dpu-support-in-vmware-cloud-foundation-5-2/ | 2024-07-26 — Performance mode："Both DPUs operate independently, providing maximum throughput" → 独立运行，非同步 |

### §A.6 联合白皮书 / RDG（命中 — 单 DPU 架构）

- AMD vDSE 白皮书：https://www.amd.com/content/dam/amd/en/documents/pensando-business-docs/white-papers/vdse-with-amd-white-paper.pdf
- NVIDIA RDG for DSE on BlueField-2：https://docs.nvidia.com/networking/display/public/SOL/RDG+for+vSphere+Distributed+Services+Engine+(Project+Monterey)+deployment+over+NVIDIA+BlueField-2+DPU
- Lenovo Press lp1768：https://lenovopress.lenovo.com/lp1768-maximize-security-and-performance-with-lenovo-dpu-enabled-servers
- Dell InfoHub vSphere 8 + DPU：https://infohub.delltechnologies.com/l/dpus-in-the-new-vsphere-8-0-and-16th-generation-dell-poweredge-servers/vmware-vsphere-8-0-distributed-services-engine-and-data-processing-units-dpu/
- 全部描述 1 DPU per host 或 dual-DPU HA Active/Standby——**0 命中** "synchronous duplicate flow programming"

### §A.2 / §A.3 / §A.5 / §A.7-19

- §A.3 宣传材料：blogs.vmware.com / Cormac Hogan 2022-09 DSE preview 全部描述单 DPU 加速 NSX 数据面
- §A.5 标准 / 测试规范：不适用（VMware 闭源）
- §A.7 上游开源贡献者：VMware contribute 给 OVS 较少，主要走自家 vDS；不适用
- §A.10-19：0 命中（VMware Explore 2023/2024/2025 / VMUG 录像 0 命中"cross-DPU sync flow"）

## §B 本地化证据归档

`_sources.md` 见本目录；URL 全部 verifiable。

## §C 子 agent 复核

由 1 个 general-purpose 子 agent（agent ID a71acf4178d4db64a，2026-05-11）完成深度调研；主 agent 复核 claim 1 + claim 11 + claim 23 verbatim 后认可。

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 33 / 36 | **已排除（第 5 档）** | 等同三步法：F4 同手段 / 同功能 / 同效果 / 显而易见 4 行——HA 模式只单卡转发；Non-HA 模式两卡不同 vSwitch / 不同 VM——两种模式均与 F4 "同一精确流表同步到 N 张 NIC" 在**同手段** 与 **同效果** 上均不成立。反向证据 vs 限定语：上表引文 1 "only one of them processes data packets" 属真反向证据 ("Y supports only Z (not X)")；引文 2 "each DPU is allowed to be consumed by a **separate** offloaded vDS" 同样属真反向。法律状态：Active；R-STANDARD：不适用；§5.0 豁免：满足 (a) 真反向证据；§A.7 patent pledge：未检索到 Huawei 对 VMware 的专利让渡承诺 | **已排除（dual-DPU 模式架构层面与 F4 不符）** |

### F# 投票汇总

- F1（M ≥ 2 + N ≥ 2）：dual-DPU 形态下 N=2 命中；single-DPU 形态下 N=1 不命中
- F2（LACP 聚合）：vDS 支持 Enhanced LACP，N ≥ 2 物理端口聚合（在单 DPU 内或跨 DPU）——字面/等同命中
- F3（N→1 二层映射）：vDS LAG 把多个 vmnic 聚合为单一 uplink——单层聚合，与本专利"两层（NIC 内 LACP + vSwitch 内 N→1 跨 NIC）"不同；**部分等同**但缺少"二层"特征
- F4（同步卸载 N 份相同）：**真反向证据**——HA 模式 standby DPU 不转发；Non-HA 模式两 DPU 服务不同 vDS / 不同流量。两种模式都**不**做"同一流表同步到 N 张 DPU 并行转发"

→ F4 真反向 → 落第 5 档已排除

### 后置调整记录（按 7 条）

1. 等同三步法：F4 不通过等同（同手段/同效果不成立 — Active/Standby vs N-active concurrent）
2. 反向证据 vs 限定语：HA "only one... processes" 属真反向 ("Y supports only Z")
3. 法律状态：Active，无降级
4. 现有技术 caveat：vSphere 8 GA 2022-10，DSE 概念更早（Project Monterey 2020）；可能与本专利新颖点存在现有技术博弈，但 **F4 的"同步卸载到 N 份相同"** 仍是本专利新点。Project Monterey 早期资料未声明 F4 → 不构成现有技术覆盖
5. R-STANDARD 转移：不适用
6. §5.0 豁免：满足 (a) 真反向证据
7. Patent pledge：未检索到

### 最终 verdict

**已排除**：VMware 在 dual-DPU 形态下采用 HA Active/Standby 或 Non-HA Isolated 双 vDS 两种模式——**两种模式都与 F4 "同一精确流表同步到 N 张 NIC 并行转发"在架构层面不一致**，构成 F4 真反向证据。

## 总结一句话

VMware vSphere 8 dual-DPU 严格 Active/Standby (HA) 或 vDS 隔离 (Non-HA) — F4 真反向证据，**落第 5 档已排除**。
