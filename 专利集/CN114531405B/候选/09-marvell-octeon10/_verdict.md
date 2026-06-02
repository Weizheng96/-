# 09-marvell-octeon10 verdict

## 候选基本信息
- 名称：OCTEON 10 DPU OVS 卸载
- 组织：Marvell
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 公开资料不足 | "Dual 100GE QSFP28 ports" / "2x100G"（单卡双端口）；OCTEON OVS offload 一致呈现为「单 DPU 卡 per host 全卸载」 | https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/ | F1 要求 host vSwitch 连 N≥2 块**独立**网卡；公开资料仅见单卡多端口形态（整数下界以下形态），按整数限定禁令不得外推为字面命中，但也无 N≥2 独立网卡的正向证据 |
| F2 | 公开资料不足 | 未找到（无跨多块独立网卡逻辑端口聚合为"第一端口"的描述） | https://www.marvell.com/content/dam/marvell/en/public-collateral/embedded-processors/marvell-octeon-10-dpu-platform-product-brief.pdf | 单卡架构下无跨卡逻辑端口聚合语义 |
| F3 | 公开资料不足 | 「LACP should not be used with OVS-based bonds」（通用建议）；OCTEON HA 为交换机层 MC-LAG，非 host vSwitch 跨卡 LACP | （query 2 / query 3 检索结果，见 _sources.md） | F3 要求"每网卡物理端口经 LACP 聚合形成逻辑端口"且跨多块独立网卡；公开资料仅见单卡形态+交换机层 MC-LAG，属不同层级，无正向跨卡 LACP 证据 |
| F4 | 公开资料不足 | "OVS offload"（罗列能力，未披露 miss/upcall 触发精确流表卸载细节） | https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/ | OVS 卸载普遍含 first-packet miss→upcall 语义，但该产品无具体披露，不记字面命中 |
| F5 | 公开资料不足 | 未找到（无"精确流表向全部 N 块网卡冗余下发"的描述） | https://www.marvell.com/content/dam/marvell/en/public-collateral/embedded-processors/marvell-octeon-10-dpu-platform-product-brief.pdf | 单卡架构无"向全部 N 网卡冗余下发流表"语义；HA 由交换机层 MC-LAG 承担，机制层级不同 |

## 已检查文档清单
- Marvell OCTEON 10 DPU Platform Product Brief（2023-10/11，授权日后）— 通用 DPU 定位，无跨卡 LACP / 流表多卡冗余描述 — https://www.marvell.com/content/dam/marvell/en/public-collateral/embedded-processors/marvell-octeon-10-dpu-platform-product-brief.pdf
- Asterfusion OCTEON CN9670 SmartNIC OVS/NFV offload 产品页（页修改日 2025-07）— 「Dual 100GE / 2x100G」单卡双端口、OVS offload — https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/
- WebSearch query 1-3 留痕（OVS offload 能力确认 / Helium 单卡 / OCTEON HA=交换机层 MC-LAG）— 见 _sources.md

## 最终判定

**第 4 档：公开资料不足（弱候选）**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。

判定依据（1-3 句，基于上表 F# 分布）：5 条 F# 全部为"公开资料不足"，0 条字面命中、0 条等同命中、亦无任何 F# 的真反向证据——OCTEON/Asterfusion 公开资料一致只描述「单卡 OVS 全卸载 + 交换机层 MC-LAG HA」，对本专利的核心区分点（host vSwitch 跨 N≥2 块独立网卡 LACP 聚合 + 精确流表向全部 N 网卡冗余下发）既无正向证实也无明示拒绝。按整数限定禁令，vendor 仅披露下界以下（单卡多端口）形态不得外推为字面命中；按第5档硬门槛，缺乏针对该产品的正向反向事实（无"另一套手段实现同目标"的自有专利/文档明示），且仍属同一 OVS 流表卸载抽象层，故不落第5档，命中率 <60% 且无反向 → 第4档。

## 升级路径（仅落第3-4档时填）
- 取 Asterfusion/Marvell 的 OVS 卸载部署 datasheet 或参考架构，确认是否存在"单 host 装 2 块以上独立 OCTEON 网卡 + vSwitch 跨卡 LACP + 流表向全部卡下发"的实际拓扑（若仅单卡 per host，可下调为更弱候选）。
- 检索 Marvell 在 2023-06-06 后申请的同主题专利（DPU 多卡流表冗余 / OVS offload HA），做机制比对——若其明示采用单卡内冗余或交换机层 MC-LAG 实现 HA，则构成正向"不同机制"反向证据，可下调至第5档。
- 查 OCTEON OVS offload 是否支持 miss→exact-flow upcall 卸载（F4）的具体实现文档，补强或排除 F4。

## 总结一句话
Marvell OCTEON 10 DPU OVS 卸载落第 4 档（公开资料不足-弱候选）：公开资料一致只见「单卡 OVS 全卸载 + 交换机层 MC-LAG」，与本专利"跨 N≥2 块独立网卡 LACP 聚合 + 流表向全部网卡冗余下发"不在同一层级，5 条 F# 全为公开资料不足、无字面命中亦无真反向证据。
