# 证据索引 — 18-banma-alios

候选：斑马 AliOS / 智驾 OTA 通道
专利公开日：2021-06-08（候选材料时间锚需 ≥ 此日）
评估时间：2026-05-26
检索工具：WebSearch（Phase 1 共 4 次，react 串行，已达上限早剪枝）；Phase 2 WebFetch 未触发。

## Phase 1 粗筛 query 留痕

### q1
- query：`斑马 AliOS 智驾 OTA 通道 抗丢包 冗余`
- 命中 F# 正向信号：0
- 关键 URL：
  - https://opens.alios.cn/solution/ota.html （仅"断点续传"，无 FEC / 业务类型自适应）
  - https://g.alicdn.com/alios-things-3.3/doc/ota.html （OTA 升级流程，无传输层冗余调度）
  - https://github.com/alibaba/AliOS-Things/wiki/AliOS-Things-OTA-Porting-Guide （接口与移植，无算法）
  - https://www.ebanma.com/product.html （产品能力描述）
  - https://zebred.com/ （斑马网络官网）
  - https://m.leiphone.com/category/transportation/uxXFRJv36CUYFodi.html （2018 云栖大会报道）
  - https://www.alios.cn/about （AliOS 关于我们）

### q2
- query：`Banma AliOS Auto vehicle cloud protocol redundancy FEC packet loss`
- 命中 F# 正向信号：0
- 关键 URL：
  - https://equalocean.com/analysis/2020052614032 （Banma 战略分析，无技术细节）
  - https://www.prnewswire.com/news-releases/banma-rolls-out-its-first-year-of-operation-of-internet-connected-vehicle-300748804.html （首年运营公告）
  - https://techdocs.f5.com/kb/en-us/products/big-ip-aam/manuals/product/aam-concepts-11-6-0/29.html （F5 通用 FEC 文档，与斑马无关 — 仅作通用对照）
  - https://community.fs.com/blog/a-fec.html （A-FEC 通用介绍，与斑马无关）

### q3
- query：`斑马智行 车云通信 协议栈 自适应 冗余 业务类型`
- 命中 F# 正向信号：0
- 关键 URL：
  - https://zh.wikipedia.org/zh-cn/斑马智行 （沿革与产品）
  - https://finance.sina.com.cn/tech/2022-04-08/doc-imcwiwst0646658.shtml （微内核稳定性分析）
  - https://www.qbitai.com/2025/09/336947.html （端侧大模型实车方案）
  - https://i.gasgoo.com/news/70314808.html （2022 WICV 袁博演讲）
  - http://www.caam.org.cn/search/con_5219242.html （阿里 + 斑马布局智能网联）
  - http://www.cnautonews.com/lingbujian/2023/04/20/detail_20230420356470.html （汽车 OS 世界观方法论）

### q4
- query：`"AliOS" OR "斑马" 传输层 丢包率 主动冗余 专利 OR 论文`
- 命中 F# 正向信号：0
- 关键 URL：
  - https://zilimeng.com/papers/phd_thesis.pdf （清华孟子立博士论文 — Hairpin 方案，非斑马 / AliOS 实现，仅作学术对照）
  - https://zhuanlan.zhihu.com/p/608343240 （知乎传输层协议综述）
  - https://www.zhihu.com/question/284471060 （知乎斑马讨论帖）
  - https://36kr.com/p/1724429320193 （AliOS / 斑马重组报道）
  - https://doc.taixueshu.com/patent/CN107819686B.html （无人机自组网专利，与本候选无关）

## 检索结果汇总表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2024+ | 官方文档 | https://opens.alios.cn/solution/ota.html | OTA 通道枚举 + 断点续传；无 F1-F5 信号 |
| 2 | 2023 | 官方文档 | https://g.alicdn.com/alios-things-3.3/doc/ota.html | OTA 升级流程；无 F1-F5 信号 |
| 3 | 2020+ | GitHub Wiki | https://github.com/alibaba/AliOS-Things/wiki/AliOS-Things-OTA-Porting-Guide | OTA 移植接口；无 F1-F5 信号 |
| 4 | — | 公司官网 | https://www.ebanma.com/product.html | 业务能力描述；无传输层细节 |
| 5 | — | 公司官网 | https://zebred.com/ | 业务方向描述；无传输层细节 |
| 6 | 2018 | 媒体报道 | https://m.leiphone.com/category/transportation/uxXFRJv36CUYFodi.html | 云栖大会产品发布；无技术内核 |
| 7 | 2022-04 | 媒体报道 | https://finance.sina.com.cn/tech/2022-04-08/doc-imcwiwst0646658.shtml | 微内核稳定性分析；未涉车云传输层 |
| 8 | 2025-09 | 媒体报道 | https://www.qbitai.com/2025/09/336947.html | 端侧大模型实车；不涉传输层 |
| 9 | 2022 | 演讲 | https://i.gasgoo.com/news/70314808.html | OS 探索与创新；未涉 F1-F5 |
| 10 | 2023-04 | 媒体报道 | http://www.cnautonews.com/lingbujian/2023/04/20/detail_20230420356470.html | 汽车 OS 方法论；架构层 |
| 11 | — | 百科 | https://zh.wikipedia.org/zh-cn/斑马智行 | 沿革与产品 |
| 12 | 2020 | 战略分析 | https://equalocean.com/analysis/2020052614032 | 公司战略；无技术细节 |
| 13 | 2018 | 公告 | https://www.prnewswire.com/news-releases/banma-rolls-out-its-first-year-of-operation-of-internet-connected-vehicle-300748804.html | 首年运营公告 |
| 14 | 2023+ | 学术论文 | https://zilimeng.com/papers/phd_thesis.pdf | 清华 Hairpin 联合丢包恢复，**与斑马无直接关联**，仅作学术对照说明本领域常见技术形态 |
| 15 | — | 媒体报道 | https://36kr.com/p/1724429320193 | AliOS / 斑马重组报道 |

## Phase 2 深抓
**未触发** —— Phase 1 四次 query 0 命中任何 F# 正向信号，且未发现可深抓的具体技术白皮书 / 学术论文 / 开源代码 / API 段落；按 SKILL 协议早剪枝，不进入 Phase 2 WebFetch（无明确深抓目标）。

## 工具受限说明
- 全程在 WebSearch 范围内完成；未做 WebFetch（无足够价值的单页可深抓）。
- 未做 curl 兜底（无 WebFetch 失败可兜底）。
- 未访问斑马 / 阿里非公开渠道（SDK 源码 / 内部专利同族 / 抓包测试）—— 这正是升级路径所需材料。
