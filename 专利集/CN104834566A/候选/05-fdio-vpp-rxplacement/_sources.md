# 证据索引 — 05-fdio-vpp-rxplacement

## Phase 1 — 粗筛 WebSearch（串行，3 条）
1. `FD.io VPP worker thread rx-placement rxq dpdk assign core`
   - 命中官方文档：默认启动时 round-robin 把 interface/queue 分配给 worker；改放置用 `set interface placement` / `show interface rx-placement` 手动 CLI。相关 → 继续。
2. `VPP automatic rx queue load balancing dynamic OR auto-scaling worker rebalance`
   - vpp-dev 邮件列表（2021）：rx/tx queue 为静态映射，无 dynamic rebalancing；有"计划实现"但当时不存在。指向 F2 弱。
3. `VPP detect worker thread load automatically move rx queue handoff overload threshold`
   - VPP "worker handoff" 是按包 hash 把流量交接到另一 worker 的 handoff queue（per-packet 流转向），**不是**把 rxq↔thread 映射重分配；congestion 仅作为问题现象（VPP-1734），无自动重放置触发器。

## Phase 2 — 深抓 WebFetch（串行）
- VPP 23.10 Multi-threading 官方文档（WebFetch 成功）
  https://s3-docs.fd.io/vpp/23.10/developer/corearchitecture/multi_thread.html
  - "On startup, the VPP platform assigns interfaces (or interface, queue pairs if RSS is used) to different worker threads in round robin fashion."
  - `set interface placement TenGigabitEthernet2/0/1 queue 1 thread 1` = 手动管理命令。
  - 明确：无 automatic load-based rebalancing；无基于 CPU 负载 / 队列深度 / 线程不均的动态重分配。
- VPP `set interface rx-placement` CLI 文档（WebFetch 成功）
  https://s3-docs.fd.io/vpp/23.10/cli-reference/clis/clicmd_src_vnet.html
  - 语法：`set interface rx-placement <interface> [queue <n>] [worker <n> | main]`
  - "This command is used to assign a given interface, and optionally a given queue, to a different thread." 纯手动 operator 命令，无 automatic/load-triggered 行为。
- VPP Multi-thread wiki（WebFetch 403；curl 兜底取回 13KB 为 MediaWiki JS 壳，正文动态加载无静态正文）
  https://wiki.fd.io/view/VPP/Using_VPP_In_A_Multi-thread_Model
  - 关键内容已由 Phase 1 query 1 命中片段覆盖（同一 round-robin + 手动 placement 表述）。

## 发布日期
- 官方文档对应 VPP 23.10（2023）；rx-placement 机制自 VPP 早期即存在，长期为手动配置。均晚于专利公开日 2015-08-12，但机制性质（手动）跨版本一致。
