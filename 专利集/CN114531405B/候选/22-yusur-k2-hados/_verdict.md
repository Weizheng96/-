# 候选：中科驭数 (Yusur) K2-Pro DPU + HADOS

## 候选标识 / 主体类型 / 适用独立权
- candidate_slug: `22-yusur-k2-hados`
- 主体类型：B. 国产 DPU 芯片厂
- 适用独立权：权 23, 35, 36

## §A 摘要

| 源 | URL | 引文 |
| --- | --- | --- |
| Yusur K2-Pro 产品页 | https://www.yusur.tech/dpu/K2-Pro | K2/K2-Pro DPU 集成 OVS 全卸载 |
| Kube-OVN YUSUR 接入 | https://kubeovn.github.io/docs/v1.13.x/en/advance/offload-yusur/ | YUSUR CONFLUX-2200E **双物理口** + OVS flow table matching + tunnel encap 卸载 |
| HADOS 3.0 平台 | https://www.yusur.tech/product/devops | "驱动/网络/安全多层 API"，无 LACP/bond 公开 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 23 / 35 / 36 | **公开资料不足（第 4 档弱候选）** | F1 倾向命中（双口）；F2/F3/F4 0 命中且无真反向；硬约束 4：0 命中 ≠ 已排除 | **公开资料不足（第 4 档弱候选）** |

## 总结一句话

中科驭数 K2-Pro/CONFLUX 双物理口 + Kube-OVN HW offload 接入，但无 LACP/sync flow 公开——**落第 4 档公开资料不足弱候选**。
