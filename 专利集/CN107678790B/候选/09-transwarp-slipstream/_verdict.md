# 09-transwarp-slipstream verdict

## 候选基本信息
- 名称：Slipstream / 实时流计算引擎 / 组织：星环科技 Transwarp（科创板 688031.SH） / 类型：产品 / 初判命中 F#：F1,F2,F3,F4,F5 / 专利公开（授权）日：2020.05.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述信息） | 确认命中（字面） | "Slipstream通过SQL的方式为用户提供开发接口，兼容ANSI SQL 2003标准"；"用户可以使用 **CREATE STREAM** 创建流；…… **DROP STREAM** 删除流"；"StreamSQL语言中有四个Stream、StreamJob 和 Application……Stream分为两种：Input Stream和Derived Stream，分别用于接收数据源传来的数据成为Input Stream" | transwarp.cn/blog/1098 ; /doc/slipstream/9.3/slipstream-introduction ; /blog/190 | SQL 驱动＋CREATE STREAM/STREAMJOB DDL 即"SQL 语句 + 输入/输出通道描述信息"提交；输入通道=Input Stream(source)，输出=写入表。 |
| F2（由 SQL 生成"第一流图"＝逻辑节点图） | 确认命中（字面） | "Slipstream包含强大的优化器……包含3级优化器：首先是基于规则的优化器,应用静态优化规则并生成一个**逻辑执行计划**"；Slipstream Studio 监控"任务**逻辑执行**和物理执行计划" | /doc/slipstream/9.3/slipstream-introduction ; /blog/1098 | SQL 经优化器解析为逻辑执行计划＝由 SQL 生成逻辑节点构成的"第一流图"。 |
| F3（逻辑分组＋从预设算子库选公共算子→"第二流图"；一个算子承载多个逻辑节点＝算子合并） | 公开资料不足（未确定） | 逻辑→物理两级转换字面命中："其次是基于成本的优化器……来选择一个更合理的计划并生成**物理执行计划**；最后是代码生成器,对一些比较核心的执行逻辑生成更高效的执行代码或者Java Byte Code"；但"逻辑节点**分组**＋从**预设算子库选公共算子**＋一个算子实现多个逻辑节点（算子合并/operator fusion）"末段子动作未见 verbatim 直证 | /doc/slipstream/9.3/slipstream-introduction | F3 含三子动作全须满足。逻辑计划→物理计划两级映射已字面命中；"代码生成器对核心执行逻辑生成融合执行代码"可对应"算子合并"的等同实现，但缺正面 verbatim。**未检索到针对该子动作的正向反据**，故判未确定而非未命中。 |
| F4（按"第二流图"控制工作节点执行流计算任务） | 确认命中（字面） | "当 **Worker 或者 Server** 发生故障时，实现秒级别的任务自动恢复"；"**分布式计算引擎，task级自动重试至可用节点**"；"StreamJob 是对一个或多个 Stream 进行计算并将结果写入一张表的过程" | /blog/1098 ; /blog/190 | Server/Worker＝管理节点/工作节点（master-worker）；task 分布式调度至工作节点执行＝按执行计划控制工作节点执行流任务。 |
| F5（输入通道：数据生产系统→流图；输出通道：流图→数据消费系统） | 确认命中（字面） | "Input Stream……用于接收数据源传来的数据"；"启动一个StreamJob时，StreamSQL会为每一个 Input Stream 启动一组称为 receiver 的任务来接收数据，接收的数据经过一系列 Derived Stream 的变形 终被插入一张表，供用户查询"；"指定使用…节点为 Kafka Broker……这些消息都将被发布给 demo"（Kafka 数据源） | /blog/190 | Input Stream/receiver 从 Kafka 等数据生产系统输入；结果写入表/下游存储＝输出至数据消费系统（实时 ETL 写目标存储）。 |

## 已检查文档清单
- Transwarp Slipstream 分布式实时计算引擎产品页/博客（StreamSQL=ANSI SQL 2003、Slipstream Studio 逻辑/物理执行计划、Worker/Server 故障恢复、task 级分布式调度）— https://www.transwarp.cn/blog/1098
- Slipstream 9.3 官方文档·Slipstream 简介（3 级优化器：逻辑执行计划→物理执行计划→代码生成；CREATE STREAM DDL）— https://www.transwarp.cn/doc/slipstream/9.3/slipstream-introduction
- 基于流的 SQL 引擎 StreamSQL 基础介绍（Input/Derived Stream、StreamJob、receiver、Kafka 源）— https://www.transwarp.cn/blog/190
- Slipstream 9.3 SQL 参考 DDL（CREATE/DROP/ALTER STREAM/TABLE/STREAMJOB；DML 输入输出章节，lastCommitDate 2024-08）— https://www.transwarp.cn/doc/slipstream/9.3/sql-referance--slipstream-ddl

## 最终判定

**第 3 档：高度疑似（多数特征确认命中，无正向反据）**

判定依据：
- F1、F2、F4、F5 四项均有官方文档 / 产品页 verbatim **字面命中**——SQL（ANSI SQL 2003）驱动 + CREATE STREAM/STREAMJOB 定义输入/输出（Input Stream→receiver 接收 Kafka 源，结果写入表/sink）；SQL 经优化器生成**逻辑执行计划**（＝第一流图）；再生成**物理执行计划**（＝第二流图）；Server/Worker（master-worker）分布式 task 调度执行。
- F3 仅"逻辑计划→物理计划两级映射"字面命中；其末段子动作"逻辑节点分组 + 从预设算子库选公共算子 + 一个算子承载多个逻辑节点（算子合并/operator fusion）"无 verbatim 直证。"代码生成器对核心执行逻辑生成融合执行代码/Java Byte Code"可作等同支撑但证据偏弱。**全程未检索到任何针对 Slipstream 的正向反据**（无"不做逻辑→物理两级映射""仅单层图""不支持 SQL"之类反向陈述）。
- 确认命中比例 4/5 ＝ 80% ≥ 60%，且无正向反据，F3 属"公开资料不足"而非"确认未命中"，时间窗内有效（9.3 文档为 2024）。→ 落第 3 档（非第 1/2：F3 末段未取得字面或确凿等同证据；非第 5：无任一正向反据，材料晚于 2020.05.08，架构层同为 SQL→逻辑/物理计划→master-worker 分布式执行）。

## 升级路径（第 3-4 档填）
- 抓取 Slipstream Studio "逻辑执行/物理执行计划"可视化的实际计划展开输出（截图/文档），核实是否存在"逻辑节点→物理算子"的**分组映射**与**算子合并/operator fusion / 算子链**的明示描述（直证 F3 末段，可升至第 1/2 档）。
- 检索星环 9.x 完整技术白皮书 / 架构文档（PDF）中关于"物理执行计划由逻辑计划经算子划分/选择生成"的章节正文（目前文档站子节正文懒加载未取得）。
- 在 patents.google.com 检索星环自有同主题专利（流式 SQL→执行计划→分布式执行），看其权利要求是否自述"逻辑节点分组 + 算子选择"机制（可作强等同/字面支撑）。

## 总结一句话
星环 Slipstream 以 ANSI SQL 2003 流式 SQL 驱动、经 3 级优化器生成逻辑执行计划→物理执行计划、由 Server/Worker 主从架构分布式调度执行、Input/Derived Stream 对应输入源与输出，F1/F2/F4/F5 官方文档字面命中、仅 F3 算子合并子动作公开资料不足且无任何正向反据，落第 3 档（高度疑似）。
