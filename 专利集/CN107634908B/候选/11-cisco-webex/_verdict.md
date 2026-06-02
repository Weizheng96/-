# 11-cisco-webex verdict

## 候选基本信息
- 名称：Cisco Webex Meetings
- 组织：Cisco（NASDAQ:CSCO）
- 类型：产品
- 初判命中 F#：F2, F4, F5
- 专利公开（授权）日：2021-06-08

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（业务类型由数据流特征自动识别） | 资料不足 | 未找到 | — | 公开资料显示 Webex 按"媒体类型(video)"选择 RTX/FEC，但业务类型来自上层媒体声明，未见"由缓存包长度/数目、到达间隔、数据突发性等数据流特征变量自动推断业务类型"的披露。F1 要求自动识别，非应用声明 → 资料不足。 |
| F2（冗余包数量依"网络状态+传输成功率+业务类型"三输入自适应） | 资料不足 | "depending on the specific network conditions encountered, video RTX or FEC will be used to improve media quality"（Webex 带宽规划白皮书检索摘要）；"Leading SD-WAN platforms adjust this ratio dynamically based on measured packet loss"（GTT，SD-WAN 非 Webex） | https://www.cisco.com/c/en/us/products/collateral/conferencing/webex-meetings/white_paper_c11-691351.html ; https://www.gtt.net/us-en/resources/blog/sd-wan-and-forward-error-correction-mitigating-packet-loss/ | 仅证明"随网络状态自适应"单/双因子；未见"网络状态 + 传输成功率 + 业务类型"三者同时驱动冗余包数量的披露。Cisco 白皮书 PDF/HTML 全被 403/TLS 拦截，无法取原文逐字。资料不足，不外推。 |
| F3（由时延要求得冗余传输总时间） | 资料不足 | 未找到 | — | WebRTC 通用资料仅言"RTX works best on connections with relatively low round-trip times. For higher latency connections, FEC may be more effective"（按 RTT 选机制），非"由时延要求计算冗余传输总时间"。无 Webex 专属披露。 |
| F4（依网络状态+传输总时间+冗余数量生成冗余调度方法） | 资料不足 | 未找到 | — | 仅见"RTX/FEC 二选一随网络条件"，未见三输入生成"冗余包调度方法"的披露。 |
| F5（按调度方法发送冗余包） | 资料不足 | 未找到（仅泛证 Webex 确实发送 FEC/RTX 冗余） | https://www.cisco.com/c/en/us/products/collateral/conferencing/webex-meetings/white_paper_c11-691351.html | Webex 确发送 FEC/RTX 冗余包，但 F5 依附 F4 的"调度方法"，F4 未坐实 → F5 不可独立认定为字面/等同命中。 |

## 已检查文档清单
- Cisco Webex Meetings 带宽规划白皮书（检索摘要可见，原文 403/TLS 被拦无法取逐字）— https://www.cisco.com/c/en/us/products/collateral/conferencing/webex-meetings/white_paper_c11-691351.html
- Cisco Preferred Architecture for Bandwidth Management for Webex（PDF 403）— https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Collaboration/AltDesigns/BWM-Wbx.pdf
- GTT：SD-WAN and FEC: Mitigating Packet Loss（仅证 SD-WAN 按丢包率调冗余比例，非 Webex，无业务类型/时延输入）— https://www.gtt.net/us-en/resources/blog/sd-wan-and-forward-error-correction-mitigating-packet-loss/
- getstream.io：WebRTC Media Resilience（通用：RTX/FEC 随 RTT 与网络条件自适应，无三输入公式）— https://getstream.io/resources/projects/webrtc/advanced/media-resilience/
- US10225045B2（adaptive FEC）— 实为 Hewlett Packard Enterprise，非 Cisco，且机制为"按重传请求时序调 FEC 等级"，不命中三输入公式 — https://patents.google.com/patent/US10225045B2/en
- Google Patents assignee:Cisco 同主题检索 — 命中 US9577682/US8015474 等均为单因子(错误率/反馈)自适应 FEC，无"网络状态+成功率+业务类型"三输入 + 时延→总时间→调度三级链

## 最终判定
**第 4 档：资料不足（弱）**

判定依据（1-3句）：公开资料仅证明 Webex 确实使用 FEC/RTX 冗余、且会"随网络条件"在 RTX 与 FEC 间自适应选择（方向契合本专利的"实时音视频自适应抗丢包"），但这仅是方向契合，非权 1 必要特征的命中。F1（业务类型由数据流特征自动识别）、F2 的三输入冗余量公式、F3/F4 的"时延要求→冗余传输总时间→调度方法"三级链，均无任何公开来源逐字坐实；Cisco 官方白皮书/架构 PDF 全程被 403/TLS 拦截，无法取原文。命中(字面/等同)的 F# 占比为 0/5，远低于 60%，且无任何反向证据，故落资料不足（弱）。

## 升级路径（仅3-4档）
- 突破 Cisco.com 反爬：经授权渠道或浏览器手动保存 white_paper_c11-691351.html 与 BWM-Wbx.pdf 全文，核验是否逐字披露"按业务/媒体类型 + 网络状态 + 传输成功率"共同决定冗余量。
- 检索 Webex/Cisco 媒体栈工程博客、RTCWeb/IETF 提案、Webex 媒体引擎逆向分析或学术测量论文（2021-06-08 后），定位是否有"业务类型自动识别"与"冗余调度方法"的实现描述。
- Google Patents 精确检索 assignee:Cisco 且权利要求同时含"redundant packet number ← network state + success rate + traffic type"与"schedule by delay-derived total time"（2021-06-08 后授权件），若命中可一步升档。

## 总结一句话
Cisco Webex 确用 FEC/RTX 并随网络条件自适应，方向契合但权 1 五特征均无公开来源逐字坐实（命中占比 0/5）、官方文档被反爬拦截，无反向证据，落第 4 档（资料不足-弱）。
