# 23-xiaomi-cyberdog verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选编号：23
- 候选名：CyberDog / 小米机器人云控
- 组织：小米（Xiaomi）
- 类型：产品（含部分开源代码）
- 初判命中 F#：F2, F3, F4, F5（来自 Step 5 元数据）
- 公开度：低（云端控制路径闭源；机器人本体 ROS 2 / motor SDK 开源）
- 时间窗：CyberDog 1 发布 2021-08（专利授权后约 2 个月），CyberDog 2 发布 2023-08——**均晚于专利公开日 2021-06-08，满足时间窗硬条件**
- 对位独立权：权 1（"发送端"=机器人 SDK 进程 / 云端推流节点 / 控制主板）；权 8（设备形式）等价

## 检索粗筛

执行了 4 条 WebSearch（Phase 1）+ 2 条 WebFetch（Phase 2），详见 `_sources.md`。粗筛结论：
- 公开通信栈 = Cyclone DDS（ROS 2）+ LCM（motor SDK）+ gRPC（bridges）+ CAN（车载总线）
- 0 公开物料提及 FEC / 主动冗余 / 业务类型自适应 / 三元组联合冗余计算
- 已具备"反向证据"（见 F5 行），符合"已排除"硬条件而非单纯 0 命中

## F# 命中表（F1-F5）

| F# | 限定要点 | 公开证据 | 命中判定 |
|---|---|---|---|
| F1 | 发送端从"缓存包长/数目、在途包长/数目、到达间隔、突发性"中至少 1 项**自动**识别业务类型 | 未检索到公开来源 | **未命中（公开层 0 证据）** |
| F2 | 冗余包数量 = f(网络状态变量, 传输成功率, 业务类型) — 三元组联合 | 未检索到公开来源；CyberDog 通信链均为通用中间件（Cyclone DDS / LCM / gRPC / CAN），无任何"冗余包数量动态计算"描述 | **未命中（公开层 0 证据）** |
| F3 | 冗余包传输总时间由时延要求决定（n 个包累计窗口长度） | 未检索到公开来源 | **未命中（公开层 0 证据）** |
| F4 | 调度方法 = f(网络状态, 总时间, 冗余包数量) — 三元组联合；可选集合：随机度/最短/最长/均匀 | 未检索到公开来源 | **未命中（公开层 0 证据）** |
| F5 | 按 F4 决定的调度发送冗余包（**主动 FEC**，非 ARQ / TCP 超时重传） | **反向证据 1**：CyberDog 机器人端通信 = `Cyclone DDS`（DDS Reliable QoS 是 ACK + history cache + retransmit，属 ARQ/reactive，**非 proactive FEC**）<br>**反向证据 2**：motor SDK = `LCM`（UDP multicast，无内建 FEC，README 自承 "difficult to ensure real-time LCM communication when running on the user PC"，即无主动冗余补偿层）<br>**反向证据 3**：bridges 模块 = `gRPC`（HTTP/2 流控 + TCP，无 FEC）/ `CAN`（车载总线，无 FEC） | **反向证据成立 — 未命中** |

**命中统计：0/5（其中 F5 有 3 条直接反向证据；F1-F4 公开层零证据）**

## 已检查文档清单

1. https://github.com/MiRoboticsLab/cyberdog_ros2/blob/main/README_EN.md — 仅声明 Cyclone DDS，无 FEC/QoS/冗余描述
2. https://github.com/MiRoboticsLab/cyberdog_motor_sdk/blob/main/README_EN.md — LCM + multicast，无 FEC/冗余/业务类型描述
3. WebSearch 4 query 覆盖：英文 CyberDog 通信、site:github MiRoboticsLab、英文云控自适应冗余、中文 FEC + 业务类型 + 传输成功率
4. 未检查（不可达）：小米云端 CyberDog 控制服务的内部协议（闭源、零公开资料）

## 最终判定 **第 5 档：已排除**

依据：
- F5 有 3 条直接反向证据（DDS Reliable QoS / LCM UDP / gRPC + CAN 均属反向技术路线，主动 FEC 不存在）
- F1–F4 在公开层 0 命中（连"业务类型识别"、"冗余包数量公式"、"调度集合"任一关键术语都未在 CyberDog 公开物料中出现）
- 时间窗虽然满足（2021-08 / 2023-08 ≥ 2021-06-08），但实质技术路径不在权 1 范围内
- "0 命中 ≠ 已排除" 原则：本案不仅是 0 命中，而是有反向证据指向 F5 错位（Reliable QoS / LCM / gRPC 都不是 proactive 冗余），符合"已排除"的硬条件

**特别说明（限定作用域）**：小米云端 CyberDog 控制服务（如 App ↔ 云 ↔ 机器人通道）闭源，本判定**只覆盖已开源的机器人本体通信栈**。如未来曝光小米云端使用业务类型 + 网络状态 + 成功率三元组自适应 FEC 算法，本档需重新评估——但目前公开层 0 证据。

## 升级路径（如出现以下情形，可升至 3-4 档）

1. 小米 CyberDog 云端控制服务（闭源）被反编译 / 内部文档泄露，显示其用 (a) 业务类型自动识别 + (b) 网络成功率反馈 + (c) 冗余包数量动态计算 三件套
2. MiRoboticsLab 后续 commit 引入自研 FEC 中间件，replace Cyclone DDS 的 reliable QoS
3. 小米相关专利申请显式引用 CN107634908B 或其权 1 方案
4. 公开学术论文 / 技术博客出现"CyberDog 通信使用业务类型自适应主动冗余"具体描述

满足任一即升至"3 档：弱命中（需进一步核证）"；满足两条以上升至"4 档：强嫌疑"。

## 总结一句话

CyberDog 公开通信栈 = Cyclone DDS + LCM + gRPC + CAN（均为标准中间件，无主动 FEC、无业务类型自适应冗余），F1–F4 公开层 0 证据、F5 有 3 条反向证据，**落第 5 档：已排除**；闭源云端路径不可达暂保留升级路径条款。

---

*免责声明：本报告基于公开可检索的源代码、README、技术报道；不构成法律意见；不替专利权人下"已构成侵权"结论；候选最终是否构成侵权应由权利人委托具备资质的法律 / 技术鉴定机构判定。*
