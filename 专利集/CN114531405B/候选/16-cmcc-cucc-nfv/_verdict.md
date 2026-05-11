# 候选：电信运营商 NFVI / 5G UPF 数据面（中国 + 国际）

## 候选标识
- candidate_slug: `16-cmcc-cucc-nfv`
- 主体类型：C. Telco
- 适用独立权：权 1, 11, 23

## §A 摘要

| 厂 | 备注 |
| --- | --- |
| Nokia Cloud Packet Core | https://www.nokia.com/core-networks/cloud-packet-core/ — UPF 卸载到 SmartNIC；LAG load sharing in hardware；LACP 支持 |
| Ericsson | https://www.ericsson.com/en/reports-and-papers/ericsson-technology-review/articles/energy-efficient-packet-processing-in-5g-mobile-systems — UPF "offload packet flows with the highest bandwidth to the network device using hardware offload" |
| Mavenir Open RAN UPF | 商业方案 |
| 国内 NFVI 集采 | C114 报道 — 集采清单含 NFVI / vCPE / vBNG 框架但**无 vSwitch 多 NIC sync flow 具体条款** |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 | **公开资料不足（第 4 档弱候选）** | Nokia / Ericsson 公开 LACP + UPF hw offload，但**0 命中** "vSwitch 内 N→1 同步流表卸载到全部 N 张 NIC" 具体描述 | **公开资料不足（第 4 档弱候选）** |

## 总结一句话

电信 NFV 5G UPF 厂（Nokia / Ericsson / Mavenir）有 LACP + UPF hw offload building blocks，但**0 公开**"vSwitch sync flow"具体实现——**落第 4 档公开资料不足弱候选**。
