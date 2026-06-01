# 17-baidu-apollo verdict

## 候选基本信息（专利公开日 2021-06-08）
- 候选 ID / slug：17-baidu-apollo
- 类型：产品
- 名称：Apollo 云控平台 + V2X 通道
- 组织：百度
- 初判命中 F#：F2, F3, F4, F5（来自 Step 5 初选）
- 公开度：中（ApolloAuto/apollo 仓库开源；云控 / V2X 服务器端闭源）
- 时间窗：Apollo 项目自 2017 起持续迭代，CyberRT / bridge / V2X 模块跨越 2021-06-08 公开日前后，时间窗**允许判定**。

## F# 命中表（F1-F5）

| F# | 限定 | 公开证据命中？ | 证据 / 反向证据 |
|----|------|---------------|----------------|
| F1（业务类型识别，基于数据流特征变量：缓存包长度 / 数目 / 到达间隔 / 突发性 ≥1 项） | 必须由发送端自动从真实流量统计得到，非应用层 hint | **未命中** | CyberRT / bridge 公开文档与代码未见"按缓存 / 到达间隔 / 突发性自动识别业务类型"逻辑；CyberRT topic 类型由开发者声明（=应用层 hint，对应专利从属权 4 而非权 1）。 |
| F2（冗余包数量 = f(网络状态变量, 传输成功率, 业务类型) 三元组联合） | 三参数缺一不可 | **未命中** | bridge 模块为单发 UDP + 分片（max 65535 B / frame），无"冗余包数量"概念；CyberRT FAQ 未提自适应 FEC。V2X 公开资料仅提"轨迹预测补偿丢包"（应用层补偿），非 packet-level 冗余。 |
| F3（冗余包传输总时间 = f(时延要求)） | n 个冗余包累计窗口长度 | **未命中** | 未见 redundancy window 配置项。 |
| F4（调度方法 = f(网络状态, 总时间, 冗余包数量) 三元组联合；随机度 / 最短 / 最长 / 均匀 ≥1 种） | 必须动态选择 | **未命中** | bridge 为固定 UDP 单发，无调度切换；CyberRT 默认 UDP multicast + RTPS，未见多种调度策略动态切换。 |
| F5（按调度方法发送冗余数据包） | 必须 proactive 主动冗余，非 ARQ / 超时重传 | **未命中** | bridge 仅发原始 frame，未发冗余副本；V2X "轨迹预测补偿"是接收端推断，非发送端主动冗余，按 SKILL 反向证据规则**轨迹预测 ≠ FEC**。 |

注：以上"未命中"基于公开代码（ApolloAuto/apollo）+ 公开技术解读。Apollo **云控平台服务器端** + **百度自营 V2X 通道**闭源，无法 100% 排除其私有协议栈使用类似机制。

## 已检查文档清单
- Phase 1 WebSearch 命中页（4 次 query，详见 _sources.md）：
  1. Apollo V2X 解决方案介绍（百度地图智慧交通）—— 提"50ms 空口时延 + 200ms 端到端 + 轨迹预测补偿丢包"，未提主动冗余 FEC。
  2. ApolloAuto/apollo CyberRT FAQ（GitHub master 与官方文档）—— 默认 UDP multicast + RTPS，未提业务类型自适应冗余。
  3. ApolloAuto/apollo modules/bridge/README.md —— bridge = UDP sender/receiver + 分片（65535 B），无 redundancy 字段。
  4. ApolloAuto/apollo Issue #9650 / #10816 / #5375 / #13276 / #14334 与 Bridge Header Protocol 文档 —— 均围绕 UDP topic 转发 / 解析，无 FEC / 冗余包逻辑。
- Phase 2 WebFetch：**未进入**（Phase 1 4/4 query 已得出"公开层面 F# 集合 0 命中"，且无新增 query budget；闭源云控不可访问，继续 Fetch 无新增证据空间）。

## 最终判定 **第 5 档：线索极弱 / 公开层面 0 命中但闭源部分不可见**
- 五档分级：
  - 第 1 档：确认侵权（不允许法律定性，本 skill 仅技术档位）
  - 第 2 档：高度疑似（多 F# 强证据 + 时间窗合规）
  - 第 3 档：中度疑似（部分 F# 命中，需补证）
  - 第 4 档：弱线索（≥1 F# 弱命中或间接证据）
  - 第 5 档：极弱 / 待观察（公开层面 0 命中 + 存在闭源不可证伪空间）
  - 已排除：必须有真反向证据（明确架构文档说"不用 packet-level 冗余 / 只用 ARQ"）/ 时间窗不合规 / 领域无关 之一
- **本候选落第 5 档**，依据：
  - 公开代码（CyberRT + bridge）F1-F5 全部 0 命中。
  - 但"0 命中 ≠ 已排除"——Apollo 云控服务器端 + 百度自营 V2X 后端闭源，无公开架构文档明确否认使用主动冗余 FEC，反向证据不充分。
  - "轨迹预测补偿"是反向证据信号但仅针对 V2X 接收端，未覆盖云控发送端全部场景。

## 升级路径（若后续欲升至 3-4 档）
1. 抓 Apollo 云控 SDK / 车云通道协议白皮书（若百度对外公开），查找是否提"业务类型自适应冗余 / 主动 FEC / packet-level redundancy"字样。
2. 检索百度 ACE 智能交通 / Apollo 云控 V2X SLA 文档，查"丢包率 vs 冗余比"配置项。
3. 检索 ApolloAuto/apollo 内 `modules/v2x/` 与 `modules/data/` 子模块是否含 FEC 模块（本轮未深查）。
4. 关注百度专利申请，若百度自有类似冗余传输专利同时覆盖业务类型 + 网络状态 + 时延三元组，提示存在 FTO 风险或共存关系。
5. 任一上述命中即可考虑升至第 4 档；同时找到 F1-F5 中 ≥3 个具体实现位点可升至第 3 档。

## 工具受限明示
- 本判定仅依据公开 Web 检索（4 次 WebSearch），未抓取 Apollo 闭源云控 / 自营 V2X 服务器端协议；未进入 Phase 2 WebFetch（Phase 1 已得出"公开层 0 命中"结论，节约 token budget）。
- 未对 ApolloAuto/apollo 仓库做 source-level grep（react sub-agent 模式下不下载完整仓库）；如需 raw-code 级证据，建议另起 Step 6 增强轮次。

## 总结一句话
Apollo 公开代码（CyberRT + bridge）走 UDP 单发 / 多播 + 分片，丢包靠应用层轨迹预测补偿而非主动冗余 FEC，F1-F5 公开层全 0 命中；但云控与自营 V2X 闭源不可证伪，**落第 5 档线索极弱**，非法律结论。

---

**免责声明**：本报告为技术档位判定，不构成法律意见，不下"已构成侵权"结论。所有判定基于公开来源，闭源部分不可验证，最终侵权认定须由专利权人通过正式取证 / 司法程序进行。
