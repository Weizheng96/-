# 证据索引 — 03-tech-corigine-agilio-ovs

## Phase 1 — 粗筛 query（react，串行）
1. `Corigine Agilio OVS offload flow table SmartNIC architecture`
   → 命中相关：确认 Agilio CX + Agilio OVS Software 做透明 OVS-TC 数据面卸载（单 SmartNIC 形态）；OVS 软件仍在主机运行，match/action 同步下到 SmartNIC。命中 F4/F5 单卡卸载信号。
2. `Corigine Agilio OVS offload bond LACP multiple SmartNICs link aggregation`
   → 命中相关：基础固件支持 IEEE 802.3ad / 802.1AX 链路聚合（网卡级），但无"跨多块独立 SmartNIC 聚合 + 流表向全部网卡下发"的描述。
3. `Netronome Agilio OVS-TC LAG bond hardware offload across two cards single PF limitation`
   → 命中关键：LAG 卸载模型 = 把可卸载端口 bond 成上层 LAG netdev（Linux Bond/Team），经 TC Shared Blocks 共享 block 机制把 filter/stats 关联到各 lower device。未见跨两块 NFP 卡的 LAG 描述。
4. `Corigine NFP VF-LAG bond two SmartNICs OVS offload redundancy 2024`
   → 无 Corigine 自有跨卡 VF-LAG/双卡冗余证据；结果中的 VF-LAG 均属 Mellanox/NVIDIA ASAP2；NFP flower firmware 描述单卡 SR-IOV/representor 卸载。

## Phase 2 — 深抓 WebFetch（react，串行）
- `https://help.netronome.com/support/solutions/articles/36000081172-agilio-open-vswitch-tc-user-guide`
  → verbatim: "The current Netronome cards supporting TC offload only have a single PF."（单 PF 卡，架构事实）。Appendix L 讲 LAG 配置（Native OVS LAG / Linux Bond / Teaming），聚焦配置方法，未述跨卡。
- `https://www.corigine.com/blog-detail-265.html`（OVS Offload Models，2018-05-23）
  → 比较 8 种 OVS datapath 放置模型（kernel/userspace/SmartNIC），关注 datapath 位置而非跨多卡分发；无 bond/LAG/多卡/冗余/单点故障内容。
- `https://www.slideshare.net/Netronome/offloading-linux-lag-devices-via-open-vswitch-and-tc`（OVS 2018 Fall Conf, 内核 4.16-4.19）
  → verbatim: "Distribute filters to all lower devices" + "Combine stats from all lower device offload to LAG upper device/flower rule"。即 filter 下发到 LAG 的**所有 lower 成员端口**（F5 端口级等同信号）。但示例端口为 nfp_p0/nfp_p1，**同一块 NFP 卡**；未述跨两块物理独立 SmartNIC。提及 "Active/backup failover" 但无跨独立 NIC 冗余/消除单点故障细节。

## 工具受限说明
- 无付费墙/登录墙阻碍；Corigine 官网与 Netronome 支持站可读。
- 未检索到 Corigine 在 2023-06-06 之后申请的同主题（跨卡流表卸载）专利。

## 关键判定要点
- Agilio = 单 SmartNIC（单 PF）透明 OVS-TC 卸载；LAG 卸载为**单卡内多端口** bond，filter 下发到所有 lower 端口（端口级，非"跨 N 块网卡"）。
- 专利核心区分限定（F1 N≥2 块独立网卡 / F3 跨网卡 LACP / F5 流表下发至全部 N 块网卡，目的=消除单网卡单点故障）在 Corigine 公开资料中**未见正向命中**；单 PF 卡为正向"不同架构"事实信号，但非对多卡聚合的明示拒绝。
