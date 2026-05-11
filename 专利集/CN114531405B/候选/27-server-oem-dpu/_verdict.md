# 候选：服务器 OEM 整机厂商集合（Dell / HPE / Supermicro / Lenovo / 浪潮 / 新华三 / 超聚变 / 中科曙光 / 宁畅）

## 候选标识
- candidate_slug: `27-server-oem-dpu`
- 主体类型：D. OEM 服务器整机厂
- 适用独立权：权 33, 34

## 候选群体说明

OEM 厂商在本专利上的角色是"将 N 张 NIC + DPU + 预装 vSwitch 集成为整机"。是否构成权 33 / 34 侵权，关键看：
- (i) OEM 自己是否在 reference architecture / deployment guide 中**主动推荐**多 NIC + LACP + 同步卸载配置
- (ii) OEM 出厂预装的 vSwitch 软件 / 固件本身是否带"跨 NIC 同步流表卸载"特性

## §A 主流来源摘要

| OEM | 关键 reference | 引文 |
| --- | --- | --- |
| Dell PowerEdge | https://infohub.delltechnologies.com/en-us/p/dell-technologies-poweredge-mx-platform-npar/ | PowerEdge MX 支持 LACP + static LAG + switch-independent teaming；NPAR 支持 NIC 分区 |
| HPE Aruba CX 10000 (with Pensando) | 见候选 19 | DPU 在 ToR 交换机内，非 host |
| Lenovo ThinkSystem | https://lenovopress.lenovo.com/lp1768 | DPU-enabled servers，单 DPU per host |
| 浪潮 NF5688G7 | https://www.ieisystem.com/product/ai/15080.html | 6U 8GPU + 12 PCIe Gen5 x16 扩展槽，可灵活支持 OCP 3.0、CX7、多种智能网卡——**架构允许多 NIC 但不强制** |
| 新华三 R5300G5 | （搜索命中） | 20 个 PCIe 4.0 插槽 + OCP 3.0 NIC，可选 200GE 高速网卡 |
| Dell DPU retrofit | https://www.theregister.com/2023/09/25/dell_poweredge_dpu_vsphere_vmware/ | 支持 DPU 改装 PowerEdge 旧服务器；通过 VMware vSphere 8 DSE 管理（参见候选 07 — VMware 已排除） |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 33 / 34 | **公开资料不足（第 4 档弱候选）** | OEM 自身仅集成硬件 + 预装第三方 vSwitch（OVS / VMware vDS / Hyper-V SET）；F# 命中需上游 vSwitch 命中——但上游已**全部已排除**（候选 01 OVS / 07 VMware / 08 Microsoft / 05-06 Red Hat）；OEM 自身公开 reference 未主动推荐"多 NIC + LACP + 同步卸载"组合 | **公开资料不足（第 4 档弱候选 — 上游 vSwitch 已排除时 OEM 整机权同步降档）** |

### 推论

OEM 整机权（权 33 / 34）的命中链路依赖于其预装的 vSwitch / 固件命中 F1-F4。在本批次中：
- 上游 OVS / Linux kernel = 已排除（候选 01 / 02）
- VMware vSphere DSE = 已排除（候选 07）
- Microsoft Hyper-V SET = 已排除（候选 08）
- Red Hat OSP = 已排除（候选 05 / 06）
- 国产 vSwitch（CIPU / TGW / BVS）= 已排除 / 公开资料不足（候选 13 / 14 / 17）

→ OEM 整机权依赖上游/中游 vSwitch 命中，上游全部已排除 → **OEM 同步降档至 已排除 / 公开资料不足**

## 总结一句话

服务器 OEM（Dell/HPE/Lenovo/浪潮/新华三/超聚变 等）整机权依赖预装 vSwitch；上游 vSwitch 全部已排除，OEM 同步降档至**第 4 档公开资料不足弱候选**。
