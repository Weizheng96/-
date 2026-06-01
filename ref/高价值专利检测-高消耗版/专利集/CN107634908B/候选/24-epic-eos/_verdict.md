# 24-epic-eos verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选 NN: 24
- 类型: 产品
- 名称: Epic Online Services (EOS)
- 组织: Epic Games
- 初判命中 F#: F2, F3, F4, F5
- 公开度: 中（开发者文档公开 API 契约，SDK 二进制实现不公开）
- 一句话定位: Epic 游戏后端服务，开发者文档披露 P2P 通信传输层 API 契约。
- 评估文档时间窗：EOS 官方 API 文档为持续维护的现行版本，远晚于 2021-06-08 专利公开日，**时间窗有效**。

## F# 命中表（F1-F5）

| F# | 权 1 verbatim 限定 | EOS 公开证据 | 判定 |
| --- | --- | --- | --- |
| F1（业务类型识别 — 基于发送端缓存/在途数据包长度/数目、到达间隔、突发性 4 项之一） | "数据流特征变量"必须由发送端自动从真实流量统计得到 | `EOS_P2P_SendPacketOptions` 不含业务类型字段，也不含任何用于推断业务类型的流量统计接口；应用层调用 `EOS_P2P_SendPacket` 时仅传 socket / channel / reliability 枚举，**无任何业务类型语义注入** | **不命中**（连应用 hint 都没有，更没有发送端自动推断） |
| F2（冗余包数量 — 三元组联合：网络状态 + 成功率 + 业务类型） | 三个输入均需参与计算 | 文档措辞 "Packets **may** be sent multiple times" 是条件性 ARQ（检测到丢失后重传），不是发送前主动生成 n 份冗余副本；API 不暴露"网络状态变量""期望成功率""业务类型"任一输入 | **不命中**（机制为 ARQ；权 1 三元组输入全缺） |
| F3（冗余包传输总时间 — 来自时延要求） | n 个冗余包累计发送窗口长度 | API 没有时延要求字段；`bAllowDelayedDelivery` 仅决定连接未建立时丢包/缓冲，与冗余总时间窗无关 | **不命中** |
| F4（调度方法 — 三元组联合：网络状态 + 总时间 + 冗余包数量） | 在随机/最短/最长/均匀中选 ≥1 | EOS 暴露的仅是 reliability 枚举三档，没有调度方法选项、也没有用于调度决策的网络状态输入 | **不命中** |
| F5（按调度方法发送冗余包） | proactive 主动冗余传输 | EOS 可靠模式语义是 ACK 触发的条件重传（ARQ），**不是 proactive FEC**；权 1 反向证据信号 | **不命中**（机制不符） |

初判将 F2/F3/F4/F5 标为命中，是基于"EOS 是低时延 P2P 网络层产品"的领域接近性推断。深抓证据后，权 1 五特征**全部不命中**，初判被推翻。

## 已检查文档清单

1. EOS 官方 API — `EOS_EPacketReliability` 枚举：https://dev.epicgames.com/docs/en-US/api-ref/enums/eos-e-packet-reliability （本地：`eos-packet-reliability-enum.html`）
2. EOS 官方 API — `EOS_P2P_SendPacketOptions` 结构体：https://dev.epicgames.com/docs/en-US/api-ref/structs/eos-p-2-p-send-packet-options （本地：`eos-sendpacket-options.html`）
3. Unreal Engine 官方文档 — Networking Overview：https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine （本地：`ue-networking-overview.html`）
4. WebSearch 检索结果索引（4 次）：见 `_sources.md`

## 最终判定 **第 5 档：已排除**

满足"第 5 档"硬条件中的 **(a) 真反向证据**：

- 反向证据 1（机制反向）：EOS 公开文档定义 ReliableUnordered / ReliableOrdered 为 "Packets **may** be sent multiple times" —— "may" 条件性措辞 + 缺少"主动一次发 n 份"语义，明确为 ACK 触发的 ARQ / 重传机制，与权 1 的**主动 FEC 冗余传输**机制范畴不同。专利说明书已显式声明 "纯 ARQ / TCP 超时重传机制不构成 F5 命中"。
- 反向证据 2（输入参数反向）：`EOS_P2P_SendPacketOptions` 字段全集（10 字段）中**完全不存在**权 1 必备的 5 类输入（业务类型 / 时延要求 / 期望成功率 / 冗余包数量 / 调度方法 / 网络状态变量），API 契约上**结构性地无法**执行权 1 的方法步骤。
- 反向证据 3（生态反向）：Unreal Engine 官方 Networking Overview 全文 0 处 `FEC` / 0 处 `forward error` / 0 处 `redundan` / 0 处 `retransmit`——Epic 整个游戏网络栈的对外文档均不涉及主动 FEC 冗余。

> 注：以上结论仅基于 EOS 对开发者公开的 API 契约。SDK 二进制内部的链路层细节不公开；理论上不能完全排除"未来某版本在 ReliableUnordered 模式底层引入主动 FEC"。但当前公开形态下没有任何线索。

## 升级路径

不适用（已落第 5 档，不存在 3-4 档升级路径需要刻画的中间证据形态）。

如果未来出现以下任一线索，应重新打开本档评估：

1. Epic 官方文档新增字段（如 `RedundancyCount` / `LatencyBudget` / `TrafficType`）暴露给 `EOS_P2P_SendPacket`。
2. Epic 工程师 talk / 博客披露 EOS 底层链路实际做了主动 FEC（即使 API 未暴露）。
3. 第三方逆向工程 / 抓包报告显示 EOS 在丢包前主动发送等量冗余副本。

## 总结一句话

EOS 公开 API 契约仅暴露 3 档 reliability 枚举与 ACK 触发的条件重传（ARQ），不含业务类型 / 时延 / 期望成功率 / 冗余数量 / 调度方法等权 1 必备输入，权 1 五特征结构性全部不命中，**落第 5 档（已排除）**。

---

**免责声明**：本判定为技术档位筛查结论，不构成法律意见、不代专利权人下"已构成侵权"结论；最终侵权认定需法律程序。
