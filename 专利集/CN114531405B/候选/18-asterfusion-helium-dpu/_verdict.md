# 候选 #18 星融元 Helium DPU — 合议判定

**主体类型**：芯片厂 + 软件 / 固件发布方（开源）
**适用独立权**：权 35 + 权 36
**判定**：**已排除**

---

## 子 agent 投票表（F1-F6 × 4 文档）

| 特征 | A (READMEs) | B (VNF blog 404) | C (EC2000 datasheet) | D (Product page) | 合议 |
| --- | --- | --- | --- | --- | --- |
| F1 vSwitch | **是**（OvS 子模块） | 无效（404） | 部分（OVS Offload） | 否 | 部分命中（OvS 卸载层面） |
| F2 N≥2 物理 NIC | **否**（单卡形态） | 无效 | 否（4×SFP28 是单卡 4 端口） | 否 | **否，强反向**（产品定义即单卡）|
| F3 NIC 内部 LACP | **否**（仓库 0 关键词） | 无效 | 否（无 LACP / bond） | 否 | **否，强反向**（开源代码可审）|
| F4 多 NIC → 同一目标端口 | 否 | 无效 | 否 | 否 | **否** |
| F5 同表多卡分发 | 否 | 无效 | 否 | 否 | **否，强反向**（仓库 0 路径）|
| F6 NIC 硬件 offload | **是** | 无效 | **是**（多种 offload） | 否 | **是**（核心卖点）|

## 反向证据汇总

1. **F2 / F5 强反向**：子 agent C 明确指出产品定位为 *"a … smart network card"*（单数）；子 agent A 指出仓库目录 `Helium/{DPDK,VPP,OvS,UPF,DPVS,Kernel,Toolchain}` **无 bond / lag / teamd / lacp / multi-nic / flow-sync** 子模块路径。开源代码完全可审，无任何 F3-F5 实现路径。
2. **F3 反向**：3 份有效文档（A/C/D）全部 0 命中 LACP / bond / 802.3ad 关键词。
3. **F4 反向**：星融元产品形态是"单卡 SmartNIC + 单台网关盒"，没有 vSwitch 第二级聚合的语义。子 agent A 引用 ET2500 README："multiple ET2500 units can be deployed as a resource pool, enabling **horizontal load balancing**" — 这是设备级横向扩展，不是单主机内多 NIC 二级聚合。

## 落入专利明确排除的相邻方案

- 第 1 项：**单网卡（N=1）+ LACP 不满足 F2 / F4** —— 命中（Helium 是单卡产品）
- 第 5 项：**仅在 NIC 内部做 LACP，但虚拟交换机没有第二级"目标端口标识"映射不满足 F4** —— 命中（即便用户在主机侧做 Linux bond，Helium 自身不实现 vSwitch 第二级聚合）

## 最终结论
**Helium DPU 在权 35 + 权 36 双重已排除**：
- 权 35（芯片）：单卡 SmartNIC 形态 + 开源代码无多 NIC 协同模块路径，F2-F5 字面 + 等同均不命中
- 权 36（开源软件二进制）：GitHub 仓库公开可审，F2-F5 反向证据由"代码缺失"直接证明

## 数据完整性说明
- VNF blog 链接已失效（站点返回 404）。星融元可能在 2024-08 后修订过博客 URL，但通过其他 3 份本地化文档（READMEs + datasheet + 产品页）已收齐能拿到的最强直接证据，结论稳健。
- 升级前提：星融元发布"主机侧 vSwitch + 多 NIC 同表 OVS 卸载"完整方案（目前路线图未见此方向）。
