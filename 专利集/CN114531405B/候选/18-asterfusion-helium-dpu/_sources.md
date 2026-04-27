# 候选 #18 星融元 Helium DPU — 资料索引

**主体类型**：芯片厂 + 软件 / 固件发布方（开源）
**适用独立权**：权 35（芯片系统）+ 权 36（计算机存储介质）
**取证日期**：2026-04-27

---

## 五类源扫描结果

### 1. 专利
- WebSearch query：`"Asterfusion" OR "星融元" patent assignee DPU OVS bond LACP 流表 多卡 2023 2024 2025`
- **结果**：**0 命中**与本专利同向的星融元专利申请（仅返回 Red Hat OVS 文档与综述）
- **结论**：星融元在该方向无公开专利布局

### 2. 学术论文
- WebSearch query：`"Asterfusion Helium" SIGCOMM OR NSDI OR APNet OR EuroSys paper DPU OVS multi-NIC`
- **结果**：**0 命中**星融元在 SIGCOMM/NSDI/APNet/EuroSys 的论文
- **结论**：星融元未在顶会发表过 Helium DPU 多 NIC + LACP + 同表分发相关论文

### 3. 宣传材料（本地存档）
- `asterfusion-helium-product-page-en.html`（67 KB）— 官方产品页
- `asterfusion-helium-2024-vnf-blog.html`（85 KB）— 官方 VNF 卸载验证博客（2024-08）
- 来源：[asterfusion.com/en/product/helium-dpu/](https://asterfusion.com/en/product/helium-dpu/)、[asterfusion.com/blog20240808-helium-vnf/](https://asterfusion.com/blog20240808-helium-vnf/)

### 4. 使用手册 / 技术文档（本地存档）
- `helium-readme-en.md`（6 KB）— GitHub 主仓 README
- `helium-et2500-readme-en.md`（8.6 KB）— ET2500 子目录 README
- `helium-ec2000-datasheet.pdf`（208 KB）— EC2000 datasheet
- 来源：[github.com/asterfusion/Helium_DPU](https://github.com/asterfusion/Helium_DPU)、[Helium DPU EC2000 datasheet](https://data.nag.wiki/Asterfusion/datasheet/Helium%20DPU%20EC2000.pdf)

### 5. 行业标准 / 测试规范
- IEEE 802.3ad LACP：Helium DPU 是 OCTEON TX2/TX3 系列，硬件层面是否实现 802.3ad 取决于 Marvell OCTEON 芯片本身的 NIC 微码；开源代码层面**未见 LACP 实现路径**
- 综述：星融元开源 Helium 是基于 Marvell OCTEON TX2 CN9670（4×25G）和 OCTEON TX3 CN10K（2×100G）；硬件 LAG 通常由 Marvell 微码实现，但**开源仓库不暴露多 NIC + 二级聚合实现**
- **结论**：开源代码不实现 LACP；硬件层面是否在 NIC 内做 LACP 取决于 Marvell 自身，与 Helium 开源软件层无关

---

## 子 agent 审阅分配
- `helium-readme-en.md` + `helium-et2500-readme-en.md` → 子 agent A（开源仓库结构 + 模块清单）
- `asterfusion-helium-2024-vnf-blog.html` → 子 agent B（VNF 卸载验证 2024-08）
- `helium-ec2000-datasheet.pdf` → 子 agent C（产品 datasheet）
- `asterfusion-helium-product-page-en.html` → 子 agent D（产品页）
