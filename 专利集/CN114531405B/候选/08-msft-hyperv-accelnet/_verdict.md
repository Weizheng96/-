# 候选：Microsoft Hyper-V SET + Azure AccelNet + Azure Boost

## 候选标识
- candidate_slug: `08-msft-hyperv-accelnet`
- 主体类型：A. vSwitch 软件方 + C. 公有云 CSP（Azure）
- 适用独立权：权 1, 11, 23, 33, 34, 35, 36
- 命中场景：场景 1（公有云 IaaS 数据面）

## §A 主流来源摘要（19 类源 — 关键命中）

### §A.4 使用手册 / 技术文档（命中 — 反向证据）

| # | 源 | URL | 发布日期 | 关键引文 |
| --- | --- | --- | --- | --- |
| 1 | Microsoft Learn — Host network requirements for Azure Local | https://learn.microsoft.com/en-us/azure-local/concepts/host-network-requirements | ms.date 2026-01-15 | **"SET supports only switch-independent configuration by using either Dynamic or Hyper-V Port load-balancing algorithms."** **"LACP or static LAG should not be configured on the physical switch ports."** |
| 2 | Microsoft Learn — Azure Network Adapter (MANA) overview | https://learn.microsoft.com/en-us/azure/virtual-network/accelerated-networking-mana-overview | ms.date 2025-09-04 | "VMs run on hardware with both Mellanox and MANA NICs, so existing mlx4 and mlx5 support still needs to be present." — 双 NIC 但用途是 driver transition / parity 而非聚合卸载同步 |
| 3 | Microsoft Q&A — Hyper-V WS2022 LACP | https://learn.microsoft.com/en-us/answers/questions/2068172/ | 2024 | "attempting to use Set-VMSwitchTeam with -Teamingmode LACP results in an error" / "Starting from Windows Server 2022, binding a vSwitch to an LBFO team will no longer be supported" |

### §A.2 学术 / 研究阵地（命中 — 仅显示单 NIC 架构）

- **NSDI 2018** — Firestone et al. "Azure Accelerated Networking: SmartNICs in the Public Cloud" — https://www.usenix.org/conference/nsdi18/presentation/firestone — AccelNet 架构：**单 SmartNIC + FPGA "bump-in-the-wire"**；failover 仅 software path（NetVSC PMD），不是跨 NIC 硬件 sync
  - **时间档**：在专利申请日（2020-10-31）之前——按 §A.9 / 9a，可作为现有技术抗辩潜在依据，但**与本专利新颖点不冲突**（专利新颖点是跨 NIC 二层映射 + 同步卸载，AccelNet 是单卡 fast-path 卸载）。Not used as侵权 evidence；仅作为 architectural baseline。

### §A.3 宣传材料（命中 — 单卡架构延续）

- Tech Community Ignite 2025 — Azure Boost 2nd gen — https://techcommunity.microsoft.com/blog/AzureInfrastructureBlog/powering-modern-cloud-workloads-with-azure-boost-ignite-2025/4470793 — **400 Gbps 单 NIC 吞吐**；单卡 scale-up，**不是 N 张卡 sync**

### §A.1 / 5 / 6 / 7-19 类源（0 命中或不适用）

- §A.1 专利墙：MS Azure 在 H04L45/76 同分类下专利数量大，但未检索到与"多 NIC 跨卡同步流表卸载"字面重合 ≥ 60% 的专利
- §A.5 标准 / 测试规范：不适用（Azure 闭源，非标准合规）
- §A.6 联合白皮书：Azure × Red Hat / SUSE / Cisco 等联合架构主要描述 AccelNet 单卡 + VFP 卸载，未见"跨 N 张 SmartNIC 同步"
- §A.7 上游开源贡献者归因：Microsoft 在 OVS / Linux netdev 上有 contributor，但 contribution 重点是 mlx5 / VFP；与本专利 F3 无关
- §A.8-19：0 命中或不适用，无强反向证据增强

## §B 本地化证据归档

- `_sources.md`：见本目录（含 Firestone NSDI 2018 PDF、MANA overview 网页 markdown、Azure Local SET requirements 网页 markdown、Ignite 2025 Azure Boost blog markdown）
- 本批次因证据链清晰直接，未做大规模本地归档；URL 全部可点击；如 Step 6 需要 verbatim 引文，按 _sources.md 中 URL 重新抓取即可

## §C 子 agent 复核

本候选由 1 个 general-purpose 子 agent 独立完成深度调研（agent ID a99e2ba05bfeecdeb，2026-05-11 报告）；主 agent 复核 claim 1 + 11 + 23 全文 verbatim 后认可。

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23（vSwitch / 物理机方法 / 装置） | **已排除（第 5 档）** | 等同三步法：未触发（已有真反向证据，不需进入等同分析）；反向证据 vs 限定语：上表 §A.4 引文 1 + 引文 3 属真反向证据"Y supports only Z (not X)"；专利法律状态：Active；R-STANDARD 转移：不适用；§5.0 豁免：满足 (a) "至少一条 F# 在所有归档证据中命中真反向引文模式" | **已排除（F2 真反向证据 + F3/F4 公开资料 0 命中）** |
| 权 33 / 34（整机型物理机） | **已排除（第 5 档）** | 整机权依赖方法权；方法权已排除 | **已排除** |
| 权 35（芯片系统） | **已排除（第 5 档）** | Azure 不自研芯片，依赖 NVIDIA / 其他芯片厂；芯片权由其他候选承载 | **已排除（领域无关 — 主体不符）** |
| 权 36（计算机存储介质） | **已排除（第 5 档）** | 介质权依赖方法权；方法权已排除 | **已排除** |

### 状态机原始判定的来源

F1（M ≥ 2 + N ≥ 2）：
- AccelNet / Azure Boost：**单 SmartNIC 架构** → F1 不命中
- Hyper-V SET：可绑 ≤ 8 个 NIC 到一个 vSwitch → F1（N ≥ 2）等同命中

F2（LACP 聚合）：
- SET：**真反向证据** — "switch-independent only" 明确排除 LACP；LBFO（曾支持 LACP）自 WS2022 起被禁止绑定 vSwitch
- → F2 真反向命中

F3（N→1 二层映射）：
- SET 用 switch-independent load-balance（Hyper-V Port / Dynamic algorithm），不是"N 个逻辑端口映射到一个 first port"
- AccelNet：单卡，无 N→1 映射
- → F3 公开资料不足（无字面命中、无等同命中、亦无真反向；但因 F2 已真反向，F3 状态由 F2 决定）

F4（同步卸载 N 份相同）：
- AccelNet GFT 卸载到单卡；flow generation ID per-card
- SET：checksum offload 是 per-NIC capability negotiation，不是同步流表 mirror
- → F4 公开资料不足（同上，由 F2 决定整体状态）

### 后置调整记录（按 7 条逐条核查）

1. **等同三步法复核**：未触发（F2 已真反向，无需进入等同）
2. **反向证据 vs 限定语区分**：F2 的"SET only switch-independent"明确属于"Y supports only Z (not X)"模式——真反向证据
3. **专利法律状态降级**：Active，无降级
4. **现有技术 caveat**：AccelNet NSDI 2018 paper 在专利申请日前，但与本专利新颖点（跨 NIC 二层映射 + 同步卸载）正交，不构成现有技术覆盖 ≥ 60%
5. **R-STANDARD 转移**：不适用
6. **§5.0 豁免**：满足 (a) 真反向证据
7. **Patent license / pledge / 专利池承诺**：未检索到 Huawei 对 Microsoft 的 patent grant / pledge / non-assert 公开承诺；F2/F3/F4 已确定为非命中，本项不构成进一步调整

### 最终 verdict

**已排除（架构层级 + 真反向证据双重支撑）**：
- F2 真反向证据（SET 明确排除 LACP）
- F3 / F4 公开资料 0 命中（Microsoft 公开文档中**不存在**跨 N 张 SmartNIC 同步流表卸载架构的描述）
- AccelNet / Azure Boost 是单卡 scale-up 架构（Ignite 2025 公布单卡 400 Gbps）

## 总结一句话

Microsoft AccelNet / Azure Boost / Hyper-V SET 在 F2 层有真反向证据（SET 明确排除 LACP）+ F3/F4 公开资料 0 命中，**落第 5 档已排除**。
