# 10-azure-stream-analytics verdict

## 候选基本信息
- 名称：Azure Stream Analytics / 组织：Microsoft（NASDAQ:MSFT） / 类型：产品 / 初判命中 F#：F1,F2,F4,F5 / 专利公开（授权）日：2020.05.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述信息） | 确认命中（字面） | "A Stream Analytics job definition includes at least one streaming input, a query, and output." / "The query is based on SQL query language" / 输入可为 Event Hubs、IoT Hub、Blob storage、Data Lake Storage Gen2 | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization | 用户提交一段 SQL 查询 + 配置 input/output（= 输入/输出通道描述信息）。ASA 查询语言为 T-SQL 子集，字面命中"结构化查询语言 SQL 语句"。 |
| F2（由 SQL + 通道信息生成"第一流图"=逻辑节点图） | 确认命中（字面/等同） | "The job diagram ... can help you visualize your job's query steps with its input source, output destination" / "A query can have one or many steps. Each step is a subquery defined by the WITH keyword." / "To see the query script snippet that is mapping the corresponding query step, select the `{}` icon in the query step node" | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-job-logical-diagram-with-metrics | SQL 被解析为由 query steps 构成的 logical job diagram（官方称"logical concept: query step"），每个 step 可回溯到 query script。query step 逻辑节点图 = 第一流图（逻辑节点）。 |
| F3（逻辑节点分组 + 从预设算子库选公共算子 → 第二流图；一个算子实现一组逻辑节点功能 = 算子合并） | 公开资料不足（未确定） | "Inside each streaming node, there are Stream Analytics processors available for processing the stream data. Each processor represents one or more steps in your query." | https://learn.microsoft.com/en-us/azure/stream-analytics/job-diagram-with-metrics | 一个 processor 承载"一个或多个 query step" —— 在"一个物理执行实体实现多个逻辑节点功能"层面与 F3 末句等同方向一致。但 F3 字面要求"对第一流图逻辑节点分组 + 从预设算子库选公共算子生成第二流图"的具体编译机制，ASA 内部逻辑→物理算子计划属未公开实现，缺正向 verbatim 证据；亦无正向反据。按纪律判"公开资料不足"。 |
| F4（按"第二流图"控制工作节点执行流计算任务） | 确认命中（字面/等同） | "Query parallelism divides the workload of a query by creating multiple processes (or streaming nodes) and executes it in parallel." / "A streaming node represents a set of compute resources that's used to process job's input data." / 物理图中 partition 分配到各 streaming node 并行执行 | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-job-physical-diagram-with-metrics ; https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization | ASA 托管服务把 query（physical diagram = streaming node）的工作负载调度到多个 streaming node（计算资源/工作节点）并行执行，与"管理节点根据流图控制工作节点执行"等同。管理/调度层为托管内部，未单独 verbatim，但 master-worker 分发为系统结构所必然。 |
| F5（输入/输出通道定义：数据生产系统→流图→数据消费系统） | 确认命中（字面） | "Inputs are where the job reads the data stream from. The query is used to transform the data input stream, and the output is where the job sends the job results to." / 输入：Event Hubs、IoT Hub、Blob、Data Lake；输出：ADLS、Functions、Table、Blob、Cosmos DB、Event Hubs、IoT Hub、Service Bus、SQL、Synapse | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization | input = 从上游数据生产系统（Event Hubs / IoT Hub 等）读流（输入通道）；output = 写到下游数据消费系统（DB / 存储 / 消息队列）（输出通道）。字面命中。 |

## 已检查文档清单
- ASA 逻辑作业图官方文档（query step = logical concept；query step ↔ query script 映射）— https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-job-logical-diagram-with-metrics （updated 2025-09-15）
- ASA 查询并行化官方文档（job = input+query+output；query steps；partition 对齐；输入/输出连接器清单）— https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization （updated 2026-04-30）
- ASA 物理作业图官方文档（streaming node = 计算资源；partition 分配到 streaming node 并行执行）— https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-job-physical-diagram-with-metrics （updated 2025-09-15）
- ASA 作业图 overview（"Each processor represents one or more steps in your query"，F3 旁证）— https://learn.microsoft.com/en-us/azure/stream-analytics/job-diagram-with-metrics
- 全部材料公开/更新日期均晚于 2020.05.08，满足时间窗。

## 最终判定

**第 3 档：≥60% 确认命中且无正向反据**

判定依据：F1、F2、F4、F5 四项均有官方文档 verbatim 支撑确认命中（4/5 = 80% ≥ 60%）。ASA 以 T-SQL 子集查询定义流作业（F1），SQL 编译为由 query steps 构成的 logical job diagram（F2，对应第一流图逻辑节点），按 partition 将工作负载分发到多个 streaming node 并行执行（F4，physical diagram = 第二流图/工作节点执行），input/output 经连接器对接上游数据生产系统与下游数据消费系统（F5）。唯一未坐实的是 F3——专利的核心区分限定"逻辑节点分组 + 从预设算子库选公共算子生成第二流图 + 一个算子承载多个逻辑节点"：ASA 公开层仅见"一个 processor 承载一个或多个 query step"（方向等同），但"分组 + 选公共算子"的具体编译机制属未公开内部实现，缺正向证据，亦无正向反据，按纪律判"公开资料不足"，故未落第 2 档。无任何"针对该候选的正向拒绝"（无作用域排除/不同机制反据/时间不合规/架构层不同），故不落第 5 档。综合落第 3 档。

> 注意：F3 的"两级流图（逻辑→物理算子图）+ 算子合并"是本专利相对现有流计算系统的核心区分限定（见特征文档"关键限定词与隐含约束"）。在 F3 未坐实前，本判定不应被读作"已落入权利要求全部技术特征"。

## 升级路径（第3-4档填）
- 取证 F3 的"逻辑→物理两级编译"与"算子合并"：检索 ASA / Trill（ASA 底层流处理引擎，Microsoft Research）相关论文与文档，确认是否存在 logical plan → physical plan 转换、operator fusion / 算子合并、从内置算子库选物理算子的机制。query：`Trill Microsoft streaming engine query compilation physical plan operator fusion`、`Azure Stream Analytics Trill execution plan operators`。
- 取证 F4 的管理/调度层：检索 ASA 是否明示 master/coordinator 把 query steps/operators 调度到 worker（streaming node），query：`Azure Stream Analytics architecture coordinator worker node scheduling`。
- 若 F3 取得"分组 + 选公共算子 + 算子合并"正向 verbatim，可升至第 2 档（含等同）；若取得明确反据（如证明 ASA 不做逻辑→物理两级映射或无算子合并），则相应下调。

## 总结一句话
Azure Stream Analytics 以 T-SQL 子集查询定义流作业、编译为 query step 逻辑图、按 partition 分发到多 streaming node 并行执行、input/output 连接上下游系统，F1/F2/F4/F5 确认命中，仅 F3 两级流图+算子合并公开资料不足，落第 3 档。
