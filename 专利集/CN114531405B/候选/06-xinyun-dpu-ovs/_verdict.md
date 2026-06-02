# 06-xinyun-dpu-ovs verdict

## 候选基本信息
- 名称：全系列 DPU 网卡（OVS 硬件流表全卸载/VTEP）
- 组织：星云智联 Xinyun
- 类型：产品
- 初判命中 F#：F1,F2,F3,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（vSwitch + M VM ≥2 + N 网卡 ≥2） | 公开资料不足 | 第三方科普："网络功能卸载是对云计算主机上的虚拟交换机的能力做硬件卸载" + vendor "面向裸金属、虚拟机、容器" | https://blog.csdn.net/yusur/article/details/124682791 ; 36氪 https://pitchhub.36kr.com/project/1958566523704326 | 确认 vSwitch + 多 VM 形态；但 **N≥2 块独立网卡** 这一整数下界无 vendor 一手证据，单卡 DPU 形态即可成立 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 公开资料不足 | 未找到（vendor 官网 SPA 空壳不可抓；4 条 query 0 命中"跨网卡聚合"） | — | 跨卡逻辑端口→单目标端口映射，公开资料完全未触及 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合形成，跨多块独立网卡） | 公开资料不足 | 未找到（query 2 仅得通用 LACP 科普，无星云跨卡聚合信号） | — | 核心区分点；无法区分星云为"单卡多端口 bond/VF-LAG"还是"跨多块独立网卡 LACP"，按整数限定外推禁令不得记字面命中 |
| F4（目标网卡流表 miss 触发） | 等同命中（受限） | "通过流表的 offload 将流表卸载到固件中，通过固件的 eswitch 进行流表匹配" + OVS 全卸载含 first-packet upcall/慢路径语义 | https://blog.csdn.net/weixin_37515230/article/details/126663561 | OVS 硬件全卸载固有 miss→upcall 机制，机制同；但为科普非 vendor 一手 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 公开资料不足 | vendor："数据面硬件实现流表操作" — 仅证单点流表卸载，**无"向全部 N 网卡冗余下发"** | 36氪 https://pitchhub.36kr.com/project/1958566523704326 | 普通单卡 OVS 卸载只下发到收包网卡；F5 的"向全部网卡冗余下发以防单点"无任何公开证据 |

## 已检查文档清单
- 星云智联官网 DPU/SmartNIC/新闻页 — JS 渲染 SPA，WebFetch/curl 仅得标题头（<1KB），技术正文不可静态抓取 — https://www.nebula-matrix.com/dpu
- 36氪 星云智联项目页（NebulaX D1055AS：数据面硬件流表操作、队列/带宽隔离） — https://pitchhub.36kr.com/project/1958566523704326
- CSDN "DPU智能网卡OVS全卸载方案"（通用单卡 OVS 全卸载机制，netdev_offload_dpdk/tc） — https://blog.csdn.net/weixin_37515230/article/details/126663561
- CSDN "DPU应用场景：网络功能卸载"（vSwitch 硬件卸载场景） — https://blog.csdn.net/yusur/article/details/124682791
- Google Patents 检索（site:patents.google.com）：未命中星云智联自有"跨卡流表卸载"专利

## 最终判定

**第 4 档：公开资料不足（弱候选）**

判定依据（1-3 句，基于上表 F# 分布）：仅 F4（OVS 全卸载固有的 miss→upcall 机制）可记等同命中（受限），F1 形态部分相符；而专利三大核心区分点——F2 跨卡逻辑端口聚合为单端口、F3 跨多块**独立网卡**的 LACP 聚合、F5 流表**向全部 N 网卡冗余下发以消单点故障**——均无任何公开证据，star云官网为 JS-SPA 致一手拓扑文档不可抓。命中率 < 60%（仅 1/5 等同命中），但**未发现任何反向证据**（vendor 未明示拒绝跨卡聚合，亦未自述"仅支持单卡"），不满足第5档硬门槛（0 命中/资料缺失 ≠ 已排除），故落第4档而非第5档。

## 升级路径（仅落第3-4档时填）
- 获取星云 DPU 一手文档：用带 JS 渲染的抓取（headless 浏览器）抓 nebula-matrix.com 产品页，或拿到 NebulaX D1055AS / S1000 datasheet PDF，定位是否描述"跨多块网卡 LACP 聚合 + 流表向全部网卡下发"。
- 检索星云智联（珠海星云智联科技）2023-06-06 后自有专利（CNIPA / Google Patents 申请人检索），看是否有"多网卡流表冗余 / 跨卡可靠性"同主题专利做机制比对。
- 查 vendor 是否支持双 DPU/双网卡主备或 LACP across-NIC 高可用方案的白皮书 / 招标应答。

## 总结一句话
星云智联 DPU 确做 OVS 硬件流表全卸载（F4 等同、F1 形态部分符），但专利核心的跨独立网卡 LACP 聚合 + 流表向全部网卡冗余下发（F2/F3/F5）无任何公开证据、官网 SPA 致一手文档不可抓，且无反向证据，故落第 4 档（公开资料不足-弱候选）。
