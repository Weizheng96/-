# Verdict — Microsoft Azure AccelNet + Catapult FPGA SmartNIC + Hyper-V Virtual Switch

> 主体类型：S1 + S2 + S3 + S4（垂直整合）；适用独立权：权 1 / 权 9 / 权 17；分级：**P1**

## 1. 核心组织

| 责任主体 | 法律性质 | 角色 |
| --- | --- | --- |
| **Microsoft Corporation（NASDAQ: MSFT）** | 上市公司 | Hyper-V vSwitch + AccelNet + Catapult FPGA SmartNIC + Azure Boost ASIC 全栈 |

## 2. F1-F5 命中表

| F# | 证据来源 | 命中类型 |
| --- | --- | --- |
| F1 | Microsoft "Azure Accelerated Networking: SmartNICs in the Public Cloud"（NSDI 2018）— 明确提及 Hyper-V vSwitch (VFP) 与 SR-IOV / FPGA 卸载的双层架构 | **字面命中** |
| F2 | NSDI 2018 论文 + Catapult ISCA 2018 论文 — VFP 是用户态多线程数据面 | **字面命中** |
| F3 | NSDI 2018 论文中描述 VFP 与 Generic Flow Tables 之间的 flow learning + offload triggering — 状态采集明确存在 | **字面命中** |
| F4 | NSDI 2018 论文 — 触发卸载的条件（流的 first packet 走 slow path → 后续 fast path 卸载到 FPGA / ASIC）；但与本专利"线程级负载均衡触发"是否完全等价存疑 | **等同命中候选 / 公开资料不足** |
| F5 | NSDI 2018 论文 — flow 卸载到 FPGA 后由 SR-IOV VF 直接交付 VM；fast path 调度 vs slow path 切换确实改变了"线程所服务的端口"概念 | **等同命中候选** |

## 3. 时间线

- Azure AccelNet GA：2018-01（约同期专利授权 2018-09，临时保护期边界附近）
- NSDI 2018 论文：2018-04 → 临时保护期边界 / post-grant 都要分别看
- Azure Boost SmartNIC GA：2023-11 → post-grant
- 判定：AccelNet v1 临时保护期 + post-grant 跨界；Boost 完全 post-grant

## 4. §A 19 类源穿透扫描

- §A.1 专利墙：Microsoft 在 H04L 拥有大量专利（含 SDN / SmartNIC offload）
- §A.2 学术论文：Microsoft NSDI 2018 / SOSP 2019 / SIGCOMM 系列详尽公开（**强证据来源**）
- §A.3 宣传：Microsoft Azure 官方博客、Build / Ignite keynote
- §A.4 使用手册：Azure Boost 官方文档（公开度高）
- §A.16 多语言源 cross：Azure 中国（21Vianet 运营）+ Azure 全球版本一致
- §A.18 国际同族专利：Microsoft 同主分类专利墙非常厚

## 5. 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 | **第 3 档：公开资料不足（强候选）** — F1/F2/F3 字面命中；F4/F5 等同命中但需更深取证 | 等同三步法对 F5：同手段（迁移 packet 处理路径）+ 同功能（提高 PMD 利用率 + NUMA 局部性）+ 同效果（吞吐 +）+ 显而易见性（vSwitch 数据面调度领域内常识） — **等同命中**；F4 维持公开资料不足 | **第 3 档：公开资料不足（强候选）**——但 F5 等同命中支持升级 |
| 权 9 | **第 3 档：公开资料不足（强候选）** | 同上 | 第 3 档 |
| 权 17 | **第 3 档：公开资料不足（强候选）** — F17a/b 部分字面命中（Catapult FPGA 是硬件层 + Hyper-V 是宿主机 + VM）| 同上 | 第 3 档 |

## 6. 总结一句话

Azure AccelNet / Catapult FPGA：F1-F3 字面命中（NSDI 2018 公开论文），F4 公开资料不足、F5 等同命中候选；落第 3 档（公开资料不足强候选）；建议深读 SOSP 2019 Snap 论文 + Azure Boost 详细 design doc。
