# 09-netease-yunxin sources

## Phase 1 WebSearch queries (react 串行, 4/4)

| # | query | 命中要点 |
|---|---|---|
| q1 | 网易云信 NERTC FEC 自适应 抗丢包 业务类型 | NERTC 文档首页/性能指标/dev-blog 弱网优化；提及"QoS 保障 = UDP 拥塞控制 + FEC + 重传 + 码率自适应" |
| q2 | 网易云信 NERTC channel profile scene 场景 setChannelProfile 通信 直播 | 决定性 F1 反向证据：场景化配置文档明示 `setChannelProfile(channelProfile)` 由上层 App 指定 COMMUNICATION/LIVE_BROADCASTING/VideoCall/HighQualityVideoCall/Chatroom 等 |
| q3 | 网易云信 NERTC 自适应 FEC 冗余 算法 丢包率 码率 NACK | "RTC 系统音频弱网对抗技术发展与实践"博客；FEC 算法为 XOR/Reed-Solomon/喷泉码 |
| q4 | "网易云信" OR "NERTC" 业务类型 自动识别 流量统计 数据流特征 冗余包 | 0 命中专利所述"流量统计自动识别业务类型"的功能描述 |

补充 q5（网易云信 视频 FEC 冗余度 算法 GE模型 丢包率 视频码率 自适应）— Phase 2 前确认，仍未找到三元组（业务类型）作为冗余计算输入的证据；反而确认 GCC 带宽估计 + 丢包率 + RTT 是主要输入。

## Phase 2 WebFetch (6 个 URL，含 1 个 curl 兜底)

| URL | 取证目标 | 关键发现 |
|---|---|---|
| https://doc.yunxin.163.com/nertc/guide/DA1NTQwNjY?platform=windows | NERTC 场景化音视频配置 | 首次 WebFetch 被反爬拦截 ("Bot not welcome")；curl 兜底成功 (1.3 MB HTML)，本地提取关键段：场景**由上层 App 通过 setChannelProfile 显式指定**，影响"音视频码率、帧率、视频分辨率、视频大小流模式、自动打开视频、自动订阅视频、**传输策略**" |
| https://www.cnblogs.com/wangyiyunxin/p/14715812.html | 音频弱网对抗技术 | 反爬；改用 163.com 镜像 |
| https://www.163.com/dy/article/G8JG3N9T0518X1HL.html | 弱网对抗技术（镜像） | "FecDelay = Block 个数 × 帧长"；ARQ 重传次数与丢包率相关；Opus inband FEC 在 Speech 场景下 ~20% 丢包；**冗余包数量决策三因素未明示**；调度算法细节未涉及 |
| https://www.nxrte.com/jishu/yinshipin/22164.html | 音频 QoS 综述（决定性证据） | **决定性反向证据**："FEC 冗余度和原始包分组长度计算准则是：根据丢包和 rtt 预置分组长度，在该分组长度下，根据贝叶斯定律，在当前丢包率下，确定至少需要多少冗余包"——冗余包数量 = f(丢包率, RTT)，**业务类型不参与冗余包数量计算**；恢复延迟 = 最大序号差，非"从时延要求换算"；调度仅含连续/跳跃二选一，非随机/最短/最长/均匀动态选择 |
| https://blog.csdn.net/netease_im/article/details/120300346 | QoS 策略介绍 | 通用框架层，未提业务类型识别；FEC+NACK 组合；未含数据流特征变量 |
| https://www.cnblogs.com/wangyiyunxin/p/14113392.html | QoS 平衡之道 | 关键场景差异化证据："通信场景：更多用 FEC，重传作为辅助；直播场景：更多用重传，FEC 作为辅助"——确认场景影响 FEC/重传配比，但场景本身仍是上层指定，且冗余包数量计算仍是丢包/RTT 驱动 |

## 工具受限说明
- 网易云信官方 doc 与 cnblogs 镜像均对 WebFetch 启动了 "Bot not welcome" 反爬
- curl 配合浏览器 UA 兜底成功；本地用 Python 提取关键关键词上下文
- CSDN 镜像与第三方转载（nxrte / 163 dy）内容与官方一致，可交叉验证

## 候选证据落盘
- `nertc-scene-config.html` (1.3 MB) — 场景化配置 doc 完整 HTML（curl 兜底）
- `_extract.txt` — 关键关键词上下文提取（UTF-8）
