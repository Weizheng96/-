# 证据索引 — 01-agora-rtc-sdk

## Phase 1 — 粗筛 query 留痕
- query 1: `Agora 声网 Adaptive FEC 自适应前向纠错 冗余 丢包率` → 命中：声网官方/知乎确认 Agora SDK 实现 Adaptive FEC（按实时丢包率动态调整冗余比例）+ 自适应 Jitter Buffer。信号相关。
- query 2: `声网 Agora FEC 冗余 业务类型 音频 视频 区分 时延 抗丢包 算法` → 命中：SD-RTN 自研 FEC 配合 SVC 实现不对等保护；"针对不同业务需求提供不同传输策略，配合 AUT 协议"。业务类型差异化信号。
- query 3: `声网 Agora AUT 传输协议 QoS 时延 冗余调度 SD-RTN 自研 FEC 论文` → 命中：AUT(Agora Universal Transport)；SD-RTN 三档时延 QoS(200ms/800ms/2s 内 99.9% 到达率)，按 QoS 级别采用 FEC/多路冗余。强信号。
- query 4: `声网 Agora 专利 自适应 冗余 FEC 数据传输 业务类型 调度 patent` → 未检索到声网自有同主题授权专利公开来源（无 Google Patents 直接命中）。
- query 5(补): `声网 AUT Agora Universal Transport 拥塞控制 冗余 FEC 业务 时延 弱网对抗 实现` → 命中 AUT 落地实践多镜像；确认 AUT 含流量模型检测、按 Stream 区分业务、流级通用信道编码集成 FEC。

## Phase 2 — 深抓

| # | 时间(发布日) | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | (后端500) | 官方 | https://www.shengwang.cn/cn/community/blog/24335 → 本地 aut-blog.html | WebFetch 500；curl 浏览器 UA 兜底仍 Nuxt 服务端 500（非 SPA 壳，是后端错误），落盘仅 error page(1881B)，放弃官方源改镜像 |
| 2 | 2021-01-06 | 官方镜像(CSDN agora_cloud) | https://blog.csdn.net/agora_cloud/article/details/112300742 | 三档时延 QoS(200ms/800ms/2s 内 99.9% 到达率) + 按 QoS 级别采用 FEC/多路冗余；冗余量计算/调度细节未披露。【发布日 < 专利公开日 2021-06-08，仅作机制理解，不单独计侵权证据】 |
| 3 | 2022-06-29 | 官方镜像(CSDN agora_cloud) | https://blog.csdn.net/agora_cloud/article/details/125530984 | AUT 含 traffic model detection(流量模型检测)、按 Stream 区分业务(音视频)、Stream 内通用分组编解码框架易集成 FEC 分组码；冗余量三输入耦合/时延预算发包窗口/调度方法细节未披露。> 专利公开日 |
| 4 | 2021-09-23 | 官方镜像(博客园 rtedev) | https://www.cnblogs.com/rtedev/p/15325518.html | verbatim 三档时延 QoS + 按 QoS 采用 FEC/多路冗余；F2/F4 自适应算法细节未披露。> 专利公开日 |

## 工具能力受限说明
- 声网官方 shengwang.cn / agora.io 社区文章正文经 WebFetch 与 curl(浏览器 UA) 均触发后端 500，无法取官方一手正文；已改用 CSDN/博客园官方账号转载镜像（agora_cloud / rtedev 均为声网官方运营账号）作为等价一手来源。
- 未检索到声网自有"自适应冗余/业务类型感知 FEC"授权专利公开来源，无法用竞品自有专利做 verbatim 机制比对。
