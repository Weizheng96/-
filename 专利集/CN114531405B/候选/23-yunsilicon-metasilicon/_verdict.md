# 候选：YunSilicon (云脉芯联) metaScale / metaConnect / metaVisor

## 候选标识
- candidate_slug: `23-yunsilicon-metasilicon`
- 主体类型：B. 国产 DPU 芯片厂
- 适用独立权：权 23, 35, 36

## §A 摘要（6 国产 DPU 中证据最强）

| 源 | URL | 引文 |
| --- | --- | --- |
| YunSilicon 官网 | https://www.yunsilicon.com/ | metaScale 智能网卡 + metaConnect AI NIC + metaVisor AI DPU |
| Kube-OVN YunSilicon 接入 | https://kubeovn.github.io/docs/v1.12.x/en/advance/offload-yunsilicon/ | metaScale 家族 PCI ID `1f67:1111` PF / `1f67:1112` VF；**显式支持 bonding**：`BR_PHY_BOND_NAME=bond0`（"specify bond name if bond enabled"），`HW_OFFLOAD=true` 启用硬件卸载，要求 **switchdev + SR-IOV** 模式 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 23 / 35 / 36 | **公开资料不足（第 3 档强候选 — 6 家国产 DPU 中证据最强）** | F1 倾向命中；F2 部分命中（bonding 支持但 LACP 模式未公开确认 — 套用 SR-IOV VF LAG 通用文档可推 active-backup/XOR/LACP，但需 vendor 确认）；F3/F4 公开资料不足；按硬约束 3 拓扑外推禁令——保守判 F2 仅"部分" | **公开资料不足（第 3 档强候选 — 比其他国产 DPU 略强）** |

## 总结一句话

YunSilicon metaScale + Kube-OVN 公开 `BR_PHY_BOND_NAME` 参数为 6 国产 DPU 最强证据，但 LACP+sync flow 仍需深度核查——**落第 3 档公开资料不足强候选**。
