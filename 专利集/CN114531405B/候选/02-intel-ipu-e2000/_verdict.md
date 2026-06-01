# 02-intel-ipu-e2000 verdict

## 候选基本信息
- 名称：IPU E2000（Mount Evans）流表硬件卸载
- 组织：Intel
- 类型：产品
- 初判命中 F#：F1, F2, F4, F5（取自 _meta.json）
- 公开（授权）日基准：2023-06-06（晚于此才计入；E2000 2022 量产，时间上有交叠，但因架构不符已剪枝）

## 检索粗筛（Phase 1 — react 串行 4×WebSearch，留痕见 _sources.md）

| query | 结果 |
| --- | --- |
| `Intel IPU E2000 Mount Evans OVS flow offload virtual switch` | 命中：E2000 是 Intel 首款 ASIC IPU，做 vSwitch/OVS 流表卸载，Google Cloud C3 部署 |
| `Intel IPU E2000 bonding LAG multiple NIC flow table offload LACP` | 无 E2000 专属命中，仅通用 LACP/bonding 文档 |
| `Intel IPU E2000 architecture single card uplink ports ... multiple NIC` | 关键命中：E2000 为单卡设备，卡上 two NIC ports + 带外管理口，卸载在单卡内部完成 |
| `"IPU E2000"/"Mount Evans" cross-card redundancy ... flow table sync multiple SmartNIC failover` | 无 E2000 专属命中，无跨多块独立网卡聚合 + 流表向全部网卡同步下发的资料 |

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（多虚机 + N≥2 块独立网卡） | 不命中 | "the card features two NIC ports and an out-of-band management port"（E2000 是单卡，两个端口在同一张卡上） | https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/ | 是"单卡含两端口"，非"vSwitch 连接 N≥2 块独立网卡"；架构层级不符 |
| F2（N 逻辑端口聚合为"第一端口"） | 公开资料不足 | —（4 query 未见 E2000 把多块独立网卡逻辑端口聚合为单一第一端口的描述） | — | 核心创新点，无证据 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合） | 公开资料不足 | — | — | 无 E2000 专属 LACP 跨卡聚合证据 |
| F4（卸载流表 miss 触发） | 部分相关/不足 | "leadership programmable packet processing engine to support ... vSwitch offload"（具备流表卸载，但未公开 miss 触发跨卡下发语义） | https://medium.com/intel-tech/intel-ipu-e2000-a-collaborative-achievement-with-google-cloud-eb1dda8c0177 | 单卡内 cache-miss-offload 常见，但缺"向全部 N 卡"语义 |
| F5（精确流表跨全部 N 块网卡同步卸载） | 公开资料不足 | —（无 E2000 把精确流表同步下发到聚合内全部独立网卡的资料） | — | 核心创新点，无证据 |

## 已检查文档清单
- ServeTheHome：Intel E2000 / Mount Evans 品牌与硬件形态（two NIC ports + 带外管理口、headless / multi-host 模式）
- Intel Tech (Medium)：E2000 与 Google Cloud 合作、vSwitch offload、200Gbps C3
- Intel IPU 产品页 / IEEE Xplore 10067333：E2000 架构（ASIC、可编程包处理流水线）
- 通用 LACP/bonding 与 SmartNIC 流表同步学术文献（无 E2000 专属内容）

## 最终判定 **第 5 档：已排除（粗筛阶段）**

判定依据：Intel IPU E2000（Mount Evans）是【单块 IPU/ASIC 卡】在卡内部承担 vSwitch/OVS 流表卸载（卡上两个 NIC 端口 + 带外管理口），属本专利背景技术明示区分的"单一网络接口卡内"硬件卸载方案。本专利核心架构限定是 vSwitch 连接 N≥2 块【独立网卡】、经 LACP 把 N 个逻辑端口聚合为"第一端口"(F2/F3)、并在 miss 时把精确流表【同步卸载至全部 N 块网卡】(F5) 以消除跨网卡单点故障——4 条 WebSearch 均未检索到 E2000 具备此跨多块独立网卡聚合 + 全网卡流表同步能力。属早剪枝条件 (iii) 架构层级不同。整数限定 N≥2 仅见单卡，禁止外推为字面命中。

（注：本判定为技术档位评估，不构成对专利权人的"已构成侵权"法律结论。）

## 总结一句话
Intel IPU E2000 是单卡内部 vSwitch 流表卸载，与本专利"跨 N≥2 块独立网卡 LACP 聚合 + 流表向全部网卡同步卸载"的核心架构不符，落第 5 档（已排除，粗筛阶段，架构层级不同）。
