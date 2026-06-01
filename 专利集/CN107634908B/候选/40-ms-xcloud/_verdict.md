# 40-ms-xcloud verdict

## 候选基本信息（专利公开日 2021-06-08）
- 候选编号 / slug：40 / `40-ms-xcloud`
- 类型：产品
- 名称：Microsoft xCloud / Xbox Cloud Gaming
- 组织：Microsoft
- 初判命中 F#：F2, F3, F4, F5
- 公开度：低
- 一句话定位：MS 云游戏服务，UDP 实时视频流 + 第三方科普文称使用 FEC，但内部协议栈完全闭源
- 时间窗判定：xCloud Beta 2019-11，Game Pass Ultimate 正式上线 2020-09-15，**至今仍持续运营**；运营时间跨越专利公开日 2021-06-08，时间窗**满足**

## 检索粗筛

参见 `_sources.md`：Phase 1 共 4 次 WebSearch（react 串行），最大信号来自 q4（clouddosage / techgaminginsight Medium）；Phase 2 共 4 次 WebFetch + 2 次 curl 兜底，3 个关键源被 CF/Anubis 拦截，1 个拿到正文但只含泛"自适应流"描述、无 F1-F5 结构性细节。0 命中 ≠ 已排除。

## F# 命中表（F1-F5）

| F# | 限定要点 | 公开证据 | 命中？ |
|---|---|---|---|
| F1 业务类型识别（基于发送端流统计的 4 项之一：缓存包长/数、在途包长/数、到达间隔、突发性） | 必须由发送端自动从真实流量统计得出，不是上层应用静态配置 | 无任何公开材料披露 xCloud 是否做"业务类型"识别；亦无证据表明区分"控制 vs 视频 vs 音频"流时使用 4 项统计变量 | **无证据** |
| F2 冗余包数量 = f(网络状态, 传输成功率, 业务类型) 三元组 | 三元组必须均参与 | clouddosage 引述 "Microsoft uses forward error correction in Xbox Cloud Gaming, which reduces visual artifacts and prevents frame skips without having to resend data"（FEC 存在）；但**该原文 CF 拦截无法核实**，且**完全无关于"业务类型"或"成功率"参与计算**的描述 | **仅泛 FEC，结构性三元组未证实** |
| F3 冗余包传输总时间 = f(时延要求) | 累计窗口长度而非单包 timeout | 无公开材料 | **无证据** |
| F4 调度方法 = f(网络状态, 总时间, 冗余包数量) | 至少 4 种可选（随机/最短/最长/均匀） | techgaminginsight Medium 仅称 "Adaptive streaming technologies adjust the quality of the game stream in real time based on current network conditions"——这是"自适应码率"而非"冗余包调度方法选择"，**不等价 F4** | **无证据** |
| F5 按调度方法发送冗余包 | 主动 FEC 非被动 ARQ | 间接证据（第三方科普文称 xCloud 用 FEC，"without having to resend data" 暗示主动而非重传），但来源被 CF 拦截、无法 verbatim 核实 | **弱间接证据，未独立核实** |

## 已检查文档清单

| 来源 | 类型 | 是否拿到正文 | 与本候选关键性 |
|---|---|---|---|
| clouddosage.com/how-xbox-is-quietly-fixing-xbox-cloud-gaming-latency/ | 第三方科普 | **未拿到**（WebFetch 403 / curl 仅得 CF 挑战页） | 高（疑似含 FEC 直引）但无法验证 |
| techgaminginsight.medium.com/...c63b67a42694（2024-04-12） | 第三方 Medium | 拿到正文 | 低（只有泛"自适应流"描述，无 FEC/三元组细节） |
| cloudloadout.com/xbox-cloud-gaming-not-working/ | 用户排错教程 | 未拿到（403） | 低（用户侧端口列表不涉及内部协议） |
| inria.hal.science/hal-03421031/document | 学术测量论文 | **未拿到**（Anubis 拦截） | 高（学术测量可能披露 xCloud 协议结构）但无法访问 |
| NSDI'25 Tooth FEC 论文 | 学术 | 未深抓 | 与 xCloud 无关 |
| Microsoft Research / Xbox Engineering Blog | 一手 | 未检索到任何相关篇目 | 关键缺失 |
| GitHub / OSS | 一手代码 | 不存在（闭源） | 关键缺失 |

## 最终判定 **第 4 档：信号不足（未排除）**

判定要点：
1. **0 命中 ≠ 已排除**：xCloud 是确证使用 FEC 的实时视频流服务（第三方多次提及），技术取向与本专利 F2/F5 在抽象层一致；并非"领域无关"或"反向证据"案例，不能落第 5 档"已排除"。
2. **未满足第 1-3 档的证据门槛**：本专利权 1 的核心限定（F1 数据流特征变量识别业务类型 + F2/F4 含"业务类型"输入的三元组）需要内部协议栈或论文级证据；xCloud 协议栈闭源、关键三方源（clouddosage / Inria）均被 CF/Anubis 反爬拦截，curl 兜底亦未穿透。**无法证明任一具体 F# 实际结构性命中**。
3. **公开度低 + 闭源** 决定本候选在不获取内部信息的前提下难以推进；这与"已排除"是不同的状态——前者是工具受限，后者是有反向证据。

## 升级路径（4 档 → 3/2/1 档所需证据）

要把 xCloud 提升到"疑似侵权 / 高度疑似 / 确认侵权"，需要至少其中之一：
- (a) 拿到 clouddosage 或同等技术媒体的 verbatim 原文，并能指证其引用的 Microsoft 一手来源（Xbox engineering blog / GDC talk / patent filing），证明 xCloud 的 FEC 决策**参考了"业务类型"+"网络状态"+"成功率"三元组**——可升至 3 档。
- (b) 拿到 Inria HAL-03421031 或同等学术测量论文正文，若其抓包分析显示 xCloud 对**不同流（视频 / 音频 / 控制）使用不同 FEC 强度，且 FEC 强度随 RTT/丢包率/业务类型同时变化**——可升至 3 档。
- (c) 找到 MS 关于 xCloud 协议栈的专利申请，若 claim 结构与 CN107634908B 权 1 重合度 ≥ 3 个 F——可升至 2 档。
- (d) 找到 MS 工程师 GDC / SIGCOMM / NSDI talk 视频或 slide，明确披露按"streaming type / signaling stream type"区分冗余策略——可升至 2 档。
- 关键 query 建议：`site:microsoft.com xCloud "forward error correction"` / `site:youtube.com GDC xCloud streaming FEC` / `xCloud "stream type" classification`。

## 总结一句话

xCloud 公开材料确证使用 FEC 且为实时流场景，与本专利 F2/F5 抽象方向一致，但内部协议栈闭源、关键三方学术与科普源被反爬拦截，无法核实 F1 业务类型识别与 F2/F4 含业务类型的三元组限定，**落第 4 档：信号不足（未排除）**。

---

**免责声明**：本判定为基于公开信息的技术线索梳理，非法律意见；不构成对 Microsoft xCloud / Xbox Cloud Gaming 已构成专利侵权的结论。最终侵权判断须由专业专利律师结合证据深度、claim construction 与诉讼程序综合裁定。
