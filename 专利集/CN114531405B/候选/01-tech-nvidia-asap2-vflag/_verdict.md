# 01-tech-nvidia-asap2-vflag verdict

## 候选基本信息
- 名称：ASAP² / SR-IOV VF-LAG OVS 硬件卸载（ConnectX-6/7、BlueField-2/3）
- 组织：NVIDIA
- 类型：技术
- 初判命中 F#：F1,F2,F3,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（vSwitch+M VM+N≥2 网卡） | 反向证据 | "To enable SR-IOV VF LAG, both physical functions of **the NIC** should first be configured to SR-IOV SwitchDev mode, and only afterwards bond the up-link representors" / "bonding separate NICs with full eswitch offload support is **not a supported configuration**. The eswitch offload functionality works within a **single NIC's** embedded switch" | https://docs.nvidia.com/networking/display/MLNXENv543580/OVS+Offload+Using+ASAP%C2%B2+Direct | VF-LAG 聚合的是**同一块网卡**的两个 PF / 物理端口（单卡双口），不是专利要求的 N≥2 块**独立网卡**；且跨独立网卡的全 e-switch 卸载明确不支持。F1 要求 N≥2 网卡，候选为单卡形态——正向反向事实 |
| F2（N 逻辑端口聚合为第一端口） | 反向证据 | "if both PFs are up, traffic from any VF will split between these two PFs"（聚合对象=同卡两 PF） | https://docs.nvidia.com/networking/display/MLNXENv543580/OVS+Offload+Using+ASAP%C2%B2+Direct | 聚合层级是"单卡两物理端口→一个 bond"，无"N 块网卡各自逻辑端口再聚合为第一端口"的跨卡结构；架构层级不同 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合） | 公开资料不足 | "The supported Bond modes are: Active-Backup, XOR and LACP"（确有 LACP bond） | https://docs.nvidia.com/networking/display/TAN10110/OVS+Kernel+-+VF+LAG+Configuration | 确有 LACP 聚合机制，但作用于单卡的两物理端口；专利 F3 的语义是"N 块网卡中每块各自形成逻辑端口"，候选只有 1 块网卡，谈不上"每个网卡"的复数结构 |
| F4（目标网卡流表 miss 触发卸载） | 等同命中 | OVS 硬件卸载 first-packet miss → upcall → 慢路径下发 exact flow（ASAP² 保持 OVS control-plane 不变，data-plane 在网卡硬件） | https://docs.nvidia.com/networking/display/MLNXENv543580/OVS+Offload+Using+ASAP%C2%B2+Direct | 这是 OVS 卸载通用 miss→offload 机制，与 F4 同手段同效果；但属行业通用，不构成对候选的正向命中加分 |
| F5（经第一端口将精确流表卸载至**全部 N 个**网卡） | 反向证据 | "offload them to **the hardware e-switch**"（单数，单卡内嵌交换机）；"works within a single NIC's embedded switch" | https://docs.nvidia.com/networking/display/MLNXENv543580/OVS+Offload+Using+ASAP%C2%B2+Direct | 流规则只卸载到**单块网卡的单个 e-switch**，不存在"向 N 块独立网卡全部下发精确流表"的冗余下发；这正是专利 F5 区别于普通单卡 OVS 卸载的核心，候选恰好落在被区分的一侧 |

## 已检查文档清单
- OVS Kernel - VF LAG Configuration（bond 成员 enp3s0f0/f1=单卡双端口，支持 LACP）— https://docs.nvidia.com/networking/display/TAN10110/OVS+Kernel+-+VF+LAG+Configuration
- OVS Offload Using ASAP² Direct（"both physical functions of the NIC"、单数 e-switch、同卡两 PF 分流）— https://docs.nvidia.com/networking/display/MLNXENv543580/OVS+Offload+Using+ASAP%C2%B2+Direct
- 搜索聚合：跨独立网卡全 e-switch 卸载"not a supported configuration"，"works within a single NIC's embedded switch"（见 _sources.md query 2）

## 最终判定

**第 5 档：已排除**

判定依据（1-3 句，基于上表 F# 分布）：候选的 VF-LAG 是把**同一块网卡的两个物理端口/PF** 经 LACP 聚合为一个 bond，并把流规则卸载到**该单块网卡的单个 e-switch**；而本专利权 1 在 F1 明确要求 N≥2 块**独立网卡**、F5 要求"经第一端口将精确流表卸载至**全部 N 块网卡**"以消除单网卡单点故障。NVIDIA 官方文档正向写明"跨独立网卡 + 全 e-switch 卸载不是受支持的配置，卸载仅在单块网卡的内嵌交换机内工作"——这是针对该候选产品的**正向反向事实**（命中第5档硬门槛 (c) 架构层级不同 + (a) F1/F5 真反向证据），而非"公开资料未提及"。专利背景技术本身即把这种"单一网络接口卡内"的卸载列为存在单点故障风险的现有技术，候选正落在被本专利区分掉的一侧。

## 升级路径（仅落第3-4档时填）
- （不适用，已落第5档）

## 总结一句话
候选 01-tech-nvidia-asap2-vflag 落第5档（已排除）：NVIDIA VF-LAG 是单卡双 PF 的 LACP bond + 单 e-switch 卸载，与专利"N≥2 独立网卡聚合 + 精确流表向全部 N 块网卡下发"在 F1/F5 上有官方正向反向证据，架构层级根本不同。
