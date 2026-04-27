# 候选 #6 中国电信 — 紫金 DPU（权 1 / 11 部署侧） — 资料索引

**主体类型**：部署方（中国电信 / 天翼云）
**适用独立权**：权 1 / 权 11
**说明**：本候选还有"芯片侧 权 35"层，那一层因紫金芯片固件不公开仍是 `公开资料没有足够证据`，本子文件夹只评估**部署侧**
**取证日期**：2026-04-27

---

## 五类源扫描结果

### 1. 专利
- WebSearch query：`"中国电信研究院" OR "天翼云科技" 申请 专利 智能网卡 DPU 流表 卸载 网络接口卡 多卡 链路聚合 2023 2024 2025`
- **结果**：**0 命中**与本专利同向的中国电信申请专利。返回的是中国电信智算 / 云网融合等综述
- **结论**：中国电信公开渠道无该方向专利布局指向

### 2. 学术论文
- 中国电信研究院在该方向无 SIGCOMM / NSDI / APNet / EuroSys 论文公开

### 3. 宣传材料 + 4. 使用手册（5 份本地存档）
- `2025_ai_network_wb.pdf`（4.9 MB）— 2025 AI 网络白皮书（第三方汇编 / 含天翼云 HPFS 部署描述）— **关键反向证据来源**
- `ctri-zhisuan-2024-report.pdf`（2.5 MB）— 中国电信研究院 / 天翼智库 2024 智算产业发展研究报告
- `ithome-zijin-dpu-launch-2022.html`（23 KB）— IT之家：紫金 DPU 2022-12-29 发布稿
- `tianyiyun-zijin-dpu-deep-2023.html`（28 KB）— 天翼云博客：深度解读紫金 DPU 软硬协同
- `tianyiyun-zijin-dpu-perf-2023.html`（27 KB）— 天翼云博客：算力基础设施升级 - 紫金 DPU 显身手
- `ctyun-zijin-dpu-news-2024.html`（1 KB，可能是 redirect / SPA 失败）
- 来源：[ithome.com](https://www.ithome.com/0/664/870.htm)、[cnblogs.com developer-tianyiyun](https://www.cnblogs.com/developer-tianyiyun/)、[2025 AI 网络白皮书](https://www.dyxnet.com/hk/wp-content/uploads/sites/2/2025/08/2025AI%E7%BD%91%E7%BB%9C%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf)

### 5. 行业标准
- 中国电信深度参与 CCSA、ITU-T、3GPP 等标准；但本专利保护的是实现细节，不在标准层面体现
- **结论**：标准层面无侵权对比基础

---

## 子 agent 审阅分配
- `2025_ai_network_wb.pdf` 第 4.x 节（紫金 DPU 部署描述） → 子 agent A（**关键反向证据**：bond mode 1 主备）
- `tianyiyun-zijin-dpu-deep-2023.html` → 子 agent B（深度解读）
- `tianyiyun-zijin-dpu-perf-2023.html` → 子 agent C（性能解读）
- `ithome-zijin-dpu-launch-2022.html` → 子 agent D（产品发布稿）
- `ctri-zhisuan-2024-report.pdf` → 子 agent E（智算产业研究报告）
