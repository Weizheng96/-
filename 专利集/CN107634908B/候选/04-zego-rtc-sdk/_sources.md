# 证据索引 — 04-zego-rtc-sdk

## Phase 1 — react 粗筛 query 留痕
1. WebSearch: `即构 ZEGO 弱网 FEC 冗余 抗丢包 自适应`
   - 信号：ZEGO 自研音视频引擎，70% 丢包下流畅；自适应 FEC 随网络状态动态调整保护策略。→ 相关，继续。
2. WebSearch: `即构 ZEGO 自适应FEC 冗余比例 网络状态 业务类型 QoS 弱网`
   - 信号：自适应 FEC 依丢包率动态决定冗余包数量；冗余率按最大端到端 Delay + 网络指标计算。未见 ZEGO 官方对"网络状态+业务类型"三输入明确披露。
3. WebSearch: `即构 ZEGO 专利 自适应冗余 FEC 调度 网络编码 数据传输`
   - 未检索到 ZEGO 自有同主题专利。找到 ZEGO 高可用架构博客（与本权要无关）。
4. WebSearch: `ZEGO 即构 70%丢包 弱网 抗丢包 传输 FEC ARQ 冗余 技术 博客`
   - 命中 ZEGO 官方 InfoQ 系列文《如何实现70%丢包下音视频的高可用之数据篇》→ Phase 2 深抓。
5. WebSearch: `即构科技 专利 数据传输 冗余 自适应 FEC 2022 2023 权利要求`
   - 未检索到 ZEGO 自有数据传输/冗余调度专利公开来源。

## Phase 2 — 深抓
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-10-18 | 弃用 | https://www.cnblogs.com/zegoinfo/p/17773031.html | ZEGO 高可用架构，与 FEC/冗余权要无关 |
| 2 | 2019-12-19 | **主证据** | https://www.infoq.cn/article/dqitwxsccjg805vujjtn （落盘 infoq-data-70loss.html, 314KB） | ZEGO 官方：混合 FEC&ARQ(HARQ) 按 RTT/PLR 智能决定比例；带宽分配按 RTT/PLR 给冗余包分配带宽。**注意发布日早于专利公开日 2021-06-08** |
| 3 | n/a | 弃用 | https://blog.csdn.net/qw225967/article/details/123405345 | 通用 FEC 科普，与 ZEGO 无关 |

## 已落盘文件
- infoq-data-70loss.html — ZEGO 官方《如何实现70%丢包下音视频的高可用之数据篇》正文 HTML

## 工具受限说明
- InfoQ 为 SPA，WebFetch 仅得页框；已按协议用 curl UA 兜底取到正文并 Grep/Python 提取。
- 未在本环境公开来源检索到 ZEGO 自有"数据传输/自适应冗余调度"专利全文（CNIPA 未直查）。
