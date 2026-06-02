# 16-asterfusion-helium verdict

## 候选基本信息
- 名称：Helium DPU 智能网卡（OVS 卸载，开放代码）
- 组织：星融元 Asterfusion
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（vSwitch 连 M VM + N≥2 网卡） | 公开资料不足 | "Helium SmartNIC adopts high-performance DPU architecture design ... offload and accelerate processing of virtual networks ... in scenarios such as cloud data centers"；公开资料仅描述**单块** DPU 网卡形态，未见"一台主机连接 N≥2 块独立 Helium 网卡 + vSwitch" | https://asterfusion.com/blog20230602-smartnic-open-source/ | Helium 支持云数据中心虚拟网络卸载，但 N≥2 跨卡拓扑无证据；单卡部署不满足 N≥2 整数下界 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 公开资料不足 | "搜索结果未包含 LACP bond / 跨卡链路聚合 / 流表冗余的具体实现信息"；README 明确无"多网卡配置 / 链路聚合 bond" | https://github.com/asterfusion/Helium_DPU/blob/main/README.en.md | 无任何"N 逻辑端口聚合为第一端口"映射证据 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合形成） | 公开资料不足 | README 明确无"LACP or link aggregation bonding" | https://github.com/asterfusion/Helium_DPU/blob/main/README.en.md | 无跨卡 LACP 聚合证据；亦无单卡多端口 bond 的明示，无法判反向 |
| F4（目标网卡流表 miss 触发） | 公开资料不足 | "traditional SmartNICs where the processing of the first packet is on the CPU, and the flow table down to the NIC chip" | https://asterfusion.com/blog20230602-smartnic-open-source/ | 存在 first-packet→流表下发 NIC 的慢路径语义迹象，但未明确 N≥2 网卡场景下"目标网卡 miss 触发"，仅可作弱信号 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 公开资料不足 | "full offloading of million-level flow tables and OVS control and forwarding planes"；但 README 明确无"flow table replication across cards / 跨卡流表复制" | https://github.com/asterfusion/Helium_DPU/blob/main/README.en.md | 仅单卡百万级流表卸载；无"向全部 N 个网卡冗余下发"证据（专利核心区分点缺失） |

## 已检查文档清单
- Asterfusion 官网 blog20230602「Introduction of an 100G open source DPU SmartNIC - Helium」（发布日 2023-06-02）：单块 Marvell OCTEON CN9670 DPU 网卡，OVS/百万级流表卸载 — https://asterfusion.com/blog20230602-smartnic-open-source/
- GitHub asterfusion/Helium_DPU README.en.md：仅单卡功能；明确无多网卡/LACP/跨卡流表复制/failover — https://github.com/asterfusion/Helium_DPU/blob/main/README.en.md
- Asterfusion 官网 blog20230601「Deploy Open Source DPU Smart NICs in Data Centers」：数据中心单卡部署 — https://asterfusion.com/blog20230601-dpu-open-source-100-200g/

## 最终判定

**第 4 档：公开资料不足（弱候选）**

判定依据（1-3 句，基于上表 F# 分布）：Helium 公开资料一致描述**单块** DPU 智能网卡做 OVS / 百万级流表卸载，仅 F4 有弱信号（first-packet → 流表下发 NIC 的慢路径语义）；而本专利的三个核心区分特征 F2（N 端口聚合映射）、F3（跨多卡 LACP 聚合）、F5（流表向全部 N≥2 网卡冗余下发以消单点故障）在官网 / GitHub / 第三方资料中**均无任何支撑证据**，命中比例显著 <60%。但同时也**无任何正向反向事实**（厂商未明示拒绝跨卡聚合，仅是公开资料未涉及），按"0 命中/资料缺失 ≠ 已排除"与"整数下界外推禁令"，不得判第 5 档，落第 4 档。

## 升级路径（仅落第3-4档时填）
- 取 Helium DPU 的 OVS 卸载技术白皮书 / 部署手册 / FusionNOS-Framework 文档，查是否支持"一台主机插多块 Helium 网卡 + 跨卡 LACP bond + 流表向全部网卡下发"的高可用拓扑。
- 检索星融元 Asterfusion 在 2023-06-06 之后申请的同主题专利（Google Patents 申请人检索），做机制比对常一步定档。
- 抓取 GitHub Helium_DPU 仓库内 OVS offload 相关源码 / 配置，Grep `bond` / `lacp` / `lag` / 多 NIC 流表同步关键词，确认是否存在跨卡冗余下发实现。

## 总结一句话
候选 16-asterfusion-helium 落第 4 档（公开资料不足-弱候选）：公开材料仅证明单卡 OVS/百万级流表卸载，专利核心区分点（跨多卡 LACP 聚合 + 流表向全部 N≥2 网卡冗余下发）无证据亦无反向事实。
