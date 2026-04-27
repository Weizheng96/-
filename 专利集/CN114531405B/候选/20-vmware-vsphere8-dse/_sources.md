# 候选 #20 VMware vSphere 8 U3 / NSX / DSE — 资料索引

**主体类型**：软件发布方（ESXi、NSX、vSphere Distributed Switch）
**适用独立权**：权 36（计算机存储介质）
**取证日期**：2026-04-27

---

## 五类源扫描结果

### 1. 专利
- 已经在 v3 报告里跑过：VMware/Broadcom 名下没有 multi-DPU 同表分发方向的专利
- 本轮不再重复

### 2. 学术论文
- VMware 不在该方向发表过顶会论文（v2 已确认）

### 3. 宣传材料 + 4. 使用手册（5 份本地存档）
- `vsphere-dse-techdocs.html`（48 KB）— Broadcom TechDocs：vSphere Distributed Services Engine 介绍（**关键文档**：dual-DPU 配置说明）
- `vsphere-8u3-announcement.html`（95 KB）— vSphere 8 Update 3 发布稿（2024-06-25）
- `vsphere-8u3-blog-detailed.html`（103 KB）— What's New in vSphere 8 Update 3（2024-07-12）
- `vsphere-lacp-techdocs.html`（50 KB）— Broadcom TechDocs：vDS 上的 LACP 配置
- `nvidia-bluefield-vsphere8-whitepaper.pdf`（908 KB）— NVIDIA-VMware 联合白皮书"Optimizing Networking and Security Performance Using VMware vSphere and NVIDIA BlueField DPU"

### 5. 行业标准
- vDS 实现 IEEE 802.3ad LACP（vSphere LACP 配置文档）
- 但 LACP 是在 host vSphere kernel 层，不是在 DPU 内部
- **结论**：vDS LACP 不命中专利 F3"NIC 内部物理端口基于 LACP 聚合"

---

## 子 agent 审阅分配
- `vsphere-dse-techdocs.html` → 子 agent A（**关键**：dual-DPU active/standby 配置）
- `vsphere-8u3-announcement.html` → 子 agent B（vSphere 8 U3 发布稿）
- `vsphere-8u3-blog-detailed.html` → 子 agent C（What's New 详细）
- `vsphere-lacp-techdocs.html` → 子 agent D（vDS LACP 配置层级）
- `nvidia-bluefield-vsphere8-whitepaper.pdf` → 子 agent E（NVIDIA-VMware 联合白皮书）
