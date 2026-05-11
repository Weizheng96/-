# Verdict — AWS Nitro Hypervisor + 多 ENI bond

> S2+S4；权 1/11/33/34；**P1**

AWS EC2 实例支持多 ENI Linux bond + LACP；Nitro Card 实现 vSwitch-like 转发但是否做跨卡 / 跨 ENI hardware offload 同步**完全闭源**。F1-F2 字面命中（Nitro + multi-ENI bond），F3-F5 闭源 → 公开资料不足。**第 3 档（强候选）**；建议反向工程 EC2 Bare Metal 实例升级。
