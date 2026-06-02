# 证据索引 — 09-gcp-andromeda-snap

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| Q1 | 2026-06 | WebSearch | query: `Google Snap userspace networking engine CPU core scaling dynamic NSDI` | 命中 Snap SOSP 2019：dynamic scaling of CPU resources、pluggable engine、kernel/userspace CPU scheduler co-design |
| Q2 | 2026-06 | WebSearch | query: `Snap engine load balancing dynamic scaling compacting cores spreading engines reassign Pony Express` | 命中 Spreading / Compacting 两种调度模式，periodic polling of engine queuing delays to detect load imbalance |
| S1 | 2019-10 (SOSP'19) | 论文 | https://courses.grainger.illinois.edu/cs598hpn/fa2020/papers/snap.pdf （本地 snap-sosp2019.pdf） | 核心证据：rebalancing function periodically performs actions — scale out engine to another thread / migrate back engine / engine compaction / engine swaps；queueing load 估计 |
| S2 | 2019-11 | 博客 | https://blog.acolyer.org/2019/11/11/snap-networking/ | 三种 scheduling mode（Spreading / Compacting / Dedicated）综述，佐证 S1 |
| S3 | 2019 | 论文官网 | https://research.google/pubs/snap-a-microkernel-approach-to-host-networking/ | 元数据 / 发表确认（SOSP 2019） |
