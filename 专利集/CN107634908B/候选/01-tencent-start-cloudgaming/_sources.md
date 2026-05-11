# Sources — 01 Tencent START Cloud Gaming

> 关联候选：T2-01 腾讯 START 云游戏 + 先游 + GameMatrix
> 关联独立权：权 1（方法） + 权 8（智能电视 / 手柄 OEM 内置时设备权）
> 主体类型：T2 云游戏 / 远程渲染

## 命中证据（每条标 §A.9a 时间档）

| # | 类型 | URL | 时间档（专利授权 2021-06-08 后）| 命中 F# | 要点 |
| --- | --- | --- | --- | --- | --- |
| 1 | §A.2 学术阵地 — NSDI 2024 论文 | [usenix.org/conference/nsdi24/presentation/wang-shibo](https://www.usenix.org/conference/nsdi24/presentation/wang-shibo) | 2024-04（授权后） | F2/F3/F4 | **Pudica**：零排队 congestion control，自适应 packet pacing |
| 2 | §A.2 + §A.7 学术阵地 + 上游开源 — NSDI 2024 论文 | [github.com/hkust-spark/hairpin](https://github.com/hkust-spark/hairpin) | 2024-04 | F2/F4 | **Hairpin**："重传和 FEC 相结合的可靠传输机制 + 实时监测 RTT 和丢包事件，动态调整 FEC 参数" — 字面命中 F2 |
| 3 | §A.2 学术阵地 — NSDI 2024 论文 | [usenix.org/conference/nsdi24/presentation/zhou-yuhan](https://www.usenix.org/conference/nsdi24/presentation/zhou-yuhan) | 2024-04 | F1/F3 | **AUGUR**：Wi-Fi + Cellular 双链路 + 长尾时延 |
| 4 | §A.3 宣传材料 — 腾讯高校合作 | [ur.tencent.com/article/1481](https://ur.tencent.com/article/1481) | 2024-04 | F2/F3/F4 | 三论文同时入选 NSDI 2024 + 已部署到 START 大规模云游戏平台 |
| 5 | §A.3 + §A.4 产品页 / 文档 | [start.qq.com](https://start.qq.com) | 持续更新 | F5 | START 客户端 (PC / Android / iOS / 智能电视 / Mac) 部署 |
| 6 | §A.13 视频演讲 | NSDI '24 Pudica YouTube 演讲 [youtube.com/watch?v=U9phrVSsr-8](https://www.youtube.com/watch?v=U9phrVSsr-8) | 2024-09 | F2/F4 | 学术演讲完整阐释 |

## 0 命中 / 工具能力受限留痕

- §A.1 反向专利墙：工具能力受限，未能在 IncoPat / 智慧芽穷尽腾讯 H04L1/00 后续族系
- §A.6 联合案例：GameMatrix B 端云游戏 PaaS 服务米哈游、咪咕快游等下游使用方 — 间接证据（米哈游云·原神部分用 GameMatrix）
- §A.11 财报：腾讯财报无单独 START 业务条目
- §A.12 招标：N/A（2C 业务）
- §A.20 反向工程：成本超出本轮，建议法务决定

详细 §D 三栏 verdict 见 [`_verdict.md`](./_verdict.md) 或 master [`../../CN107634908B"潜在违约".md`](../../)。
