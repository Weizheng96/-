# Verdict — AWS Nitro Hypervisor + Nitro Card + ENA driver

> 主体类型：S2（公有云部署方）+ S4（自研 Nitro DPU 芯片）；适用独立权：权 1 / 权 9 / 权 17；分级：**P1**

## 1. 核心组织

| 责任主体 | 法律性质 | 角色 |
| --- | --- | --- |
| **Amazon Web Services（NASDAQ: AMZN 子公司）** | 上市子公司 | 自研 Nitro 整体设计 + Annapurna Labs ASIC + ENA 驱动 + 内部 vSwitch |

## 2. F1-F5 命中表

| F# | 证据来源 | 命中类型 |
| --- | --- | --- |
| F1 | AWS re:Invent NET 系列演讲、Anthony Liguori "Nitro" 介绍、AWS 官方 ENA 文档 — 提及 "Nitro Hypervisor" + "ENA poll mode driver" + 内部 SDN | **字面命中** |
| F2 | AWS ENA 驱动开源代码（GitHub aws/amzn-drivers）— 多线程 poll-based 转发架构 | **字面命中** |
| F3 | 闭源；公开材料未明示状态属性检测 | **公开资料不足** |
| F4 | 闭源；公开材料未明示触发条件 | **公开资料不足** |
| F5 | 公开材料明示 Nitro 架构有 SR-IOV + queue↔CPU 映射，但是否动态调整不公开 | **公开资料不足** |

## 3. 时间线

- AWS Nitro 系统：2017 GA → 临时保护期到 post-grant 边界
- AWS Nitro v3 / v4：post-grant
- Anthony Liguori "Reinventing virtualization with Nitro" 系列演讲：2017-2024，多数 post-grant

## 4. §A 19 类源穿透扫描

- §A.2 学术论文：未发现 AWS Nitro 详细 PMD scheduler 论文（AWS 较少发表 SIGCOMM）；公开度低
- §A.3 宣传：AWS re:Invent NET402 系列演讲、AWS What's New 公告
- §A.4 使用手册：ENA driver GitHub、AWS Nitro System overview docs
- §A.6 联合案例：未发现（AWS 不与上游合作公开案例）
- §A.7 上游贡献归因：AWS 工程师在 DPDK、Linux 内核、Open vSwitch 上游贡献——可定位 @amazon.com 邮箱域 commit
- §A.18 国际同族专利：AWS 在 SDN / dataplane scheduling 方向有 US 专利墙（如 US10802881B1 等）

## 5. 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 | **第 3 档：公开资料不足（强候选）** | 闭源限制；建议反向工程 / NDA 渠道升级 | 第 3 档 |
| 权 9 | **第 3 档：公开资料不足（强候选）** | 同上 | 第 3 档 |
| 权 17 | **第 3 档：公开资料不足（强候选）** — Nitro Card SoC + 主机 + VM 三层架构匹配 F17a | 同上 | 第 3 档 |

## 6. 升级路径

- 反向工程 AWS EC2 Bare Metal 实例的 Nitro Card 行为
- 法务获取 AWS 提交给法院 / 监管机构的技术披露文件
- 检索 AWS Annapurna Labs 在 USPTO 的同主分类专利墙

## 7. 总结一句话

AWS Nitro 闭源限制致 F3-F5 无法从公开资料字面比对，落第 3 档（公开资料不足强候选）；F1-F2 字面命中支持继续追查，建议反向工程 + 专利墙补查。
