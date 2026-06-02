# 证据索引 — 19-bilibili-live-rtc

## Phase 1 — react 粗筛 query 留痕
1. WebSearch: `哔哩哔哩 B站 直播 实时传输 弱网 FEC 冗余 抗丢包`
   - 命中 B站技术博客《B站在实时音视频技术领域的探索与实践》(bilibili.com/read/cv19672379)、《B站WebRTC测试实践》(nxrte.com/40585)。相关 → 确认 B站有发送端 FEC/冗余实时传输，继续。
2. WebSearch: `哔哩哔哩 直播 连麦 FEC 冗余 网络状态 业务类型 自适应 QoS 弱网对抗`
   - 命中网易/腾讯/融云通用弱网对抗文 + nxrte B站 WebRTC 文。确认通用 RTC 按"通信 vs 直播"业务类型选 FEC/重传策略、按丢包率动态调冗余度；但这些是行业通法描述，非 B站专属算法披露。
3. WebSearch: `哔哩哔哩 Bilibili 专利 FEC 冗余 自适应 数据传输 网络编码 H04L1/1867`
   - 未检索到 B站在"自适应冗余调度"主题的同主题专利（仅一篇"实时视频流播放方法"专利，与发送端冗余调度无关）。Google Patents assignee:Bilibili + 自适应FEC 未命中本主题。

## Phase 2 — react 深抓
- WebFetch https://bilibili.com/read/cv19672379 — 返回空（SPA，正文由 JS 渲染）。
- curl UA 兜底 https://www.bilibili.com/read/cv19672379 → 落盘 bili-rtc-cv19672379.html（3326 字节，仅 SPA 外壳，正文走 article-web.*.js 异步加载，curl 抓不到正文）。SPA 兜底失败，注明。
- WebFetch https://www.nxrte.com/jishu/webrtc/40585.html — 成功。确认 B站直播互动业务（视频连线/PK/语聊房/语音连麦）底层用 WebRTC；该文为弱网"测试方法论"，未披露 FEC 冗余自适应的算法细节（网络状态+成功率+业务类型三输入 / 时延→传输总时间→调度链均未提及）。

## 已落盘文件
- bili-rtc-cv19672379.html（B站 read 页 SPA 外壳，无正文，仅留痕）

## 工具受限说明
- B站 read 文章正文为前端异步渲染，WebFetch 返回空、curl 仅得 SPA 外壳，无法获取《B站在实时音视频技术领域的探索与实践》正文 verbatim。已用 nxrte 二手转述与通用弱网对抗文交叉佐证 B站确有 FEC/冗余 RTC，但无 B站专属三输入自适应冗余调度的正向 verbatim 证据。
