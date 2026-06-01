# 22-xag-control 检索 + 抓取留痕

候选：极飞 XAG 农业无人机控制 / 数据链 / 飞控
专利公开（授权）日：2021-06-08

## Phase 1 — WebSearch (react 串行 5 query — 头 4 个按粗筛规则，q5 为追加)

| # | Query | 命中数 / 反向证据信号 | 备注 |
|---|---|---|---|
| q1 | `极飞 XAG 无人机集群控制 通信协议 抗丢包` | 仅返回 XAG 产品首页 / 产品族列表（V50 Pro、P100、R150 等）— 无任何技术细节 | 无技术信号、无反向证据 |
| q2 | `XAG RTK SuperX 通信链路 数传 FEC 冗余` | 命中 SUPERX 飞控页（仅文案"数据链路无缝切换"）+ 通用 FEC 算法教程；无 XAG 自身 FEC 实现细节 | "data link seamless switching" 仅一句营销文案 |
| q3 | `XAG agricultural drone communication protocol packet loss redundancy` | 命中 XAG Local Network Terminal + DL1 Data Link + ARC3 Pro 等产品描述；无协议级技术细节 | 只确认 "在 4G 信号差或无 4G 环境提供稳定通信链路" |
| q4 | `XAG DL1 data link "forward error correction" OR "FEC" OR "redundancy" drone telemetry` | DL1 经销页 / FCC 用户手册 PDF / pegasusrobotics 列页 — 无 FEC / 冗余 / 调度技术陈述 | FCC PDF 是 binary，文本不可抽取 |
| q5（追加） | `"XAG" OR "极飞" UAV data link "数据链" protocol scheduling redundant packet adaptive` | 命中 `protocols.xag.cn` —— 抓取后发现实际是 **用户协议 / 隐私权 / 售后服务合同** 站点，**非通信协议**（"协议" 在中文里同时表示 agreement 与 protocol，此处为 agreement） | 进一步确认 XAG 不公开通信协议技术文档 |

Phase 1 小结：5 个 query 中 0 个返回任何关于"业务类型识别 / 主动冗余包数量决策 / 冗余包调度方法"的技术陈述；同时 0 个返回"明确不使用 FEC / 不区分业务类型 / 仅用 ARQ"等反向证据。判定为 **公开资料严重不足** 模式，不进入 5 档（已排除）档位。

## Phase 2 — WebFetch / curl 兜底（react 串行 10 次）

| # | URL | 工具 | 状态 | 抽取到的载荷 |
|---|---|---|---|---|
| f1 | https://fcc.report/FCC-ID/2A46G-M3DL1A/7816239.pdf （XAG DL1 Data Link User Manual EN v1.0） | WebFetch | PDF binary，HTML→Markdown 渠道无法抽取（已落盘 2.1MB） | 无可用文本 |
| f2 | https://www.xag.cn/flight-controller （SuperX 飞控页） | WebFetch | unknown certificate verification error | 失败 |
| f3 | 同上 | curl -sk | TLS 握手失败（exit 35 / HTTP_CODE=000） | 失败 — XAG 国内域名 TLS 配置拒绝本工具链 |
| f4 | https://manuals.plus/xag/dl1-data-link-extended-long-range-system-manual | WebFetch | 403 Forbidden | 失败 |
| f5 | https://www.pegasusrobotics.com/products/xag-dl1-data-link-cn | WebFetch | 抓回经销页 — 仅产品名 / SKU / 价格 / app 下载链接，**无任何技术规格**（频率 / 调制 / 距离 / 延迟都没有） | 无技术信号 |
| f6 | https://dronetechpro.com/accessories/xag-dl1-data-link/ | WebFetch | 同上 — 仅经销列页 | 无技术信号 |
| f7 | https://www.xa.com/en | curl -sk | 200，52KB —— 公司介绍页，无协议技术 | 无 |
| f8 | https://www.xa.com/en/superx | curl -sk | 404 | 无此页 |
| f9 | https://www.xa.com/service/downloads | curl -sk | 200，222KB —— 已 grep `SDK\|FEC\|协议\|冗余\|丢包\|前向纠错` 全部 0 命中（仅 JS 协议探测代码假阳性） | 无 SDK / 无技术文档下载 |
| f10 | https://protocols.xag.cn/ + README.md + _sidebar.md | curl / Read | 200 —— **docsify 客户端站点；内容确认是"用户协议 / 隐私权 / 电力服务合同 / 硬件增值保障服务合同 / 炸机照片要求"**，不是通信协议 | 反而构成"XAG 不公开通信协议文档"的间接证据 |

## 反向证据搜索结果

- 未检索到任何 XAG 官方 / 第三方文档**明确**陈述："不使用主动冗余 / 仅使用 ARQ / 不区分业务类型 / 固定调度间隔"。
- 未检索到 XAG 的开发者 SDK / 协议白皮书 / 学术合作论文披露具体传输层方案。
- 未检索到任何 "XAG 与华为存在数据传输专利交叉许可" 或 "已规避 CN107634908B" 的公告。
- 同时也**未检索到**任何 XAG 文档**正向**陈述 "按业务类型自适应决策冗余包数量"。

**关键裁决依据**：缺失"反向证据"≠"已排除"；缺失"正向证据"≠"已确认"。本候选两侧都缺，属公开资料不足。
