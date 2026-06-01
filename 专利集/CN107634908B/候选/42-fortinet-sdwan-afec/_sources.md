# 42-fortinet-sdwan-afec — 检索留痕

## WebSearch queries

1. `FortiGate SD-WAN Adaptive FEC FortiOS 7.0.2 dynamic redundancy SLA`
2. `Fortinet adaptive FEC application aware policy DPI traffic classification`
3. `FortiGate SD-WAN FEC redundant packet ratio scheduling algorithm timing`
4. `"fortinet" "adaptive FEC" "packet loss" OR "latency" OR "jitter" mapping configuration`
5. `Fortinet patent "adaptive FEC" OR "adaptive forward error correction" SD-WAN US patent`

## WebFetch / curl URLs

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2026-05-26 | WebFetch | https://docs.fortinet.com/document/fortigate/7.0.0/sd-wan-new-features/169010/adaptive-forward-error-correction-7-0-2 | FortiOS 7.0.2 首次引入 Adaptive FEC；config 范本含 packet-loss-threshold / bandwidth-up-threshold；无任何流量统计字段；无调度方法选项 |
| 2 | 2026-05-26 | curl 兜底 → fortios_7.6.0_adaptive_fec.html | https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/169010/adaptive-forward-error-correction | 完整 FortiOS 7.6 CLI 示例 + verify 输出 (`diagnose sys sdwan health-check` 输出 packet-loss / latency / jitter / bandwidth)；fec-codec=xor 与 timeout=10ms 是 encode block 局部超时，非业务时延推导 |
| 3 | 2026-05-26 | WebFetch | https://docs.fortinet.com/document/fortigate/7.6.0/sd-wan-architecture-for-enterprise/228050/forward-error-correction-fec | 仅含 Adaptive FEC 概念性描述 ("dynamically adjusts the ratio … according to network conditions") |
| 4 | 2026-05-26 | curl 兜底 → fortios_8.0.0_adaptive_fec.html | https://docs.fortinet.com/document/fortigate/8.0.0/administration-guide/169010/adaptive-forward-error-correction | FortiOS 8.0 引入 **二轮匹配**："first round: packet-loss/latency/bandwidth; second round: ToS value and mask" — 关键证实 Fortinet 用 ToS/DSCP 做业务类型 hint，非流量统计推断 |
| 5 | 2026-05-26 | curl 兜底 → fortios_8.0.0_tos_matching.html | https://docs.fortinet.com/document/fortigate/8.0.0/administration-guide/187229/tos-matching-and-negate-options-on-adaptive-fec-profiles-new | ToS matching CLI 范本 (`config tos / set tos / set tos-mask`) + negate options (packet-loss/latency/bandwidth-up/down/bi)；全部为链路状态阈值 + DSCP 类别，无流量统计 |

## 落盘文件

- `fortios_7.6.0_adaptive_fec.html` — FortiOS 7.6 完整官方文档（含 config 范本 + diagnose 输出）
- `fortios_8.0.0_adaptive_fec.html` — FortiOS 8.0 完整官方文档（含 8.0 新特性 ToS 二轮匹配段）
- `fortios_8.0.0_tos_matching.html` — FortiOS 8.0 ToS matching + negate threshold 选项专项页

## 工具受限说明

- `WebFetch` 直访 `docs.fortinet.com` 多次仅返回 nav frame 而无文章正文；用 `Invoke-WebRequest` 直接 GET 完整 HTML + Grep / Read 局部读取章节工作可靠。已在 7.6.0、8.0.0、8.0.0-tos 三个 URL 上完成兜底。
