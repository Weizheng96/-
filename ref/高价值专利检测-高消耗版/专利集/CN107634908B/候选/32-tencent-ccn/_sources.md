# 证据索引 — 32-tencent-ccn

## Phase 1 WebSearch queries

### q1: `腾讯云 CCN 云联网 FEC 主动冗余`
- https://cloud.tencent.com/document/product/877/18675 — 云联网 产品概述
- https://cloud.tencent.com/product/ccn — 云联网 CCN 产品页
- https://www.shangyun51.com/productdetail?id=449 — CCN 简介（第三方转载）
- https://www.tencentcloud.com/products/ccn — 国际版产品页
- https://cloud.tencent.com/document/product/877 — 云联网文档总览
- https://main.qcloudimg.com/raw/document/product/pdf/877_18673_cn.pdf — 云联网产品简介 PDF
- https://cloud.tencent.com/document/product/215/53884 — VPC 下的云联网
- https://cloud.tencent.com/document/product/215/19204 — 私有网络创建 CCN API
- https://cloud.tencent.com/developer/article/1020364 — 基于内容关键性的高效 FEC 抗网络丢包算法（注：与 CCN 无关，VoIP 上下文）
- https://cloud.tencent.com/document/product/301/37292 — 云联网 SLA

**初判**：除 1 篇与 CCN 无关的 VoIP FEC 文章外，**所有 CCN 官方文档均未出现 "FEC / 主动冗余 / 冗余包" 字样**。CCN 关键词为 "全网互联 / 智能调度 / 路由自学习 / 链路选优 / 故障快速收敛"，全部为 path-level / 路由层能力。

### q2: `Tencent Cloud CCN packet-level redundancy forward error correction`
- https://www.tencentcloud.com/techpedia/103160 — How does UDP handle packet loss and errors?（techpedia 通用文，与 CCN 产品无关）
- 其余结果为 USPTO 专利文档与学术论文，**均与 CCN 产品无关**

**初判**：英文检索同样未发现 CCN 与 packet-level FEC 的关联描述。

### q3: `腾讯云 云联网 CCN 业务类型 冗余包 自适应 丢包`
- https://cloud.tencent.com/document/product/877/18675 — 云联网 产品概述（重复命中）
- https://cloud.tencent.com/product/ccn — 产品页（重复）
- https://www.cnblogs.com/qcloud1001/p/14068039.html — 腾讯云博客《带宽利用率提升50%，腾讯云联网架构方案解析》
- https://zhuanlan.zhihu.com/p/323800776 — 知乎转载同上
- https://www.cnblogs.com/RilyLC29/p/TencentCC3.html — 腾讯云从业者认证笔记

**初判**：CCN 丢包应对依靠"专线故障时自动恢复 / 链路故障快速收敛"，即**链路级故障切换**，而非"按业务类型生成冗余包"。

## Phase 2 WebFetch（仅 1 次，已锁定反向证据，无需深抓）

### WF1. https://cloud.tencent.com/document/product/877/18675
- **Verbatim 命中**："全网多点互联、路由自学习、链路选优及故障快速收敛等能力"
- **反向命中**：
  - 未提及 packet-level FEC / 前向纠错 / 主动冗余包
  - 未提及按业务类型（控制消息 / 在线游戏 / 视频 / IoT）自适应决策
  - 未提及监测丢包率 / 传输成功率并据此生成冗余包
  - 明确定位为**链路选优**层面的优化（"链路选优"= path-level selection，不是 packet-level redundancy）

## 证据索引表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | — | 官方文档 | https://cloud.tencent.com/document/product/877/18675 | 反向：CCN 自定位为"路由自学习 / 链路选优 / 故障快速收敛"，无 packet-level FEC |
| 2 | — | 官方产品页 | https://cloud.tencent.com/product/ccn | 反向：同上，业务定位为跨地域 VPC / IDC 互联 |
| 3 | — | SLA | https://cloud.tencent.com/document/product/301/37292 | 反向：SLA 维度为可用性 / 链路恢复，非传输成功率主动补偿 |
| 4 | — | 第三方综述 | https://www.cnblogs.com/qcloud1001/p/14068039.html | 反向：架构方案关键词为"带宽利用率 / 智能调度 / SDN 控制面" |
