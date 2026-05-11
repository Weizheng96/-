# Verdict — VMware Antrea

> S1；权 1/9；**P2**；Antrea 是基于 OVS 的 CNI——直接继承 OVS 上游的 PMD auto-LB 能力——但作为 CNI 在 K8s 节点上运行，是否实际启用 auto-LB 取决于部署配置；
> F1-F2 字面命中（OVS-based CNI），F3-F5 取决于具体部署（默认未启用 auto-LB；VMware 也未主动推荐）；**第 4 档（弱候选）**。
> 与 OVS 上游候选 01 共享技术本体 — 主要责任由 OVS 上游 + Red Hat 等承担；Antrea 作为下游使用方降一档。
