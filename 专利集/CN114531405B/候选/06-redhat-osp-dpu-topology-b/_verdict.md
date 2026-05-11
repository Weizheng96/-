# Verdict — Red Hat OSP with OVS bond + DPU 拓扑 T-B：多 DPU HA 部署

> 主体类型：S1 + S5；适用独立权：权 1 / 11 / 23 / 33 / 34 / 36；分级：**P0**

## 核心组织
Red Hat（IBM 子公司，NYSE: IBM）

## F1-F5 命中（T-B）
依赖 NVIDIA VF-LAG T-B（候选 04）；Red Hat × NVIDIA 联合 reference architecture 可能描述多 DPU HA 部署。
- F2 字面命中（OSP 17 推荐 OVS bond LACP）
- F1 / F3 / F5：依赖下游 NVIDIA T-B 拓扑未明示路径 → 公开资料不足

## 状态机三栏：**第 3 档：公开资料不足（强候选）+ 强现有技术 caveat**

## 升级路径
- Red Hat × NVIDIA 联合 reference architecture 多 DPU HA 部署指南深读
- Red Hat OSP 客户案例（运营商 NFV）是否实际部署 T-B

## 总结
Red Hat OSP 多 DPU HA 部署 T-B：F2/F4 字面、F1/F3/F5 公开资料不足；落第 3 档强候选；同 NVIDIA T-B 的取证升级路径。
