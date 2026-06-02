# 证据索引 — 01-tech-ovs-dpdk-pmd-autolb

## Phase 1 — react 粗筛（WebSearch）
- query 1: `OVS-DPDK pmd-auto-lb rxq reassignment PMD thread load`
  → 命中高度相关。官方 OVS 文档 + Red Hat Developer 博客明确描述"周期性检测 PMD 线程负载 → 条件满足 → RxQ 重分配"。信号强，不剪枝。
- query 2: `ovs pmd-auto-lb variance improvement threshold dry-run rebal-interval rxq reassign PMD core`
  → 命中。补充阈值机制细节：variance improvement threshold 默认 25%、rebal-interval 默认 1 分钟、dry-run 估算后再实施重分配。

## Phase 2 — react 深抓（WebFetch）
- WebFetch: https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
  → 一手官方文档。verbatim 命中 F1（measure PMD CPU utilization）、F2（above load threshold every 10 secs for 1 minute + variance improvement threshold）、F3（new Rx queue to PMD assignment）、F4（PMD threads pinned to cores / isolated）。成功。
- WebFetch: https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk
  → 主要维护者（Red Hat）官方技术博客，发布日 2021-04-29（更新 2024-02-05）。verbatim 命中 F1-F4，且明确 PMD 1:1 跑在专用 core 上、每 PMD 服务一组 RxQ（多 PMD 多 RxQ 多 core）。成功。

## 证据索引表
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2021-04-29(更新2024-02-05) | 官方技术博客(主维护者 Red Hat) | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | F1-F4 全命中；PMD 1:1 专用 core，多 PMD 多 RxQ |
| 2 | latest 文档 | OVS 官方一手文档 | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | F1-F4 verbatim；utilization 检测/阈值/dry-run/RxQ 重分配 |

## 时间窗
- 专利公开（授权）日：2015-08-12
- pmd-auto-lb 特性文档/博客发布日：2021（远晚于公开日）→ 满足"公开日后"时间窗，非现有技术。

## 工具受限说明
- 无。WebSearch / WebFetch 均一次成功，未触发兜底。
