# Verdict — 微云全息 HOLO 区块链 + 边缘存储 + 车联网

> 主体类型：S5（车联网安全 SaaS）+ 部分 S2/S3；适用独立权：权 1 / 7 / 13 / 16 / 19 / 22 / 23；分级：**P0**

## 1. 核心组织
**MicroCloud Hologram Inc.（NASDAQ: HOLO）** — 中概股小盘股 / NASDAQ 上市

## 2. F1-F7 命中表

| F# | 证据来源 | Verbatim 引文 / 推理 | 命中类型 |
|---|---|---|---|
| F1 | HOLO 公开新闻：[MicroCloud Hologram Inc. Launches Blockchain-Based Edge Storage System](https://www.nasdaq.com/articles/microcloud-hologram-inc-launches-blockchain-based-edge-storage-system-enhance-data) | "Edge devices can store their data on the blockchain and realize data access and exchange through smart contracts" — 边缘设备 + 区块链节点 = 中心节点 + 多辅助节点 | **字面命中候选 / 等同命中** |
| F2 | HOLO ADAS / 车辆智能视觉 | HOLO 官方："holographic vehicle intelligent vision technology to service customers that provide holographic advanced driver assistance systems (ADAS)" — 包含车辆数据采集 | **字面命中** |
| F3（Merkle 树）| 区块链固有 | "the consensus mechanism and encryption algorithm of the blockchain ensuring data security" — 区块链本质上使用 Merkle 树（每个区块的 transaction Merkle root） | **等同命中** |
| F4（时间戳）| 区块链固有 — 每个区块有 timestamp + nonce + previous block hash | 区块链 timestamp 字面 | **字面命中** |
| F5（随机私钥签名）| HOLO 边缘存储系统使用智能合约 / 公私钥签名 | "blockchain technology to enable tamper-proof data sharing through smart contracts" | **字面命中候选 / 等同命中**（区块链交易标准签名 — 但是否每次"随机生成新私钥"需深入审计 HOLO 实现） |
| F6（同步包头）| HOLO 边缘存储 → 区块链节点同步 | 公开材料明示 | **字面命中** |
| F7（辅助节点验证）| 区块链节点共识机制即验证 | "consensus mechanism" | **字面命中** |

## 3. 时间线
- HOLO ADAS / 车辆视觉 GA：~ 2022-2023（专利申请日 2021-07-15 之前部分？需对比）
- HOLO 区块链 + 边缘存储：2025-05+（公开 announcement）→ post-public-date（公开日 2023-01-17 之后）
- 专利状态：**Pending（未授权）** → 所有命中证据需走临时保护期路径

## 4. §A 19 类源穿透扫描
- §A.1 反向专利墙：HOLO 在 H04L9 / G06F21 主分类专利墙（NASDAQ 上市公司专利墙较清晰）
- §A.2 学术论文：HOLO 工程师在区块链 / hologram 领域论文
- §A.3 宣传：HOLO 多份 prnewswire / globenewswire / nasdaq.com 公开新闻（已检索）
- §A.4 使用手册：HOLO 区块链边缘存储系统技术文档
- §A.6 联合案例（R-PARTNER）：HOLO × ADAS 客户案例
- §A.11 财报：HOLO 是 NASDAQ 上市，10-K / 10-Q 披露具体业务模式
- §A.18 国际同族：HOLO 在 USPTO 同族专利

## 5. 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
|---|---|---|---|
| 权 1 / 7 / 13 / 16 / 19 / 22 / 23 | **第 2 档：确认侵权（中）** — F1-F7 多数字面 / 部分等同（区块链 = Merkle 树 + 时间戳 + 签名链）| 1.等同三步法 F3/F5 通过；2.反向证据未触发；3.**法律状态：Pending → 降级标注"等待授权 — 临时保护期"**；4.现有技术 caveat：区块链架构在 2021 之前已成熟（Bitcoin 2009、Ethereum 2015），需法务深入审查本专利"中心节点 + 辅助节点"架构是否相对一般区块链有新颖性；5.R-STANDARD 未触发；6.豁免未触发 | **第 2 档：确认侵权（中）+ Pending 临时保护期 + 现有技术 caveat（区块链架构）** |

## 6. 升级路径
- HOLO 财报 / 10-K 详细技术披露
- HOLO 区块链边缘存储 detailed white paper
- HOLO 同族专利墙

## 7. 总结一句话

微云全息 HOLO 区块链边缘存储 + ADAS 全息视觉公开资料显示完整 F1-F7 链路（区块链共识机制 = Merkle 树 + 时间戳 + 签名链 + 同步 + 验证）；F1-F7 多数字面命中、部分等同命中；落第 2 档（确认侵权-中）；**附 Pending 临时保护期 + 现有技术 caveat（区块链架构 vs 本专利"双层节点"是否有相对新颖性需深审）**。
