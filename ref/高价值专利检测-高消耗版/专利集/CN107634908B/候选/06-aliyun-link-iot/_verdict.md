# 06-aliyun-link-iot verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选 NN：06
- 类型：产品
- 名称：Link IoT Kit / Link Kit SDK
- 组织：阿里云
- 初判命中 F#（来自 Step 5）：F2、F3、F4、F5
- 时间窗：阿里云 IoT 平台与 Link SDK 在 2021-06-08 之前已长期商用（早于公开日），但**专利侵权判定的关键是"功能特征是否命中"而非"是否在售"**——此处时间窗不构成排除理由；以"功能反向证据"为判定基础。

## 检索粗筛

- Phase 1：4 次 WebSearch（详见 `_sources.md` 1–4）
  - 阿里云 IoT 平台底层消息传输可靠性 = **标准 MQTT QoS 0/1/2**（ARQ：发送 → 等 ACK → 未收到则在重连时按相同 packet ID 重发）
  - 离线消息处理 = **服务端缓存 +重连后下发**（QoS 0 ≤1 天 / QoS 1 ≤7 天）
  - 未检索到任何 packet-level 主动 FEC / 业务类型自适应 / 动态冗余调度的产品功能描述
- Phase 1 决策：未 0 命中（拿到充分反向信号），**进入 Phase 2 深抓确认**

- Phase 2：6 次 WebFetch + 2 次 curl（详见 `_sources.md` 7–13）
  - 阿里云官方"产品功能特性"页：弱网通信不可靠的官方解决方案明示为 **"设备影子缓存机制"**（云端缓存最新状态、设备重连后同步），**而非 packet-level 主动 FEC**
  - Link SDK 全模块清单（官方）：连接认证 / 消息通信（MQTT/CoAP/HTTP）/ 物模型 / 网关子设备 / OTA / 远程登录 / 日志 / 远程配置 / NTP / 文件管理 —— **无 FEC / 主动冗余 / 业务类型识别 / 自适应调度任一模块**
  - C-SDK GitHub `src/` 13 个子目录全清单（`atm, coap, dev_bind, dev_model, dev_reset, dev_sign, dynamic_register, http, http2, infra, mqtt, ota, wifi_provision`）—— **无 FEC / scheduler / classifier / redundancy 任一子目录**；MQTT 子目录走标准协议

## F# 命中表（F1–F5）

| F# | 限定要点 | 命中？ | 证据 / 反向证据 |
|---|---|---|---|
| F1 业务类型识别（基于数据流特征变量 a/b/c/d ≥1 项） | 发送端自动从真实流量统计中得到业务类型 | **不命中** | SDK 全模块清单 + GitHub `src/` 子目录均无 traffic classifier / business type 模块。MQTT topic 由应用层手工指定，属"应用制定的业务类型"形态（专利从属权 4 而非权 1） |
| F2 冗余包数量 = f(网络状态, 成功率, 业务类型) | 三元组联合计算，必须有"业务类型"输入；冗余包是 proactive 副本 | **不命中** | Link SDK / 平台未生成任何"冗余包"——MQTT QoS 1 是 ARQ（reactive 重传相同包），不是 packet-level proactive FEC；F2 整数 ≥1 的限定不满足 |
| F3 冗余包传输总时间 = f(时延要求) | n 个冗余包累计发送窗口长度 | **不命中** | 不存在"冗余包传输总时间"概念；MQTT QoS 1 是基于连接超时与重连触发，无"冗余传输窗口"语义 |
| F4 调度方法 = f(网络状态, 总时间, 冗余包数量) | 动态选随机度/最短/最长/均匀调度 ≥1 种 | **不命中** | 无冗余包对象 → 无调度方法可选；不存在"动态选调度策略"逻辑 |
| F5 按调度方法发送冗余包 | proactive 发送 redundant 包 | **不命中** | 阿里云对"不稳定无线网络下的通信不可靠"的官方方案是**设备影子缓存**（reactive，云端缓存 + 重连同步）+ MQTT QoS 重传（reactive ARQ），均非 proactive FEC |

**核心反向证据**：MQTT QoS 1 / QoS 2 重传机制 ≠ F5。专利说明书明确把"现有技术 TCP 超时重传"作为本发明要解决的痛点，本发明核心区别正是"主动 FEC 替代被动重传"；阿里云 Link SDK 的可靠性栈完全落在"被动重传"侧。

## 已检查文档清单

| # | 文档 / 资源 | 关键结论 |
|---|---|---|
| 1 | help.aliyun.com Link SDK 集成方式与功能特性 | 列 SDK 全功能模块，无 FEC / 主动冗余 |
| 2 | help.aliyun.com C Link SDK 概览 v5 | 列 C SDK 接入协议（MQTT/HTTPS/CoAP），无 redundancy API |
| 3 | help.aliyun.com 物联网平台产品全部功能特性 | 弱网方案 = 设备影子（reactive 缓存），无 FEC |
| 4 | help.aliyun.com 消息通信 FAQ / MQTT QoS / 离线消息 | QoS 1 = ACK-based 重传（reactive ARQ） |
| 5 | partners-intl.aliyun.com Message Queue for MQTT 产品页 | 提供标准 MQTT QoS 0/1/2，未提及任何专有可靠性扩展 |
| 6 | github.com/aliyun/iotkit-embedded README + src/ 目录 | 13 个子目录全清单，无 FEC / scheduler / classifier |
| 7 | github.com/aliyun/alibabacloud-linkkit-python-sdk | OpenAPI 包装，与设备端传输栈无关 |

本地落盘：`iotkit-embedded-readme.md`、`iotkit-embedded-src-modules.md`

## 最终判定

**第 5 档：已排除**

**判定依据（满足"已排除"的硬条件 (i) 反向证据）**：

1. **(i) 反向证据**：阿里云 IoT 平台官方"产品功能特性"明示弱网通信可靠性方案是 **"设备影子缓存机制"**（reactive 云端缓存 + 重连同步）+ 标准 **MQTT QoS 0/1/2**（reactive ARQ）。两路机制均为"被动响应"，与专利核心要素"主动 FEC packet-level 冗余"在机制层面相互排斥——专利说明书把"TCP 超时重传"列为要解决的痛点，本发明的本质区别正是从"reactive 重传"切换到"proactive 冗余副本"。阿里云的方案完整落在 reactive 侧。

2. **结构层反向证据**：C-SDK GitHub `src/` 顶层 13 个子目录（atm, coap, dev_bind, dev_model, dev_reset, dev_sign, dynamic_register, http, http2, infra, mqtt, ota, wifi_provision）+ 官方 Link SDK 全功能模块清单（约 10 项）两路一致表明：SDK 中**不存在** traffic classifier / business type identifier / redundancy packet generator / adaptive packet scheduler 任一模块。F1–F5 均无落点。

3. **限定语 vs 反向证据区分**：官方文档对 MQTT QoS 的描述（"resends unanswered QoS=1 packets"）+ 对弱网的描述（"设备影子缓存机制解决不稳定无线网络下的通信不可靠痛点"）均为**正面陈述其机制是 reactive 的**，而非"X 不在本工作范围"式的限定语——构成严格意义上的反向证据。

## 升级路径

不适用（第 5 档）。

如需重启评估，触发条件为：阿里云后续发布带"业务类型自适应主动冗余" / "packet-level FEC" 关键词的 SDK 新模块或专利白皮书；或在 iotkit-embedded 仓库 src/ 下新增 `fec / scheduler / classifier / redundancy` 子目录。

## 总结一句话

阿里云 Link IoT Kit / Link SDK 在不可靠网络场景下的官方解决方案是**设备影子缓存（reactive 云端缓存）+ 标准 MQTT QoS ARQ（reactive 重传）**，与本专利权 1 核心要素"基于业务类型的 packet-level 主动 FEC 冗余调度"在机制层面相互排斥，F1–F5 全部不命中，**落第 5 档（已排除）**。

---

> 本结论仅为技术档位评估（依据公开资料分析机制是否落入权利要求技术特征集合），不构成法律意义上的侵权认定；最终是否构成侵权需由权利人通过司法 / 行政程序核实。
