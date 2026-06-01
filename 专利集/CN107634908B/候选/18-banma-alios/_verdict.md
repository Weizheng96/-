# 18-banma-alios verdict

## 候选基本信息（专利公开日 2021-06-08）
- 类型：产品
- 名称：斑马 AliOS / 智驾 OTA 通道
- 组织：斑马智行（上汽 + 阿里合资 / 重组后阿里主导）
- 命中 F#（初判）：F2, F3, F4, F5
- 公开度：低（meta.json 即标 "低"；本轮 react 检索证实公开技术细节确实极少）
- 一句话定位：上汽阿里合资车联网，AliOS 之上的 OTA 下发通道与车云通信框架。
- 评估锚定的专利时间窗：候选公开材料必须 ≥ 2021-06-08；本轮检索到的资料含 2016 年 RX5 首发、2018 云栖大会、2022 智能驾驶系统内核、2023 操作系统方法论、2025 端侧大模型方案，时间窗本身覆盖足够（不是因为时间窗被排除）。

## 检索粗筛（react 串行 4 次 WebSearch — 已达上限）

| # | query | 命中 F# 正向信号 | 备注 |
|---|-------|-----------------|------|
| q1 | `斑马 AliOS 智驾 OTA 通道 抗丢包 冗余` | 0 | 命中通用 OTA 解决方案页 (opens.alios.cn / g.alicdn / AliOS-Things wiki)，止步于通道枚举与"断点续传"，无 FEC / 业务类型自适应 |
| q2 | `Banma AliOS Auto vehicle cloud protocol redundancy FEC packet loss` | 0 | 命中 Banma 公司战略报道 + F5 / FS 等通用 FEC 介绍，斑马自身 FEC 实现 0 资料 |
| q3 | `斑马智行 车云通信 协议栈 自适应 冗余 业务类型` | 0 | 命中架构 / 中间件 / Fusion SOA 框架描述，未触及传输层冗余调度 |
| q4 | `"AliOS" OR "斑马" 传输层 丢包率 主动冗余 专利 OR 论文` | 0 | 命中清华孟子立 PhD 论文（Hairpin 联合丢包恢复，非斑马实现）与 36 氪重组报道；无斑马传输层冗余 paper / 专利 |

**剪枝判断**：4 次 query 全部 0 命中任何 F# 正向信号；同时未发现可深抓的具体技术白皮书 / 学术论文 / GitHub 实现代码 / API 文档段落 — 没有"可深抓的目标"则进入 Phase 2 也无意义。按 SKILL 协议早剪枝。

## F# 命中表（F1-F5）

| F# | 特征摘要 | 命中状态 | 证据（verbatim / URL） |
|----|---------|---------|----------------------|
| F1 | 业务类型识别 — 基于发送端"数据流特征变量"自动得到（缓存包长度/数目、在途包长度/数目、到达间隔、突发性 ≥1 项） | 未知 | 公开材料未披露 AliOS / Fusion / OTA 通道在传输层是否做了基于数据流特征变量的业务类型自动识别 |
| F2 | 冗余包数量 = f(网络状态变量, 传输成功率, 业务类型) — 三元组联合 | 未知 | 同上；公开材料仅提及 OTA 支持"弱网断点续传"（reactive 续传 ≠ proactive 冗余） |
| F3 | 冗余包传输总时间 ← 时延要求 | 未知 | 公开材料未披露 AliOS / 斑马传输层是否按时延要求计算冗余包总发送窗口 |
| F4 | 调度方法 = g(网络状态, 总时间, 冗余包数量) — 三元组联合，并从随机度/最短/最长/均匀时间至少 1 种 | 未知 | 公开材料未披露任何调度策略细节 |
| F5 | 按调度方法发送冗余包 | 未知 | 公开材料未披露主动 FEC / packet-level 冗余发送动作；仅见 HTTP/HTTPS/BLE/3G/4G 等通道枚举与"断点续传" |

**初判 vs 终判变化说明**：meta.json 初判 F2/F3/F4/F5 命中是基于"OTA 通道天然需要解决弱网传输"的语义猜测；本轮 react 检索后，4 个特征均无任何公开证据支持，但同时也无反向证据（即未检索到任何资料明确说 AliOS / 斑马传输层"没有用业务类型自适应冗余 / 只用 TCP 重传 / 无主动 FEC"）。按 "0 命中 ≠ 已排除" 原则，不能落 "已排除" 档。

## 已检查文档清单

Phase 1 粗筛 4 次 query 扫描到的页面（未做 Phase 2 单页 WebFetch 深读，理由见上节）：

1. https://opens.alios.cn/solution/ota.html — AliOS 官方 OTA 解决方案页（仅枚举通道与"断点续传"）
2. https://g.alicdn.com/alios-things-3.3/doc/ota.html — AliOS Things 3.3 OTA 文档（设备 OTA 升级流程，不涉传输层冗余调度）
3. https://github.com/alibaba/AliOS-Things/wiki/AliOS-Things-OTA-Porting-Guide — AliOS Things OTA 移植指南（接口与流程，无冗余 / FEC 算法）
4. https://www.ebanma.com/product.html — 斑马网络产品页（位置 / 支付 / 语音 / AR / 智慧服务，无传输层细节）
5. https://zebred.com/ — 斑马网络官网首页（业务方向描述）
6. https://m.leiphone.com/category/transportation/uxXFRJv36CUYFodi.html — 雷峰网 2018 云栖大会 AliOS 发布报道（产品方向，无技术内核）
7. https://finance.sina.com.cn/tech/2022-04-08/doc-imcwiwst0646658.shtml — 新浪 2022 斑马智行智能驾驶系统内核优势分析（微内核稳定性，未涉车云传输层）
8. https://www.qbitai.com/2025/09/336947.html — 量子位 2025 斑马智行端侧大模型实车方案（AI 大模型上车，不涉传输层）
9. https://i.gasgoo.com/news/70314808.html — 2022 WICV 袁博演讲（OS 探索与创新，未涉 F1-F5）
10. http://www.cnautonews.com/lingbujian/2023/04/20/detail_20230420356470.html — 2023 斑马智行汽车 OS 世界观方法论（架构方向）
11. https://zh.wikipedia.org/zh-cn/斑马智行 — 维基百科斑马智行条目（沿革与产品）
12. https://equalocean.com/analysis/2020052614032 — EqualOcean Banma 战略分析（无技术细节）
13. https://www.prnewswire.com/news-releases/banma-rolls-out-its-first-year-of-operation-of-internet-connected-vehicle-300748804.html — Banma 首年运营公告
14. https://zilimeng.com/papers/phd_thesis.pdf — 清华孟子立博士论文（Hairpin 联合丢包恢复，与斑马 / AliOS 无关联，仅作为传输层 FEC 学术对照）
15. https://36kr.com/p/1724429320193 — 36 氪 AliOS / 斑马重组报道

## 最终判定 **第 4 档：公开资料不足**

判定理由：
- F1-F5 全部 "未知"，**0 命中也 0 反证**。
- 斑马 / AliOS 在传输层 / OTA 通道的技术细节几乎完全闭源（OTA 文档止步于通道枚举与"断点续传"），无白皮书 / 学术论文 / 开源代码 / 专利交叉引用可供锚定。
- "断点续传 / TCP-based OTA"和"主动 FEC + 业务类型自适应冗余"在外部观察者视角不可区分——既不能据此命中权 1，也不能据此排除权 1。
- 不落"已排除"（缺反向证据 — 未检索到任何说明 AliOS / 斑马不使用主动冗余 / 不区分业务类型 / 仅依赖 TCP 重传的资料）；不落"疑似侵权"（缺正向证据）；只能落第 4 档。

## 升级路径（3-4 档时）

要把本候选从"公开资料不足"升级到"疑似 / 确认侵权"，需要：
- 拿到 AliOS / 斑马**车云通信 SDK 源代码** 或 反编译产物，定位 send 路径是否调用 FEC 编码器并以"业务类型"为输入参数；
- 或 斑马 / 阿里**专利申请文件**（CN 国知局检索）中描述车云传输层冗余调度的同族 / 引用专利，反查是否引用或绕开 CN107634908B；
- 或 斑马技术人员**公开技术演讲 / Paper**（云栖 / WAIC / WICV / IEEE）直接讨论 OTA / 车云通道的 FEC 自适应策略；
- 或 第三方**抓包测试**（实际车机抓取上行 / 下行 packet，分析是否有冗余副本及其调度规律）。

要把本候选下降到"已排除"档，需要：
- 公开资料明确陈述 AliOS / 斑马 OTA 通道**仅依赖 TCP / HTTPS 标准协议栈无应用层 FEC**（reactive 重传），或
- 明确陈述其冗余策略**不区分业务类型**（仅做网络状态自适应），或
- 时间锚证据 — 例如核心传输模块版本固化于 2021-06-08 之前且之后无更新（本轮未检索到此类证据）。

## 总结一句话
斑马 AliOS / 智驾 OTA 通道公开技术细节极少，4 次 react 粗筛 0 命中任何 F# 正向证据，亦无反向证据，落**第 4 档：公开资料不足**；建议保留候选，待 SDK / 抓包 / 专利同族数据再复评。

---

**免责声明**：本判定为基于公开材料的技术档位评估，不构成法律意见，更不构成"已构成侵权"的终局结论。是否真正落入权利要求 1 / 8 的保护范围，需由权利人通过司法 / 仲裁程序结合非公开技术资料正式举证认定。
