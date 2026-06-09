# 证据索引 — 10-azure-stream-analytics

候选：Azure Stream Analytics（Microsoft）/ 产品
时间窗基准：专利公开（授权）日 2020.05.08，仅其后公开材料计入。

## Phase 1 — react 粗筛（WebSearch，串行）

1. `Azure Stream Analytics query language SQL job topology streaming units query steps`
   - 命中。ASA = T-SQL 子集查询语言；job = input + query + output；存在 job topology、streaming units、query steps、query parallelization。强信号。
2. `Azure Stream Analytics query parallelization streaming nodes query steps partition compilation physical execution`
   - 命中。query 被切分为 query steps，按 partition 并行分发到多个 streaming nodes 执行；"job is parallel only when all inputs, outputs, and query steps use the same key"。
3. `Azure Stream Analytics job diagram query steps streaming nodes compiler optimize "job simulation" logical physical`
   - 命中。官方明确区分 **logical diagram = query step（逻辑概念）** vs **physical diagram = streaming node（物理计算概念）**；"Each processor represents one or more steps in your query"。对应专利两级流图 + 算子承载多逻辑节点。

3 条全部命中，强信号，进入 Phase 2。

## Phase 2 — react 深抓（WebFetch，串行）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | ms.date 2022-10-12 / updated 2025-09-15 | 官方文档 L1 | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-job-logical-diagram-with-metrics | "visualize your job's query steps with its input source, output destination"；query step node 可 `{}` 映射回 query script —— 逻辑层（第一流图）证据 |
| 2 | ms.date 2026-04-29 / updated 2026-04-30 | 官方文档 L1 | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization | "A Stream Analytics job definition includes at least one streaming input, a query, and output"；"all inputs, all query logic steps, and all outputs"；"A query can have one or many steps. Each step is a subquery defined by the WITH keyword" —— F1/F2/F4/F5 主证据 |
| 3 | ms.date 2023-02-17 / updated 2025-09-15 | 官方文档 L1 | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-job-physical-diagram-with-metrics | streaming node = 一组计算资源；partition 分配到各 streaming node 并行执行 —— 物理执行/工作节点（第二流图/F4）证据 |
| 4 | （搜索摘要旁证，未单独 WebFetch） | 官方文档摘要 | https://learn.microsoft.com/en-us/azure/stream-analytics/job-diagram-with-metrics | "A streaming node represents a set of compute resources..."；"Inside each streaming node, there are Stream Analytics processors... Each processor represents one or more steps in your query" —— F3 末句最强对应 |

## 工具受限说明
- 未遇到 WebFetch 失败或证书拦截；官方 learn.microsoft.com 可直接抓取，verbatim 充分，未触发 curl 兜底；未落盘 PDF（全部为可直链 HTML 官方文档）。
- ASA 内部"逻辑计划→物理算子计划"的编译器实现（是否真做逻辑节点分组 + 从算子库选公共算子）属未公开内部实现；公开文档仅以"query step（逻辑）↔ streaming node / processor（物理）"两级可观测层呈现。F3 的"逻辑节点分组 + 选公共算子 + 一个算子承载多逻辑节点"以"Each processor represents one or more steps in your query"为最强对应，但分组/选算子的具体机制公开度不足。
