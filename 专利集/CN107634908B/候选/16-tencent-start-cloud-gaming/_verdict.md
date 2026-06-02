# 16-tencent-start-cloud-gaming verdict

## 候选基本信息
- 名称：START 云游戏 / 腾讯先锋
- 组织：腾讯
- 类型：产品
- 初判命中 F#：F2, F4, F5
- 专利公开（授权）日：2021-06-08

## 检索粗筛（react 留痕）
- query 1：`腾讯 START 云游戏 先锋 串流 弱网 FEC 冗余 抗丢包` → 命中腾讯 START 团队 NSDI 2024 三项成果（Pudica 拥塞控制 / AUGUR 多路径 / Hairpin 丢包恢复），强相关。
- query 2：`腾讯 START Hairpin NSDI 2024 云游戏 FEC 冗余 网络状态 自适应 重传` → 命中官方文 + Hairpin MDP 建模 / 实时调 FEC，强相关。
- query 3：`Hairpin NSDI 2024 cloud gaming FEC redundancy retransmission Markov decision process paper Tencent` → 命中 Hairpin (NSDI'24)、Tooth (NSDI'25) 论文 PDF，强相关。
- 时间窗：均为 2024/2025 公开，> 2021-06-08，合规。未早剪枝。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（业务类型由数据流特征识别） | 资料不足（弱） | "the frame length can be readily acquired … from the application-layer frame length and transmission-layer network loss pattern to per-frame redundancy"（Tooth 用帧长=包数这一数据流特征→冗余率） | https://zilimeng.com/papers/tooth-nsdi25.pdf | Hairpin 为单一云游戏流，**未**做"业务类型"识别；Tooth 用帧长(包数)这一数据流特征但映射对象是冗余率而非"业务类型"。专利 F1 要求由流特征推断"业务类型"——无直接对应。Tooth 厂商匿名"Company W"，非明示 START。资料不足。 |
| F2（冗余包数量依 网络状态+传输成功率+业务类型 三输入自适应） | 等同（部分缺失第三输入） | "β(α,B,RTT,t)=k· (RTT/t) ·β0(α,B)"，其中 α 为丢包率（=网络状态/传输成功率逆量），并"dynamically adjusting FEC parameters by real-time monitoring network conditions including RTT and packet loss events" | https://zilimeng.com/papers/hairpin-nsdi24.pdf ; https://ur.tencent.com/article/1481 | 命中"按网络状态(丢包率α/RTT)+传输成功率自适应算冗余量"两输入；但**缺"业务类型"第三输入**（云游戏单业务，无按业务类型分级）。专利 F2 硬约束三输入同时依赖——本候选仅两输入，故判等同而非字面。 |
| F3（时延要求→冗余传输总时间） | 等同 | "with an RTT of 10-20 ms and a deadline of 50-150 ms, multiple retransmissions are tolerable … The ratio of RTT and remaining time t indicates the potential number of (re)transmissions"（由 deadline 时延要求得出剩余可用时间 t） | https://zilimeng.com/papers/hairpin-nsdi24.pdf | deadline(时延要求)→剩余传输时间 t，对应"由时延要求得冗余传输总时间"。等同命中。 |
| F4（调度方法由 网络状态+传输总时间+冗余数量 生成） | 等同 | "we propose Hairpin … finds the optimal combination of data packets, retransmissions, and redundant packets over multiple rounds of transmissions"；"a Markov chain-based optimization algorithm to efficiently improve both the DMR and BWC"（按网络状态+剩余时间 t+冗余率联合规划多轮(重)传调度） | https://zilimeng.com/papers/hairpin-nsdi24.pdf | MDP 按网络状态(α,RTT)+传输总时间(t,deadline)+冗余量联合生成多轮(重)传调度方案，对应"获取冗余包调度方法"。等同命中。 |
| F5（按调度方法发送冗余包） | 等同 | "finds the optimal combination of data packets, retransmissions, and redundant packets over multiple rounds of transmissions, which significantly reduces the bandwidth cost while ensuring the end-to-end latency requirement"（按上述最优组合实际发送数据/重传/冗余包） | https://zilimeng.com/papers/hairpin-nsdi24.pdf | 按 MDP 得出的调度发送冗余/重传包，对应"按调度方法发送冗余数据包"。等同命中。 |

## 已检查文档清单
- Hairpin: Rethinking Packet Loss Recovery in Edge-based Interactive Video Streaming（NSDI 2024，作者含 Tencent；START 云游戏生产部署，降带宽 40% / 降 deadline miss 32%）— https://zilimeng.com/papers/hairpin-nsdi24.pdf
- 犀牛鸟硬核｜腾讯 START 团队三项成果入选 NSDI 2024（2024-05-13，官方确认 Pudica/AUGUR 生产部署、Hairpin 动态调 FEC + 初传/重传差异化冗余）— https://ur.tencent.com/article/1481
- Tooth: Fine-Grained FEC in Cloud Gaming Streaming（NSDI 2025，per-frame 冗余率按帧长+网络丢包分布；厂商匿名"Company W"，仅作同领域佐证）— https://zilimeng.com/papers/tooth-nsdi25.pdf

## 最终判定
**第 3 档：公开资料不足（强候选）**

判定依据（1-3句）：Hairpin 系腾讯 START 云游戏生产部署的丢包恢复机制，F3/F4/F5 三步（时延要求→传输总时间→MDP 调度→按调度发送冗余/重传包）与权 1 链路等同命中，F2 命中"按网络状态+传输成功率自适应算冗余量"两输入（缺"业务类型"第三输入故判等同非字面），F1（由数据流特征识别业务类型）仅 Tooth 用帧长这一流特征部分沾边且厂商匿名、资料不足。命中(字面/等同)的 F# 为 F2/F3/F4/F5 共 4/5（80% ≥60%），无任何反向证据。按五档定义，**第 2 档须 F1-F5 全部命中**，而 F1 仅"资料不足"（非命中、亦非反向）→ 不符第 2 档；F1 无反向 → 不入第 5 档；命中比 ≥60% 且无反向 → 落**第 3 档（强候选）**。本候选与 05-netease-nertc 并列为证据最充分的强候选。

## 升级路径（仅 3-4 档）
- 补 F1 即可升至第 2 档（确认-中）：取证 Hairpin/START 是否对"控制信令流 vs 画面流 vs 音频流"按业务类型分级设不同冗余目标（若是→F1 与 F2 第三输入"业务类型"补齐，升第 2 档；若进一步字面坐实三输入→第 1 档）。
- 确认 Tooth 的"Company W"是否即腾讯 START（若是，帧长→冗余的"数据流特征→冗余"链路可强化 F1）。

## 总结一句话
腾讯 START 云游戏 Hairpin 丢包恢复机制 F3/F4/F5 等同命中、F2 两输入等同（缺业务类型）、F1 资料不足，命中 4/5 且无反向证据，落第 3 档（强候选，与 NeRTC 并列证据最充分），不构成法律侵权结论。
