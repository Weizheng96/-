# 证据索引 — 07-bytedance-rtc

## Phase 1 WebSearch (4 queries — react 串行)

| # | Query | 关键命中 / 摘录 | 走向 |
| --- | --- | --- | --- |
| 1 | `火山引擎 veRTC 自适应抗丢包 FEC 业务类型` | volcengine.com/product/veRTC, volcengine.com/docs/6459/72363, adg.csdn.net RTC FEC 走读多篇 | 文档/社区有 FEC 抗丢包提及, 进入 Phase 2 |
| 2 | `volcengine veRTC SDK setRoomProfile scenario API ChannelProfile` | github.com/volcengine/VolcEngineRTC, docs.emqx.com/.../volcengine-rtc | SDK 暴露 `RoomProfileType`, 由应用调用方设置 |
| 3 | `火山引擎 veRTC 抗丢包策略 业务场景 setBusinessId NACK FEC 自适应算法` | explinks.com API 介绍 + volcengine.com/product/veRTC; 摘录 "应用 FEC、ARQ、HARQ、自适应 Jitter Buffer、自适应码率下发等弱网策略, 实现 50% 丢包无感知恢复, 最高 80% 抗丢包能力" | 确认有 FEC + 自适应冗余, 未见 setBusinessId 类 API |
| 4a | `"VolcEngineRTC" "RoomProfile" "CommunicationModeBasic" "LiveBroadcasting" 场景` | github.com/volcengine/VolcEngineRTC bytertc_room.h, volcengine.com/docs/6348/106914 (Web SDK) | 文档明确 `roomProfileType:RoomProfileType.communication // 自 V4.51 ，无需设置该项` |
| 4b | `火山引擎 veRTC 弱网对抗 FEC ARQ 算法原理 业务区分 直播 通话` | csdn 抗弱网算法总结、网易云信 RTC 音频弱网对抗实践 | 通用 FEC/ARQ 原理资料; 未见 veRTC 内部以"业务类型"作为冗余量计算输入的直接披露 |

## Phase 2 WebFetch / curl 深抓

| # | URL / 方式 | 结果 | 命中要点 |
| --- | --- | --- | --- |
| P2-1 | WebFetch https://github.com/volcengine/VolcEngineRTC/blob/main/Windows/3rd/Windows/VolcEngineRTC/include/bytertc_room.h | 200, 内容含 IRTCRoom 接口 (无 RoomProfile/FEC) | 引导至 RTCRoomConfig 结构 |
| P2-2 | WebFetch https://www.volcengine.com/docs/6348/106914 | ECONNREFUSED → curl 兜底成功 → 本地 vertc_web_doc.html (1.76 MB) | 关键: `roomProfileType:RoomProfileType.communication // 自 V4.51 ，无需设置该项` |
| P2-3 | curl https://api.github.com/repos/volcengine/VolcEngineRTC/contents/Windows/3rd/Windows/VolcEngineRTC/include 及 /rtc 子目录 | 列出 28 个 rtc/*.h header | 定位 bytertc_video_defines.h / bytertc_media_defines.h |
| P2-4 | curl https://raw.githubusercontent.com/volcengine/VolcEngineRTC/main/Windows/3rd/Windows/VolcEngineRTC/include/rtc/bytertc_video_defines.h | 2616 行, 本地 bytertc_video_defines.h | line 1857: `RoomProfileType room_profile_type = kRoomProfileTypeCommunication;` + 注释 "房间模式, 默认为 kRoomProfileTypeCommunication, 进房后不可更改"; 0 处 `setBusinessId`/`fec`/`auto.*detect`/`adapt` API |
| P2-5 | curl https://raw.githubusercontent.com/volcengine/VolcEngineRTC/main/Windows/3rd/Windows/VolcEngineRTC/include/rtc/bytertc_media_defines.h | 5258 行, 本地 bytertc_media_defines.h | line 411-501: `enum RoomProfileType : int { kRoomProfileTypeCommunication=0, Game=2, CloudGame=3, LowLatency=4, ChatRoom=6, InteractivePodcast=10, Chorus=12, GameStreaming=14, Meeting=16, MeetingRoom=17, Classroom=18, Call=19, Live=20 }`; 0 处 FEC/business 配置 API |
| P2-6 | WebSearch `字节跳动 火山引擎 veRTC 抗丢包 FEC 算法 80% 弱网 技术博客 实现` | 未检索到字节官方披露 veRTC 内部冗余包数量计算的具体输入变量 | "业务类型 → 冗余包数量"计算链无公开证据 |
| P2-7 | WebSearch `VolcEngineRTC AudioScenarioType setAudioScenario` | AudioScenarioType 存在(grep media_defines header 也见 kAudioScenarioTypeCommunication 引用), 作用是回声/音频路由策略 | 与冗余包数量计算无直接证据链 |

## 已下载证据文件 (本地)

- `bytertc_video_defines.h` (2616 行, github raw)
- `bytertc_media_defines.h` (5258 行, github raw) — 含 RoomProfileType 全枚举 verbatim
- `vertc_web_doc.html` (1.76 MB, volcengine.com docs/6348/106914)
