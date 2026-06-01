# 01-tech-nvidia-asap2-vflag verdict

## 候选基本信息
- 名称：ASAP² / SR-IOV VF-LAG OVS 硬件卸载（跨 bond/LAG 多端口下发到硬件 eSwitch）
- 组织：NVIDIA（Mellanox）
- 类型：技术
- 初判命中 F#：F1, F2, F3, F4, F5
- 专利公开（授权）日：2023-06-06

## 检索粗筛
- query 1 `NVIDIA ASAP2 VF-LAG OVS hardware offload bond` → 命中：ASAP² 把 OVS 数据面卸载到 ConnectX-5+ 网卡 eSwitch；VF-LAG "single bonded PF port"，bond "both physical functions of the NIC"。
- query 2 `NVIDIA VF-LAG offload LAG both physical ports of NIC e-switch single bonded PF port` → 再确认单卡双 PF 端口聚合 + LACP(mode=4) 支持。
- Phase 1 命中信号强 → 未剪枝，进入 Phase 2 深抓 2 篇 NVIDIA 官方 docs。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（多虚机+多网卡 N≥2） | 公开资料不足（架构层级不同） | "A single virtual function is backed by two physical bond ports." / "The two network interfaces from the NIC PFs are bounded in the hypervisor." | https://docs.nvidia.com/networking/display/public/SOL/QSG+for+High+Availability+with+NVIDIA+Enhanced+SR-IOV+with+Bonding+Support+(VF-LAG) | **关键分歧**：VF-LAG 聚合的是**单块网卡的两个物理端口/两个 PF**，不是 N≥2 块**独立网卡**。整数限定外推禁令：vendor 仅描述单卡(N=1)双端口，不得外推为字面命中 N≥2 块网卡。 |
| F2（N 逻辑端口聚合为第一端口） | 等同命中 | "The bonding creates a single bonded PF port." / "SR-IOV VF LAG ... offload them to the hardware e-switch." | https://docs.nvidia.com/networking/display/MLNXENv495100/OVS+Offload+Using+ASAP2+Direct | 把多个 uplink 聚合为单一逻辑 bond 口并卸载到 eSwitch——"聚合为一个端口"机制等同；但聚合对象是端口而非独立网卡。 |
| F3（LACP 形成逻辑端口） | 字面命中 | "Bond modes supported are: Active-Backup, Active-Active, LACP" / "BONDING_OPTS=\"mode=4 miimon=100 lacp_rate=1\"" | https://docs.nvidia.com/networking/display/MLNXENv495100/OVS+Offload+Using+ASAP2+Direct | LACP(mode=4) 显式支持；逻辑端口由 LACP 聚合形成，与 F3 一致。 |
| F4（卸载流表 miss 触发） | 公开资料不足 | "SR-IOV VF LAG allows the NIC's physical functions to get the rules that the OVS will try to offload to the bond net-device, and to offload them to the hardware e-switch." | https://docs.nvidia.com/networking/display/MLNXENv495100/OVS+Offload+Using+ASAP2+Direct | ASAP² 本质是 OVS first-packet/cache-miss 驱动卸载（标准 OVS 卸载语义），概念相容；但所抓文档未 verbatim 描述"miss 触发"措辞，记公开资料不足。 |
| F5（精确流表卸载至全部 N 网卡） | 公开资料不足（架构层级不同） | "A single virtual function is backed by two physical bond ports."（无任何"同步卸载至多块独立网卡"描述） | 同 F1 URL | F5 核心限定是把同一精确流表**同步卸载到全部 N 块独立网卡**以消除单网卡单点故障；VF-LAG 卸载到单卡 eSwitch 的双端口，单卡故障整 bond 即失效，正是本专利背景批评的单网卡单点故障。架构层级不同 → 不得判命中。 |

## 已检查文档清单
- OVS Offload Using ASAP² Direct（MLNX_EN v4.9-5.1.0.0 LTS）— VF-LAG 配置、bond 模式、eSwitch 卸载机制 — https://docs.nvidia.com/networking/display/MLNXENv495100/OVS+Offload+Using+ASAP2+Direct
- QSG for High Availability with NVIDIA Enhanced SR-IOV with Bonding Support (VF-LAG) — 单卡双端口 bond 架构、LACP mode=4、页面 Last updated 2023-09-12 — https://docs.nvidia.com/networking/display/public/SOL/QSG+for+High+Availability+with+NVIDIA+Enhanced+SR-IOV+with+Bonding+Support+(VF-LAG)

## 最终判定
**第 4 档：公开资料不足（弱候选）**
五档定义：第1档=确认侵权(高)F全字面命中；第2档=确认侵权(中)含≥1等同命中；第3档=公开资料不足(强候选)≥60%F#命中且无反向证据；第4档=公开资料不足(弱候选)<60%；第5档=已排除(仅当≥1条F#真反向证据 OR 全部证据<2023-06-06 OR 架构层级不同)。
**0 命中 ≠ 已排除**。无正向也无反向 → 第3或4档。
判定依据（基于 F# 命中分布）：F3 字面命中、F2 等同命中，但本专利**核心创新限定 F1+F5（N≥2 块独立网卡聚合 + 精确流表同步卸载至全部网卡以跨卡消除单点故障）公开资料显示架构层级不同**——NVIDIA VF-LAG 是单块网卡的两个物理端口做 LAG（"single bonded PF port"/"two physical bond ports"），属卡内端口聚合而非跨卡聚合，且单卡故障即整体失效。两个核心区分限定未命中，命中比例 <60%（2/5 且 F4 不足），落第4档而非第3档。注：未达第5档已排除——NVIDIA 文档只是默认描述单卡双端口，并未**显式拒绝/排除**多卡部署，不构成"真反向证据"，故保留为弱候选而非排除。

## 升级路径（第4档）
- 检索 NVIDIA / 云厂商是否有"把同一 OVS 精确流表同步卸载到**两块独立 ConnectX 网卡**"的 multi-NIC HA 部署文档或 commit（关键词：multi-NIC bond hardware offload、cross-card eSwitch flow sync、dual-card SR-IOV failover offload）。
- 若找到把 bond 跨两块独立网卡且流表同步下发到两卡 eSwitch 的一手证据（且发布日 ≥2023-06-06），F1/F5 可升级为等同/字面命中，整体升至第2-3档。
- 抓更细的 OVS-DOCA / OVS-Kernel 卸载源码或 release note 验证 F4 "miss 触发卸载"的 verbatim 措辞。

## 总结一句话
候选 01-tech-nvidia-asap2-vflag 落第 4 档（公开资料不足-弱候选）：VF-LAG 命中 LACP(F3)与端口聚合(F2)，但其"单卡双端口"架构与本专利"N≥2 块独立网卡聚合+流表同步卸载至全部网卡"的核心限定 F1/F5 架构层级不同，且未见显式拒绝多卡的反向证据，故为弱候选而非排除。
