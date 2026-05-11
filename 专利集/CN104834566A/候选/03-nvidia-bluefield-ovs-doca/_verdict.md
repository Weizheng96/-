# Verdict — NVIDIA BlueField + DOCA + OVS-DOCA / ASAP² Direct

> 候选标识：`03-nvidia-bluefield-ovs-doca`
> 主体类型：S3（DPU 整机）+ S4（芯片 + SDK）
> 适用独立权：权 1（方法）、权 9（装置）、权 17（计算节点 / 整机）
> 候选分级：**P0**（依据：行业头部 + 公开宣传 OVS 加速）

## 1. 核心组织

| 责任主体 | 法律性质 | 角色 |
| --- | --- | --- |
| **NVIDIA Corporation（NASDAQ: NVDA）** | 上市公司 | DPU 设计 + DOCA SDK + OVS-DOCA 维护方 |
| **Mellanox Technologies, Ltd.（NVIDIA 2020 收购的子公司）** | NVIDIA 子公司 | 历史 BlueField 设计方 |

## 2. F1-F5 命中表（基于 NVIDIA 自身文档；遵守 §D 禁止上游继承推断规则）

| F# | 证据来源（NVIDIA 自身文档）| Verbatim 引文 | 命中类型 |
| --- | --- | --- | --- |
| F1 | [docs.nvidia.com/doca/sdk/multi-pmd-configuration](https://docs.nvidia.com/doca/sdk/multi-pmd-configuration/index.html) + [Virtual Switch on BlueField DPU](https://docs.nvidia.com/networking/display/bluefielddpuosv385/virtual+switch+on+bluefield+dpu) | "Open vSwitch (OVS)" 直接出现在 NVIDIA BlueField 用户手册多处 | **字面命中** |
| F2 | NVIDIA Multi-PMD Configuration 页面 | "Poll Mode Driver (PMD) threads are responsible for performing datapath processing of packets" + "Open vSwitch (OVS) assigns one core per NUMA node" + "A set bit in the [pmd-cpu-mask] mask means a PMD thread is created and pinned to the corresponding CPU core" | **字面命中** |
| F3 | NVIDIA Multi-PMD Configuration 页面 | "OVS automatically schedules port-queue tuples across available PMD threads, using only cores from the card's NUMA node by default" | **字面命中**（NUMA 状态属性 + 自动调度——对应从属权 2 alt 的"亲和性"路径）|
| F4 | NVIDIA 文档明确**未提及** auto-LB / pmd-auto-lb / load threshold / variance threshold / rebal-interval；仅提及 NUMA 默认调度 + 手动 pmd-rxq-affinity | （NVIDIA 文档无相应字面表述）| **公开资料不足**（不构成真反向证据；Step 5 §D 反向证据表第 1-3 行不命中——NVIDIA 没有写"OVS-DOCA does NOT support auto-LB"，只是"未提及"，属于⚠️作用域限定 / 未涉及）|
| F5 | NVIDIA Multi-PMD Configuration 页面 | "pmd-rxq-affinity=`"0:4,1:17"` ... Queue 0 is scheduled on core 4 ... Queue 1 is scheduled on core 17"（手动重分配 queue↔core）+ NUMA 自动调度也覆盖此 | **字面命中**（手动 pmd-rxq-affinity 即"调整线程所服务的端口"——满足 F5 字面要求；F5 不要求"自动"）|

**关键 caveat**（按 §D §D 禁止上游继承推断）：NVIDIA BlueField 出货时**捆绑 OVS-DPDK 软件包**（来自上游 OVS 项目），上游 auto-LB 特性技术上仍可被启用——但 NVIDIA **官方文档没有主动推荐启用**该特性。F4 不能由"上游提供"直接推断到 NVIDIA 候选——主 agent 严格遵守"禁止上游继承"规则，因此 F4 标"公开资料不足"。

## 3. 配置参数双引证

| 参数 | 默认值（NVIDIA 文档）| prose 引文 | 对应 F# |
| --- | --- | --- | --- |
| `pmd-cpu-mask` | 1 PMD per NUMA（NVIDIA 默认）| NVIDIA Multi-PMD config | F2 |
| `pmd-rxq-affinity="0:4,1:17"` | 未设置时按 NUMA 自动 | NVIDIA Multi-PMD config | F5 |
| `pmd-auto-lb` | （NVIDIA 文档未提及）| 不可双引证 | F4 公开资料不足 |

## 4. 时间线交叉验证

- NVIDIA BlueField-2 GA：2020-08（post-grant）
- BlueField-3 GA：2023（post-grant）
- DOCA SDK 1.x → 2.x → 2.9.x（最新）：均 post-grant
- NVIDIA Multi-PMD Configuration 页面：2024+（post-grant）
- 判定：所有证据 post-grant

## 5. §A 19 类源穿透扫描（精简版）

| # | 源类别 | 命中要点 |
| --- | --- | --- |
| 1 | 专利墙（NVIDIA H04L / G06F 13）| 工具能力受限——建议法务通过 IncoPat 补查；NVIDIA 在 SmartNIC 数据面调度方向有大量专利布局，存在自家专利墙佐证间接侵权可能 |
| 2 | 学术论文 | NVIDIA Mellanox 工程师在 SIGCOMM / NSDI / OSDI 多次发表 ASAP² Direct / OVS hardware offload 论文（如 "ASAP² Direct: efficient SR-IOV based virtualization"）；论文未直接讲 PMD auto-LB |
| 3 | 宣传材料 | docs.nvidia.com 多页（已抓取）；NVIDIA developer 博客 OVS-DOCA acceleration |
| 4 | 使用手册 | BlueField BSP 4.x 用户手册系列 — pmd-cpu-mask / pmd-rxq-affinity 字面命中 |
| 5 | 行业标准 | 不适用 |
| 6 | 联合案例（R-PARTNER）| NVIDIA × Red Hat × VMware × OpenShift × OpenStack 联合白皮书；含 ASAP² Direct + OVS-DPDK 集成案例 |
| 7 | 上游贡献归因（R-OPENSOURCE）| Mellanox / NVIDIA 多名工程师为 OVS / DPDK / mlx5 PMD 上游贡献者；建议本地 git clone OVS + grep `@mellanox.com\|@nvidia.com` |
| 8 | 开源 fork（R-OPENSOURCE）| NVIDIA 维护 OVS-DOCA fork；fork 自身 NEWS / 关键源文件需独立审 |
| 9 | 现有技术 | 同 OVS 上游候选；不构成 NVIDIA 抗辩 |
| 10-19 | 招聘 / 财报 / 案例 / 招标书等 | NVIDIA Inception 合作伙伴页、客户案例、Red Hat OpenShift × BlueField 联合 reference architecture（公开度高）|

## 6. 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 | **第 3 档：公开资料不足（强候选）** — F1/F2/F3/F5 字面命中；F4（auto-LB 触发条件）NVIDIA 自身文档未明示 | 1.等同三步法：F4 等同三步法——NUMA 默认调度提供"亲和性低于范围"alt path 的间接命中，但仍未达字面强度；2.反向证据：未触发；3.法律状态：Active 不降级；4.现有技术：未触发；5.R-STANDARD：未触发；6.豁免：未触发 | **第 3 档：公开资料不足（强候选）** |
| 权 9 | **第 3 档：公开资料不足（强候选）** — 同权 1 | 同上 | **第 3 档：公开资料不足（强候选）** |
| 权 17（整机权）| **第 3 档：公开资料不足（强候选）** — F17a（计算节点 = 硬件层 + 宿主机 + VM）：BlueField 卖给整机厂作为预装 DPU，构成"包含硬件层 + DPU OS 即宿主机 + 用户 VM"；F17b（K 处理器一一对应 K 转发线程）：BlueField 内部 ARM 多核 + PMD 线程一一对应可推 | 同上 + 整机权命中需 NVIDIA 出货整机或 OEM 整合 BlueField 后预装 OVS-DOCA 才完整命中——整机权命中度略低一档 | **第 3 档：公开资料不足（强候选）** |

## 7. 升级路径建议

NVIDIA 候选 F4 仅"公开资料不足"——**不应**判已排除。建议升级取证：
- (a) **联合白皮书深读**：Red Hat × NVIDIA OpenShift on BlueField 白皮书可能在配置示例段中含 `pmd-auto-lb` 推荐
- (b) **客户案例**：金融 / 电信客户使用 BlueField + OpenStack 的 reference architecture 经常包含 auto-LB 配置
- (c) **NVIDIA Networking Customer Success**：NVIDIA Cumulus Linux + OVS 客户案例
- (d) **法务通过 NVIDIA Inception 渠道获取 BlueField BSP 完整 default config**

## 8. 总结一句话

NVIDIA BlueField + DOCA + OVS-DOCA：F1/F2/F3/F5 字面命中（NUMA-aware PMD scheduling + pmd-cpu-mask + pmd-rxq-affinity 是 NVIDIA 自家文档明示），F4 因 NVIDIA 文档未主动推荐 auto-LB 标公开资料不足，落第 3 档（公开资料不足强候选）；建议联合白皮书 / 客户案例升级取证。
