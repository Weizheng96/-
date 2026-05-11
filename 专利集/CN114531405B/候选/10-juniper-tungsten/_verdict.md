# 候选：Juniper Tungsten Fabric + Apstra

## 候选标识
- candidate_slug: `10-juniper-tungsten`
- 主体类型：E. SDN 控制器 / 网络方案
- 适用独立权：权 1, 11, 23, 36

## §A 主流来源摘要

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | Tungsten Fabric SmartNIC offload spec | https://github.com/tungstenfabric/tf-specs/blob/master/smart-nic-generic-offload.md | "generic offload layer is responsible for programming offload rules to the smart NIC through the existing standard open source hardware offload APIs (e.g. DPDK rte_flow and/or Linux TC flower)" |
| 2 | Tungsten Fabric Architecture | https://tungstenfabric.github.io/website/Tungsten-Fabric-Architecture.html | vRouter forwarder 可下沉到 smart NIC |
| 3 | Juniper Aggregated Ethernet Interfaces | https://www.juniper.net/documentation/us/en/software/junos/interfaces-ethernet/topics/topic-map/aggregated-ethernet-interfaces-lacp-configure.html | LACP 在 ae interfaces 支持——**交换机侧**，非 host 内 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 36 | **公开资料不足（第 4 档弱候选）** | TF 提供 generic offload layer 抽象，但**0 命中**"跨多 NIC 同步流表"具体实现；Apstra 主要是 IBN 控制器，不在 host vSwitch 层 | **公开资料不足（第 4 档弱候选）** |

### 最终 verdict

**公开资料不足**：Tungsten Fabric 提供 SmartNIC offload 通用抽象层，但公开 spec 0 命中"跨 N 张 NIC 二层映射 + 同步卸载"实现。

## 总结一句话

Tungsten Fabric 提供 SmartNIC offload 抽象层但 0 公开"跨 NIC 同步" 实现，**落第 4 档公开资料不足弱候选**。
