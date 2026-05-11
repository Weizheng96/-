# 候选：Cisco ACI + Cilium (Isovalent)

## 候选标识
- candidate_slug: `09-cisco-aci`
- 主体类型：E. SDN 控制器 / CNI
- 适用独立权：权 1, 11, 23, 36

## §A 主流来源摘要

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | Cisco ACI VMM Active-Active LACP | https://www.cisco.com/c/en/us/support/docs/lan-switching/link-aggregation-control-protocol-lacp-8023ad/220713-troubleshoot-active-active-nic-teaming-o.html | Active-Active NIC Teaming with Enhanced LACP supported in VMM domain |
| 2 | Cisco ACI Virtual Edge | https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/aci_virtual_edge/configuration/2-x/Cisco-ACI-Virtual-Edge-Configuration-Guide-22x/m_virtual_edge_config_pc_vpc.html | "Cisco ACI Virtual Edge **does not support LACP** on its uplinks because VDS does not support it for vEth interfaces" |
| 3 | Cilium eBPF Datapath | https://docs.cilium.io/en/stable/network/ebpf/index.html | eBPF datapath in software，无硬件 sync flow |
| 4 | Cilium issue #18706 | https://github.com/cilium/cilium/issues/18706 | bond NIC failure mode — Cilium runs on top of Linux bond/LACP，但**不**实现 hardware exact-match flow sync |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 36 | **已排除（第 5 档）** | ACI 服务在 fabric leaf/spine 而非 host NIC（架构 off-axis）；Cilium eBPF 软件路径，无硬件多 NIC sync；ACI Virtual Edge 显式真反向"does not support LACP" | **已排除（架构 off-axis + 局部真反向）** |

### 最终 verdict

**已排除（架构层级不符）**：Cisco ACI 数据面服务位于 fabric leaf/spine 交换机（不在 host）；Cilium 是 eBPF 软件路径（不下沉硬件多 NIC sync）；Cisco ACI Virtual Edge 显式不支持 LACP——三处与本专利不一致。

## 总结一句话

Cisco ACI 在 fabric 服务（off-axis）+ Cilium 软件 eBPF（无硬件 sync）+ ACI Virtual Edge 显式不支持 LACP——**落第 5 档已排除**。
