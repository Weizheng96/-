# 候选：腾讯云银杉 SmartNIC + TGW + 黑石 CBM

## 候选标识
- candidate_slug: `14-tencent-yinshan-tgw`
- 主体类型：C. 公有云 CSP + B. SmartNIC 设计方
- 适用独立权：权 1, 11, 23, 36
- 命中场景：场景 1 / 4

## §A 主流来源摘要

### §A.2 学术阵地

| 源 | URL | 日期 | 引文 |
| --- | --- | --- | --- |
| Layong Luo (Tencent) — APNet 2018 | https://conferences.sigcomm.org/events/apnet2018/slides/larry.pdf | 2018 | "统一 SmartNIC 架构同时服务裸金属和公有云"愿景；**未涉及单主机多 SmartNIC 同步卸载**；时间档：早于专利申请日（2020-10-31），不构成命中 |
| Layong Luo 个人主页 | https://luolayong.com/ | 长期 | 公开作品中**无**"单主机多张智能网卡 + LACP + 跨卡同步流表"主题 |

### §A.4 使用手册 / 技术文档

| 源 | URL | 引文 |
| --- | --- | --- |
| Tencent Cloud CBM 产品页 | https://www.tencentcloud.com/products/cbm | "It can **bond two ENIs** in a 100 Gigabit network" — **ENI = 弹性网卡（虚拟接口）**，并非两张物理智能网卡；未提 LACP，未提流表卸载 |
| Tencent Cloud CBM FAQ | https://www.tencentcloud.com/document/product/1171/52414 | "you can flexibly adjust the number of ENIs"，**未提** LACP / SmartNIC 卸载 / 跨卡同步流表 |

### §A.3 宣传材料 / §A.13 技术博客

- 腾讯云开发者社区 SmartNIC 文章群 6+ 篇：cloud.tencent.com/developer/article/{1077179, 1628455, 1852634, 1887310, 2325590, 2357350}（2018-2024）
- 全部为通用科普 / Mellanox 移植 / SR-IOV / OVS-TC offload 介绍——**未声明腾讯生产环境采用"多智能网卡 + 跨卡流表副本"架构**

### §A.5 / 6 / 7-19 类源

- §A.5 标准：不适用
- §A.6 联合：未检索到
- §A.7 上游归因：腾讯在 OVS / DPDK 上游有 contributor，但与跨 NIC 二层映射 feature 无关
- §A.10 招聘 JD：搜"银杉 智能网卡 多卡"等技术词组合 0 命中具体岗位描述
- §A.11 财报：腾讯财报技术披露中无相关 keyword
- §A.13 视频 / 演讲：APNet 2018 已覆盖；其他平台未命中
- §A.14 招标：腾讯云 to-B 招标公开材料 0 命中
- §A.18 国际同族专利：0 命中
- §A.19 关联企业：0 命中

## §C 子 agent 复核

由 1 个 general-purpose 子 agent（agent ID ab791667901e144a7，2026-05-11）独立完成。主 agent 复核认可。

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 36 | **公开资料不足（第 4 档弱候选）** | 反向证据 vs 限定语：CBM "bond two ENIs" 不是真反向证据（ENI 是虚拟接口而非物理 NIC，与 F1 物理 NIC 拓扑不同维度，不构成"Y does NOT do X"）；§5.0 豁免：未触发；硬约束 4：0 命中 ≠ 已排除——必须满足 5 条硬条件之一才能判已排除 | **公开资料不足（第 4 档弱候选）** |

### F# 投票汇总

- F1：CBM "bond two ENIs" 是虚拟接口绑定，未明示物理 NIC 数；公开资料不足（无字面命中、无真反向证据）
- F2：未声明 LACP；公开资料不足
- F3：无 N→1 二层映射描述；公开资料不足
- F4：腾讯公开口径只到"OVS 流表卸载到智能网卡"单卡叙事；公开资料不足

### 后置调整记录（按 7 条）

1. 等同三步法：信息不足无法 assess
2. 反向证据 vs 限定语：CBM "bond two ENIs" 措辞模糊但不是真反向；按硬约束 4，0 命中 ≠ 已排除
3. 法律状态：Active，无降级
4. 现有技术 caveat：APNet 2018 在专利申请日前但与本专利新颖点不冲突
5. R-STANDARD 转移：不适用
6. §5.0 豁免：未触发
7. Patent pledge：未检索到

### 最终 verdict

**公开资料不足（第 4 档弱候选）**：腾讯关于 SmartNIC / TGW 的公开材料停留在"OVS 流表卸载到智能网卡"单卡叙事，与本专利 F1（多 NIC 拓扑）+ F2（LACP）+ F4（同步卸载 N 份相同）的组合**全部 0 命中**，但亦无明确反向证据。腾讯云架构闭源，公开度低；按硬约束 4，0 命中 ≠ 已排除。

## 证据穷尽性证明

| # | 源类别 | query 关键词 / URL | 命中要点 / 0 命中 |
| --- | --- | --- | --- |
| 1 | §A.1 专利墙 | `assignee:Tencent + cpc:H04L45/76 + after:2023-06-06` | 工具能力受限（IncoPat 登录墙）；建议法务通过 IncoPat / 智慧芽账号补查 |
| 2 | §A.2 学术阵地 | APNet / SIGCOMM / NSDI Tencent SmartNIC papers | APNet 2018 命中（早于申请日）；其他 0 命中 |
| 3 | §A.3 宣传 | Tencent Cloud blog + DevOps community | 6+ 篇 SmartNIC 通用文章命中，无具体多 NIC + LACP + 同步卸载架构描述 |
| 4 | §A.4 文档 | tencentcloud.com/products/cbm + document | "bond two ENIs"（虚拟接口），无物理多 NIC 描述 |
| 5 | §A.5 标准 | 不适用 | — |
| 6 | §A.6 联合 | Tencent × upstream 联合 PoC 报告 | 0 命中相关组合 |
| 7 | §A.7 上游归因 | @tencent.com 在 OVS / DPDK / Linux netdev 上游 contribution | 未发现与跨 NIC 二层映射 feature 直接相关 |
| 8 | §A.8 fork 仓库 | Tencent OVS fork | 未发现公开 fork |
| 9 | §A.9 现有技术 | APNet 2018 paper | 见上 |
| 10 | §A.10 招聘 JD | boss / 拉勾 / 脉脉 "腾讯 银杉 多网卡" | 0 命中具体技术描述 |
| 11 | §A.11 财报 | HKEX 0700 年报 / 季报技术披露 | 0 命中 |
| 12 | §A.12 招标 | Tencent 不通过公开招标做云架构（自营） | 不适用 |
| 13 | §A.13 视频 | 腾讯云 Lighthouse / TVP 视频平台 | 未命中具体多 NIC 同步流表内容 |
| 14 | §A.14 bug tracker | OVS bug tracker @tencent.com 邮箱 | 工具能力受限 |
| 15 | §A.15 标准化会议 | CCSA TC614 / ODCC 文档 Tencent 贡献 | 0 命中本专利相关 |
| 16 | §A.16 多语言 cross | 中英文 cross 已执行 | — |
| 17 | §A.17 客户案例 | Tencent × CSDN / 上汽 / 美的等客户案例 | 0 命中 |
| 18 | §A.18 国际同族 | Tencent USPTO / EPO 同分类 | 工具能力受限 |
| 19 | §A.19 关联企业 | Tencent 子公司 / 投资公司 | 0 命中 |
| 20 | §A.20 反向工程 | （成本超出本轮） | 待法务决定 |

最终缺失证据：F1 / F2 / F3 / F4 全部 unprovable
最强证据缺口：腾讯云内部架构闭源，无公开材料披露多智能网卡同步流表机制
建议升级路径：法务 NDA 渠道访问 Tencent 客户合同 / 反向工程裸金属 BM4 实例 / IPR 律师询证函

## 总结一句话

腾讯银杉 / TGW / CBM 公开材料停留在单卡 OVS 卸载叙事，F1-F4 全部 0 命中且无真反向，**落第 4 档公开资料不足弱候选**——闭源架构需法务取证升级。
