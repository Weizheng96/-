# 07-bytedance-rtc verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选 NN: 07
- 类型: 产品
- 名称: 火山引擎 veRTC (VolcEngineRTC)
- 组织: 字节跳动 / 火山引擎
- 公开度: 中（官网产品页 + GitHub 开源 SDK header + 多个 Demo 仓库）
- 初判命中 F#: F1, F2, F3, F4, F5
- 时间窗判定: veRTC 商业化时间 ≥ 2020, SDK header / 文档 2021-2026 持续迭代, **晚于专利公开日 2021-06-08 的版本明显存在** → 时间窗成立

## F# 命中表（F1-F5）

| F# | 权 1 限定 | veRTC 公开行为 | 命中度 | 关键证据 |
| --- | --- | --- | --- | --- |
| **F1** | "数据流特征变量"（缓存包长度/数目、在网包长度/数目、到达间隔、突发性中**至少 1 项**）→ **由发送端自动得到**业务类型 | veRTC SDK 暴露 `RoomProfileType` enum（13 个枚举: Communication / Game / CloudGame / LowLatency / ChatRoom / InteractivePodcast / Chorus / GameStreaming / Meeting / MeetingRoom / Classroom / Call / Live）, 由应用调用方在 `joinRoom` 时通过 `RTCRoomConfig.room_profile_type` 显式传入, "进房后不可更改"; Web SDK 文档明示"自 V4.51, 无需设置该项"(默认 communication); 0 处 `setBusinessId` / `auto.*detect` / 从数据流统计推导业务类型的 API | **反向证据 — 不命中** | `bytertc_media_defines.h` line 411-501 (RoomProfileType 全枚举 verbatim); `bytertc_video_defines.h` line 1857 (默认值 + 注释 "进房后不可更改"); vertc_web_doc.html line 38 |
| **F2** | 冗余包数量 = f(网络状态 + 传输成功率 + **业务类型**) | 公开材料披露 veRTC 应用 FEC + ARQ + HARQ + 自适应 Jitter Buffer + 自适应码率, 最高 80% 抗丢包能力(网络状态自适应明确); 但**业务类型作为冗余量计算输入**这一环节: SDK 仅有应用层 RoomProfile 静态 hint, 内部"hint → 算法参数集"映射未公开披露, 同时该 hint 不是 F1 意义的"数据流特征导出" | 部分（仅"网络状态 + 成功率"侧成立, 业务类型侧仍依赖应用层 hint 而非数据流推导） | volcengine.com/product/veRTC ("应用 FEC、ARQ、HARQ、自适应 Jitter Buffer、自适应码率下发等弱网策略, 实现 50% 丢包无感知恢复, 最高 80% 抗丢包能力") |
| **F3** | 冗余包传输总时间 ← 时延要求 | 商业 RTC 引擎普遍按业务模式(通话/直播/低延时)隐含时延预算并调控 FEC 窗口长度; veRTC 暴露 LowLatency / Call / Meeting / Live 等 profile 隐含不同时延预算, 但"总时间 ← 时延要求"具体算法链未公开 | 等同命中（中间变量省略 / 推定存在） | RoomProfileType 含 `kRoomProfileTypeLowLatency=4` 与 `kRoomProfileTypeLive=20` 分档隐含时延预算 |
| **F4** | 调度方法 = f(网络状态 + 总时间 + 冗余包数量), 集合: 随机度/最短/最长/均匀时间 (≥ 1 种) | 通用 RTC FEC 实现通常包含 ULP/Flex 模式选择 + 包内调度策略; veRTC 公开材料只到"自适应"高层级, 未披露具体调度策略集合 | 等同命中（中间变量省略, 但无 SDK 级反向证据） | (无 SDK 直接 API 证据, 仅产品页"自适应"措辞) |
| **F5** | 按调度方法发送冗余包（主动 FEC, 非 ARQ） | veRTC 明示"应用 FEC … ARQ … HARQ" — FEC 部分构成主动冗余, 与权 5 步骤吻合 | 命中 | volcengine.com/product/veRTC |

**核心问题: F1 不命中**。veRTC 的"业务区分"来自应用层 `RoomProfileType` 静态 hint(应用调用方传入), 而专利权 1 把"业务类型"**硬钉为发送端从数据流特征变量(缓存包长度/数目、在网包长度/数目、到达间隔、突发性)自动得到**, 并明示"应用层 hint 形态"属于从属权 4(非权 1)。F1 是权 1 的入口条件, F1 不命中即不构成权 1 直接侵权。

## 已检查文档清单

1. github.com/volcengine/VolcEngineRTC — 主仓库
2. github.com/volcengine/VolcEngineRTC/blob/main/Windows/3rd/Windows/VolcEngineRTC/include/rtc/bytertc_video_defines.h (本地 bytertc_video_defines.h, 2616 行) — 含 `RoomProfileType room_profile_type` 默认值与"进房后不可更改"注释
3. github.com/volcengine/VolcEngineRTC/blob/main/Windows/3rd/Windows/VolcEngineRTC/include/rtc/bytertc_media_defines.h (本地 bytertc_media_defines.h, 5258 行) — 含 `enum RoomProfileType` 13 项全枚举 verbatim
4. github.com/volcengine/VolcEngineRTC/blob/main/Windows/3rd/Windows/VolcEngineRTC/include/bytertc_room.h — IRTCRoom 接口(无 FEC API)
5. volcengine.com/docs/6348/106914 (本地 vertc_web_doc.html, 1.76 MB) — Web SDK 文档, 明示 `roomProfileType:RoomProfileType.communication // 自 V4.51 ，无需设置该项`
6. volcengine.com/product/veRTC — 产品页, 披露 FEC/ARQ/HARQ + 80% 抗丢包能力
7. explinks.com/api/scd20240624421918b8c5e0 — veRTC API 接口介绍
8. github.com/volcengine/VolcEngineRTC_Solution_Demo — Demo 仓库
9. blog.csdn.net adg/.../adg.csdn.net (火山引擎 ADG 社区) — RTC FEC 走读多篇

## 最终判定 **第 4 档：弱关联 / 反向证据**

判定依据:
1. **F1 反向证据明确**: veRTC SDK header 直接证明业务类型由应用层 `RoomProfileType` 静态枚举传入, 而非"发送端从缓存/在网/到达间隔/突发性等数据流特征变量自动推导" — 这正是专利说明书在区分权 1(数据流特征导出)与从属权 4(应用制定)时所明示排除的形态。
2. F2-F5 虽在"FEC + 自适应抗丢包"层面有概念重叠, 但因 F1 不成立 → 权 1 入口条件不满足, 不构成权 1 直接侵权。
3. 内部具体冗余量算法字节未公开披露, 因此**无法升档到 3 档**(等同侵权 — 中间变量省略)的强证据; 也**无法降档到 5 档**(已排除 — 时间不合规 / 领域无关), 因 veRTC 确实做 FEC + 自适应抗丢包, 与专利同领域且时间窗成立。

## 升级路径（3-4 档时）

若后续披露以下任一项, 可考虑升档至 3 档(等同侵权候选):
- 字节官方技术博客或论文披露 veRTC 内部冗余包数量计算使用"缓存中待发包长度/数目"或"在网包数目"等**数据流特征变量**作为输入(即等价于 F1 的"自动推导")
- veRTC SDK 新版本暴露 `setBusinessIdFromTrafficStats` / 自动业务类型识别 API
- 字节专利申请文件中描述类似的"数据流特征 → 业务类型 → 冗余量"算法链(可在 CNIPA / Google Patents 查 assignee=字节跳动 / Volcano Engine 的 RTC 相关申请)
- 反编译 veRTC SDK 二进制(libbytertc.so / VolcEngineRTC.framework)定位是否存在内部 traffic profiler 模块

## 总结一句话

字节跳动火山引擎 veRTC 虽明示具备 FEC+ARQ+HARQ+自适应抗丢包(80% 上限)且业务区分通过 13 项 `RoomProfileType` enum 实现, 但该 enum 由**应用调用方静态传入**且"进房后不可更改", 不构成权 1 要求的"发送端从数据流特征变量自动得到业务类型", F1 反向证据明确, **落第 4 档(弱关联 / 反向证据)**。

> 免责声明: 本报告仅为侵权排查线索与证据链, 不构成法律意见; 是否实际构成专利侵权应由专利权人结合完整证据链经法律程序判定。
