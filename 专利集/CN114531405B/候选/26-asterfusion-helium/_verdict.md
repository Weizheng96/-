# 候选：星融元 Asterfusion Helium DPU（基于 Marvell OCTEON）

## 候选标识
- candidate_slug: `26-asterfusion-helium`
- 主体类型：B. 国产 SmartNIC + 系统集成
- 适用独立权：权 23, 35, 36

## §A 摘要

| 源 | URL | 引文 |
| --- | --- | --- |
| Asterfusion Helium DPU 产品页 | https://asterfusion.com/en/product/helium-dpu/ | EC2004Y (4×25GE)、EC2002P (2×100GE)；24-core ARM Marvell OCTEON TX2 |
| Helium GitHub | https://github.com/asterfusion/Helium_DPU | **开源**——可白盒级证据采集；README 未含 LACP/bonding/多口共享流表段落 |
| AsterNOS MC-LAG | asterfusion.com/cx-n | MC-LAG 是 CX-N **交换机** OS 特性，非 Helium DPU |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 23 / 35 / 36 | **公开资料不足（第 4 档弱候选 — 但开源代码可深挖）** | F1 倾向命中（多口硬件）；F2/F3/F4 0 命中；建议下一轮 grep Helium GitHub 仓库 `lag` / `lacp` / `bond` / `vf_lag` 升档 | **公开资料不足（第 4 档弱候选）** |

## 总结一句话

Asterfusion Helium 多口硬件 + OVS 全卸载 + **开源代码可深挖**，公开 README 不直接命中 F2/F4——**落第 4 档公开资料不足弱候选**（升档路径：grep GitHub 仓库源码）。
