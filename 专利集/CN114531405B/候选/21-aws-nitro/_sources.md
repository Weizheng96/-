# 候选 #21 AWS Nitro System — 资料索引

**主体类型**：部署方（AWS EC2 / VPC）+ 芯片厂（自研 Nitro Card）
**适用独立权**：权 1 / 11（部署方法）+ 权 35（Nitro 芯片）
**取证日期**：2026-04-27

---

## 五类源扫描结果

### 1. 专利
- AWS / Amazon 名下 EC2 / Nitro 相关专利较多，但本专利核心要求是 LACP 二级聚合 + 同表分发；AWS Nitro 不走 OvS / 不走 LACP（私有协议），方向不重合
- 本轮不再单独深查

### 2. 学术论文
- AWS Nitro 内部论文：re:Invent 2024 NET402（PDF 8 MB，本地存档）
- SIGCOMM/NSDI/APNet：AWS 自身较少在该方向发表

### 3. 宣传材料 + 4. 使用手册（5 份）
- `nitro-overview.html`（262 KB）— [aws.amazon.com/ec2/nitro/](https://aws.amazon.com/ec2/nitro/) 官方 Nitro 概览
- `ena-nitro-perf.html`（35 KB）— ENA Nitro Performance Tuning 用户指南
- `enhanced-networking.html`（14 KB）— Enhanced Networking 用户指南
- `reinvent-2024-nitro-net402.pdf`（8 MB）— re:Invent 2024 NET402 "EC2 Nitro networking under the hood"（**关键**：技术深潜）
- `nitro-security-design.pdf`（508 KB）— AWS Whitepaper：The Security Design of AWS Nitro System

### 5. 行业标准
- AWS Nitro 自定义协议，不实现 IEEE 802.3ad LACP 标准
- ENA 是 AWS 私有 NIC 接口
- **结论**：AWS 不基于 LACP / OvS 开放标准

---

## 子 agent 审阅分配
- `nitro-overview.html` → 子 agent A（Nitro 整体架构）
- `reinvent-2024-nitro-net402.pdf` → 子 agent B（**关键**：re:Invent 2024 技术深潜）
- `ena-nitro-perf.html` → 子 agent C（ENA 多卡性能调优）
- `enhanced-networking.html` → 子 agent D（Enhanced Networking 架构）
- `nitro-security-design.pdf` → 子 agent E（Nitro 安全设计白皮书 — 含架构细节）
