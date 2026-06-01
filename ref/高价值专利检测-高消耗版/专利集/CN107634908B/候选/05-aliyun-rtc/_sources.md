# 05-aliyun-rtc 检索留痕

## Phase 1 WebSearch

1. `阿里云 RTC 自适应 FEC 抗丢包 冗余` → 多条命中，含 developer.aliyun.com / juejin / aliyun help
2. `阿里云 RTC SDK setChannelProfile 通话场景 配置 文档` → ARTC `setChannelProfile('communication'|'interactive_live')`、`setClientRole` 文档
3. `site:help.aliyun.com 音视频通信 FEC 冗余 配置` → mPaaS 多终端音视频文档 169413"改进 FEC 算法 40% 抗丢包"
4. `阿里云 RTC 弱网 FEC 关键帧 非关键帧 冗余率 动态调整` → developer.aliyun.com 文章 668499 / 781463 / 781479 / 783329 等
5. `site:developer.aliyun.com RTC FEC 自适应 业务类型` → light-rtc（781463）、HaaS RTC（785332）等
6. `阿里云 RTC ARTC 通话场景 教育 互娱 配置 文档 setAudioProfile` → help.aliyun.com `setAudioProfile` API 文档（手动配置场景模式）

> 粗筛上限 4，因首两条已显著命中、需深入区分 F1 是否真自动识别，沿着线索追加了 2 条作为 Phase 2 的检索入口；总共 6 条 WebSearch。

## Phase 2 WebFetch / curl

| # | URL | 工具 | 结果 |
|---|-----|------|------|
| 1 | https://help.aliyun.com/document_detail/2640056.html | WebFetch | 200，"精准带宽侦测、抗丢包率支持 70%"，无 FEC 细节 |
| 2 | https://juejin.cn/post/7145069820956901390 | WebFetch | 200，实为字节跳动**火山引擎 RTC** 团队文章（非阿里云）→ 排除 |
| 3 | https://developer.aliyun.com/article/668499 | WebFetch | 200，阿里云李刚 2018-11-07："关键帧 10% / 非关键帧 5%，根据丢包动态调整冗余度" |
| 4 | https://developer.aliyun.com/article/781463 | WebFetch | 200，阿里云熊金水 2021-01-25 light-rtc："FEC 调参：冗余度、MaxFrames、Table 类型；固定 + 动态自适应两类；WebRTC::FecControllerFactoryInterface" |
| 5 | https://zhuanlan.zhihu.com/p/361876006 | WebFetch | 403；PowerShell `Invoke-WebRequest` 兜底亦 403（知乎反爬）— 工具受限 |
| 6 | https://developer.aliyun.com/article/781479 | WebFetch | 200，阿里云 2021-01-26 屏幕共享弱网编码器优化（不涉 FEC） |
| 7 | https://help.aliyun.com/zh/live/user-guide/set-audio-encoding-and-scene-mode | WebFetch | 200，`setAudioProfile(qualityMode, sceneMode)` 入会前手动设置，入会后不可改 |
| 8 | https://help.aliyun.com/document_detail/2640058.html | WebFetch | 200，6 大应用场景（视频会议/在线教育/音乐教学/互动连麦/视频社交/游戏娱乐），未提 SDK 自动识别业务类型 |

## 工具受限明示

- 知乎单篇 `zhuanlan.zhihu.com/p/361876006` WebFetch 403、PowerShell `Invoke-WebRequest` 亦 403（知乎反爬），未能取得正文。该文题为"阿里云 RTC QoS 弱网对抗之变分辨率编码"，主题为编码而非 FEC 业务类型识别，对本判定边际信息有限。
