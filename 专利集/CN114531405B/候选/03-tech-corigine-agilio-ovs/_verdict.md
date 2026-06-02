# 03-tech-corigine-agilio-ovs verdict

## 候选基本信息
- 名称：Agilio CX SmartNIC + Agilio OVS Software（完整 OVS 数据面卸载）
- 组织：芯启源 Corigine
- 类型：技术
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（vSwitch + M VM + N≥2 网卡） | 公开资料不足（偏反向） | "The current Netronome cards supporting TC offload only have a single PF."；产品定位为"transparent offload of OVS datapath to Agilio SmartNIC"（单 SmartNIC） | https://help.netronome.com/support/solutions/articles/36000081172-agilio-open-vswitch-tc-user-guide ; https://www.corigine.com/UploadFiles/pdf/2021-07-21/124206809322973.pdf | Agilio 公开资料只描述单 SmartNIC（单 PF）形态；未见"虚拟交换机同时连 N≥2 块独立网卡并按本专利聚合"的正向证据。单 PF 是正向不同架构事实，但非对多卡的明示拒绝→不足够升第5档 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 等同信号（受限）/ 公开资料不足 | "Distribute filters to all lower devices"；LAG 上层 netdev 通过 TC Shared Blocks 把多个 lower device 关联到一个 block | https://www.slideshare.net/Netronome/offloading-linux-lag-devices-via-open-vswitch-and-tc | LAG 把多个成员端口聚合为一个上层 LAG netdev（概念上"多端口→一聚合口"），但成员为**单卡内端口**（nfp_p0/nfp_p1），非"N 块独立网卡的 N 个逻辑端口"，与 F2 的跨卡映射语义不同层级 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合，再聚合 N 个） | 公开资料不足（偏反向） | 基础固件支持 "IEEE 802.3ad" / "802.1AX Link Aggregation"；LAG 示例端口 nfp_p0、nfp_p1 在同一块 NFP 卡 | https://www.slideshare.net/Netronome/offloading-linux-lag-devices-via-open-vswitch-and-tc ; https://help.netronome.com/support/solutions/articles/36000081172-agilio-open-vswitch-tc-user-guide | 支持卡级 LACP/802.3ad，但聚合发生在单卡多端口；未见"跨多块物理网卡的物理端口经 LACP 形成逻辑端口、再把 N 个逻辑端口二次聚合"的两级跨卡结构 |
| F4（目标网卡流表 miss 触发） | 等同命中 | "OVS software still runs on the server, the OVS-TC datapath match/action modules are synchronized down to the Agilio SmartNIC"；透明卸载模型为 first-packet 走慢路径→同步下发 | https://www.corigine.com/TechnologiesandApplications-201.html ; https://www.corigine.com/blog-detail-265.html | OVS-TC 卸载本质即 miss→upcall/慢路径→把 exact flow 同步下到网卡，与 F4 的"查不到卸载流表时触发"语义一致 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 等同信号（受限）/ 公开资料不足 | "Distribute filters to all lower devices" + "Combine stats from all lower device offload to LAG upper device/flower rule" | https://www.slideshare.net/Netronome/offloading-linux-lag-devices-via-open-vswitch-and-tc | LAG 卸载会把 filter 下发到**所有 lower 成员**——端口级"向全部成员下发"与 F5 形式相近；但成员=单卡内端口，非"N 块独立网卡"，缺"跨卡向全部 N 块网卡下发"的正向证据 |

## 已检查文档清单
- Agilio OVS-TC User Guide（Netronome 支持站）：明确"单 PF 卡"，含 LAG 配置附录 — https://help.netronome.com/support/solutions/articles/36000081172-agilio-open-vswitch-tc-user-guide
- "Offloading Linux LAG Devices Via OVS and TC"（OVS 2018 Fall Conf）：LAG filter 下发到所有 lower 成员端口，示例为单卡 nfp_p0/p1 — https://www.slideshare.net/Netronome/offloading-linux-lag-devices-via-open-vswitch-and-tc
- Corigine "OVS Offload Models"（2018-05-23）：比较 8 种 datapath 放置模型，无跨多卡/冗余内容 — https://www.corigine.com/blog-detail-265.html
- Agilio OVS Software / SmartNIC 产品页与 Product Brief：透明卸载 OVS 数据面到单 SmartNIC — https://www.corigine.com/TechnologiesandApplications-201.html ; https://www.corigine.com/UploadFiles/pdf/2021-07-21/124206809322973.pdf

## 最终判定

**第 4 档：公开资料不足（弱候选）**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除。

判定依据（基于上表 F# 分布）：仅 F4 达等同命中、F2/F5 为"端口级等同信号"但停留在单卡内、F1/F3 公开资料不足且偏反向；专利的核心区分限定（F1 N≥2 块**独立网卡** + F3 **跨网卡** LACP 两级聚合 + F5 流表下发至**全部 N 块网卡**，目的=消除单网卡单点故障）在 Corigine 公开资料中均未见正向命中，命中度 < 60%。"单 PF 卡 / 单 SmartNIC 透明卸载"是正向不同架构事实，但 Corigine 未**明示拒绝**多卡聚合，不满足第5档"针对该候选产品的正向反向事实"硬门槛，故落第4档而非第5档。

## 升级路径（仅落第3-4档时填）
- 取证方向：(a) 查 Corigine/芯启源 2023-06-06 后是否发布"双 Agilio 卡 bond + OVS 流表跨卡卸载 / 网卡级冗余消单点"的方案文档或专利；(b) 在中国移动网络云 / 浙江移动 SD-WAN 实际部署文档中确认单服务器是否插 ≥2 块 Agilio 卡并做跨卡 LACP + 流表向两卡同时下发；(c) 抓 NFP 内核驱动 / agilio-ovs-hooks 源码，确认 LAG offload 是否允许 lower device 跨两个 PCIe 设备（跨卡）。任一确认到"跨卡聚合 + 流表向全部网卡下发"即可升至第2/3档。

## 总结一句话
芯启源 Agilio 为单 SmartNIC（单 PF）透明 OVS-TC 卸载，仅命中 miss 触发（F4）与单卡内 LAG"向全部成员下发"（F2/F5 受限信号），缺专利核心的跨多块独立网卡 LACP 两级聚合与跨卡流表下发正向证据，命中 <60% 且无明示反向，落第 4 档（公开资料不足-弱候选）。
