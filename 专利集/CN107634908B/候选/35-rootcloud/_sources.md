# 35-rootcloud 检索 query 与 URL 留痕

## Phase 1 — WebSearch（4 次）

### q1: `树根互联 根云 工业互联网 通信协议 抗丢包`
返回相关 URL：
- https://www.rootcloud.com/sem/  根云平台官网
- https://www.rootcloud.com/product/gypt.html  根云平台 — 工业互联网操作系统
- https://aws.amazon.com/cn/partners/success/rootcloud/  AWS APN 合作伙伴案例
- http://www.aii-alliance.org/resource/c330/m79.html  树根互联（工业互联网产业联盟）
- https://baike.baidu.com/item/根云平台4.0/53304265  百度百科

要点摘录：根云"支持 140+ 种工业协议，覆盖多种控制器的采集"；"为开发者提供 API 文档及在线调试工具、设备消息通信协议、CBOR 转换工具、MQTT 在线测试工具"——属于 IIoT 接入平台范式，未提抗丢包 / 冗余传输。

### q2: `RootCloud 三一重工 工业设备 通信 FEC 冗余`
返回相关 URL：
- https://www.rootcloud.com/knowledge/case18.html  树根互联联合三一重工打造工业互联网服务平台
- https://www.dostor.com/p/76178.html  根云平台服务三一重工"工程机械智能灯塔工厂"
- https://telecom.chinabyte.com/178/725795178.shtml  三一重工数字化转型工业物联网案例

要点摘录：2007 起三一重工在设备上装"工业智能通信终端" → 2016/12 三一 IoT 团队基于大数据平台创建 RootCloud；已接入约 91 万台工业设备；定位是设备数据采集、故障预测、智能调度——与 FEC / 冗余包毫无关联。

### q3: `树根互联 根云 MQTT CoAP 通信 时延 业务类型 自适应`
返回相关 URL（皆为通用 MQTT/CoAP 科普，无根云专属内容）：
- https://blog.csdn.net/2501_90675742/article/details/146592479  MQTT vs CoAP 解析
- https://cloud.tencent.com/developer/article/2530544  腾讯云 — IoT 协议选择
- https://www.cnblogs.com/emqx/p/16008091.html  EMQX — 主流 IoT 协议

要点：未检索到任何"根云 + 业务类型自适应 + 时延驱动 + 冗余包"语义命中。

### q4: `"树根互联" OR "RootCloud" 前向纠错 OR FEC OR "冗余包" OR "丢包重传" 工业互联网`
返回相关 URL：
- https://www.rootcloud.com/sem/
- https://www.rootcloud.com/product/gypt.html
- https://www.irootech.com/about/  树根科技 — 公司介绍
- https://www.irootech.com/knowledge/case.html  标杆案例
- 其余命中均为 FEC / KCP 等通用科普文（freshwlnd.github.io、jianshu.com、vearne.cc），与树根互联无关

要点：未检索到任何把"树根互联 / 根云 / RootCloud"与"FEC / 前向纠错 / 冗余包 / 丢包重传"放在同一份公开技术材料中的命中。

## Phase 2 — WebFetch（1 次，已早结）

### f1: https://www.irootech.com/product/gypt.html  （从 rootcloud.com/product/gypt.html 301 跳转至 irootech.com 同路径）
提取结论 verbatim：
- "支持超 1100 种工业协议"——未具体列出
- 强调"毫秒级的实时数据采集"能力
- 未提 FEC / 冗余包 / packet-level redundancy
- 未提"根据业务类型动态调整冗余包数量"
- 未区分 reactive 重传（ARQ / TCP 超时重传）与 proactive 冗余传输
- 整页定位为"产品营销材料"，缺少底层通信传输层技术细节

### 未必要的后续 WebFetch
q4 + f1 已三角化清晰反向证据：公开技术语料中找不到把"根云"与"FEC / 主动冗余"放在同一份材料的来源；继续深挖不会改变结论。

## 工具使用统计
- WebSearch：4/4 上限
- WebFetch：1/6 上限（早结）
- 落盘文件：仅本 _sources.md + _verdict.md（未下载任何 PDF / HTML — 公开材料中无可证明 FEC 行为的技术细节文档存在）
