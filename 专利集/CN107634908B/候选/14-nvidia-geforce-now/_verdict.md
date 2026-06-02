# 14-nvidia-geforce-now verdict

## 候选基本信息
- 名称：GeForce NOW / 组织：NVIDIA（NASDAQ:NVDA） / 类型：产品 / 初判命中 F#：F2, F4, F5 / 专利公开（授权）日：2021-06-08

## 检索粗筛（react 留痕）
- WebSearch①：`NVIDIA GeForce NOW streaming FEC packet loss adaptive redundancy network` → 命中 NVIDIA L4S 官方文档（拥塞码率自适应，非冗余调度）。
- WebSearch②：`GeForce NOW cloud gaming forward error correction FEC redundant packets network condition adaptive` → 证实 GeForce NOW 使用 FEC（二手）；通用 adaptive FEC = 按丢包率/SLA 调冗余比（单因子）。
- WebSearch③：`NVIDIA cloud gaming streaming patent FEC redundancy adaptive bitrate latency 2022 2023` → 命中 NVIDIA 自有专利 US10230405。
- 结论：粗筛通过（领域契合、确认在用 FEC），进入深抓。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（业务类型由数据流特征自动识别） | 资料不足 | 所查 NVIDIA 自有专利 US10230405 未描述业务类型识别机制（**注：这是"该专利未提及"，非该专利正向声明"不做业务类型识别"**） | https://patents.google.com/patent/US10230405B2/en | 单篇 2019 年专利未提及 ≠ GeForce NOW 正向排除该特征；按规则"公开资料未提及=资料不足，非反向证据"。GeForce NOW 现网（post-2021）是否按业务类型分流冗余，无公开资料，资料不足 |
| F2（冗余包数量按"网络状态+传输成功率+业务类型"三输入） | 资料不足（弱）/部分 | 权1 verbatim："changing said FEC repair rate at least once during said streaming session based on a number of unrecovered source packets and a number of unused repair packets"；adjuster 输入含未恢复源包数（≈丢包/成功率）+ 未用修复包数 + 网络稳定性 | https://patents.google.com/patent/US10230405B2/en | 命中"网络状态+传输成功率"二输入，但缺业务类型第三输入；属丢包反馈驱动调"修复比率(rate)"，与权1调"冗余包数量(count)+调度方法"路径不同——属实现路径不同，**不构成反向证据** |
| F3（时延要求→冗余传输总时间） | 资料不足 | 所查专利 US10230405 未描述"时延要求→传输总时间"环节（"该专利未提及"，非正向否定） | https://patents.google.com/patent/US10230405B2/en | 单篇专利未提及 ≠ 正向反证；资料不足，不外推 |
| F4（冗余调度方法生成：网络状态+总时间+冗余数量三输入） | 资料不足 | US10230405 聚焦调"修复比率(repair rate)"而非生成"冗余包调度方法"；但其侧重点 ≠ 对 GeForce NOW 现网架构的正向否定 | https://patents.google.com/patent/US10230405B2/en | rate vs count+scheduling 属实现路径不同（非反向）；且该专利非 GeForce NOW 现网完整机制的权威披露，资料不足 |
| F5（按调度方法发送冗余包） | 资料不足 | 发送 repair packets（"each of said frames comprising a plurality of source packets and at least one repair packet"）但无"按调度方法"发送的公开描述 | https://patents.google.com/patent/US10230405B2/en | 有 FEC 修复包发送动作，但 F5 的"按调度方法"限定无对应公开证据，资料不足 |

## 已检查文档清单
- NVIDIA L4S 串流质量设置官方文档 — https://nvidia.custhelp.com/app/answers/detail/a_id/5522/ （L4S=ECN 拥塞标记触发码率自适应，非冗余包数量/调度）
- "What is Forward Error Correction... Gaming" TESmart 博客 — https://www.tesmart.com/blogs/news/what-is-forward-error-correction-how-does-it-improve-gaming-experience （确认 GeForce NOW 使用 FEC；机制描述为按丢包率调冗余比）
- US10230405B2「System and method of forward error correction for streaming media」(assignee NVIDIA Corp, 授权 2019-03-12) — https://patents.google.com/patent/US10230405B2/en （NVIDIA 自有同主题 primary 证据）
- PatSnap 云游戏低延迟专利族概览 — https://www.patsnap.com/resources/blog/articles/cloud-gaming-sub-100ms-latency-patent-landscape-2026/ （NVIDIA 族集中于 frame-rate capping / RTVL 码率自适应）

## 最终判定
**第 4 档：公开资料不足（弱候选）**

判定依据（1-3句）：GeForce NOW 与本专利同属"发送侧实时串流 FEC"抽象层，确在用自适应 FEC，无任何正向反向事实证明它"不做"权 1 机制，故不入第 5 档。所查 NVIDIA 自有专利 US10230405（2019，pre-grant）显示其按丢包反馈调"修复比率(rate)"，仅 F2 命中"网络状态+传输成功率"两输入（缺业务类型第三输入）；F1/F3/F4/F5 在可得公开资料中均"未提及"——按规则**"单篇专利未提及/通用机制反推 = 资料不足，非反向证据"**，且 rate-vs-count 属实现路径不同（非反向）。命中(字面/等同)占比 0/5、<60%，无针对该候选本身的反向事实，故落**第 4 档**而非第 5 档。〔复核更正：原 sub-agent 把"该专利未提及 F1/F3/F4"当作"反向证据"判第 5 档，违反"未提及≠反向"硬规则，已下修为第 4 档。〕

## 升级路径（仅3-4档）
- 取 GeForce NOW 现网（post-2021）工程披露 / NVIDIA 近年串流专利，核验是否按"业务类型/数据流特征"差异化冗余 + 由时延驱动生成冗余包调度方法；若坐实 → 可升第 3/2 档。
- 反向若取到 NVIDIA 官方明示"GeForce NOW 串流仅调 FEC 比率、不按业务类型分级、不做时延驱动冗余调度"的正向声明 → 方可升级为第 5 档（已排除）。

## 总结一句话
GeForce NOW 用丢包反馈自适应 FEC（调修复比率），仅 F2 两输入部分命中、F1/F3/F4/F5 公开资料不足且无针对其本身的反向事实，落第 4 档（资料不足-弱）。
