# 20-tesla-cloud verdict

## 候选基本信息（专利公开日 2021-06-08）
- 候选编号 / slug：20 / 20-tesla-cloud
- 类型 / 名称：产品 — Tesla 车云控制 / OTA（含 Fleet Telemetry 车-云上行通道）
- 组织：Tesla, Inc.（美国；中国市场亦有售）
- 初判命中 F#：F2, F3, F4, F5（基于"Tesla 在不可靠移动网络环境做车云通信，理应有可靠性优化"的假设）
- 公开度：低（车机内部协议栈不公开；车-云上行通道开源 = Fleet Telemetry）
- 时间窗：Fleet Telemetry 仓库自 2022 年开源、之后持续演进；OTA 通道自 2012 至今 — **均在专利公开日 2021-06-08 之后仍在运行**，时间窗满足

## 检索粗筛
见同目录 _sources.md（Phase 1 4 次 WebSearch + Phase 2 4 次 WebFetch，其中 developer.tesla.com 403）。

## F# 命中表（F1-F5）

| F# | 权 1 限定 | Tesla 公开证据 | 判定 |
|----|----|----|----|
| F1 | 发送端从「数据包长度/数目、到达间隔、突发性」中至少 1 项**自动**推断业务类型 | Fleet Telemetry 由车端**配置文件**指定要上报的 telemetry 字段集 + 频率；proto schema 无业务类型字段；无任何"由流量统计推断业务类型"的证据 | ✗ 未命中 |
| F2 | 由「网络状态 + 传输成功率 + 业务类型」三元组联合计算冗余包数量 | 公开实现中**完全没有"冗余包数量"概念** — 唯一可靠性原语是 ack；ack 未到则未 ack 数据全部重发（reactive）。无业务类型输入 | ✗ 未命中 |
| F3 | 由时延要求决定冗余包传输总时间 | 无时延 budget 输入；重连用指数退避（max 30s）— 与时延 budget 无关，是连通性补救 | ✗ 未命中 |
| F4 | 由「网络状态 + 总时间 + 冗余包数量」联合选择调度方法（随机度/最短/最长/均匀间隔） | 无调度方法选择 — 重发即"reconnect 后一次性补发缓冲队列"，固定 store-and-forward，与网络状态无动态调度耦合 | ✗ 未命中 |
| F5 | 按调度方法发送冗余包（proactive 冗余，非 ARQ） | **反向证据**：官方机制明确是"WebSocket 断连 → 车端 buffer ≥5000 条消息 / ≥2500 秒 → 重连后投递所有未 ack 数据"。这正是专利「背景技术」段所批判的"TCP 超时重传机制" reactive 范式 | ✗ 反向命中（明确不是 proactive 冗余）|

**核心反向证据 verbatim**（来自 fleet-telemetry Issue #319 + 官方 README 摘录）：
> "When there's loss of connectivity, the vehicle will buffer 5000 messages (at least 2,500 seconds of data), and once reconnected, all messages will be delivered."
> "the vehicle will resend data which is not acknowledged by the server, and when data is resent, all un-acked data will be resent."

按 SKILL.md 中 "F5 关键限定词与隐含约束" 的明文规则：
> "纯 ARQ / TCP 超时重传机制**不构成 F5 命中**——它们是 reactive 重传不是 proactive 冗余"

故 F5 不命中。F1-F4 亦均无支撑。

## 已检查文档清单

1. teslamotors/fleet-telemetry README（github.com）— WebFetch 成功
2. teslamotors/fleet-telemetry protos/vehicle_data.proto（raw.githubusercontent.com）— WebFetch 成功
3. bnxt.ai Tesla App Architecture 长文 — WebFetch 成功
4. fleet-telemetry Issue #319（断连缓冲行为）— WebSearch 摘录
5. developer.tesla.com/docs/fleet-api/fleet-telemetry — HTTP 403，curl 兜底亦 403（**工具受限**：Tesla 私有协议规格不可独立验证；但开源 server 实现已覆盖车-云上行通道，足以判定本专利权 1 不命中）
6. WebSearch q1-q4 + 补 1，覆盖：「FEC 冗余」「业务类型分类」「reverse engineering 协议栈」「adaptive FEC packet loss」「websocket reconnect buffer reliability」— 均无 Tesla 命中证据

## 最终判定 **第 5 档：已排除**

判定理由（非 0 命中草率排除）：
- 已掌握**真实反向证据**：Tesla 公开车-云通道使用 ack + buffer + reconnect 的 reactive 范式，明确属于专利"背景技术"段所批判、欲取代的方案；
- F1-F5 五要素全部不支持，且 F5 出现反向命中；
- 时间窗虽满足，但技术形态根本性偏离权 1 限定的 "proactive FEC + 业务类型自适应调度" 方案；
- 工具受限部分（Tesla 私有车内协议、内部 OTA 下行 PHY/MAC 优化）虽无法直接验证，但权 1 是「方法」类，定位的是"发送端"完整执行 F1-F5 五要素；只要可观察的车-云上行通道完全不符合，无据可证"侵权"；
- 推测性"内部可能也有 FEC"不构成证据 — 按 SKILL 纪律不外推。

## 升级路径（不适用 — 已落第 5 档）

如未来出现以下任一新证据，可重新评估升档：
- Tesla 公开新车型/新固件的车-云协议规格，明确包含「按消息业务类型（control / OTA / video / heartbeat）差分冗余度」逻辑；
- Tesla 在中国市场被诉本专利或答辩材料披露车端协议栈含 packet-level FEC + 业务类型联动；
- 反向工程社区（teslascope / wkjagt / TeslaLogger 等）抓包公开揭示车端在弱网下主动发送冗余副本（而非重发缺失副本）。

## 总结一句话
Tesla 公开车-云通道（Fleet Telemetry）使用「ack + 断连缓冲 5000 条 + 指数退避重连 + 未 ack 数据重发」的纯 reactive ARQ 范式，proto schema 无任何业务类型 / 冗余度 / 调度方法字段，正是本专利"背景技术"段所批判的方案，**落第 5 档：已排除**（反向证据，非 0 命中）。

---
*免责声明：本判定仅为基于公开资料的技术档位归类，不构成对侵权与否的法律意见。*
