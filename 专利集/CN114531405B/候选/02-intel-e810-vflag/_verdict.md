# 02-intel-e810-vflag verdict

## 候选基本信息
- 名称：Ethernet 800 系列（E810）OVS TC 卸载 + SR-IOV VF-LAG
- 组织：Intel
- 类型：产品
- 初判命中 F#：F1,F2,F3,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（虚拟交换机 + M VM + N 网卡，M、N≥2，N 为"网络接口卡"） | 反向证据 | "the bond comprises exactly two ports from the same NIC MAC chip" | https://docs.kernel.org/networking/device_drivers/ethernet/intel/ice.html ；EDC ice LAG 文档 | E810 VF-LAG 的 bond 是"同一块网卡 MAC 芯片上的两个端口"，即聚合发生在单块网卡内部的 2 个物理端口，而非 N≥2 块独立网络接口卡。F1 要求 N≥2 块"网络接口卡(NIC)"，E810 形态为单 NIC 双端口——架构层级不同，构成正向反向事实 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 反向证据 | bond = ens2f0 + ens2f1（同一适配器 ens2 的两端口）；"two ports from the same NIC MAC chip" | https://edc.intel.com/content/www/us/en/design/products/ethernet/appnote-e800-eswitch-switchdev-mode-config-guide/script-d-switchdev-mode-with-lag-configuration/ | bond netdev 确将两端口聚合为一个逻辑口，但被聚合对象是"同一网卡的两物理端口"，不是"N 块网卡各自的逻辑端口"。与 F2"N 个网卡对应的 N 个逻辑端口"的跨卡结构不符 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合，再跨网卡聚合） | 反向证据 | "supported bonding modes: active-backup (1), balance-xor (2), broadcast (3), and 802.3ad (4)"；"exactly two ports from the same NIC MAC chip" | https://docs.kernel.org/networking/device_drivers/ethernet/intel/ice.html ；EDC ice LAG 文档 | LACP/802.3ad 本身支持（FW 4.80+），但聚合是"单网卡内两端口的 LACP"，不存在"每块网卡先各自形成 LACP 逻辑端口、再把 N 个逻辑端口跨卡聚合成第一端口"的两级跨卡结构。F3 的跨网卡聚合不成立 |
| F4（目标网卡流表 miss → 触发精确流表卸载） | 字面命中 | "skip_sw denotes that the rule is added to hardware but not software"；"In O/P, if the flag shows as offloaded:yes, dp:tc, it means flows are on hardware" | https://cdrdv2-public.intel.com/645272/645272_E810%20eSwitch%20switchdev%20Mode%20TechConfigGuide_Rev1.0.pdf（本地 E810-switchdev-techconfig-rev1.0.pdf） | TC-Flower exact-match 规则首包 miss 经 upcall 慢路径下发 exact flow 到硬件 eSwitch——与 F4 first-packet miss → exact-match 卸载语义一致 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 反向证据 | "exactly two ports from the same NIC MAC chip"（无跨 N 块网卡复制下发机制）；上游内核更"You cannot use SR-IOV when link aggregation (LAG)/bonding is active, and vice versa. To enforce this, the driver checks for this mutual exclusion." | https://docs.kernel.org/networking/device_drivers/ethernet/intel/ice.html | E810 卸载目标是单块网卡的 eSwitch（双端口），不存在"把精确流表向 N 块独立网卡全部下发以做冗余/防单点"的机制。F5 的"下发至全部 N 个网卡"无对应实现，且其架构恰是专利所要解决的单网卡单点故障形态 |

## 已检查文档清单
- Intel E810 eSwitch switchdev Mode Tech & Config Guide（Rev1.0 PDF，本地全文抽取）：确认 TC-Flower exact-match skip_sw 硬件卸载 + OVS hw-offload dp:tc — https://cdrdv2-public.intel.com/645272/645272_E810%20eSwitch%20switchdev%20Mode%20TechConfigGuide_Rev1.0.pdf
- kernel.org Intel ice 驱动文档：上游默认 SR-IOV 与 LAG/bonding 互斥（驱动强制）；VF-LAG 兼容条件为同一 NIC MAC 芯片的两端口 — https://docs.kernel.org/networking/device_drivers/ethernet/intel/ice.html
- EDC Script D（Switchdev + LAG 配置）：bond 由同一适配器 ens2f0/ens2f1 两端口组成 — https://edc.intel.com/content/www/us/en/design/products/ethernet/appnote-e800-eswitch-switchdev-mode-config-guide/script-d-switchdev-mode-with-lag-configuration/

## 最终判定

**第 5 档：已排除**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。

判定依据（1-3 句，基于上表 F# 分布）：E810 VF-LAG 的 bond 被官方/内核文档明确限定为"同一块网卡 MAC 芯片上的两个端口"（exactly two ports from the same NIC MAC chip），属单网卡双端口聚合，与专利 F1/F3/F5 要求的"跨 N≥2 块独立网络接口卡做 LACP 聚合 + 把精确流表向全部 N 块网卡下发以消除单点故障"是不同的架构层级——这正是专利背景技术所批判的"单一网卡内链路可靠性、网卡故障即系统故障"形态。F4（exact-match miss 卸载）字面命中，但 F1/F2/F3/F5 均有针对该产品的正向反向事实，满足第5档硬门槛(a)(c)。

## 升级路径（仅落第3-4档时填）
- （不适用，已落第5档）

## 总结一句话
候选 02-intel-e810-vflag 落第 5 档（已排除）：E810 VF-LAG 是"同一网卡 MAC 芯片两端口"的单卡聚合，与专利 F1/F3/F5 要求的"跨 N≥2 块独立网卡 LACP 聚合 + 流表向全部网卡下发防单点"架构层级不同，构成正向反向证据；仅 F4 命中。
