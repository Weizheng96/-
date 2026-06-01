# 29-nvidia-cloudxr verdict

## 候选基本信息（专利公开日 2021-06-08）

- **候选名称**：NVIDIA CloudXR（NVIDIA 云端 XR 串流方案）
- **组织**：NVIDIA Corporation
- **类型**：商业产品 / SDK（CloudXR SDK 1.x → 6.0 持续演进）
- **初判命中 F#**：F2、F3、F4、F5（来自 Step 5）
- **公开度**：中
- **时间窗**：CloudXR 公开版本中 3.1（2021-09）、3.2（2021-12）、4.0（2022-09）、6.0（2024+）均在专利公开日 2021-06-08 **之后** —— 时间窗合规。
- **一句话定位**：NVIDIA RTX 服务器把 XR 渲染结果（H.264/H.265 视频 + 音频 + 控制器 / 头显姿态等多 stream）通过 UDP/5G/Wi-Fi 实时下发到 AR/VR 终端，并内置 QoS + FEC 模块以应对网络丢包与抖动。

## F# 命中表（F1-F5）

| F# | 专利限定（verbatim 关键短语） | CloudXR 证据 | 命中? | 命中原因 / 反向证据 |
|----|--------------------------|------------|------|-------------------|
| F1 | 发送端**根据数据流特征变量**（缓存包长度/数目、在网包长度/数目、到达间隔、突发性 4 项中至少 1 项）**获取业务类型** | NVIDIA staff tegradave："The QoS tuning is all black box under the hood." 官方暴露给客户端的接口（CloudXR 3.2 networking API）只允许应用**静态声明** "network topology type (5G, Wi-Fi, LAN) and maximum bitrate"；未公开任何"由发送端实时统计 4 项流特征 → 推断业务类型"的逻辑。CloudXR 的 stream 是**显式 typed**（video stream / audio stream / controller stream / haptic stream 等在 SDK 初始化时即被分配 stream:N），并非由发送端通过统计推断而来。 | **不命中（缺 verbatim 证据）** | F1 要求"由发送端根据 4 项流特征**推断**业务类型"。CloudXR 的 stream 类型是**应用层静态指定**的（对应专利从属权 4 形态："应用制定的业务类型"），而非权 1 的"从流特征统计推断"。在不可触达源码 / header 的前提下，**未找到** verbatim 证据能确认 CloudXR 发送端有"从 4 项流特征推断业务类型"的逻辑。 |
| F2 | 发送端根据**网络状态变量 + 传输成功率 + 业务类型**三元组联合计算**冗余数据包的数量** | NVIDIA staff Veronica："Regarding FEC, this is used part of our QoS." tegradave："Yes, FEC is used, you'll actually see it noted in the log when it adjusts." log 中可见 FEC 随网络变化"adjusts"； QoS log 已被官方文档列入 Latency / RTT / Estimated Available Bandwidth / Bandwidth Utilization / Average Video Rate 等指标（→ 网络状态变量 ✓）。stream 是 typed 的（video / audio / controller / haptic）——但**这是应用层声明的 stream，不是权 1 意义上"从流特征统计推断"的业务类型**。 | **部分命中（缺 F1 输入的业务类型）** | F2 的"三元组"要求其中"业务类型"输入是 F1 推断结果。CloudXR 的 FEC adjustment 显然依赖网络状态（log "adjusts" 行为），也很可能按 stream type 设不同 FEC 强度（video 与 audio/controller 对丢包敏感度差异巨大），但**官方未 verbatim 公开 FEC 数量公式**（"black box under the hood"），且若 CloudXR 区分 stream 是按应用静态声明的 stream type 而非按流特征推断 → 落入从属权 4 的"应用制定的业务类型"范畴，**严格按权 1 不命中**。 |
| F3 | 发送端根据**预先获取的时延要求**获取**冗余数据包的传输总时间** | CloudXR 全栈以"low-latency"为核心 KPI，官方 overview："Low-latency streaming: Optimized frame timing and network handling"。XR 串流的时延预算公开给开发者（max bitrate / topology API 输入），但**未公开** "时延 → 冗余包传输总窗口长度" 这一具体公式。 | **未确认（间接相关）** | "low-latency" 是产品级目标，不等同于权 1 "F3 把时延要求转换为冗余包发送窗口总时间" 的 verbatim 步骤。无源码访问下无法验证。 |
| F4 | 发送端根据**网络状态 + 总时间 + 冗余包数量**三元组联合**选择调度方法**（权 2/9 限定：随机度 / 最短 / 最长 / 均匀 4 选 1 至少 1 种） | tegradave："FEC ... noted in the log when it adjusts." 表明 FEC 参数在运行时随网络变化动态调整 —— 但**调整的是 FEC 强度还是发送时间分布**官方未澄清。 | **未确认** | "adjusts" 一词覆盖范围宽，无法 verbatim 锁定到"选择 4 类调度方法之一"。 |
| F5 | 发送端按调度方法**发送冗余数据包**（必须是 proactive FEC 而非 reactive ARQ / 重传） | **强证据**：NVIDIA staff 两次确认 "FEC is used"（Veronica + tegradave）；CloudXR 走 UDP（NuShrike1："UDP use was confirmed as transport technology"）—— UDP 本身无 ARQ，需要 FEC 才能恢复丢包；GeForce NOW（NVIDIA 兄弟产品）公开使用 FEC 作旁证。 | **命中** | 已 verbatim 锁定 CloudXR 主动发送 FEC 冗余包（非 TCP 重传），命中 F5 的"proactive 冗余"核心。 |

**汇总命中度**：F5 verbatim 命中；F2 部分命中（"网络状态 + 成功率 → FEC 数量"在 log 中可见 "adjusts"，但"业务类型"输入是应用静态声明而非 F1 推断）；F1 / F3 / F4 受限于"QoS black box"无 verbatim 命中。**全部权 1 五要件 5/5 命中无法 verbatim 确认**；目前**仅 1 个完整命中 + 1 个部分命中**。

## 已检查文档清单

1. https://forums.developer.nvidia.com/t/possible-to-configure-tune-cloudxr-encoding/208977 — NVIDIA staff (Veronica + tegradave) 关于 FEC / QoS / log 的官方回复 [本目录 `encoding_tune_forum.json` 已保存]
2. https://forums.developer.nvidia.com/t/network-qos-implementation/175926 — 用户提问 AFEC / XOR / ACK-NACK / HTB，无 staff 回复 [本目录 `qos_impl_forum.html` 已保存]
3. https://forums.developer.nvidia.com/t/understanding-cloudxr-client-qos-log-file/203674 — QoS log 字段（Latency / RTT / Available BW / BW Util / Avg Video Rate）
4. https://forums.developer.nvidia.com/t/qos-and-event-trace-logs/177754 — 仅用户提问，无 staff 回复
5. https://developer.nvidia.com/blog/build-scalable-immersive-experiences-with-networking-apis-swift-support-and-more-using-nvidia-cloudxr-3-2/ — CloudXR 3.2 networking API（client → server topology + max bitrate；client query QoS info）
6. https://developer.nvidia.com/blog/dialed-into-5g-cloudxr-4-0-brings-enhanced-flexibility-and-scalability-for-xr-deployment/ — CloudXR 4.0 引入 L4S togglable
7. https://docs.nvidia.com/cloudxr-sdk/latest/overview/overview.html — 官方 overview "low-latency streaming"
8. https://docs.nvidia.com/cloudxr-sdk/usr_guide/network_setup.html — 官方网络配置文档（curl 受 JS 渲染限制，仅得搜索摘要）
9. https://docs.nvidia.com/cloudxr-sdk/prog_guide/api_doxygen.html — 官方 API doxygen（curl 受限，未触达字段 verbatim）

## 最终判定 **第 3 档：可能侵权，但缺关键证据 / 需补证**

### 判定逻辑

- **正向证据**：CloudXR 是 UDP 流媒体协议栈 + NVIDIA staff 两次 verbatim 确认 "FEC is used part of our QoS" 且 "noted in the log when it adjusts" —— **F5 verbatim 命中**，F2 的"FEC 数量随网络状态自适应"也 log 可见。
- **关键缺口（导致不能升至第 2 档 / 第 1 档）**：
  1. **F1 弱**：CloudXR 的 stream 类型是**应用层静态声明**（video / audio / controller stream），而非"发送端根据 4 项流特征统计推断"的业务类型。这正对应专利从属权 4 "应用制定的业务类型"，**权 1 的 F1 要求落空**。
  2. **F2 / F3 / F4 黑盒**：tegradave 明言 "The QoS tuning is all black box under the hood." 在不能下载 SDK 源码 / header 的情况下，"三元组联合计算冗余包数量 + 调度方法"无法 verbatim 验证。L4S 是另一条机制（拥塞控制位标），不等同于 packet-level FEC 数量与调度。
  3. **业务类型自适应的关键创新点未被 verbatim 命中**：专利明书已将"基于业务类型决策"列为相对线性网络编码先有技术的创新点；若 CloudXR 仅做了网络状态自适应而未按 F1 推断的业务类型联合决策，则**不落入权 1**（但可能落入权 1 的从属或抽象上位发明内容描述）。
- **不能直接判第 4 档 / 第 5 档的原因**：FEC 在 CloudXR 中**确证存在**（两次 staff verbatim）且 UDP 传输 + "adjusts" 表明属于 proactive 自适应 FEC 而非 reactive ARQ —— **这与专利"主动冗余"核心高度同构**，没有反向证据（不是"X 是 future work"也不是"X 不在范围"）。仅是技术细节不可触达，不能就此判已排除。

### 备注：本判定**不替专利权人下"已构成侵权"法律结论**，仅给出技术档位。

## 升级路径（3-4 档时）

要从第 3 档升至 **第 2 档"高度疑似"** 或 **第 1 档"明确命中"**，需要拿到以下 verbatim 证据之一：

1. **首选 — CloudXR SDK header / 源码**（需 EA portal 注册）：
   - `cxrQoS` / `cxrStream` / `cxrTransport` 等结构里若存在按 stream type **静态分配** FEC 参数的字段 → 巩固"按应用声明的业务类型差异化"（但仍是 F1 弱命中，落从属权 4）。
   - 若存在 `cxrFECParams` 之类结构，且其字段同时引用网络丢包率 + 时延预算 + stream type → 全 F1-F5 verbatim 命中可达。
2. **次选 — CloudXR log 实测样本**（任一第三方部署的 log 节录）：抓取 log 中 FEC adjustment 行的格式，验证 "FEC strength changes with packet loss rate" 或 "different FEC level for stream:0 (video) vs stream:1 (audio)"。
3. **次选 — NVIDIA 专利 / SIGGRAPH / GTC 公开演讲**：检索 NVIDIA 在 USPTO / CNIPA 的 XR streaming FEC 相关专利文件、GTC session 录像中是否 verbatim 描述算法。
4. **次选 — 反向证据**：若发现 NVIDIA 公开说明 CloudXR 的 FEC 是 **fixed-rate** 或 **不区分 stream**（即纯 packet-level XOR 无业务类型感知）→ 反向确认不命中权 1 → 降至第 4 档"低度可能"。
5. **次选 — 时间证据**：CloudXR 1.0（2020-10）已存在 FEC ？还是 3.2 才引入？专利公开日 2021-06-08；若 CloudXR FEC 早于 2021-06-08 即引入且无重大变动 → 时间窗内"使用本专利方法"的成立性削弱（在先实施抗辩可能性）。

## 总结一句话

**NVIDIA CloudXR 已 verbatim 确认使用自适应 FEC（NVIDIA staff 两次官方表态 + log 可见 "adjusts"），落第 3 档"可能侵权、需补证"——技术形态与 CN107634908B 权 1 的"主动冗余 + 网络状态自适应"核心同构，但 F1 业务类型推断、F3 时延 → 总时间映射、F4 调度方法选择 3 项在 QoS 黑盒下无 verbatim 命中。**
