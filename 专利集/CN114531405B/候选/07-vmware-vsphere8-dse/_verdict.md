# Verdict — VMware NSX-T + vSphere 8 DSE LAG

> S1+S3；权 1/11/23/33/34；**P1**

F1-F2 字面命中（NSX-T 支持 LACP bond，vSphere 8 DSE 集成 DPU）；F3-F5 闭源 + 依赖 DPU 厂实现 → 公开资料不足。
按 R-2 拓扑变体细分：单 DPU 部署 = 第 5 档（已排除 N=1）；多 DPU HA = 第 3 档强候选。
**状态机判定**：T-B 多 DPU = **第 3 档（公开资料不足强候选）**；T-A 单 DPU 已排除。
