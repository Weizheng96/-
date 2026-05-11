# Verdict — 01 Tencent START Cloud Gaming

> 关联候选：T2-01 腾讯 START 云游戏 + 先游 + GameMatrix
> 适用独立权：权 1（方法） + 权 8（设备）
> 主体类型：T2 云游戏 / 远程渲染
> Priority：P0

## F# 命中表（基于 §A 证据 + 子 agent 独立审）

| F# | Path 1 字面 | Path 2 从属权 alt | Path 3 等同 | 综合判定 |
| --- | --- | --- | --- | --- |
| F1 业务类型识别 | Hairpin 论文 + START 云游戏区分视频帧/控制信令/音频 | 权 4 默认/应用指定（START 客户端区分 game-stream 业务类型） | — | **字面命中** |
| F2 冗余包数量 = f(网络状态, 成功率, 业务类型) | Hairpin："实时监测 RTT 和丢包事件 → 动态调整 FEC 参数" | — | — | **字面命中** |
| F3 传输总时间 ← 时延要求 | Pudica + AUGUR 均围绕 cloud gaming 严格 deadline（frame-level QoE）| 权 3 ≤ 时延 | — | **字面命中** |
| F4 调度方法 = f(网络状态, 总时间, 数量) | Pudica zero-queuing pacing + Hairpin 重传 + FEC 多轮组合 | 权 2 random/shortest/longest/uniform（Pudica pacing 算法属"均匀时间调度方法"等同变体） | — | **字面命中** |
| F5 实际发送冗余包 | START 已大规模部署到云游戏平台（millions of players） | — | — | **字面命中** |

**字面命中 5/5**。

## 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 | **第 1 档 确认侵权（高 — 字面 5/5）** | 1. 等同三步法 N/A（字面命中）；2. 反向 vs 限定语区分：无反向引文 ✅；3. 法律状态 = Active（2021-06-08 ~ 2036-07-19）；4. §A.9 现有技术 = 未发现覆盖度 ≥60%（2016 申请日前业务感知+自适应 FEC+时延约束三因子完整方案未在公开顶会发表）；5. R-STANDARD 转移 = false；6. §5.0 豁免 = N/A；7. patent pledge = 工具能力下未充分核查，建议法务通过 IPR 律师补查华为 ETSI / 3GPP IPR declaration | **第 1 档 确认侵权（高）** |
| 权 8 | **第 1 档 确认侵权（高）** —— START 智能电视客户端 / 手柄硬件 OEM 出厂内置时设备权直接命中 | 同上 | **第 1 档 确认侵权（高）** |

## 总结一句话

腾讯 START 在 NSDI 2024 发表的 Hairpin + Pudica + AUGUR 三篇论文公开了与 CN107634908B 几乎逐项字面对应的"业务感知 + 网络状态 + 时延要求自适应冗余调度"全链路；本候选落第 1 档（确认侵权高）+ Active 标准维权路径。
