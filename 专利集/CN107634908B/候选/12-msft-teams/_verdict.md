# 12-msft-teams verdict

## 候选基本信息
- 名称：Microsoft Teams
- 组织：Microsoft（NASDAQ:MSFT）
- 类型：产品
- 初判命中 F#：F2, F4, F5
- 专利公开（授权）日：2021-06-08

## 检索粗筛（query 留痕）
- Phase 1 react（串行 WebSearch）：
  1. `Microsoft Teams Skype FEC forward error correction packet loss adaptive redundancy` → 命中泛 FEC 资料，非 Teams 专属，但确认"adaptive FEC 按网络丢包调整冗余比例"机制存在。
  2. `Microsoft Teams media FEC redundancy network condition adaptive bandwidth estimation engineering` → 命中 Teams 实时媒体栈在生产环境用自适应 BWE + FEC，"adapt the amount of FEC to best fit the observed network loss rate"（方向契合 F2）。
  3. `assignee:Microsoft patent forward error correction redundancy packet loss adaptive real-time media traffic type` → 返回的近似专利 US20150180785A1 实为 Imagination Technologies 受让，非微软；其余为 2002–2009 老专利（且早于专利公开日）。
  4. `Microsoft Skype Teams patent adaptive FEC redundancy amount traffic type loss rate delay scheduling real-time media` → "Skype adjusts its rates, FEC redundancy and video quality by varying packet loss rate, propagation delay and bandwidth"（方向契合，但无 F1/F3/F4 距离锚点）。
- Phase 2 react（串行 WebFetch）：
  - WebFetch `https://patents.google.com/patent/US20150180785A1/en` → 受让方 Imagination Technologies（非微软），不计入本候选。
  - WebFetch `https://arxiv.org/pdf/2409.19867`（Teams 生产 BWE 论文）→ 仅带宽估计，无 FEC 冗余量/调度链披露。
  - WebFetch `https://wp.nyu.edu/minghao/rl-afec/` → NYU/Fortinet 研究提案（2022-06-14），非 Teams 生产实现。
- 未剪枝理由：Phase 1 有方向信号（Teams 媒体栈确用自适应 FEC，F2 方向契合），不满足早剪枝任一硬条件（非全 0/全无关、非全早于 2021-06-08、架构层级一致——均为发送侧实时媒体抗丢包）。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（业务类型由数据流特征自动识别） | 资料不足 | 未找到 Teams 由"缓存包长/数目、在网包长/数目、到达间隔、突发性"自动推断业务类型的公开披露 | — | Teams 中音/视频为应用显式声明的 RTP 流，非由流特征自动识别；无公开来源支持 F1 自动识别路径 |
| F2（冗余包数量按网络状态+传输成功率+业务类型三输入） | 资料不足（部分方向契合） | "adapt ... the amount of FEC (or FEC interval) to best fit the observed network loss rate"；"Skype adjusts its rates, FEC redundancy and video quality by varying packet loss rate, propagation delay and bandwidth" | https://arxiv.org/pdf/1310.1582 ; https://tonyzhang95.github.io/2020/04/28/USF-AFEC/ | 公开资料显示冗余量随丢包率+时延+带宽自适应，但未见"传输成功率 + 由流特征推断的业务类型"三输入的明确证据；仅方向契合，非字面命中 |
| F3（时延要求→冗余传输总时间） | 资料不足 | 未找到 Teams 由时延要求推导"冗余传输总时间"这一中间量的公开披露 | — | 公开资料有"时延约束限制 FEC span"的近似表述（属第三方/他司专利），但非 Teams 自有披露 |
| F4（按网络状态+传输总时间+冗余数量生成调度方法） | 资料不足 | 未找到 Teams 生成"冗余数据包调度方法"三级链的公开披露 | — | 媒体栈闭源，无工程博客/论文披露调度方法生成逻辑 |
| F5（按调度方法发送冗余包） | 资料不足 | 未找到 Teams 公开披露其冗余包发送调度细节 | — | F5 依附 F4；F4 无证据则 F5 不可单独认定 |

## 已检查文档清单
- Congestion Control using FEC for Conversational Multimedia Communication（FEC 随网络丢包率自适应的一般机制，方向契合 F2） — https://arxiv.org/pdf/1310.1582
- Offline Meta-learning for Real-time Bandwidth Estimation（Teams 生产媒体栈 BWE，仅带宽估计，无 FEC 冗余量/调度链） — https://arxiv.org/pdf/2409.19867
- US20150180785A1 Packet Loss Mitigation（受让方 Imagination Technologies，非微软；不计入本候选） — https://patents.google.com/patent/US20150180785A1/en
- RL-AFEC（NYU/Fortinet 研究提案 2022-06-14，非 Teams 生产实现） — https://wp.nyu.edu/minghao/rl-afec/
- Paper Study: Adaptive FEC Loss Control for VoIP / Skype（"Skype adjusts ... FEC redundancy ... by varying packet loss rate, propagation delay and bandwidth"） — https://tonyzhang95.github.io/2020/04/28/USF-AFEC/

## 最终判定
**第 4 档：资料不足（弱）**

判定依据（1-3句）：公开来源仅证明 Microsoft Teams/Skype 媒体栈使用"按网络丢包率/时延/带宽自适应的 FEC 冗余"（与 F2 方向契合），但 5 个特征中仅 F2 部分方向契合、无任何字面/等同命中，F1（业务类型由数据流特征自动识别）、F3（时延→冗余传输总时间）、F4（三输入调度方法生成）、F5 均无公开证据（Teams 媒体栈闭源、无工程披露）。命中（字面/等同）F# 占比 0/5，远低于 60%，故落资料不足（弱）；不存在真反向证据、时间不合规或架构层级不同，故不入第 5 档。

## 升级路径（仅3-4档）
- 在 Google Patents 用 `assignee:Microsoft`（含 `Skype Technologies` 受让）+ `forward error correction / redundancy / repair packet` 检索 2021-06-08 后微软自有同主题专利/申请，核验是否披露"业务类型自动识别 + 三输入冗余量 + 时延→总时间→调度"链（本轮 curl/WebFetch 受 schannel TLS 限制，未能在 Google Patents 完成 assignee 过滤检索）。
- 抓取 Microsoft Teams / Skype 媒体引擎工程博客、IETF 草案或 MS-* 协议文档，确认 FEC 冗余量计算是否引入"传输成功率"与"由数据流特征推断的业务类型"两输入（针对 F1/F2）。
- 检索是否存在 Teams 媒体栈对"时延要求→冗余传输总时间→调度方法"三级链的披露（针对 F3/F4），如有则可上探第 3 档。

## 总结一句话
Microsoft Teams 媒体栈确用按丢包/时延/带宽自适应的 FEC（方向契合 F2），但 F1/F3/F4/F5 无公开证据、F2 无字面命中，闭源资料不足，落第 4 档。

## 工具受限说明
- Google Patents 在本环境下 WebFetch 出现 "unknown certificate verification error"、curl 出现 "schannel: failed to receive handshake (35)"，无法完成 `assignee:Microsoft` 过滤检索；US20150180785A1 经 WebFetch 读取确认为 Imagination Technologies 受让，已排除。
