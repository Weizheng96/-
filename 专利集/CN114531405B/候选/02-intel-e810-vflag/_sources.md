# 证据索引 — 02-intel-e810-vflag

## 检索粗筛 query 留痕（react，串行）
- query 1: `Intel E810 OVS TC offload SR-IOV VF-LAG bond hardware offload switchdev` → 命中 Intel 官方 switchdev/LAG 配置指南、kernel.org ice 文档（强信号）
- query 2: `Intel E810 switchdev LAG bond mode LACP 802.3ad VF-LAG offload supported active-backup` → 命中关键约束："bond comprises exactly two ports from the same NIC MAC chip"；支持模式含 802.3ad(4)/LACP
- query 3: `"E810" VF LAG offload "same NIC" OR "same MAC" bond two ports requirement edc.intel.com switchdev` → 命中 EDC Technical Details / Limitations / Script D 页
- query 4: `ice driver VF LAG offload bond "two ports" "same" NIC switchdev kernel.org documentation aggregator` → kernel.org ice 文档确认 same-NIC-MAC-chip 约束 + 支持模式列表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | Rev1.0 2021-08 / 在线版 rev1.7 2025-12-29 | 一手 vendor 文档(PDF) | https://cdrdv2-public.intel.com/645272/645272_E810%20eSwitch%20switchdev%20Mode%20TechConfigGuide_Rev1.0.pdf（本地：E810-switchdev-techconfig-rev1.0.pdf） | TC-Flower exact-match skip_sw 硬件卸载（F4 命中）；hw-tc-offload；OVS dp:tc offloaded:yes。LAG 段未含 same-NIC 细节（旧版） |
| 2 | live | 一手 kernel 文档 | https://docs.kernel.org/networking/device_drivers/ethernet/intel/ice.html | 反向："You cannot use SR-IOV when link aggregation (LAG)/bonding is active, and vice versa. To enforce this, the driver checks for this mutual exclusion."（上游内核 ice 默认 SR-IOV 与 bond 互斥） |
| 3 | live rev1.7 | 一手 vendor 文档(搜索摘要) | https://edc.intel.com/.../technical-details-eswitch-switchdev-mode/ ；同主题 ice LAG 文档 | 反向/限定："the bond comprises exactly two ports from the same NIC MAC chip"；支持模式 active-backup(1)/balance-xor(2)/broadcast(3)/802.3ad(4)；802.3ad 需 FW 4.80+ |
| 4 | live | 一手 vendor 文档(在线) | https://edc.intel.com/content/www/us/en/design/products/ethernet/appnote-e800-eswitch-switchdev-mode-config-guide/script-d-switchdev-mode-with-lag-configuration/ | Script D：bond 用同一适配器两端口 ens2f0/ens2f1；hw-tc-offload on PF+VF_PR |

## 工具受限说明
- EDC（edc.intel.com）在线页 WebFetch 60s 超时 + curl(浏览器 UA) 兜底未在窗口内写回（疑似反爬/重定向墙）；其关键约束已由 WebSearch 对官方文档与 kernel.org ice 文档的摘要交叉确认。
- cdrdv2 Rev1.0 PDF 已本地落盘并用 pypdf 抽取全文（43909 字符），确认 TC-Flower exact-match 卸载，但该旧版 LAG 段无 same-NIC / 模式细节。
