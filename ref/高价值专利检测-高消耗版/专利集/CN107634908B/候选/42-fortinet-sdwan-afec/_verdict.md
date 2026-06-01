# 42-fortinet-sdwan-afec verdict

## 候选基本信息（专利公开日 2021-06-08）

- 类型：产品 / 商业部署
- 名称：FortiGate SD-WAN **Adaptive Forward Error Correction (Adaptive FEC)**
- 组织：Fortinet, Inc.（NASDAQ: FTNT，加拿大 / 美国跨国企业）
- 形态：FortiGate 防火墙 / SD-WAN 网关设备内 FortiOS 操作系统的内置 SD-WAN 功能。**FortiOS 7.0.2** 首次引入（2021-Q4 之后 GA），延续至 7.4 / 7.6 / 8.0 持续增强（8.0 新增 ToS/DSCP 二轮匹配 + negate 选项）。
- 时间窗：**满足**——Adaptive FEC 在 FortiOS 7.0.2（2021-Q4 之后）公开商用，晚于专利公开日 2021-06-08
- 命中场景（来自专利"潜在应用场景"）：**场景 3**（DC 间 / 跨广域控制消息保活，对应 FortiGate IPsec/SD-WAN overlay 部署）+ **场景 6**（VoIP / 实时音视频会议——官方示例显式以 ALL_UDP / VoIP 为典型对象）。次要：场景 4（远程操控 / 工业控制）。
- 技术形态对照专利"发送端"主体：FortiGate 设备作为 IPsec/SD-WAN 隧道的 **发送端 (egress)**，对 base packets 生成并发送 redundant (parity) packets — 符合权 8（设备形态）适用主体。

## F# 命中表（F1-F5）

| F# | 专利限定要点（verbatim 核心） | Fortinet Adaptive FEC 对应实现 | 命中 |
|----|------------------------------|------------------------------|-----|
| **F1**（业务类型识别 — 必须基于"数据流特征变量"，从 {缓存中待传输包长度数目 / 网络中传输包长度数目 / 到达间隔 / 数据突发性} **至少 1 项** 由发送端自动统计推断） | Adaptive FEC 区分 / 选择业务的方式有 **两条且仅两条**：(a) `config firewall policy` 中由管理员显式配置 `set service "ALL_UDP" / set fec enable`（端口 / 协议 / 服务规则匹配）；(b) `config vpn ipsec fec` mappings 中按 **ToS / DSCP 标志位**二轮匹配（FortiOS 8.0 原文："In the first round of matching, traffic will be matched against packet-loss, latency, and bandwidth. In the second round of matching, the ToS value and mask will be used."）。**全部 CLI 字段 / 文档段落中没有任何**关于"缓存队列待发包长度 / 网络在途包长度 / 包到达间隔 / 突发性"等流量统计特征的输入。 | **未命中**（关键差异 — 路径完全不同；Fortinet 走的是专利从属权 4 "应用制定的业务类型"路径，**不是**权 1 的 F1 统计推断路径） |
| **F2**（冗余包数量 ← 网络状态变量 + 传输成功率 + 业务类型 **三元组联合** 计算） | base:redundant 数量由 `mappings` 表项决定，可叠加触发条件：`packet-loss-threshold` / `latency-threshold` / `bandwidth-up-threshold` / `bandwidth-down-threshold` / `bandwidth-bi-threshold`（网络状态 + 成功率代理）+ `tos / tos-mask`（DSCP 类别 hint）。运行时 `diagnose sys sdwan health-check` 实时输出当前 packet-loss / latency / jitter / bandwidth-up / bandwidth-dw，按 mappings 表项 top-to-bottom 匹配定 base:redundant。 | **部分命中**（网络状态 √；传输成功率 ≈ packet-loss √；"业务类型"仅以 ToS/DSCP 显式 hint 形式参与而非 F1 推断结果——若严格读取权 1 要求 F2 的业务类型来源于 F1，则链条断裂；若放宽读取"业务类型可来自任意源"则部分命中） |
| **F3**（冗余包传输总时间 ← 预先获取的**时延要求**） | 文档存在两个 timeout：`fec-send-timeout`（默认 8）、`fec-receive-timeout`（默认 5000ms，接收侧重组等待 timeout）。这是 FEC 编 / 解码块层的**本地常量**，**非由业务时延要求动态推导**。`latency-threshold` 存在，但只作"是否升档冗余比例"的二元判据，**不参与计算"传输总时间"窗口**。 | **未命中**（无 "时延要求 → 总时间"推导链） |
| **F4**（调度方法 ← 网络状态 + 总时间 + 冗余包数量 三元组联合，从 {随机度策略 / 最短时间 / 最长时间 / 均匀时间} **至少 1 种** 中选择） | 文档无任何关于"redundant packets 之间的发送时机 / 间隔 / 调度策略"的描述。NPU 路径下 parity packets 在 base 块完成后立即生成并发出（事件驱动，无 CLI 字段控制策略集合）。**没有随机度 / 最短 / 最长 / 均匀四选一的等价机制**。 | **未命中**（关键差异） |
| **F5**（按调度方法发送冗余包） | FortiGate Adaptive FEC 确实做 **主动 packet-level 冗余**（生成 parity 包发送，非 ARQ 重传）— 此动作语义层面与本专利"主动冗余传输"概念一致。但因 F4 未命中，"按调度方法"前缀不成立。 | **部分命中**（"发送冗余包"动作存在 √；"按调度方法"不成立 ✗） |

**总评**：F1 / F3 / F4 三项权 1 关键限定**未命中**；F2 / F5 部分命中。权 1 整体**不构成字面侵权**；考虑等同原则，F1（流量统计推断 vs 应用层 hint）和 F4（调度方法集合 vs 无调度概念）的差异不是"路径不同 / 结果相同"的等同关系，而是"输入维度不同 + 算法步骤不存在"，因此**也难以构成等同侵权**。

## 已检查文档清单

1. FortiOS 7.0.2 Adaptive FEC 官方文档（首次引入版本）— https://docs.fortinet.com/document/fortigate/7.0.0/sd-wan-new-features/169010/adaptive-forward-error-correction-7-0-2
2. FortiOS 7.6.0 Adaptive FEC Administration Guide — https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/169010/adaptive-forward-error-correction（完整 CLI + diagnose 输出）
3. FortiOS 7.6.0 SD-WAN Architecture for Enterprise — FEC 概念章节
4. FortiOS 8.0.0 Adaptive FEC Administration Guide（含 ToS/DSCP 二轮匹配 + negate 选项）— https://docs.fortinet.com/document/fortigate/8.0.0/administration-guide/169010/adaptive-forward-error-correction
5. FortiOS 8.0.0 ToS matching and negate options on adaptive FEC profiles (NEW) — https://docs.fortinet.com/document/fortigate/8.0.0/administration-guide/187229/tos-matching-and-negate-options-on-adaptive-fec-profiles-new
6. （网检 verify）公开检索未发现 Fortinet 在 adaptive FEC 上的 US/EP/CN 专利记录

## 最终判定 **第 4 档：架构同 / 关键技术特征缺失，无法证立等同**

依据：

- **架构同**：都是"SD-WAN/VPN 隧道发送端做主动 FEC、按链路状态动态调整 base:redundant 比例"——本专利场景 3（DC 间 / 跨广域控制消息保活）与 Fortinet 官方示例（IPsec overlay + SD-WAN health-check + UDP/VoIP）在系统形态上高度对应。
- **关键技术特征缺失**：
  - **F1 缺失**：业务类型识别走 policy + ToS/DSCP 路径，**不是**专利限定的"由发送端从数据流统计特征自动推断"路径——专利在权 1 与从属权 4 中明确区分这两条路径，Fortinet 完全走从属权 4 形态。
  - **F3 缺失**：无"时延要求 → 冗余包传输总时间"的推导；FEC encode/receive timeout 是本地常量。
  - **F4 缺失**：无"调度方法选自随机/最短/最长/均匀"的等价机制；redundant packets 紧随 base 块完成后立即发出，无可配置的调度策略集合。
- **不构成等同**：F1 / F4 的差异属于"输入维度 + 算法步骤" 层面的实质区别，非简单的"等效替换"。

## 升级路径（若证据补强可升至 3 档"高度疑似 / 部分命中"）

需补充以下任一证据：

- (a) 发现 FortiOS 某版本 CLI / 内部白皮书 / 抓包 trace 中存在按 **包长 / 包到达间隔 / 队列突发**等流量统计字段触发 FEC 适配的隐藏机制；
- (b) 发现 redundant packets 之间的发射顺序 / 间隔由可配置的策略集合控制（如类似 `fec-schedule-mode {random | shortest | longest | uniform}` 的 CLI 字段）；
- (c) 抓取 FortiGate 实机 packet trace 反向证明 "FEC 编码窗口 + 包间隔"是按业务时延要求实时计算而非静态 timeout。

上述三项**目前公开材料中均无证据**——若专利权人有进一步评估意图，应优先对实机做 packet-level 取证而非依赖官方文档。

## 总结一句话

Fortinet SD-WAN Adaptive FEC 在系统架构（发送端主动 FEC + 链路状态触发动态比例）上与 CN107634908B 权 1 同构，但其业务类型识别走 policy + ToS/DSCP 显式 hint 路径（非 F1 流量统计推断）、无"时延要求 → 总时间"推导（缺 F3）、无调度方法四选一（缺 F4），关键技术特征链条断裂，**落第 4 档：架构同 / 关键技术特征缺失，无法证立等同**。

---

**免责声明**：本判定基于 Fortinet 公开技术文档（FortiOS 7.0 / 7.6 / 8.0 Administration Guide）的字面阅读与专利权 1 的逐项要件比对，仅作为"是否构成可起诉的技术线索"的初步技术档位评估；不构成法律意见，不替专利权人下"已构成侵权 / 未构成侵权"的法律结论。最终侵权与否需结合实机取证、专利诉讼程序与具体判例由专利律师与法院认定。
