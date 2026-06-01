# 15-cmcc-onenet 检索留痕

## 权属核查（重点）
- CN107634908B 当前权利人 = Huawei Technologies Co Ltd（CN107634908B.md 第 14 行）
- 发明人 = 王凡钊 / 陈如杰 / 郑凯（均为华为系研究人员）
- 上下文提示中"中国移动可能在专利权人范围内"已核实**不成立**：
  - CN107634908B.md 第 13 行"原始申请人"列出 24+ 个不相关机构（包括 Citrix、Thomson、松下、平安银行等），且"中国移动通信集团公司"出现 2 次——这是 fetch_patent.py 抓取 Google Patents 时把同族 / 被引专利的申请人列表混入了该字段的已知工程问题，**并非 CN107634908B 本身的真实申请人**。
  - 真实申请人 / 权利人是 Huawei，与中国移动无权属关联，OneNET 不享有"专利权人内部使用"抗辩，需正常按侵权候选评估。
  - 尝试 WebFetch + curl + PowerShell 直接拉 Google Patents CN107634908B 页面均 503，无法在线二次确认；以 CN107634908B.md 已记载的"当前权利人 = Huawei"为准。

## Phase 1 粗筛 WebSearch（4 次 + 补充 2 次，react 串行）

### q1
- query: `CN107634908B 华为 王凡钊 申请人 数据传输方法 专利权人`
- 命中：未直接命中 CN107634908B 申请人字段（百度百科 / patenthub 通用页）
- 用途：交叉验证专利权属——结合 CN107634908B.md 已记录 "当前权利人 Huawei" 足够定性。

### q2
- query: `"CN107634908" applicant Huawei "中国移动" 申请人`
- 命中：未直接命中（返回均为不相关 US 专利 + 医学论文）
- 用途：跨语种验证——也未发现中国移动作为本专利申请人的任何记录。

### q3
- query: `OneNET 中国移动 物联网平台 数据传输 协议 MQTT CoAP 弱网 重传`
- 命中关键 URL：
  - https://open.iot.10086.cn/ —— OneNET 官方首页
  - http://img.tijos.net/docstore/tijos-development-guide/tijos.framework.networkcenter.onenet/
  - https://blog.csdn.net/klandor2008/article/details/133820355
  - https://www.cnblogs.com/ibrahim/p/iot-china-mobile-onenet.html
- 关键结论：OneNET 支持 MQTT / CoAP / HTTP / LwM2M(NB-IoT) / EDP / Modbus / JT/T808 / TCP 透传 / RGMP，**全是标准 IoT 协议**，弱网环境靠"相对可靠传输"（即 ACK + 重传），未提及 FEC / packet-level 冗余。

### q4
- query: `OneNET IoT platform FEC forward error correction redundancy packet adaptive`
- 命中关键 URL：均为 Fortinet / F5 / 通用 USPTO 专利文档，**与 OneNET 无关**
- 关键结论：跨语言强制搜索 OneNET + FEC/forward error correction 0 命中——说明 OneNET 公开技术体系中**完全不存在** FEC / 主动冗余包概念。

### 补充 q5
- query: `OneNET EDP 协议 自适应 冗余 编码 业务类型 调度`
- 命中关键 URL：
  - https://open.iot.10086.cn/doc/book/device-develop/multpro/EDP/introduce.html —— EDP 官方协议文档
  - https://blog.csdn.net/weixin_40973138/article/details/89762768
- 关键结论：EDP（Enhanced Device Protocol）是 OneNET 自研的 TCP-based 长连接协议，定位"设备-平台长期点对点控制连接"，无 FEC / 业务类型自适应冗余调度提及。

### 补充 q6
- query: `中国移动 OneNET 平台 论文 网络编码 主动冗余 packet-level FEC 业务类型自适应`
- 命中关键 URL：均为 OneNET 入门 / 应用介绍博客，无学术论文
- 关键结论：未检索到公开学术论文证明 OneNET 实现了权 1 的"业务类型自适应主动冗余调度"。

## Phase 2 深抓 WebFetch（2 次，react 串行）

### f1 — OneNET EDP 协议官方文档
- URL: https://open.iot.10086.cn/doc/book/device-develop/multpro/EDP/introduce.html
- 本地存档: `onenet_edp_introduce.html` (276 KB)
- 关键引文 1：> "长连接协议"
- 关键引文 2：> "该协议只传输数据包到达目的地，不保证传输的顺序与到达的顺序相同，事务机制需要在上层实现"
- 反向证据强度：**强**——EDP 仅依赖 TCP 内置重传，无任何 FEC / 主动冗余 / 业务类型自适应调度。

### f2 — OneNET 平台官方首页
- URL: https://open.iot.10086.cn/
- 本地存档: `onenet_home.html` (411 KB)
- 关键引文：> "MQTT、CoAP、HTTP、LwM2M等行业标准协议及私有协议"
- 反向证据强度：**强**——0 命中 FEC / 前向纠错 / 主动冗余包 / 业务类型自适应冗余调度。

## 工具受限说明
- Google Patents `patents.google.com` 在本次会话中所有 WebFetch / curl / PowerShell 拉取均 503，无法实时二次验证 CN107634908B 申请人字段；以 CN107634908B.md 已记载的"当前权利人 = Huawei"为准。
- 未搜索 OneNET 闭源内部论文 / 内部专利申请，可能存在内部研发但未公开的 FEC 模块；当前依据所有公开技术文档，已可排除权 1 的 packet-level FEC 命中。
