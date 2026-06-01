# 33-aws-global-accel 检索粗筛 + 深抓 query / URL 留痕

## Phase 1：WebSearch（4 次）

| # | Query | 关键结果 / 信号 |
|---|-------|----------------|
| q1 | `AWS Global Accelerator FEC packet-level redundancy forward error correction` | 0 条结果将 AWS Global Accelerator 与 FEC 并列；FEC 出现在 F5 BIG-IP / Fortinet / SMPTE 2022-7 / MediaConnect 等其他产品。官方 AWS 结果（FAQs / How it works）描述机制为 anycast + backbone routing，不涉及 FEC。 |
| q2 | `AWS Global Accelerator architecture anycast TCP termination adaptive redundancy` | 多个 AWS 官方文档命中；明示机制为 anycast IP + edge TCP termination + 双静态 IP（network zone A/B）。"adaptive redundancy" 语义被官方文档限定为"健康检查驱动的 endpoint 切换"——不是包级 FEC。 |
| q3 | `site:aws.amazon.com Global Accelerator FEC forward error correction packet loss` | 站内 0 命中；FEC 在 AWS 上下文中只与 MediaConnect / Nova Sonic / Elemental Live 关联，与 Global Accelerator 无关。Global Accelerator 抑制丢包的方式被明示为"沿 AWS backbone 走最优路径"，非 FEC。 |
| q4 | `"AWS Global Accelerator" UDP packet duplication retransmit redundant copies` | 0 条结果显示 Global Accelerator 主动复制 UDP 包；UDP 处理被明示为"分片转发 + endpoint 重组"。再次确认服务不做包级冗余副本。 |

## Phase 2：WebFetch（2 次成功 — 已足以闭合判定）

| # | URL | 用途 / 抽取结论 |
|---|-----|----------------|
| f1 | https://aws.amazon.com/global-accelerator/faqs/ | 官方 FAQ；明确表述：(a) 机制为 anycast routing + edge proxy；(b) 0 处提及 FEC / 冗余副本生成 / 业务类型自适应；(c) "redundant" 一词仅指网络 + 双 IP。 |
| f2 | https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html | 官方开发者指南 "How it works"；完整机制描述（anycast + edge TCP 终结 + 健康检查 + traffic dial + endpoint weight + UDP 分片转发 / TCP 分片在 edge 丢弃 + ICMP 行为 + idle timeout）；0 处提及 packet-level proactive redundancy。 |

## Phase 2 未触发的源（资源节流）
- AWS blog "Maximising application resiliency with Global Accelerator" — 标题级阅读已显示话题为 endpoint 健康切换 + 多 AZ 部署，与 packet-level FEC 无关，不再独立 WebFetch。
- AWS blog "Achieve up to 60% better performance for internet traffic" — 标题级阅读显示话题为路径优化 / 测量方法 ，与 packet-level FEC 无关，不再 WebFetch。
- 公开第三方资料（jayendrapatil / tutorialsdojo / digitalcloud）— 均为对官方文档的二次整理，权重低于官方原文，未独立抓取。

## 工具受限说明
- 本次未发生 WebFetch 失败 / 重定向，未触发 curl 兜底。
- 4 次 WebSearch + 2 次 WebFetch 已足以形成 3 条独立反向证据（机制不同义 + 业务类型未识别 + 定位非"发送端"），按"反向证据明确时止 search"原则收敛，未继续耗用其余 Phase 2 quota。
