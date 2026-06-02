# 证据索引 — 02-agora-rtc-sdk

## Phase 1 — WebSearch 留痕（react，逐条）
1. `声网 Agora 弱网 FEC 冗余 抗丢包 自适应 网络状态` → 命中相关：声网技术博客 / 文档披露 FEC+ARQ 自适应抗丢包（ULPFEC、码率自适应、80% 丢包仍可用）。
2. `声网 Agora 专利 冗余 FEC 业务类型 网络状态 传输成功率 自适应 patent` → 命中相关：SD-RTN 演进文披露"根据网络链路评估状况，根据所需的 QoS 级别，采用 FEC 或多路冗余"；自研 FEC、AUT 协议、强化学习全链路流控。
3. `Agora Shanghai patent FEC redundancy ... 2021 2022` → 未检索到声网名下 verbatim 同主题专利（仅他方 FEC 专利）。
4. `声网 AUT Agora Universal Transport FEC 冗余比例 业务场景 RTC FPA 弱网评估 调度` → 命中相关：AUT 自研传输层，Stream 级别通用信道编码 / 不同编码力度保护；不同业务场景不同传输需求。
5. `"上海兆言" OR "Agora Lab" ... 冗余 数据包 网络状态 业务类型` → 未检索到声网名下 verbatim 命中专利。
6. `Agora Lab Inc patent forward error correction ... justia/google patents` → 未检索到声网名下 FEC 专利（结果均为他方）。

## Phase 2 — WebFetch / curl 深抓
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2021-09-23 | 博客(mirror) | https://www.cnblogs.com/rtedev/p/15325518.html ；本地 cnblogs-sdrtn-15325518.html | verbatim "根据网络链路评估状况，根据所需的 QoS 级别，采用 FEC 或多路冗余等技术，来实现包级别的实时可靠投递"；路由按链路质量/带宽/QoS 要求/负载计算下发——支持 F2 部分（网络状态+QoS/业务级别），但未披露"传输成功率"第三输入、F1 自动业务识别、F3/F4 时延→总时间→调度链。 |
| 2 | 2021-10-11 | 博客(mirror) | https://www.cnblogs.com/Agora/p/15394528.html ；本地 cnblogs-weaknet-15394528.html | "开启 FEC 和 NACK 同时工作的机制"；FEC+NACK 配合抗丢包；未披露冗余量三输入计算、业务类型自动识别、时延调度链。 |
| 3 | 2022-06-29 | 博客 | https://zhuanlan.zhihu.com/p/535602151 （WebFetch）；zhihu/shengwang 镜像 curl SSL 握手失败，无法落盘 | AUT："不同的 Stream 在重传、流控等差别之外，还具备不同编码力度的保护"；Stream 级通用信道编码、分组码集成——支持"按业务/流差异化冗余保护"概念，但未披露具体三输入冗余量、F1 自动识别、F3/F4 链。 |

## 工具受限说明
- WebFetch 对 zhihu.com / shengwang.cn 返回 "unknown certificate verification error" 或 HTTP 500；curl 对 zhihu.com 返回 schannel SSL/TLS 握手失败，无法落盘。改用 cnblogs.com 官方镜像（声网/RTE 开发者社区授权转载）成功 WebFetch + curl 落盘两篇。
- 未检索到声网名下（Agora Lab / 上海兆言）verbatim 披露权 1 F1-F5 链的公开专利，无法一步定档。
